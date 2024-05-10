from django import forms
from .models import Course, Section
from user_management.models import User


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'title']  # replace 'description' with 'description_html'
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


class SectionForm(forms.ModelForm):
    semester = forms.CharField(max_length=20)
    year = forms.IntegerField()

    class Meta:
        model = Section
        fields = ['course', 'number', 'section_type', 'campus', 'start_date', 'end_date', 'credits', 'semester', 'year']
        widgets = {
            'meeting_html': forms.TextInput(attrs={'placeholder': 'e.g., MW 9:00-10:15'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'course': 'Select the associated course.',
            'number': 'Enter the section number.',
        }
