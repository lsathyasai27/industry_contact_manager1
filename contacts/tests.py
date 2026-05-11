from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from contacts.models import Contact

class ContactAppTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='password123')
        self.contact = Contact.objects.create(
            user=self.user,
            name='Jane Doe',
            company='Acme Co',
            job_title='Product Manager',
            phone='1234567890',
            email='jane@example.com',
            address='123 Test Ave',
            category='professional',
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_dashboard_search_returns_contact(self):
        self.client.login(username='tester', password='password123')
        response = self.client.get(reverse('dashboard'), {'q': 'Acme'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jane Doe')

    def test_api_contacts_returns_json(self):
        self.client.login(username='tester', password='password123')
        response = self.client.get(reverse('api_contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('contacts', response.json())
        self.assertEqual(response.json()['contacts'][0]['name'], 'Jane Doe')

    def test_profile_renders_with_contact_stats(self):
        self.client.login(username='tester', password='password123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account Information')
        self.assertContains(response, 'Total Contacts')
        self.assertContains(response, 'Professional Contacts')
