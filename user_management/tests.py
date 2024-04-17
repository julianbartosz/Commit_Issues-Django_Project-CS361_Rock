from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

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
