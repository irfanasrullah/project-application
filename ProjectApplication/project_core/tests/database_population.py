from datetime import datetime

from django.contrib.auth.models import User

from project_core.models import BudgetCategory, Call, TemplateQuestion, GeographicalArea, Keyword, KeywordUid, Source, \
    PersonTitle, Gender, Organisation, Country, OrganisationUid, ProposalStatus, CareerStage, OrganisationName


def create_call():
    call, created = Call.objects.get_or_create(long_name='GreenLAnd Circumnavigation Expedition',
                                               call_open_date=datetime(2019, 1, 1),
                                               submission_deadline=datetime(2025, 1, 31),
                                               budget_maximum=100_000, other_funding_question=False,
                                               proposal_partner_question=True)

    return call


def create_geographical_areas():
    antarctic, created = GeographicalArea.objects.get_or_create(name='Antarctic', definition='Very south')
    arctic, created = GeographicalArea.objects.get_or_create(name='Arctic', definition='Very north')
    high_peak, created = GeographicalArea.objects.get_or_create(name='High peaks', definition='Very high')

    return antarctic, arctic, high_peak


def create_keywords():
    source, created = Source.objects.get_or_create(source='Unit test')

    keyword_uuid, created = KeywordUid.objects.get_or_create(uid='test-2040242', source=source)

    algae, created = Keyword.objects.get_or_create(name='Algae', uid=keyword_uuid)
    birds, created = Keyword.objects.get_or_create(name='Birds', uid=keyword_uuid)

    return algae, birds


def create_career_stages():
    career, created = CareerStage.objects.get_or_create(name='PhD More than 5 years')

    return career,


def create_proposal_status():
    proposal_status_submitted, created = ProposalStatus.objects.get_or_create(name='Submitted')
    proposal_status_draft, created = ProposalStatus.objects.get_or_create(name='Draft')

    return proposal_status_submitted, proposal_status_draft


def create_budget_categories():
    travel, created = BudgetCategory.objects.get_or_create(name='Travel',
                                                           defaults={
                                                               'description': 'Funds needed to reach the destination'})

    data_processing, created = BudgetCategory.objects.get_or_create(name='Data processing',
                                                                    defaults={
                                                                        'description': 'Funds needed to process data'})

    equipment_consumables, created = BudgetCategory.objects.get_or_create(name='Equipment / consumables', defaults={
        'description': 'Budget required for equipment or other consumables that would be needed for the proposed work'})

    return travel, data_processing, equipment_consumables


def create_template_questions():
    template_question1, created = TemplateQuestion.objects.get_or_create(
        question_text='Explain which methods of transport are needed to go to the location',
        question_description='Explain it detailed',
        answer_type=TemplateQuestion.TEXT,
        answer_max_length=500)

    template_question2, created = TemplateQuestion.objects.get_or_create(
        question_text='Explain how to do science',
        question_description='In very short',
        answer_type=TemplateQuestion.TEXT,
        answer_max_length=50)

    return template_question1, template_question2


def create_management_user():
    user = User.objects.create_user(username='unittest', password='12345')
    user.save()

    return user


def create_person_titles():
    person_title_mr, created = PersonTitle.objects.get_or_create(title='Mr')

    return person_title_mr,


def create_genders():
    gender, created = Gender.objects.get_or_create(name='Man')

    return gender,


def create_organisations():
    country, created = Country.objects.get_or_create(name='Switzerland')
    source, created = Source.objects.get_or_create(source='Somewhere in the brain')

    organisation1_uid, created = OrganisationUid.objects.get_or_create(source=source,
                                                                       uid='646a6e1c-2378-46d9-af42-a3710c5aee89')
    organisation1, created = Organisation.objects.get_or_create(long_name='École Polytechnique Fédérale de Lausanne',
                                                                short_name='EPFL', country=country,
                                                                uid=organisation1_uid)

    organisation2_uid, created = OrganisationUid.objects.get_or_create(source=source,
                                                                       uid='646a6e1c-2378-46d9-af42-a3710c5aee89')
    organisation2, created = Organisation.objects.get_or_create(long_name='Swiss Polar Foundation',
                                                                short_name='SPF', country=country,
                                                                uid=organisation2_uid)

    return organisation1, organisation2


def create_organisation_names():
    organisation1, created = OrganisationName.objects.get_or_create(name='EPFL')
    organisation2, created = OrganisationName.objects.get_or_create(name='SPF')

    return organisation1, organisation2

