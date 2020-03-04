import os

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator
from django.db import models
from simple_history.models import HistoricalRecords
from storages.backends.s3boto3 import S3Boto3Storage

from ProjectApplication import settings
from project_core.models import Call, Proposal, CreateModifyOn
from project_core.utils import user_is_in_group_name


class Reviewer(models.Model):
    objects = models.Manager()  # Helps Pycharm CE auto-completion

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    calls = models.ManyToManyField(Call, blank=True)

    def __str__(self):
        calls = ', '.join([str(call) for call in self.calls.all()])
        return f'R: {self.user} C: {calls}'

    @staticmethod
    def filter_proposals(proposals, user):
        if user_is_in_group_name(user, settings.REVIEWER_GROUP_NAME):
            try:
                reviewer = Reviewer.objects.get(user=user)
            except ObjectDoesNotExist:
                proposals = Proposal.objects.none()
                return proposals

            proposals = proposals.filter(call__in=reviewer.calls.all()).filter(eligibility=Proposal.ELIGIBLE)

        return proposals


class ProposalEvaluation(CreateModifyOn):
    PANEL_RECOMMENDATION_FUND = 'Fund'
    PANEL_RECOMMENDATION_RESERVE = 'Reserve'
    PANEL_RECOMMENDATION_DO_NOT_FUND = 'NotFund'

    PANEL_RECOMMENDATION = (
        (PANEL_RECOMMENDATION_FUND, 'Fund'),
        (PANEL_RECOMMENDATION_RESERVE, 'Reserve'),
        (PANEL_RECOMMENDATION_DO_NOT_FUND, 'Do not fund'),
    )

    BOARD_DECISION_FUND = 'Fund'
    BOARD_DECISION_DO_NOT_FUND = 'NotFund'

    BOARD_DECISION = (
        (BOARD_DECISION_FUND, 'Fund'),
        (BOARD_DECISION_DO_NOT_FUND, 'Not Fund'),
    )

    ELIGIBILITYNOTCHECKED = 'Eligibility not checked'
    ELIGIBLE = 'Eligible'
    NOTELIGIBLE = 'Not eligible'

    objects = models.Manager()  # Helps Pycharm CE auto-completion

    proposal = models.OneToOneField(Proposal, on_delete=models.PROTECT)

    allocated_budget = models.DecimalField(help_text='Allocated budget', decimal_places=2, max_digits=10,
                                           validators=[MinValueValidator(0)], blank=True, null=True)

    panel_remarks = models.TextField(blank=True, null=True)
    feedback_to_applicant = models.TextField(blank=True, null=True)
    panel_recommendation = models.CharField(choices=PANEL_RECOMMENDATION, max_length=7)
    board_decision = models.CharField(choices=BOARD_DECISION, max_length=7)
    decision_date = models.DateField(blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.proposal} Recommendation: {self.panel_recommendation}-{self.board_decision}'


def call_evaluation_sheet_rename(instance, filename):
    upload_to = 'call_evaluation'

    filename = f'{instance.call.id}-{filename}'

    return os.path.join(upload_to, filename)


class CallEvaluation(CreateModifyOn):
    objects = models.Manager()  # Helps Pycharm CE auto-completion

    call = models.OneToOneField(Call, on_delete=models.PROTECT)

    panel_date = models.DateField()

    evaluation_sheet = models.FileField(storage=S3Boto3Storage(),
                                        upload_to=call_evaluation_sheet_rename,
                                        blank=True, null=True)

    def __str__(self):
        return f'CallEvaluation {self.id} for call: {self.call.id}'