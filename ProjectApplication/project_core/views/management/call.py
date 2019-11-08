from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from project_core.forms.call import CallForm, CallQuestionItemFormSet
from project_core.models import Call, BudgetCategory

CALL_QUESTION_FORM_NAME = 'call_question_form'
CALL_FORM_NAME = 'call_form'


class CallsList(TemplateView):
    template_name = 'management/call-list.tmpl'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['open_calls'] = Call.open_calls()
        context['closed_calls'] = Call.closed_calls()
        context['future_calls'] = Call.future_calls()

        context['active_section'] = 'calls'
        context['active_subsection'] = 'calls-list'
        context['sidebar_template'] = 'management/_sidebar-calls.tmpl'

        return context


class CallDetailView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        call = Call.objects.get(id=kwargs['id'])

        context['call'] = call
        context['active_section'] = 'calls'
        context['active_subsection'] = 'calls-list'
        context['sidebar_template'] = 'management/_sidebar-calls.tmpl'

        call_budget_categories_names = list(call.budget_categories.all().values_list('name', flat=True))

        budget_categories_status = []

        for budget_category_name in BudgetCategory.all_ordered().values_list('name', flat=True):
            in_call = budget_category_name in call_budget_categories_names
            budget_categories_status.append({'in_call': in_call,
                                             'name': budget_category_name})

        context['budget_categories_status'] = budget_categories_status
        return render(request, 'management/call-detail.tmpl', context)


class CallView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'id' in kwargs:
            call_id = kwargs['id']
            call = Call.objects.get(id=call_id)

            context[CALL_FORM_NAME] = CallForm(instance=call, prefix=CALL_FORM_NAME)
            context[CALL_QUESTION_FORM_NAME] = CallQuestionItemFormSet(instance=call, prefix=CALL_QUESTION_FORM_NAME)
            context['call_action_url'] = reverse('management-call-update', kwargs={'id': call_id})
            context['call_action'] = 'Edit'
            context['active_subsection'] = 'calls-list'

        else:
            context[CALL_FORM_NAME] = CallForm(prefix=CALL_FORM_NAME)
            context[CALL_QUESTION_FORM_NAME] = CallQuestionItemFormSet(prefix=CALL_QUESTION_FORM_NAME)
            context['call_action_url'] = reverse('call-add')
            context['call_action'] = 'Create'
            context['active_subsection'] = 'call-add'

        context['active_section'] = 'calls'
        context['sidebar_template'] = 'management/_sidebar-calls.tmpl'

        return render(request, 'management/call.tmpl', context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'id' in kwargs:
            call = Call.objects.get(id=kwargs['id'])
            call_form = CallForm(request.POST, instance=call, prefix=CALL_FORM_NAME)
            call_question_form = CallQuestionItemFormSet(request.POST, instance=call, prefix=CALL_QUESTION_FORM_NAME)

            context['call_action_url'] = reverse('management-call-update', kwargs={'id': call.id})
            call_action = 'Edit'
            action = 'updated'
            active_subsection = 'calls-list'

        else:
            # creates a call
            call_form = CallForm(request.POST, prefix=CALL_FORM_NAME)
            call_question_form = CallQuestionItemFormSet(request.POST, prefix=CALL_QUESTION_FORM_NAME)
            context['call_action_url'] = reverse('call-add')
            context['call_action'] = 'Create'
            call_action = 'Create'
            action = 'created'
            active_subsection = 'call-add'

        if call_form.is_valid() and call_question_form.is_valid():
            call = call_form.save()
            call_question_form.save()

            messages.success(request, 'Call has been saved')
            return redirect(reverse('management-call-detail', kwargs={'id': call.id}) + '?action={}'.format(action))

        context = super().get_context_data(**kwargs)

        context['call_action'] = call_action
        context[CALL_FORM_NAME] = call_form
        context[CALL_QUESTION_FORM_NAME] = call_question_form

        context['active_section'] = 'calls'
        context['active_subsection'] = active_subsection
        context['sidebar_template'] = 'management/_sidebar-calls.tmpl'

        messages.error(request, 'Call not saved. Please correct the errors in the form and try again')

        return render(request, 'management/call.tmpl', context)