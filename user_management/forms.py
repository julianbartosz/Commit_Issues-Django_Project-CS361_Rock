from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from user_management.models import User
from course_management.models import Course


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'phone', 'address')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['role'].choices = [('Teaching Assistant', 'Teaching Assistant'), ('Instructor', 'Instructor')]


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
    send_to_all_instructors = forms.BooleanField(required=False, label=_("Send to all instructors"))
    send_to_all_tas = forms.BooleanField(required=False, label=_("Send to all TAs in my courses"))
    send_to_all_tas_in_one_course = forms.BooleanField(required=False, label=_("Send to all TAs in one of my courses"))
    course = forms.ModelChoiceField(queryset=Course.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            if user.role == 'Instructor':
                self.fields['course'].queryset = user.taught_courses.all()
            else:
                self.fields.pop('send_to_all_tas_in_one_course')
                self.fields.pop('course')
            if user.role != 'Supervisor':
                self.fields.pop('send_to_all')
            if user.role != 'Supervisor' and user.role != 'Instructor':
                self.fields.pop('send_to_all_tas')
                self.fields.pop('send_to_all_instructors')
