from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username', 'role', 'phone', 'address')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['role'].required = True

class CustomUserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'address']


class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')


class CustomUserUpdateForm(UserChangeForm):
    password = None  # Hide password field t

    class Meta:
        model = User
        fields = ('email', 'username', 'phone', 'address')

    def __init__(self, *args, **kwargs):
        super(CustomUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True  # Prevent changing the email


class CustomPasswordChangeForm(forms.ModelForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ()

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', 'New password and Confirm new password do not match')

        return cleaned_data
