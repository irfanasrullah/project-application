from django.views.generic import TemplateView
# import logging

# logger = logging.getLogger('project_core')


class Homepage(TemplateView):
    template_name = 'external/homepage.tmpl'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
