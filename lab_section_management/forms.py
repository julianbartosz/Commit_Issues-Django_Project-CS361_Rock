from django import forms
from lab_section_management.models import LabSection
from user_management.models import User


class LabSectionForm(forms.ModelForm):
    class Meta:
        model = LabSection
        fields = ['course', 'number', 'tas', 'schedule', 'has_credits', 'credits']  # Add new fields
        widgets = {
            'schedule': forms.TextInput(attrs={'placeholder': 'e.g., Mondays, 3-5 PM'}),
            'tas': forms.SelectMultiple(attrs={'size': 8}),
        }
        help_texts = {
            'number': 'Enter the lab section number or identifier.',
            'tas': 'Select one or more TAs for this lab section.',
            'has_credits': 'Check if this lab section has separate credits.',
            'credits': 'Enter the credits for this lab section.'
        }

    def __init__(self, *args, **kwargs):
        super(LabSectionForm, self).__init__(*args, **kwargs)
        self.fields['tas'].queryset = User.objects.filter(role='TA')
        # Hide credits field if has_credits is not checked
        if not self.instance.has_credits:
            self.fields['credits'].widget = forms.HiddenInput()

    def clean_number(self):
        number = self.cleaned_data['number'].upper()
        if not number.isalnum():
            raise forms.ValidationError('Lab section number must be alphanumeric.')
        return number

    def clean(self):
        cleaned_data = super().clean()
        has_credits = cleaned_data.get('has_credits')
        credits = cleaned_data.get('credits')

        if has_credits and credits is None:
            raise forms.ValidationError('Credits must be specified if this lab section has separate credits.')

        return cleaned_data
