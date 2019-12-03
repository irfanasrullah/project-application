from django.test import Client
from django.test import TestCase
from django.urls import reverse
from project_core.tests import database_population


class CallFormTest(TestCase):
    def setUp(self):
        database_population.create_management_user()

    def test_homepage_redirects(self):
        c = Client()

        response = c.get(reverse('management-homepage'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '{}?next={}'.format(reverse('accounts-login'), reverse('management-homepage')))

    def test_homepage(self):
        c = Client()

        login = c.login(username='unittest', password='12345')
        self.assertTrue(login)

        response = c.get(reverse('management-homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Homepage')
        self.assertContains(response, 'User:')
        self.assertContains(response, 'unittest')