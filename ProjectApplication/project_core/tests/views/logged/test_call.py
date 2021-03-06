from django.test import TestCase
from django.urls import reverse

from project_core.tests import database_population
from variable_templates.tests.database_population import create_default_template_variables


class CallListTest(TestCase):
    def setUp(self):
        self._call = database_population.create_call()
        self._user = database_population.create_management_user()
        self._client_management = database_population.create_management_logged_client()

    def test_list_calls(self):
        response = self._client_management.get(reverse('logged-call-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self._call.long_name)

    def test_call_view(self):
        response = self._client_management.get(reverse('logged-call-detail', kwargs={'pk': self._call.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self._call.long_name)

    def test_create_call_view(self):
        response = self._client_management.get(reverse('logged-call-update', kwargs={'pk': self._call.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self._call.long_name)

    def test_load_create_call_add(self):
        response = self._client_management.get(reverse('logged-call-add'))
        self.assertEqual(response.status_code, 200)


class ProposalListTest(TestCase):
    def setUp(self):
        self._proposal = database_population.create_proposal()
        self._client_management = database_population.create_management_logged_client()

    def test_list_of_proposals_for_call(self):
        response = self._client_management.get(
            reverse('logged-call-list-proposals', kwargs={'call_id': self._proposal.call.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self._proposal.title)


class ProposalDetailTest(TestCase):
    def setUp(self):
        self._proposal = database_population.create_proposal()
        self._client_management = database_population.create_management_logged_client()
        create_default_template_variables()

    def test_proposal_detail(self):
        response = self._client_management.get(
            reverse('logged-call-proposal-detail', kwargs={'pk': self._proposal.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self._proposal.title)
