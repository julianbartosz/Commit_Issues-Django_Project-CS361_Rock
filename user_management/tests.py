from django.test import TestCase, SimpleTestCase, RequestFactory
from django.urls import reverse
from unittest.mock import patch
from django.http import HttpResponse
from .models import User
from .forms import CustomUserCreationForm
from .views import UserCreateView
from user_management.models import User


class UserModelTestCase(TestCase):
    def test_user_full_name(self):
        user = User(email='test@example.com', first_name="John", last_name="Doe")
        self.assertEqual(user.get_full_name(), 'John Doe')

    def test_user_short_name(self):
        user = User(email='test@example.com', first_name="John")
        self.assertEqual(user.get_short_name(), 'John')


class UserFormTestCase(SimpleTestCase):
    def test_custom_user_creation_form_password_validation(self):
        form = CustomUserCreationForm(data={
            'email': 'test@example.com',
            'password1': 'password',
            'password2': 'password_mismatch'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_custom_user_creation_form_required_fields(self):
        form = CustomUserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class UserViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('user_management.views.UserCreateView.form_valid')
    @patch('user_management.forms.CustomUserCreationForm.save')
    def test_user_create_view_post(self, mock_save, mock_form_valid):
        mock_save.return_value = None
        mock_form_valid.return_value = HttpResponse()

        request = self.factory.post(reverse('create_user'), data={
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'role': 'TA'
        })
        response = UserCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
