from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse
from django.views.generic import TemplateView
from .forms.proposal import PersonForm, ProposalForm, QuestionsForProposalForm, BudgetForm
from .models import Proposal, Call, ProposalStatus


class Homepage(TemplateView):
    template_name = 'homepage.tmpl'

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        return context


class CallsView(TemplateView):
    template_name = 'list_calls.tmpl'

    def get_context_data(self, **kwargs):
        context = super(CallsView, self).get_context_data(**kwargs)

        context['calls'] = Call.objects.all()

        return context


class ProposalThankYouView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = super(ProposalThankYouView, self).get_context_data(**kwargs)

        context['pk'] = kwargs['pk']

        return render(request, 'proposal-thank-you.tmpl', context)


class ProposalView(TemplateView):
    def get(self, request, *args, **kwargs):
        super(ProposalView, self).get_context_data(**kwargs)

        information = {}

        if 'pk' in kwargs:
            proposal_pk = kwargs['pk']
            call = Proposal.objects.get(pk=kwargs['pk']).call

            proposal: Proposal = Proposal.objects.get(pk=proposal_pk)

            information['proposal_form'] = ProposalForm(call=call, prefix='proposal', instance=proposal)
            information['person_form'] = PersonForm(prefix='person', instance=proposal.applicant)

            information['questions_for_proposal_form'] = QuestionsForProposalForm(proposal=proposal, prefix='questions_for_proposal')
            information['budget_form'] = BudgetForm(proposal=proposal, prefix='budget')

            information['proposal_action_url'] = reverse('proposal-update', kwargs={'pk': proposal_pk})

        else:
            call_pk = information['call_pk'] = request.GET.get('call')
            call = Call.objects.get(pk=call_pk)

            information['proposal_form'] = ProposalForm(call=call, prefix='proposal')
            information['person_form'] = PersonForm(prefix='person')
            information['questions_for_proposal_form'] = QuestionsForProposalForm(call=call, prefix='questions_for_proposal')
            information['budget_form'] = BudgetForm(call=call, prefix='budget')

            information['proposal_action_url'] = reverse('proposal-add')

        information.update(ProposalView._call_information_for_template(call))

        return render(request, 'proposal.tmpl', information)

    @staticmethod
    def _call_information_for_template(call):
        information = {}
        information['maximum_budget'] = call.budget_maximum
        information['call_name'] = call.long_name
        information['call_introductory_message'] = call.introductory_message
        information['call_submission_deadline'] = call.submission_deadline

        return information

    def post(self, request, *args, **kwargs):
        context = super(ProposalView, self).get_context_data(**kwargs)

        proposal_pk = None

        if 'pk' in kwargs:
            proposal_pk = int(kwargs['pk'])
            call = Proposal.objects.get(pk=proposal_pk).call
        else:
            call = Call.objects.get(id=int(request.POST['proposal-call_id']))

        if proposal_pk is None:
            # It's a new Proposal
            person_form = PersonForm(request.POST, prefix='person')
            proposal_form = ProposalForm(request.POST, prefix='proposal')
            questions_for_proposal_form = QuestionsForProposalForm(request.POST,
                                                                   call=call,
                                                                   prefix='questions_for_proposal')
            budget_form = BudgetForm(request.POST, call=call, prefix='budget')
        else:
            # It needs to modify an existing Proposal
            proposal = Proposal.objects.get(pk=proposal_pk)

            person_form = PersonForm(request.POST, instance=proposal.applicant, prefix='person')
            proposal_form = ProposalForm(request.POST, instance=proposal, prefix='proposal')
            questions_for_proposal_form = QuestionsForProposalForm(request.POST,
                                                                   proposal=proposal,
                                                                   prefix='questions_for_proposal')
            budget_form = BudgetForm(request.POST, proposal=proposal, prefix='budget')

        if person_form.is_valid() and proposal_form.is_valid() and questions_for_proposal_form.is_valid() \
                and budget_form.is_valid():
            applicant = person_form.save()
            proposal = proposal_form.save(commit=False)

            proposal.applicant = applicant

            proposal.proposal_status = ProposalStatus.objects.get(name='test01')

            proposal = proposal_form.save(commit=True)

            budget_form._proposal_id = proposal.id

            questions_for_proposal_form._proposal_id = proposal.pk
            questions_for_proposal_form.save_answers()

            proposal.save()

            budget_form.save_budget()

            return redirect(reverse('proposal-thank-you', kwargs={'pk': proposal.pk}))

        context['person_form'] = person_form
        context['proposal_form'] = proposal_form
        context['questions_for_proposal_form'] = questions_for_proposal_form
        context['budget_form'] = budget_form

        context.update(ProposalView._call_information_for_template(call))

        return render(request, 'proposal.tmpl', context)
