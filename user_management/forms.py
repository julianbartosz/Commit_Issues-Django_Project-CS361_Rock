from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import forms

from user_management.models import MyUser


class MyUserUpdateForm(UserChangeForm):#t
    password = None  # Hide password field

    class Meta:
        model = MyUser
        fields = ('email', 'phoneNumber', 'streetAddress')

    def __init__(self, *args, **kwargs):
        super(MyUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True

class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ('email', 'role', 'phoneNumber', 'streetAddress')

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['role'].required = True