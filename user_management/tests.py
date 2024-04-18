from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from pydantic import ValidationError

User = get_user_model()

def get_edit_account_url(user):
    return reverse_lazy('edit_account', kwargs={'pk': user.pk})

class EditAccountViewTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword',
            first_name='John',
            last_name='Doe',
            role='Supervisor',  # or any other role as needed
            phone='1234567890',
            address='123 Test St'
        )

        # Login the user
        self.client.login(email=self.user.email, password='testpassword')

    def test_edit_own_account(self):
        # Ensure the user can edit their own account
        url = get_edit_account_url(self.user)
        updated_data = {
            'email': 'updated_email@example.com',
            'username': 'updated_username',
            'phone': '9999999999',
            'address': '789 Updated St'
        }

        response = self.client.post(url, updated_data, follow=True)
        self.assertEqual(response.status_code, 200)  # Check if update was successful

        # Refresh the user object from the database
        self.user.refresh_from_db()

        # Check if the user's information has been updated
        self.assertEqual(self.user.email, updated_data['email'])
        self.assertEqual(self.user.username, updated_data['username'])
        self.assertEqual(self.user.phone, updated_data['phone'])
        self.assertEqual(self.user.address, updated_data['address'])

    def test_edit_account_unauthenticated(self):
        # Ensure an unauthenticated user cannot access the edit account page
        self.client.logout()  # Logout current user
        url = get_edit_account_url(self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_edit_account_invalid_data(self):
        # Ensure user information does not change with invalid data
        url = get_edit_account_url(self.user)
        invalid_data = {
            'email': 'invalid_email',  # Invalid email format
            'phone': 'abc123',         # Invalid phone number
        }

        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, 200)  # Form should not be valid

        # Refresh the user object from the database
        self.user.refresh_from_db()

        # Check if the user's information remains unchanged
        self.assertNotEqual(self.user.email, invalid_data['email'])
        self.assertNotEqual(self.user.phone, invalid_data['phone'])

    def test_edit_account_blank_data(self):
        # Ensure user information does not change with blank data
        url = get_edit_account_url(self.user)
        blank_data = {
            'email': '',
            'username': '',
            'phone': '',
            'address': '',
        }

        response = self.client.post(url, blank_data)
        self.assertEqual(response.status_code, 200)  # Form should not be valid

        # Refresh the user object from the database
        self.user.refresh_from_db()

        # Check if the user's information remains unchanged
        self.assertNotEqual(self.user.email, blank_data['email'])
        self.assertNotEqual(self.user.username, blank_data['username'])
        self.assertNotEqual(self.user.phone, blank_data['phone'])
        self.assertNotEqual(self.user.address, blank_data['address'])
class CreateUserTests(TestCase):
    def test_create_user_success(self):
        # Attempt to create a user with valid data
        user = User.objects.create_user(
            email="test@example.com",
            username="test_user",
            first_name="Test",
            last_name="User",
            role="Instructor",
            phone="1234567890",
            address="123 Test St"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.role, "Instructor")
        self.assertEqual(user.phone, "1234567890")
        self.assertEqual(user.address, "123 Test St")

    def test_create_user_invalid_information(self):
        # Attempt to create a user with invalid information
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="",
                username="",
                first_name="",
                last_name="",
                role="",
                phone="",
                address=""
            )

    def test_create_user_duplicate_email(self):
        # Create a user with a specific email
        User.objects.create_user(
            email="unique@example.com",
            username="unique_user",
            first_name="Unique",
            last_name="User",
            role="TA",
            phone="1234567890",
            address="456 Unique St"
        )
        # Attempt to create another user with the same email
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="unique@example.com",
                username="another_user",
                first_name="Another",
                last_name="User",
                role="TA",
                phone="9876543210",
                address="789 Another St"
            )

    def test_create_user_duplicate_phone(self):
        # Create a user with a specific phone number
        User.objects.create_user(
            email="another_unique@example.com",
            username="another_unique_user",
            first_name="Another",
            last_name="Unique",
            role="Supervisor",
            phone="1112223333",
            address="789 Another St"
        )
        # Attempt to create another user with the same phone number
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="yet_another@example.com",
                username="yet_another_user",
                first_name="Yet Another",
                last_name="User",
                role="Instructor",
                phone="1112223333",
                address="123 Test St"
            )

        # Attempt to create another user with the same email
        with self.assertRaises(ValueError):
            User.objects.create_user(
                name="Another Jane",
                email="janedoe@example.com",
                office_hours="10:00 AM - 6:00 PM",
                address="789 Elm St, Village",
                role="Assistant",
                phone="5555555555"
            )

        # Attempt to create another user with the same phone number
        with self.assertRaises(ValueError):
            User.objects.create_user(
                name="Yet Another Jane",
                email="yetanotherjane@example.com",
                office_hours="8:00 AM - 4:00 PM",
                address="321 Oak St, Park",
                role="Intern",
                phone="9876543210"
            )

    def test_create_user_invalid_email_format(self):
        # Attempt to create a user with an invalid email format
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="invalid_email_example.com",
                username="invalid_email_user",
                first_name="Invalid",
                last_name="Email",
                role="TA",
                phone="1234567890",
                address="123 Invalid St"
            )

    def test_create_user_invalid_phone_format(self):
        # Attempt to create a user with an invalid phone number format
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="invalid_phone@example.com",
                username="invalid_phone_user",
                first_name="Invalid",
                last_name="Phone",
                role="TA",
                phone="12345",
                address="123 Invalid St"
            )

    def test_create_user_max_length_validation(self):
        # Attempt to create a user with fields exceeding maximum length
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="max_length@example.com",
                username="max_length_user",
                first_name="Max",
                last_name="Length",
                role="Instructor",
                phone="12345678901234567890",
                address="Max Length Address" * 10
            )

    def test_create_user_min_length_validation(self):
        # Attempt to create a user with fields not meeting minimum length
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="a@example.com",
                username="a",
                first_name="A",
                last_name="A",
                role="A",
                phone="1",
                address=""
            )

    def test_create_user_invalid_role(self):
        # Attempt to create a user with an invalid role
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="invalid_role@example.com",
                username="invalid_role_user",
                first_name="Invalid",
                last_name="Role",
                role="Invalid Role",
                phone="1234567890",
                address="123 Invalid St"
            )

    def test_create_user_missing_required_fields(self):
        # Test missing required fields (username, first_name, last_name, email)
        with self.assertRaises(ValidationError) as context:
            User.objects.create_user()

        # Check ValidationError messages for missing fields
        self.assertTrue('username' in context.exception.error_dict)
        self.assertTrue('first_name' in context.exception.error_dict)
        self.assertTrue('last_name' in context.exception.error_dict)
        self.assertTrue('email' in context.exception.error_dict)

