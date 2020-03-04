from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from ProjectApplication import settings
from evaluation.forms.call_evaluation import CallEvaluationForm
from evaluation.forms.proposal_evaluation import ProposalEvaluationForm
from evaluation.models import CallEvaluation
from project_core.models import Proposal, Call
from project_core.utils import user_is_in_group_name
from project_core.views.common.proposal import AbstractProposalDetailView


def update_context(context, proposal_uuid):
    proposal = Proposal.objects.get(uuid=proposal_uuid)

    proposal_evaluation_form = ProposalEvaluationForm(prefix=ProposalEvaluationForm.FORM_NAME,
                                                      proposal=proposal)

    context[ProposalEvaluationForm.FORM_NAME] = proposal_evaluation_form

    context.update({'active_section': 'proposals',
                    'active_subsection': 'proposals-list',
                    'sidebar_template': 'logged/_sidebar-proposals.tmpl'})


class ProposalEvaluationDetail(AbstractProposalDetailView):
    def get(self, request, *args, **kwargs):
        if not user_is_in_group_name(request.user, settings.MANAGEMENT_GROUP_NAME):
            raise PermissionDenied()

        context = self.prepare_context(request, *args, **kwargs)
        update_context(context, kwargs['uuid'])

        return render(request, 'logged/proposal-detail-evaluation-detail.tmpl', context)


class ProposalEvaluationList(TemplateView):
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        context['calls'] = Call.closed_calls()

        context['view_button'] = True
        context['edit_button'] = False
        context['proposal_list_button'] = True
        context['evaluation_spreadsheet_button'] = True
        context['evaluate_button'] = True

        context['active_section'] = 'evaluation'
        context['active_subsection'] = 'evaluation-list'
        context['sidebar_template'] = 'evaluation/_sidebar-evaluation.tmpl'

        return render(request, 'evaluation/evaluation-list.tmpl', context)


class ProposalEvaluationUpdate(AbstractProposalDetailView):
    def get(self, request, *args, **kwargs):
        if not user_is_in_group_name(request.user, settings.MANAGEMENT_GROUP_NAME):
            raise PermissionDenied()

        context = self.prepare_context(request, *args, **kwargs)
        update_context(context, kwargs['uuid'])

        return render(request, 'logged/proposal-detail-evaluation-form.tmpl', context)

    def post(self, request, *args, **kwargs):
        if not user_is_in_group_name(request.user, settings.MANAGEMENT_GROUP_NAME):
            raise PermissionDenied()

        context = self.prepare_context(request, *args, **kwargs)

        proposal = Proposal.objects.get(uuid=kwargs['uuid'])

        proposal_evaluation_form = ProposalEvaluationForm(request.POST, request.FILES, prefix=ProposalEvaluationForm.FORM_NAME,
                                                          proposal=proposal)

        if proposal_evaluation_form.is_valid():
            proposal_evaluation_form.save(user=request.user)

            messages.success(request, 'Evaluation saved')
            return redirect(reverse('logged-proposal-evaluation-detail', kwargs={'uuid': proposal.uuid}))
        else:
            messages.warning(request, 'Evaluation not saved. Verify errors in the form')
            context[ProposalEvaluationForm.FORM_NAME] = proposal_evaluation_form

            context.update({'active_section': 'proposals',
                            'active_subsection': 'proposals-list',
                            'sidebar_template': 'logged/_sidebar-proposals.tmpl'})

            return render(request, 'logged/proposal-detail-evaluation-form.tmpl', context)


class CallEvaluationUpdate(TemplateView):
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'id' in kwargs:
            call_evaluation = CallEvaluation.objects.get(id=kwargs['id'])
            call = call_evaluation.call
        else:
            call_evaluation = None
            call = Call.objects.get(id=self.request.GET['call'])

        context['active_section'] = 'evaluation'
        context['active_subsection'] = 'evaluation-list'
        context['sidebar_template'] = 'evaluation/_sidebar-evaluation.tmpl'

        context['call'] = call

        call_evaluation_form = CallEvaluationForm(instance=call_evaluation, prefix=CallEvaluationForm.FORM_NAME,
                                                  call=call)

        context[CallEvaluationForm.FORM_NAME] = call_evaluation_form

        return render(request, 'evaluation/call_evaluation-form.tmpl', context)

    def post(self, request, *args, **kwargs):
        if not user_is_in_group_name(request.user, settings.MANAGEMENT_GROUP_NAME):
            raise PermissionDenied()

        context = super().get_context_data(**kwargs)

        if 'id' in kwargs:
            call_evaluation = CallEvaluation.objects.get(id=kwargs['id'])
            call = call_evaluation.call
        else:
            call_evaluation = None
            call = Call.objects.get(id=self.request.GET['call'])

        call_evaluation_form = CallEvaluationForm(request.POST, request.FILES, instance=call_evaluation,
                                                  prefix=CallEvaluationForm.FORM_NAME, call=call)

        if call_evaluation_form.is_valid():
            call_evaluation = call_evaluation_form.save_call_evaluation(user=request.user)

            messages.success(request, 'Call evaluation saved')
            return redirect(reverse('logged-call-evaluation-detail', kwargs={'id': call_evaluation.id}))
        else:
            context['active_section'] = 'evaluation'
            context['active_subsection'] = 'evaluation-list'
            context['sidebar_template'] = 'evaluation/_sidebar-evaluation.tmpl'

            messages.warning(request, 'Call evaluation not saved. Verify errors in the form')
            context[CallEvaluationForm.FORM_NAME] = call_evaluation_form

            context['call'] = call

            return render(request, 'evaluation/call_evaluation-form.tmpl', context)


class CallEvaluationDetail(TemplateView):
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        context['active_section'] = 'evaluation'
        context['active_subsection'] = 'evaluation-list'
        context['sidebar_template'] = 'evaluation/_sidebar-evaluation.tmpl'

        context['call_evaluation'] = CallEvaluation.objects.get(id=kwargs['id'])

        return render(request, 'evaluation/call_evaluation-detail.tmpl', context)
