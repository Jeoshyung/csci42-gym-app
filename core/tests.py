from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Exercise, ExerciseCategory, MuscleGroup, Equipment

class AuthTests(TestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.index_url = reverse('index')
        self.workouts_url = reverse('workouts')

        self.user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        self.login_data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        self.user = User.objects.create_user(username='testuser', password='testpassword123')

        self.category = ExerciseCategory.objects.create(name='Cardio')
        self.muscle_group = MuscleGroup.objects.create(name='Legs')
        self.equipment = Equipment.objects.create(name='Treadmill')

        for i in range(15):
            Exercise.objects.create(
                name=f'Exercise {i}',
                description=f'Description for exercise {i}',
                category=self.category,
                muscle_group=self.muscle_group,
                equipment=self.equipment
            )

    def test_register_view(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_user(self):
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)

    def test_index_view_requires_login(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.index_url}')

    def test_workouts_view_requires_login(self):
        response = self.client.get(self.workouts_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.workouts_url}')

    def test_workouts_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.workouts_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workouts.html')
        self.assertContains(response, 'Exercise 0')
        self.assertContains(response, 'Exercise 8')

    def test_workouts_view_pagination(self):
        self.client.login(username='testuser', password='testpassword123')
        
        response = self.client.get(self.workouts_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Exercise 0')
        self.assertContains(response, 'Exercise 8')
        self.assertNotContains(response, 'Exercise 9')

        response = self.client.get(self.workouts_url + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Exercise 9')
        self.assertContains(response, 'Exercise 14')
        self.assertNotContains(response, 'Exercise 0')

    def test_workouts_view_search(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.workouts_url + '?q=Exercise 1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Exercise 1')
        self.assertNotContains(response, 'Exercise 0')
        self.assertNotContains(response, 'Exercise 2')
