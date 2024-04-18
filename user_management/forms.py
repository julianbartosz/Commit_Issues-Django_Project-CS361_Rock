from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'phone', 'address')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['role'].required = True


class CustomUserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'phone', 'address')

    def __init__(self, *args, **kwargs):
        super(CustomUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True


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


class EmailForm(forms.Form):
    subject = forms.CharField(max_length=100, help_text=_("Enter the subject of your email."))
    message = forms.CharField(widget=forms.Textarea, help_text=_("Enter your message here."))
    recipient = forms.EmailField(help_text=_("Enter the recipient's email address."), required=False)
    send_to_all = forms.BooleanField(required=False, label=_("Send to all users"))
    send_to_all_tas = forms.BooleanField(required=False, label=_("Send to all TAs in my courses"))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            if not user.is_superuser:
                self.fields.pop('send_to_all')
            if user.role != 'Instructor':
                self.fields.pop('send_to_all_tas')
