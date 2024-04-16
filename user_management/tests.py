from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

User = get_user_model()

class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='old_password'
        )
        self.user.save()

    def test_password_reset_request(self):
        """
        Test the password reset request process: submitting email should send an email.
        """
        response = self.client.post(reverse('user_management:password_reset'), {'email': 'testuser@example.com'})
        self.assertEqual(response.status_code, 302)  # Expect redirection to password_reset_done
        self.assertEqual(len(mail.outbox), 1)  # Ensure that one email has been sent
        self.assertIn('Password reset on', mail.outbox[0].subject)  # Check email subject
        self.assertIn('testuser@example.com', mail.outbox[0].to)  # Ensure email is sent to the right user

    def test_password_reset_flow(self):
        """
        Test the full password reset flow from email request to confirming new password.
        """
        # Simulate the user clicking the link in the email
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        # User goes to reset password page
        response = self.client.get(reverse('user_management:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}), follow=True)
        self.assertEqual(response.status_code, 200)  # Check the page is accessible

        # Post new password
        post_response = self.client.post(reverse('user_management:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}), {
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        }, follow=True)
        self.assertRedirects(post_response, reverse('user_management:password_reset_complete'))  # Ensure redirection to reset complete page

        # Ensure the password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

        # Ensure user can login with new password
        login_response = self.client.login(username='testuser@example.com', password='new_password')
        self.assertTrue(login_response)
