from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from dal import autocomplete
from django import forms
from django.urls import reverse

from project_core.forms.utils import cancel_edit_button
from project_core.models import Project
from project_core.widgets import XDSoftYearMonthDayPickerInput


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        XDSoftYearMonthDayPickerInput.set_format_to_field(self.fields['start_date'])
        XDSoftYearMonthDayPickerInput.set_format_to_field(self.fields['end_date'])

        self.helper = FormHelper(self)
        cancel_url = reverse('logged-project-detail', kwargs={'pk': self.instance.id})

        self.helper.layout = Layout(
            Div(
                Div('title', css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div('keywords', css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div('geographical_areas', css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div('location', css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div('start_date', css_class='col-6'),
                css_class='row'
            ),
            Div(
                Div('end_date', css_class='col-6'),
                css_class='row'
            ),
            FormActions(
                Submit('save', 'Save Project'),
                cancel_edit_button(cancel_url)
            )
        )

    def clean(self):
        cd = super().clean()

        if self.errors:
            return cd

        errors = {}

        if 'start_date' in cd and 'end_date' in cd and \
                cd['start_date'] > cd['end_date']:
            errors['start_date'] = forms.ValidationError(
                'Start date needs to be before the end date')

        if errors:
            raise forms.ValidationError(errors)

        return cd

    class Meta:
        model = Project
        fields = ['title', 'keywords', 'geographical_areas', 'location', 'start_date', 'end_date']
        labels = {'location': 'Precise region'}
        widgets = {'start_date': XDSoftYearMonthDayPickerInput,
                   'end_date': XDSoftYearMonthDayPickerInput,
                   'keywords': autocomplete.ModelSelect2Multiple(url='autocomplete-keywords'),
                   'geographical_areas': forms.CheckboxSelectMultiple
                   }
