from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator, ValidationError
from django.forms import Form

from project_core.models import PersonTitle, Gender, PhysicalPerson, PersonPosition, Contact, CareerStage
from project_core.utils.orcid import orcid_div, field_set_read_only
from .utils import organisations_name_autocomplete, get_field_information
from ..utils.utils import create_person_position
from ..widgets import XDSoftYearMonthPickerInput


class PersonForm(Form):
    def __init__(self, *args, **kwargs):
        self.person_position = kwargs.pop('person_position', None)
        super().__init__(*args, **kwargs)

        orcid_initial = first_name_initial = surname_initial = organisations_initial = group_initial = \
            academic_title_initial = email_initial = gender_initial = career_stage_initial = phd_date_initial = None

        if self.person_position:
            orcid_initial = self.person_position.person.orcid
            first_name_initial = self.person_position.person.first_name
            surname_initial = self.person_position.person.surname
            organisations_initial = self.person_position.organisation_names.all()
            group_initial = self.person_position.group
            academic_title_initial = self.person_position.academic_title
            career_stage_initial = self.person_position.career_stage
            gender_initial = self.person_position.person.gender
            email_initial = self.person_position.main_email()

            if self.person_position.person.phd_date:
                # In the database is always saved as yyyy-mm (validator in the model) but it's visualized as mm-yyyy
                phd_date_parts = self.person_position.person.phd_date.split('-')
                phd_date_initial = f'{phd_date_parts[1]}-{phd_date_parts[0]}'

        self.fields['orcid'] = forms.CharField(initial=orcid_initial,
                                               **get_field_information(PhysicalPerson, 'orcid', label='ORCID iD',
                                                                       help_text='Enter your ORCID iD (e.g.: 0000-0002-1825-0097).<br>'
                                                                                 'Please create an <a href="https://orcid.org">ORCID iD</a> if you do not already have one.'))

        self.fields['academic_title'] = forms.ModelChoiceField(queryset=PersonTitle.objects.all(),
                                                               initial=academic_title_initial)

        self.fields['gender'] = forms.ModelChoiceField(queryset=Gender.objects.all(),
                                                       initial=gender_initial)

        self.fields['career_stage'] = forms.ModelChoiceField(queryset=CareerStage.objects.all(),
                                                             initial=career_stage_initial)

        self.fields['first_name'] = forms.CharField(initial=first_name_initial,
                                                    label='First name(s)',
                                                    help_text='Your name is populated from your ORCID record. If you would like to change it please amend it in <a href="https://orcid.org/login">ORCID</a>.')

        self.fields['surname'] = forms.CharField(initial=surname_initial,
                                                 label='Surname(s)',
                                                 help_text='Your surname is populated from your ORCID record. If you would like to change it please amend it in <a href="https://orcid.org/login">ORCID</a>.')

        field_set_read_only([self.fields['first_name'], self.fields['surname']])

        self.fields['email'] = forms.EmailField(initial=email_initial)

        self.fields['phd_date'] = forms.CharField(initial=phd_date_initial,
                                                  label='Date of PhD',
                                                  help_text='Where applicable, please enter the date on which you were awarded, or expect to be awarded your PhD (use the format mm-yyyy).',
                                                  required=False,
                                                  widget=XDSoftYearMonthPickerInput,
                                                  validators=[RegexValidator(regex='^[0-9]{2}-[0-9]{4}$',
                                                                             message='Format is mm-yyyy',
                                                                             code='Invalid format')])

        self.fields['organisation_names'] = organisations_name_autocomplete(initial=organisations_initial,
                                                                            help_text='Please select the organisation(s) to which you are affiliated for the purposes of this proposal.')

        self.fields['group'] = forms.CharField(initial=group_initial,
                                               help_text='Please type the names of the group(s) or laboratories to which you are affiliated for the purposes of this proposal',
                                               label='Group / lab',
                                               required=False)

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            orcid_div('orcid'),
            Div(
                Div('first_name', css_class='col-4'),
                Div('surname', css_class='col-4'),
                Div('academic_title', css_class='col-2'),
                Div('gender', css_class='col-2'),
                css_class='row'
            ),
            Div(
                Div('email', css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div('organisation_names', css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div('group', css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div('career_stage', css_class='col-8'),
                Div('phd_date', css_class='col-4'),
                css_class='row'
            ),
        )

    def get_person_positions(self):
        """ Matches and returns the person_position from the database. """

        try:
            physical_person = PhysicalPerson.objects.get(
                orcid=self.cleaned_data['orcid']
            )
        except ObjectDoesNotExist:
            # Non-existing PHysicalPerson so it doesn't have any PersonPositions associated
            return []

        person_positions = PersonPosition.objects.filter(
            person=physical_person,
            academic_title=self.cleaned_data['academic_title'],
            group=self.cleaned_data['group'],
            career_stage=self.cleaned_data['career_stage']
        )

        return person_positions

    def clean_phd_date(self):
        if 'phd_date' not in self.cleaned_data:
            return None

        if self.cleaned_data['phd_date'] == '':
            return None

        # It has the correct format mm-yyyy because the field has a validator
        # In the DB it's always yyyy-mm because the model has this validator (consistent with general mysql date format)
        month, year = self.cleaned_data['phd_date'].split('-')

        month_int = int(month)
        if month_int < 1 or month_int > 12:
            raise ValidationError(f'Invalid month: {month}', code='invalid', params={'value': month})

        return f'{year}-{month}'

    def clean(self):
        super().clean()

    def save_person(self):
        cd = self.cleaned_data

        person_position = create_person_position(cd['orcid'], cd['first_name'], cd['surname'], gender=cd['gender'],
                                                 phd_date=cd['phd_date'], academic_title=cd['academic_title'],
                                                 group=cd['group'], career_stage=cd['career_stage'],
                                                 organisation_names=cd['organisation_names'])

        try:
            email_contact = person_position.contact_set.get(method=Contact.EMAIL)
        except ObjectDoesNotExist:
            email_contact = Contact()
            email_contact.method = Contact.EMAIL
            email_contact.person_position = person_position

        email_contact.entry = self.cleaned_data['email']
        email_contact.save()

        return person_position
