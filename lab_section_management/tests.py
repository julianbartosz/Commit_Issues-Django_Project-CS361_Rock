from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from .admin import LabSectionAdmin
from lab_section_management.models import LabSection
from .forms import LabSectionForm
from .views import LabSectionListView, LabSectionCreateView, LabSectionDetailView, LabSectionUpdateView, LabSectionDeleteView
from course_management.models import Course
from user_management.models import User


class LabSectionModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(code='CS101', title='Intro to CS', year=2023)
        self.user = User.objects.create(email='testuser', role='TA')
        self.lab_section = LabSection.objects.create(course=self.course, number='001', schedule='MWF 10-11')

    def test_lab_section_creation(self):
        self.assertIsInstance(self.lab_section, LabSection)
        self.assertEqual(self.lab_section.__str__(), 'CS101 - Lab 001 (MWF 10-11)')

    def test_lab_section_with_tas(self):
        self.lab_section.tas.add(self.user)
        self.assertEqual(self.lab_section.tas.count(), 1)
        self.assertEqual(self.lab_section.tas.first(), self.user)

    def test_lab_section_without_tas(self):
        self.assertEqual(self.lab_section.tas.count(), 0)

    def test_lab_section_number_max_length(self):
        max_length = self.lab_section._meta.get_field('number').max_length
        self.assertEqual(max_length, 10)

    def test_lab_section_schedule_max_length(self):
        max_length = self.lab_section._meta.get_field('schedule').max_length
        self.assertEqual(max_length, 50)


class LabSectionViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.course = Course.objects.create(code='CS101', title='Intro to CS', year=2023)
        self.user = User.objects.create(email='testuser', role='Supervisor')
        self.lab_section = LabSection.objects.create(course=self.course, number='001', schedule='MWF 10-11')

    def test_lab_section_list_view(self):
        request = self.factory.get(reverse('lab_section_management:lab_section_list'))
        request.user = self.user
        response = LabSectionListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['lab_sections'].count(), 1)

    def test_lab_section_create_view(self):
        request = self.factory.get(reverse('lab_section_management:lab_section_create'))
        request.user = self.user
        response = LabSectionCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_lab_section_detail_view(self):
        request = self.factory.get(reverse('lab_section_management:lab_section_detail', args=[self.lab_section.pk]))
        request.user = self.user
        response = LabSectionDetailView.as_view()(request, pk=self.lab_section.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['lab_section'], self.lab_section)

    def test_lab_section_update_view(self):
        request = self.factory.get(reverse('lab_section_management:lab_section_update', args=[self.lab_section.pk]))
        request.user = self.user
        response = LabSectionUpdateView.as_view()(request, pk=self.lab_section.pk)
        self.assertEqual(response.status_code, 302)  # Redirects as the user is not a Supervisor or Instructor

    def test_lab_section_delete_view(self):
        request = self.factory.get(reverse('lab_section_management:lab_section_delete', args=[self.lab_section.pk]))
        request.user = self.user
        response = LabSectionDeleteView.as_view()(request, pk=self.lab_section.pk)
        self.assertEqual(response.status_code, 302)  # Redirects as the user is not a Supervisor or Instructor


class LabSectionFormTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(code='CS101', title='Intro to CS', year=2023)
        self.user = User.objects.create(email='testuser', role='TA')
        self.lab_section = LabSection.objects.create(course=self.course, number='001', schedule='MWF 10-11')

    def test_lab_section_form_valid_data(self):
        form = LabSectionForm(data={
            'course': self.course.pk,
            'number': '001',
            'tas': [self.user.pk],
            'schedule': 'MWF 10-11'
        })
        self.assertTrue(form.is_valid())

    def test_lab_section_form_invalid_number(self):
        form = LabSectionForm(data={
            'course': self.course.pk,
            'number': '001!',
            'tas': [self.user.pk],
            'schedule': 'MWF 10-11'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['number'], ['Lab section number must be alphanumeric.'])

    def test_lab_section_form_tas_queryset(self):
        form = LabSectionForm()
        self.assertEqual(form.fields['tas'].queryset.count(), 1)
        self.assertEqual(form.fields['tas'].queryset.first(), self.user)


class LabSectionURLsTest(SimpleTestCase):
    def test_lab_section_list_url_resolves(self):
        url = reverse('lab_section_management:lab_section_list')
        self.assertEqual(resolve(url).func.view_class, LabSectionListView)

    def test_lab_section_create_url_resolves(self):
        url = reverse('lab_section_management:lab_section_create')
        self.assertEqual(resolve(url).func.view_class, LabSectionCreateView)

    def test_lab_section_detail_url_resolves(self):
        url = reverse('lab_section_management:lab_section_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, LabSectionDetailView)

    def test_lab_section_update_url_resolves(self):
        url = reverse('lab_section_management:lab_section_update', args=[1])
        self.assertEqual(resolve(url).func.view_class, LabSectionUpdateView)

    def test_lab_section_delete_url_resolves(self):
        url = reverse('lab_section_management:lab_section_delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, LabSectionDeleteView)


class LabSectionAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = LabSectionAdmin(LabSection, self.site)
        self.course = Course.objects.create(code='CS101', title='Intro to CS', year=2023)
        self.user = User.objects.create(email='testuser', role='TA')
        self.lab_section = LabSection.objects.create(course=self.course, number='001', schedule='MWF 10-11')
        self.lab_section.tas.add(self.user)

    def test_list_display(self):
        self.assertEqual(list(self.admin.list_display), ['course', 'number', 'schedule', 'display_tas'])

    def test_search_fields(self):
        self.assertEqual(list(self.admin.search_fields), ['course__code', 'course__title', 'number'])

    def test_list_filter(self):
        self.assertEqual(list(self.admin.list_filter), ['course'])

    def test_display_tas(self):
        self.assertEqual(self.admin.display_tas(self.lab_section), 'testuser')
