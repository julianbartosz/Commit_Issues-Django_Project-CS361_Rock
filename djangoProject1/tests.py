from django.test import TestCase, Client
from .classes import Auth
from .models import MyUser

class AuthUserTest(TestCase):
    def setUp(self):
        self.auth1 = Auth("test@uwm.edu", "test")
        self.auth2 = Auth("test@uwm.edu", "awooga")
        self.auth3 = Auth("", "awooga")
        self.auth4 = Auth("awooga@uwm.edu", "awooga")
        self.client = Client()
        temp = MyUser(email="test@uwm.edu", password="test")
        temp.save()

    def test_authUser(self):
        self.assertEqual(self.auth1.authUser(), True)
        self.assertEqual(self.auth2.authUser(), True)
        self.assertEqual(self.auth3.authUser(), False)
        self.assertEqual(self.auth4.authUser(), False)

    def test_logIn(self):
        self.assertEqual(self.auth1.logIn(), True)
        self.assertEqual(self.auth2.logIn(), False)
        self.assertEqual(self.auth3.logIn(), False)
        self.assertEqual(self.auth4.logIn(), False)