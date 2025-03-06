from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTests(TestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.index_url = reverse('index')
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        self.login_data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }

    def test_register_view(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_user(self):
        User.objects.create_user(username='testuser', password='testpassword123')
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertRedirects(response, self.index_url)

    def test_index_view_requires_login(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertRedirects(response, f'{self.login_url}?next={self.index_url}')
