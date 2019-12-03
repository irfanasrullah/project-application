from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML
from django import forms
from django.forms import ModelForm

from project_core.forms.utils import get_field_information
from project_core.models import ExternalProject
from project_core.models import PersonPosition, PhysicalPerson, PersonTitle


class PersonPositionMixin:
    def __init__(self):
        pass

    def _add_person_fields(self):
        self.fields['person__physical_person__first_name'] = forms.CharField(
            **get_field_information(PhysicalPerson, 'first_name', help_text=''),
            label='First name(s)')
        self.fields['person__physical_person__surname'] = forms.CharField(
            **get_field_information(PhysicalPerson, 'surname', help_text=''),
            label='Surname(s)')
        self.fields['person__academic_title'] = forms.ModelChoiceField(PersonTitle.objects.all().order_by('title'),
                                                                       label='Academic title',
                                                                       help_text='Select from list',)
        self.fields['person__group'] = forms.CharField(
            **get_field_information(PersonPosition, 'group', label='Group / lab',
                                    help_text='Please type the names of the working group(s) or laboratories to which the overarching project supervisor belongs'))

    def _set_person(self, person):
        if person:
            self.fields['person__group'].initial = person.group
            self.fields['person__academic_title'].initial = person.academic_title
            self.fields['person__physical_person__first_name'].initial = person.person.first_name
            self.fields['person__physical_person__surname'].initial = person.person.surname

    def _save_person(self, person_position):
        person__group = self.cleaned_data['person__group']
        person__academic_title = self.cleaned_data['person__academic_title']
        person__physical_person__first_name = self.cleaned_data['person__physical_person__first_name']
        person__physical_person__surname = self.cleaned_data['person__physical_person__surname']

        if person_position:
            # Needs to update and existing partner
            person_position.group = person__group
            person_position.academic_title = person__academic_title
            person_position.save()

            person__physical_person = person_position.person
            assert person__physical_person

            person__physical_person.first_name = person__physical_person__first_name
            person__physical_person.surname = person__physical_person__surname
            person__physical_person.save()

            return person_position

        else:
            # Needs to create a partner
            physical_person, created = PhysicalPerson.objects.get_or_create(
                first_name=person__physical_person__first_name,
                surname=person__physical_person__surname)

            person_position, created = PersonPosition.objects.get_or_create(
                person=physical_person,
                academic_title=person__academic_title,
                group=person__group,
            )

            return person_position

    def _person_layout(self, description):
        return [
            Div(
                Div(
                    HTML(description), css_class='col-12'),
                css_class='row'),
            Div(
                Div('person__academic_title', css_class='col-2'),
                Div('person__physical_person__first_name', css_class='col-5'),
                Div('person__physical_person__surname', css_class='col-5'),
                css_class='row'
            ),
            Div(
                Div('person__group', css_class='col-12'),
                css_class='row'
            )
        ]


class ProjectOverarchingForm(ModelForm, PersonPositionMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self._add_person_fields()

        # self.fields['id'] = None
        # self.fields['id'].widget = forms.HiddenInput()

        if self.instance:
            self._set_person(self.instance.leader)
            # self.fields['id'] = self.instance.pk

        self.helper.layout = Layout(
            Div(
                Div('id', hidden=True),
                Div('title')
            ),
            *self._person_layout('Please add the details of the overarching project supervisor.')
        )

    def save(self, commit=True):
        project_overarching = super().save(commit=False)

        person = self._save_person(project_overarching.leader)

        project_overarching.leader = person

        if commit:
            project_overarching.save()

        return project_overarching

    class Meta:
        model = ExternalProject
        fields = ['id', 'title', ]