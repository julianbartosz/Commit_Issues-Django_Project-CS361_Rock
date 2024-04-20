from django.shortcuts import render
from TAScheduler.models import MyUser
class Auth:
    def __init__(self, email, password):
        self.email = email
        self.password = password
    def authUser(self):
        # returns true if the user exists within the MyUser database, false otherwise
        return MyUser.objects.filter(email=self.email).exists()

    def logIn(self):
        if not self.authUser():
            return False

        if MyUser.objects.get(email=self.email).password != self.password:
            return False
        return True

class AdjustUser:
    pass #t