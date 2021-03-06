from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from project_core.forms.utils import cancel_edit_button
from project_core.models import TemplateQuestion


class TemplateQuestionList(ListView):
    model = TemplateQuestion
    context_object_name = 'template_questions'
    template_name = 'logged/template_question-list.tmpl'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({'active_section': 'calls',
                        'active_subsection': 'template-question-list',
                        'sidebar_template': 'logged/_sidebar-calls.tmpl'})

        context['breadcrumb'] = [{'name': 'Template questions'}]

        return context


class TemplateQuestionMixin:
    fields = ['question_text', 'question_description', 'answer_type', 'answer_max_length', 'answer_required']

    @property
    def success_msg(self):
        return NotImplemented


class CrispyNoFormTag:
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        if form.instance.id:
            action = 'Save'
            cancel_edit_url = reverse('logged-template-question-detail', kwargs={'pk': form.instance.id})
        else:
            action = 'Create'
            cancel_edit_url = reverse('logged-template-question-add')

        form.fields['question_text'].widget.attrs = {'rows': 2}
        form.fields['question_description'].widget.attrs = {'rows': 2}

        form.helper.layout = Layout(
            Div(
                Div('question_text', css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div('question_description', css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div('answer_type', css_class='col-6'),
                Div('answer_max_length', css_class='col-6'),
                css_class='row'
            ),
            Div(
                Div('answer_required', css_class='col-12'),
                css_class='row'
            ),
            Div(
                Div(HTML('<br>'), css_class='col-12'),
                css_class='row'
            ),
            FormActions(
                Submit('save', f'{action} Template Question'),
                cancel_edit_button(cancel_edit_url)
            )
        )

        return form


class TemplateQuestionCreateView(TemplateQuestionMixin, CrispyNoFormTag, SuccessMessageMixin, CreateView):
    template_name = 'logged/template_question-form.tmpl'
    model = TemplateQuestion
    success_message = 'Template question created'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({'active_section': 'calls',
                        'active_subsection': 'template-questions-add',
                        'sidebar_template': 'logged/_sidebar-calls.tmpl'})

        context['breadcrumb'] = [{'name': 'Template questions', 'url': reverse('logged-template-question-list')},
                                 {'name': 'Create'}]

        return context


class TemplateQuestionUpdateView(TemplateQuestionMixin, CrispyNoFormTag, SuccessMessageMixin, UpdateView):
    template_name = 'logged/template_question-form.tmpl'
    model = TemplateQuestion
    success_message = 'Template question updated'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({'active_section': 'calls',
                        'active_subsection': 'template-question-list',
                        'sidebar_template': 'logged/_sidebar-calls.tmpl'})

        context['breadcrumb'] = [{'name': 'Template questions', 'url': reverse('logged-template-question-list')},
                                 {'name': 'Edit'}]

        return context


class TemplateQuestionDetailView(TemplateQuestionMixin, DetailView):
    template_name = 'logged/template_question-detail.tmpl'
    model = TemplateQuestion
    context_object_name = 'template_question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({'active_section': 'calls',
                        'active_subsection': 'template-question-list',
                        'sidebar_template': 'logged/_sidebar-calls.tmpl'})

        context['breadcrumb'] = [{'name': 'Template questions', 'url': reverse('logged-template-question-list')},
                                 {'name': 'Details'}]

        return context
