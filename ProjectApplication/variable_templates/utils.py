from collections import OrderedDict
from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.forms import Field

from project_core.models import Call, FundingInstrument
from variable_templates.models import CallVariableTemplate, TemplateVariableName, FundingInstrumentVariableTemplate


def get_template_variables_for_call(call: Call):
    template_variables = []

    for template_variable in TemplateVariableName.objects.all():
        template_variables.append(
            {'name': template_variable.name, 'value': get_template_value_for_call(template_variable.name, call)})

    return template_variables


def get_template_variables_for_funding_instrument(funding_instrument: FundingInstrument):
    template_variables = []

    for template_variable in TemplateVariableName.objects.all():
        template_variables.append(
            {'name': template_variable.name,
             'value': get_template_value_for_funding_instrument(template_variable.name, funding_instrument)})

    return template_variables


def copy_template_variables_from_funding_instrument_to_call(call: Call):
    for template_variable in call.funding_instrument.fundinginstrumentvariabletemplate_set.all():
        call_template_variable = CallVariableTemplate(call=call,
                                                      name=template_variable.name,
                                                      value=template_variable.value)
        call_template_variable.save()


def apply_templates_to_string(string: Optional[str], call: Call) -> Optional[str]:
    if string is None:
        return None

    # Replaces the {{ name }}
    template_name_values = {}

    for template_name_value in TemplateVariableName.objects.all():
        template_name_values[template_name_value.name] = template_name_value.default

    for template_name_value in FundingInstrumentVariableTemplate.objects.filter(
            funding_instrument=call.funding_instrument):
        template_name_values[template_name_value.name.name] = template_name_value.value

    for template_name_value in CallVariableTemplate.objects.filter(call=call).all():
        template_name_values[template_name_value.name.name] = template_name_value.value

    for template_name, template_value in template_name_values.items():
        string = string.replace(f'{{{{ {template_name} }}}}',
                                template_value)

    return string


def apply_templates_to_fields(fields: OrderedDict, call):
    for field in fields.items():
        if field[1] is None:
            continue

        if not issubclass(type(field[1]), Field):
            # Check opening a proposal with a ProposalPartnerItemForm
            # It does: self.fields['id'] = self.instance.pk
            # And then here it expects a field (with .label, .help_text)
            # but an int is received
            continue

        field[1].label = apply_templates_to_string(field[1].label, call)
        field[1].help_text = apply_templates_to_string(field[1].help_text, call)


def get_template_value_for_funding_instrument(name, funding_instrument):
    # Returns the template value of the template name for call or the default
    try:
        template_variable_name = FundingInstrumentVariableTemplate.objects.get(funding_instrument=funding_instrument,
                                                                               name__name=name)
        value = template_variable_name.value
        return value

    except ObjectDoesNotExist:
        pass

    try:
        template_variable_name = TemplateVariableName.objects.get(name=name)
        value = template_variable_name.default
        return value
    except ObjectDoesNotExist:
        pass

    assert False


def get_template_value_for_call(name, call):
    # Returns the template value of the template name for call or the default
    try:
        template_variable_name = CallVariableTemplate.objects.get(call=call, name__name=name)
        value = template_variable_name.value
        return value

    except ObjectDoesNotExist:
        pass

    if call.funding_instrument:
        try:
            template_variable_name = FundingInstrumentVariableTemplate.objects.get(
                funding_instrument=call.funding_instrument,
                name__name=name)
            value = template_variable_name.value
            return value
        except ObjectDoesNotExist:
            pass

    try:
        template_variable_name = TemplateVariableName.objects.get(name=name)
        value = template_variable_name.default
        return value
    except ObjectDoesNotExist:
        pass

    assert False
