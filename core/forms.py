# forms.py
from django import forms
from .models import Course
from user_management.models import User


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'title', 'description', 'instructor', 'tas', 'semester', 'year']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'tas': forms.SelectMultiple(attrs={'size': 8}),
        }
        help_texts = {
            'code': 'Enter the unique course code.',
            'title': 'Enter the full title of the course.',
        }

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        # Limit instructor choices to only those who have the role 'Instructor'
        self.fields['instructor'].queryset = User.objects.filter(role='Instructor')
        # Limit TA choices to only those who have the role 'TA'
        self.fields['tas'].queryset = User.objects.filter(role='TA')

    def clean_code(self):
        code = self.cleaned_data['code'].upper()
        if not code.isalnum():
            raise forms.ValidationError('Course code must be alphanumeric.')
        return code
