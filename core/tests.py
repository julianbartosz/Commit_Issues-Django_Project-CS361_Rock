from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthenticationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='12345',
            first_name='Test',
            last_name='User'
        )

    def test_login_positive(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser@example.com',
            'password': '12345'
        }, follow=True)
        self.assertRedirects(response, reverse('home'))

    def test_login_negative(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser@example.com',
            'password': 'wrongpassword'
        }, follow=True)
        self.assertTrue(
            "Please enter a correct email address and password. Note that both fields may be case-sensitive." in response.content.decode())

    def test_logout(self):
        self.client.login(email='testuser@example.com', password='12345')
        response = self.client.post(reverse('logout'), follow=True)
        self.assertRedirects(response, reverse('home'))

    def test_logout_without_login(self):
        response = self.client.post(reverse('logout'), follow=True)
        self.assertRedirects(response, reverse('home'))
