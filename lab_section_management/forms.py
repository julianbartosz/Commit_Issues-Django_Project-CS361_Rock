from django import forms
from .models import LabSection
from user_management.models import User


class LabSectionForm(forms.ModelForm):
    class Meta:
        model = LabSection
        fields = ['course', 'number', 'tas', 'schedule']
        widgets = {
            'schedule': forms.TextInput(attrs={'placeholder': 'e.g., Mondays, 3-5 PM'}),
            'tas': forms.SelectMultiple(attrs={'size': 8}),
        }
        help_texts = {
            'number': 'Enter the lab section number or identifier.',
            'tas': 'Select one or more TAs for this lab section.',
        }

    def __init__(self, *args, **kwargs):
        super(LabSectionForm, self).__init__(*args, **kwargs)
        self.fields['tas'].queryset = User.objects.filter(role='TA')

    def clean_number(self):
        number = self.cleaned_data['number'].upper()
        if not number.isalnum():
            raise forms.ValidationError('Lab section number must be alphanumeric.')
        return number


#t