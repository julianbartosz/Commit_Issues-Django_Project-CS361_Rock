from django.contrib.auth.forms import UserChangeForm
from django.forms import forms

from TAScheduler.models import MyUser


class MyUserUpdateForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'firstName', 'lastName', 'phoneNumber', 'streetAddress', 'city', 'state', 'zipCode']

    def __init__(self, *args, **kwargs):
        super(MyUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True  # Prevent changing the email

# forms.py


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = '__all__'

