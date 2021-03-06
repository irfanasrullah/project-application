from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, HTML
from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, BaseInlineFormSet, ModelChoiceField
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe

from ProjectApplication import settings
from comments.forms.comment import CommentForm
from grant_management.models import Invoice, LaySummary, LaySummaryType, Installment
from project_core.fields import FlexibleDecimalField
from project_core.models import Project
from project_core.templatetags.ordinal import ordinal
from project_core.templatetags.thousands_separator import thousands_separator
from project_core.utils.utils import format_date
from project_core.widgets import XDSoftYearMonthDayPickerInput
from . import utils


class InstallmentModelChoiceField(ModelChoiceField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._sequence = 0

    def label_from_instance(self, obj):
        self._sequence += 1
        amount = thousands_separator(obj.amount)
        return mark_safe(f'{ordinal(self._sequence)} - {amount} CHF')


def html_message(message):
    return f'''
    <div class="form-group">
        <label for="id_FORM_SET-1-installment" class="invisible">l</label>
        <div class="">{message}</div>
    </div>
    '''


class InvoiceItemModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user', None)  # When the form is created to visualise user is not needed
        # user is used when saving comments at the moment

        self._project = kwargs.pop('project')

        super().__init__(*args, **kwargs)

        self._comment_form = None

        if self.instance and self.instance.id:
            self.comment_prefix = f'comment-invoice-{self.instance.id}'
            self.comments = self.instance.comments()
            self.comment_count = len(self.comments)
            self.comments_save_text = 'Save Invoices'

            self._comment_form = CommentForm(form_action=reverse('logged-proposal-evaluation-comment-add',
                                                                 kwargs={'pk': self.instance.id}),
                                             category_queryset=self.instance.comment_object().category_queryset(),
                                             prefix=CommentForm.FORM_NAME,
                                             form_tag=False,
                                             fields_required=False)
            self.fields.update(self._comment_form.fields)

        self.fields['installment'].queryset = Installment.objects.filter(project=self._project).order_by('id')

        XDSoftYearMonthDayPickerInput.set_format_to_field(self.fields['due_date'])
        XDSoftYearMonthDayPickerInput.set_format_to_field(self.fields['sent_for_payment_date'])
        XDSoftYearMonthDayPickerInput.set_format_to_field(self.fields['received_date'])
        XDSoftYearMonthDayPickerInput.set_format_to_field(self.fields['paid_date'])

        self.fields['can_be_deleted'] = forms.CharField(initial=1, required=False)

        installment_url = reverse('logged-grant_management-installments-update', kwargs={'project': self._project.id})
        self.fields['installment'].help_text = f'Select the installment to which this invoice is assigned. ' \
                                               f'<a href="{installment_url}">Create an installment</a> if the one you ' \
                                               f'require does not exist'

        message = ''

        if self.instance:
            if self.instance.invoicecomment_set.exists():
                self.fields['can_be_deleted'].initial = 0
                message = 'This invoice cannot be removed because it has comments.'

            if self.instance.paid_date is not None:
                self.fields['can_be_deleted'].initial = 0
                message = '''<strong>This invoice has been paid and can no longer be changed.
                        To edit any of the fields, delete the date paid, click on <em>Save Invoices</em> 
                        and come back to the invoices page.</strong>'''

                field_names_to_disable = ['due_date', 'received_date', 'sent_for_payment_date', 'file', 'amount',
                                          'installment']

                if 'allow_overbudget' in self.fields:
                    field_names_to_disable.append('allow_overbudget')

                for field_name in field_names_to_disable:
                    self.fields[field_name].disabled = True

        self.helper = FormHelper()
        self.helper.form_tag = False

        # It's included in the main formset, it avoids problems when adding new invoices and the jquery.formset.js
        self.helper.disable_csrf = True

        divs = [
            Div(
                Div('id', hidden=True),
                Div(Field('DELETE', hidden=True)),
                Div('can_be_deleted', hidden=True, css_class='can_be_deleted'),
                css_class='row', hidden=True
            ),
            Div(
                Div(HTML(f'<h4>{self.title()}</h4>'), css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div('installment', css_class='col-4'),
                Div(HTML(html_message(message)), css_class='col-8 to-delete'),
                css_class='row'
            ),
            Div(
                Div('due_date', css_class='col-4'),
                Div('received_date', css_class='col-4'),
                Div('file', css_class='col-4'),
                css_class='row'
            ),
            Div(
                Div('amount', css_class='col-4'),
                Div('sent_for_payment_date', css_class='col-4'),
                Div('paid_date', css_class='col-4'),
                css_class='row'
            )
        ]

        self._add_allow_overbudget_checkbox(divs)

        if self._comment_form:
            divs += Div(HTML('{% include "comments/_accordion-comment-list-fields-for-new.tmpl" %}'))

        self.helper.layout = Layout(*divs)

    def _add_allow_overbudget_checkbox(self, divs):
        # This is a non-straightforward way to decide if the invoice is overbudget or not at the time
        # that the invoice has been submitted but not accepted yet.
        #
        # It's a sad way (because it access self.data) and it might be refactored. I also think that allow paying
        # invoices that go overbudget is not the best way and the budget should be changed (with history). This
        # needs to be discussed with the whole team.
        #
        # The reason of not accessing self.errors as initially done to decide if the invoice has been rejected because
        # it would go overbudget (and then in the constructor it's showing the checkbox to confirm that this is ok):
        # self.errors is BaseForm.errors which calls self.full_clean()
        # only the first time (it's cached).
        #
        # This Invoice form is constructed by the Django BaseFormSet._construct_form. It does:
        #         form = self.form(**defaults)
        #         self.add_fields(form, i)
        #
        # self.add_fields(form, i) adds the 'DELETE' in the self.fields. But because BaseForm.errors calls
        # fulL_clean, etc. and they cache results:
        # if self.errors is called in the Invoice constructor (before self.add_fields) the deletion of invoices
        # doesn't work anymore ('DELETE' never appears in the self.clean_fields)
        #
        # Another solution was to use self.errors and then self._errors = None to force the recalculation but other
        # cached data might stay and I wanted to avoid changing internal variables.
        #
        # Doing, in the Invoice constructor: "self.fields['DELETE'] = BooleanField(required=False)" : this is similar
        # to what's happening in BaseFormSet.add_fields and it fixes the deletion of invoices. But other
        # code is executed, cached so I wanted to avoid this as well.
        #
        # The third and chosen option is to access self.data. A unit test will be added to see that this doesn't break.

        decimal_field = FlexibleDecimalField()
        try:
            amount = decimal_field.clean(self.data.get(f'{self.prefix}-amount', None))
        except ValidationError:
            amount = None

        installment_data_name = f'{self.prefix}-installment'
        installment = None

        if installment_data_name in self.data and len(self.data[installment_data_name]) > 0:
            installment = Installment.objects.get(id=self.data[installment_data_name])

        if (self.instance and self.instance.allow_overbudget) or \
                self.is_overbudget(amount, installment):
            self.fields['allow_overbudget'] = forms.BooleanField(label='Ignore going overbudget',
                                                                 required=False,
                                                                 initial=self.instance.allow_overbudget,
                                                                 help_text='This invoice takes payments over the allocated budget or installment ' \
                                                                           'amount. Check the amount and tick the box to acknowledge it is ok to ' \
                                                                           'continue')

            divs.append(Div(
                Div('allow_overbudget', css_class='col-4 allow-overbudget-field'),
                css_class='row'
            ))

    def title(self):
        if self.instance:
            invoice = self.instance
            if invoice.paid_date:
                return f'Invoice paid {format_date(invoice.paid_date)}'
            if invoice.sent_for_payment_date:
                return f'Invoice sent for payment {format_date(invoice.sent_for_payment_date)}'
            elif invoice.received_date:
                return f'Invoice received {format_date(invoice.received_date)}'
            elif invoice.due_date:
                return f'Invoice due {format_date(invoice.due_date)}'
            else:
                return f'Invoice'

        return 'Invoice'

    def clean(self):
        cd = super().clean()

        if self.errors:
            return cd

        DELETE = cd.get('DELETE', None)

        project_starts = self._project.start_date
        project_ends = self._project.end_date

        due_date = cd.get('due_date', None)
        received_date = cd.get('received_date', None)
        sent_for_payment_date = cd.get('sent_for_payment_date', None)
        paid_date = cd.get('paid_date', None)
        installment = cd.get('installment', None)

        amount = cd.get('amount', None)
        file = cd.get('file', None)

        errors = {}
        sent_for_payment_errors = []

        today = timezone.now().date()

        if received_date and received_date > today:
            errors['received_date'] = 'Date received cannot be in the future'

        if sent_for_payment_date and sent_for_payment_date > today:
            errors['sent_for_payment_date'] = 'Date sent for payment cannot be in the future'

        if paid_date and paid_date > today:
            errors['paid_date'] = 'Date paid cannot be in the future'

        # This check is disabled waiting for further discussion
        # if due_date and due_date < project_starts:
        #     errors['due_date'] = utils.error_due_date_too_early(self._project)

        # if received_date and received_date < project_starts:
        #     errors['received_date'] = utils.error_received_date_too_early(self._project)

        if sent_for_payment_date and received_date and sent_for_payment_date < received_date:
            sent_for_payment_errors.append(
                f'Date sent for payment should be after the date the invoice was received')

        if paid_date and sent_for_payment_date and paid_date < sent_for_payment_date:
            errors['paid_date'] = f'Date paid should be after the date the invoice was sent for payment'

        if due_date and due_date > project_ends:
            errors['due_date'] = utils.error_due_date_too_late(self._project)

        if not file and received_date:
            errors['file'] = f'Please attach the invoice file (a date received has been entered).'

        if not received_date and sent_for_payment_date:
            errors[
                'received_date'] = f'Please enter the date the invoice was received (a date sent for payment has been entered).'

        if not received_date and paid_date:
            errors[
                'received_date'] = f'Please enter the date the invoice was recevived (a date paid has been entered).'

        if not amount and sent_for_payment_date:
            errors['amount'] = f'Please enter the invoice amount (a date sent for payment has been entered).'

        if sent_for_payment_date and (
                hasattr(self._project, 'grantagreement') is False):
            grant_agreement_url = reverse('logged-grant_management-grant_agreement-add',
                                          kwargs={'project': self._project.id})
            sent_for_payment_errors.append(
                f'Please attach the <a href="{grant_agreement_url}">grant agreement<a> in order to enter the date the invoice was sent for payment')

        if sent_for_payment_date and \
                hasattr(self._project, 'grantagreement') and self._project.grantagreement.signed_date is None:
            grant_agreement_url = reverse('logged-grant_management-grant_agreement-update',
                                          kwargs={'pk': self._project.grantagreement.id})
            sent_for_payment_errors.append(
                f'Please add the signed by in the <a href="{grant_agreement_url}">grant agreement<a> in order to enter the date the invoice was sent for payment')

        original_lay_summary_type = LaySummaryType.objects.get(name=settings.LAY_SUMMARY_ORIGINAL)
        if sent_for_payment_date and LaySummary.objects.filter(project=self._project).filter(
                lay_summary_type=original_lay_summary_type).exists() is False:
            lay_summary_url = reverse('logged-grant_management-lay_summaries-update',
                                      kwargs={'project': self._project.id})
            sent_for_payment_errors.append(
                f'Please attach the <a href="{lay_summary_url}">original lay summary</a> in order to send the invoice for payment')

        if amount and installment and amount > installment.amount and not cd.get('allow_overbudget', False):
            errors[
                'amount'] = mark_safe(
                f'Invoice amount is greater than the installment amount ({thousands_separator(installment.amount)}&nbsp;CHF)')

        if amount and amount > self._project.allocated_budget and not cd.get('allow_overbudget', False):
            errors[
                'amount'] = mark_safe(
                f'Invoice amount is greater than the project allocated budget ({thousands_separator(self._project.allocated_budget)}&nbsp;CHF)')

        if sent_for_payment_date is None and paid_date:
            sent_for_payment_errors.append('Please fill in sent for payment if the invoice is paid')

        if sent_for_payment_errors:
            errors['sent_for_payment_date'] = mark_safe('<br>'.join(sent_for_payment_errors))

        if DELETE and paid_date:
            errors['paid_date'] = 'A paid invoice cannot be deleted. Delete the date paid and try again.'

        if self._project.is_active() is False:
            raise forms.ValidationError(
                f'Cannot modify installments for this project: the status is {self._project.status}')

        if 'allow_overbudget' in self.cleaned_data and cd['allow_overbudget'] is False and \
                self.is_overbudget(amount, installment):
            errors['allow_overbudget'] = 'Click to proceed'

        comment_form = CommentForm(data=self.data,
                                   form_action=None,  # Because form_tag=False it's not needed
                                   category_queryset=self.instance.comment_object().category_queryset(),
                                   prefix=self.prefix,
                                   form_tag=False)

        comment_form.is_valid()

        comment_forms_errors = comment_form.get_errors()
        errors.update(comment_forms_errors)

        if errors:
            raise forms.ValidationError(errors)

    def is_overbudget(self, amount, installment):
        return (amount and installment and amount > installment.amount) or (
                amount and amount > self._project.allocated_budget)

    def save(self, *args, **kwargs):
        comment_category = self.cleaned_data.get('category', None)
        comment_text = self.cleaned_data.get('text', None)

        if comment_text:
            data = {'category': comment_category,
                    'text': comment_text}

            comment_form = CommentForm(data=data,
                                       form_action=reverse('logged-proposal-evaluation-comment-add',
                                                           kwargs={'pk': self.instance.id}),
                                       category_queryset=self.instance.comment_object().category_queryset(),
                                       form_tag=False)
            comment_form.save(parent=self.instance,
                              user=self._user)

        invoice = super().save(commit=False)
        invoice.project = self._project

        if 'allow_overbudget' in self.cleaned_data:
            invoice.allow_overbudget = self.cleaned_data['allow_overbudget']

            if 'allow_overbudget' in self.changed_data and invoice.allow_overbudget:
                invoice.overbudget_allowed_by = self._user

        invoice.save()

        return invoice

    class Meta:
        model = Invoice
        fields = ['installment', 'due_date', 'received_date', 'sent_for_payment_date', 'paid_date', 'amount',
                  'file']
        field_classes = {'installment': InstallmentModelChoiceField,
                         'amount': FlexibleDecimalField}
        widgets = {
            'due_date': XDSoftYearMonthDayPickerInput,
            'received_date': XDSoftYearMonthDayPickerInput,
            'sent_for_payment_date': XDSoftYearMonthDayPickerInput,
            'paid_date': XDSoftYearMonthDayPickerInput,
        }
        labels = {'due_date': 'Due',
                  'received_date': 'Received',
                  'sent_for_payment_date': 'Sent for payment',
                  'paid_date': 'Paid',
                  'amount': 'Amount (CHF)'
                  }
        help_texts = {
            'due_date': 'Date the invoice is due',
            'received_date': 'Date the invoice was received',
            'amount': 'Total of the invoice'
        }


class InvoicesFormSet(BaseInlineFormSet):
    wants_user = True
    can_force_save = True

    def __init__(self, *args, **kwargs):
        self._save_force = kwargs.pop('save_force', False)
        self._is_overbudget = False

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

    def get_queryset(self):
        return super().get_queryset().order_by('due_date')

    def clean(self):
        super().clean()

        if not self.is_valid():
            # if one of the budget items is not valid: doesn't validate the general form
            # E.g. if an amount is negative it will have an error in the amount but the
            # amount is removed from the form.cleaned_data
            return

        if self._save_force:
            return

        self._raise_errors_invoice_amounts_installments()
        self._raise_errors_invoice_amounts_project_budget()

    def _raise_errors_invoice_amounts_project_budget(self):
        invoiced_amount = 0
        for invoice_form in self.forms:
            amount = invoice_form.cleaned_data.get('amount', None) or 0  # It's None if the amount is not filled in

            invoiced_amount += amount

        allocated_budget = self.instance.allocated_budget
        if invoiced_amount > allocated_budget:
            self._is_overbudget = True
            raise forms.ValidationError(
                f'The total amount of the invoices {thousands_separator(invoiced_amount)} CHF is greater than the allocated project budget {thousands_separator(allocated_budget)} CHF')

    def _raise_errors_invoice_amounts_installments(self):
        installment_to_amounts = {}

        for invoice_form in self.forms:
            if not invoice_form.cleaned_data['installment']:
                # Invoices without an installment are checked separately
                continue

            amount = invoice_form.cleaned_data.get('amount', None) or 0  # It's None if the amount is not filled in

            if invoice_form.cleaned_data['installment'].id in installment_to_amounts:
                installment_to_amounts[invoice_form.cleaned_data['installment'].id] += amount
            else:
                installment_to_amounts[invoice_form.cleaned_data['installment'].id] = amount

        errors = []
        for installment_id, invoiced_amount in installment_to_amounts.items():
            installment = Installment.objects.get(id=installment_id)
            installment_amount_allocated = installment.amount

            if invoiced_amount > installment_amount_allocated:
                self._is_overbudget = True
                errors.append(
                    f'Invoice totals for {ordinal(installment.number())} installment are greater than the installment amount. '
                    f'Installment amount: {thousands_separator(installment.amount)} CHF. '
                    f'Total invoiced against {ordinal(installment.number())} installment: {thousands_separator(invoiced_amount)} CHF. '
                    f'If you want to continue click on the "Save Force Going Overbudget" button at the bottom of the page')

        if errors:
            raise forms.ValidationError(errors)

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['project'] = self.instance
        return kwargs

    def force_save_text(self):
        if self._is_overbudget:
            return 'Save Force Going Overbudget'


InvoicesInlineFormSet = inlineformset_factory(Project, Invoice, form=InvoiceItemModelForm, formset=InvoicesFormSet,
                                              min_num=1, extra=0, can_delete=True)
