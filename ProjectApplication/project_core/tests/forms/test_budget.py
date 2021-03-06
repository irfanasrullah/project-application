from django.test import TestCase

from project_core.forms.budget import BudgetItemForm
from project_core.tests import database_population
from project_core.tests.utils_for_tests import dict_to_multivalue_dict


class BudgetItemFormTest(TestCase):
    def setUp(self):
        self._budget_categories = database_population.create_budget_categories()
        self._proposal = database_population.create_proposal()

    def test_invalid_amount(self):
        budget_item_data = dict_to_multivalue_dict(
            {
                'category': self._budget_categories[0].id,
                'details': 'Trips',
                'amount': 'Some Invalid Number'
            }
        )

        budget_item_form = BudgetItemForm(data=budget_item_data)

        self.assertFalse(budget_item_form.is_valid())
        self.assertIn('amount', budget_item_form.errors)

    def test_no_amount_with_details(self):
        budget_item_data = dict_to_multivalue_dict(
            {
                'category': self._budget_categories[0].id,
                'details': 'Trips'
            }
        )

        budget_item_form = BudgetItemForm(data=budget_item_data)

        self.assertFalse(budget_item_form.is_valid())
        self.assertIn('amount', budget_item_form.errors)

    def test_amount_is_zero_with_details(self):
        budget_item_data = dict_to_multivalue_dict(
            {
                'category': self._budget_categories[0].id,
                'details': 'Trips',
                'amount': '0'
            }
        )

        budget_item_form = BudgetItemForm(data=budget_item_data)

        self.assertTrue(budget_item_form.is_valid())

    def test_no_details_with_amount(self):
        budget_item_data = dict_to_multivalue_dict(
            {
                'category': self._budget_categories[0].id,
                'amount': '100'
            }
        )

        budget_item_form = BudgetItemForm(data=budget_item_data)

        self.assertFalse(budget_item_form.is_valid())
        self.assertIn('details', budget_item_form.errors)

    def test_valid_budget(self):
        budget_item_data = dict_to_multivalue_dict(
            {
                'category': self._budget_categories[0].id,
                'details': 'Trips',
                'amount': 100
            }
        )

        budget_item_form = BudgetItemForm(data=budget_item_data)

        self.assertTrue(budget_item_form.is_valid())
