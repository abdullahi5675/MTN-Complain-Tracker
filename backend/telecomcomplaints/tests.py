from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from telecomcomplaints.models import Complaint

class TelecomComplaintsTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='testuser@example.com'
        )

    def test_signup_view_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_view_post(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)  # redirects to login
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302, f"Form errors: {response.context.get('form').errors if response.context and 'form' in response.context else 'No form context'}")
        self.assertEqual(response.url, '/')

    def test_home_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_submit_complaint_authenticated_post(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('submit_complaint'), {
            'phone_number': '1234567890',
            'email': 'testuser@example.com',
            'service_type': 'Call Drop',
            'description': 'Frequent dropped calls in my area.',
            'latitude': '6.45',
            'longitude': '3.39'
        })
        # Note: submit_complaint in views.py redirects to thank_you
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Complaint.objects.filter(description='Frequent dropped calls in my area.').exists())
