from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from TAScheduler.classes import Auth, AdjustUser
from TAScheduler.models import MyUser, Roles
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model

User = get_user_model() # t

def get_edit_account_url(user):
    return reverse_lazy('edit_account', kwargs={'pk': user.pk})

class EditAccountViewTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = MyUser.objects.create(
            email='testuser@example.com',
            firstName='John',
            lastName='Doe',
            role=Roles.Instructor,
            phoneNumber='1234567890',
            streetAddress='123 Test St',
            city='Test City',
            state='Test State',
            zipCode='12345'
        )

        # Login the user
        self.client.login(email=self.user.email, password='testpassword')

    def test_edit_own_account(self):
        # Ensure the user can edit their own account
        url = reverse('edit_account')  # Assuming the URL name is 'edit_account'
        updated_data = {
            'email': 'updated_email@example.com',
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone_number': '9999999999',
            'street_address': '789 Updated St',
            'city': 'Updated City',
            'state': 'Updated State',
            'zip_code': '54321'
        }

        response = self.client.post(url, updated_data, follow=True)
        self.assertEqual(response.status_code, 200)  # Check if update was successful

        # Refresh the user object from the database
        self.user.refresh_from_db()

        # Check if the user's information has been updated
        self.assertEqual(self.user.email, updated_data['email'])
        self.assertEqual(self.user.firstName, updated_data['first_name'])
        self.assertEqual(self.user.lastName, updated_data['last_name'])
        self.assertEqual(self.user.phoneNumber, updated_data['phone_number'])
        self.assertEqual(self.user.streetAddress, updated_data['street_address'])
        self.assertEqual(self.user.city, updated_data['city'])
        self.assertEqual(self.user.state, updated_data['state'])
        self.assertEqual(self.user.zipCode, updated_data['zip_code'])

    def test_edit_account_unauthenticated(self):
        # Ensure an unauthenticated user cannot access the edit account page
        self.client.logout()  # Logout current user
        url = reverse('edit_account')  # Assuming the URL name is 'edit_account'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_edit_account_invalid_data(self):
        # Ensure user information does not change with invalid data
        url = reverse('edit_account')  # Assuming the URL name is 'edit_account'
        invalid_data = {
            'email': 'invalid_email',  # Invalid email format
            'phone_number': 'abc123',  # Invalid phone number
        }

        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, 200)  # Form should not be valid

        # Refresh the user object from the database
        self.user.refresh_from_db()

        # Check if the user's information remains unchanged
        self.assertNotEqual(self.user.email, invalid_data['email'])
        self.assertNotEqual(self.user.phoneNumber, invalid_data['phone_number'])

    def test_edit_account_blank_data(self):
        # Ensure user information does not change with blank data
        url = reverse('edit_account')  # Assuming the URL name is 'edit_account'
        blank_data = {
            'email': '',
            'first_name': '',
            'last_name': '',
            'phone_number': '',
            'street_address': '',
            'city': '',
            'state': '',
            'zip_code': '',
        }

        response = self.client.post(url, blank_data)
        self.assertEqual(response.status_code, 200)  # Form should not be valid

        # Refresh the user object from the database
        self.user.refresh_from_db()

        # Check if the user's information remains unchanged
        self.assertNotEqual(self.user.email, blank_data['email'])
        self.assertNotEqual(self.user.firstName, blank_data['first_name'])
        self.assertNotEqual(self.user.lastName, blank_data['last_name'])
        self.assertNotEqual(self.user.phoneNumber, blank_data['phone_number'])
        self.assertNotEqual(self.user.streetAddress, blank_data['street_address'])
        self.assertNotEqual(self.user.city, blank_data['city'])
        self.assertNotEqual(self.user.state, blank_data['state'])
        self.assertNotEqual(self.user.zipCode, blank_data['zip_code'])
class CreateUserTests(TestCase):
    def test_create_user_success(self):
        # Attempt to create a user with valid data
        user = MyUser.objects.create(
            email="test@example.com",
            firstName="Test",
            lastName="User",
            role=Roles.Instructor,
            phoneNumber="1234567890",
            streetAddress="123 Test St",
            city="Test City",
            state="Test State",
            zipCode="12345"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.firstName, "Test")
        self.assertEqual(user.lastName, "User")
        self.assertEqual(user.role, Roles.Instructor)
        self.assertEqual(user.phoneNumber, "1234567890")
        self.assertEqual(user.streetAddress, "123 Test St")

    def test_create_user_invalid_information(self):
        # Attempt to create a user with invalid information
        with self.assertRaises(ValidationError):
            MyUser.objects.create(
                email="",
                firstName="",
                lastName="",
                role="",
                phoneNumber=0,
                streetAddress="",
                city="",
                state="",
                zipCode=0
            )

    def test_create_user_duplicate_email(self):
        # Create a user with a specific email
        MyUser.objects.create(
            email="unique@example.com",
            firstName="Unique",
            lastName="User",
            role=Roles.TA,
            phoneNumber="1234567890",
            streetAddress="456 Unique St",
            city="Unique City",
            state="Unique State",
            zipCode="54321"
        )
        # Attempt to create another user with the same email
        with self.assertRaises(IntegrityError):
            MyUser.objects.create(
                email="unique@example.com",
                firstName="Another",
                lastName="User",
                role=Roles.TA,
                phoneNumber="9876543210",
                streetAddress="789 Another St",
                city="Another City",
                state="Another State",
                zipCode="67890"
            )

class TestAdjustUser(TestCase):
    def setUp(self):
        temp = MyUser(email="test@uwm.edu", password="test")
        temp.save()

    def test_createUser(self): #THIS IS REDUNDANT WITH WHAT IS ABOVE, I INCLUDED IT B/C IT WASN'T MINE
        adjUser = AdjustUser()
        adjUser.createUser("Dragon Dragon", "dragon@uwm.edu", "test", "1234447070", "101 Awooga St. blah blah", Roles.TA)
        self.assertEqual(MyUser.objects.filter(email="dragon@uwm.edu").exists(), True)

        self.assertEqual(adjUser.createUser("Test Wrong", "test@uwm.edu", "11111", "12344448080", "101 Awooga St. blah nah", Roles.Instructor), False)

    def test_deleteUser(self):
        adjUser = AdjustUser()
        self.assertEqual(adjUser.deleteUser("test@uwm.edu"), True)
        self.assertEqual(MyUser.objects.filter(email="test@uwm.edu").exists(), False)
        self.assertEqual(adjUser.deleteUser("test@uwm.edu"), False)
        self.assertEqual(adjUser.deleteUser("nonexistent@uwm.edu"), False)