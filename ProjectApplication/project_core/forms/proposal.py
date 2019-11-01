from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelChoiceField, ModelMultipleChoiceField
from django.forms import ModelForm, Form
from crispy_forms.layout import Layout, Div
from ..widgets import DatePickerWidget

from ..models import Proposal, Organisation, \
    Contact, \
    PhysicalPerson, PersonPosition, PersonTitle, Gender

from crispy_forms.helper import FormHelper
from dal import autocomplete


class OrganisationChoiceField(ModelChoiceField):
    def label_from_instance(self, organisation):
        return organisation.long_name


class OrganisationMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, organisation):
        return organisation.long_name


class PersonForm(Form):
    def __init__(self, *args, **kwargs):
        self.person_position = kwargs.pop('person_position', None)
        super().__init__(*args, **kwargs)

        first_name_initial = surname_initial = organisations_initial = group_initial = \
            academic_title_initial = email_initial = gender_initial = None

        if self.person_position:
            first_name_initial = self.person_position.person.first_name
            surname_initial = self.person_position.person.surname
            organisations_initial = self.person_position.organisations.all()
            group_initial = self.person_position.group
            academic_title_initial = self.person_position.academic_title
            gender_initial = self.person_position.person.gender
            email_initial = self.person_position.main_email()

        self.fields['academic_title'] = forms.ModelChoiceField(queryset=PersonTitle.objects.all(),
                                                               help_text='Select from list',
                                                               initial=academic_title_initial)

        self.fields['gender'] = forms.ModelChoiceField(queryset=Gender.objects.all(),
                                                       help_text='Select from list',
                                                       initial=gender_initial)

        self.fields['first_name'] = forms.CharField(initial=first_name_initial,
                                                    label='First name(s)')

        self.fields['surname'] = forms.CharField(initial=surname_initial,
                                                 label='Surname(s)')

        self.fields['email'] = forms.CharField(initial=email_initial,
                                               )

        self.fields['organisations'] = OrganisationMultipleChoiceField(queryset=Organisation.objects.all(),
                                                                       widget=autocomplete.ModelSelect2Multiple(
                                                                           url='autocomplete-organisations'),
                                                                       initial=organisations_initial,
                                                                       help_text='Please select the organisation(s) to which you are affiliated for the purposes of this proposal',
                                                                       label='Organisation(s)', )

        self.fields['group'] = forms.CharField(initial=group_initial,
                                               help_text='Please type the names of the working group(s) or laboratories to which you are affiliated for the purposes of this proposal',
                                               label='Group / lab',
                                               required=False)

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Div(
                Div('academic_title', css_class='col-2'),
                Div('gender', css_class='col-2'),
                Div('first_name', css_class='col-4'),
                Div('surname', css_class='col-4'),
                css_class='row'
            ),
            Div(
                Div('email', css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div('organisations', css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div('group', css_class='col-12'),
                css_class='row'
            )
        )

    def save_person(self):
        physical_person, created = PhysicalPerson.objects.get_or_create(
            first_name=self.cleaned_data['first_name'],
            surname=self.cleaned_data['surname'],
            gender=self.cleaned_data['gender']
        )

        if self.person_position:
            person_position = self.person_position
        else:
            person_position = PersonPosition()

        person_position.person = physical_person
        person_position.academic_title = self.cleaned_data['academic_title']
        person_position.group = self.cleaned_data['group']

        person_position.save()

        person_position.organisations.set(self.cleaned_data['organisations'])

        try:
            email_contact = person_position.contact_set.get(method=Contact.EMAIL)
        except ObjectDoesNotExist:
            email_contact = Contact()
            email_contact.method = Contact.EMAIL
            email_contact.person_position = person_position

        email_contact.entry = self.cleaned_data['email']
        email_contact.save()

        return person_position


class ProposalForm(ModelForm):
    call_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self._call = kwargs.pop('call', None)

        super().__init__(*args, **kwargs)

        if self.instance.id:
            self.fields['call_id'].initial = self.instance.call.id
        else:
            self.fields['call_id'].initial = self._call.id

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.fields['duration_months'].widget.attrs['min'] = 0

        self.helper.layout = Layout(
            Div(
                Div('call_id', css_class='col-12', hidden='true'),
                Div('title', css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div('geographical_areas', css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div('keywords', css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div('provisional_start_date', css_class='col-4'),
                Div('provisional_end_date', css_class='col-4'),
                Div('duration_months', css_class='col-4'),
                css_class='row'
            )
        )

    def save(self, commit=True):
        self.instance.call_id = self.cleaned_data['call_id']

        model = super().save(commit)

        return model

    class Meta:
        model = Proposal
        fields = ['call_id', 'title', 'geographical_areas', 'keywords', 'provisional_start_date',
                  'provisional_start_date', 'provisional_end_date', 'duration_months']

        widgets = {'keywords': autocomplete.ModelSelect2Multiple(url='autocomplete-keywords'),
                   'geographical_areas': forms.CheckboxSelectMultiple,
                   'provisional_start_date': DatePickerWidget,
                   'provisional_end_date': DatePickerWidget
                   }


class PlainTextWidget(forms.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        if value:
            if type(value) == str:
                final_value = value
            else:
                final_value = value.id

            return '<input type="hidden" name="{}" value="{}" id="{}">'.format(name, final_value, attrs['id'])
        else:
            return '-'


class DataCollectionForm(Form):
    def __init__(self, *args, **kwargs):
        person_position = kwargs.pop('person_position', None)

        super().__init__(*args, **kwargs)

        data_policy_initial = contact_newsletter_initial = None

        if person_position:
            data_policy_initial = person_position.data_policy
            contact_newsletter_initial = person_position.contact_newsletter

        self.fields['data_policy'] = forms.BooleanField(initial=data_policy_initial,
                                                        help_text='By ticking this box you agree to the Swiss Polar Insitute (SPI) storing your '
                                                                  'personal data for the purpose of administering your '
                                                                  'proposal. The data you provide here will be kept private and '
                                                                  'held securely by the SPI and EPFL according '
                                                                  'to the <a href="https://cipd.epfl.ch/en/privacy-policy/">EPFL Privacy Policy</a>. '
                                                                  'Anonymised statistics will also be produced about the proposal applications. '
                                                                  'If your proposal is successful, your data will also be used '
                                                                  'for the administration of your project and may also contribute as '
                                                                  'scientific metadata for the project.',
                                                        label='I agree to my personal data being saved by SPI for administration of my proposal')

        self.fields['contact_newsletter'] = forms.BooleanField(initial=contact_newsletter_initial,
                                                               help_text='By ticking this box you agree to being contacted '
                                                                  'by SPI with news and future opportunities. '
                                                                  'Your contact details will not be used for other purposes.',
                                                               required=False,
                                                               label='I would like to be contacted by SPI with news and future opportunities')

        self.helper = FormHelper(self)
        self.helper.form_tag = False

    def update(self, person_position):
        person_position.data_policy = self.cleaned_data['data_policy']
        person_position.contact_newsletter = self.cleaned_data['contact_newsletter']
        person_position.save()
