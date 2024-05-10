from django.test import TestCase, RequestFactory, Client
from course_management.models import Course
from user_management.models import User
from course_management.forms import CourseForm
from django.contrib.auth.models import AnonymousUser, Permission
from django.urls import reverse, resolve
from course_management.views import CourseDetailView, CourseListView, CourseCreateView, CourseUpdateView, CourseDeleteView
from django.contrib.admin.sites import AdminSite
from course_management.admin import CourseAdmin

# UNIT TESTS


class CourseModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(email='instructor@test.com', password='testpassword')
        self.user2 = User.objects.create(email='ta1@test.com', password='testpassword')
        self.user3 = User.objects.create(email='ta2@test.com', password='testpassword')

    def test_create_course_with_all_fields(self):
        course = Course.objects.create(
            code='CS101',
            title='Intro to CS',
            description='This is a test course.',
            instructor=self.user1,
            semester='Fall',
            year=2022
        )
        course.tas.add(self.user2, self.user3)
        self.assertEqual(course.code, 'CS101')
        self.assertEqual(course.title, 'Intro to CS')
        self.assertEqual(course.description, 'This is a test course.')
        self.assertEqual(course.instructor, self.user1)
        self.assertEqual(list(course.tas.all()), [self.user2, self.user3])
        self.assertEqual(course.semester, 'Fall')
        self.assertEqual(course.year, 2022)

    def test_str_method(self):
        course = Course.objects.create(
            code='CS101',
            title='Intro to CS',
            description='This is a test course.',
            instructor=self.user1,
            semester='Fall',
            year=2022
        )
        self.assertEqual(str(course), 'CS101 - Intro to CS')

    def test_code_unique(self):
        Course.objects.create(
            code='CS101',
            title='Intro to CS',
            description='This is a test course.',
            instructor=self.user1,
            semester='Fall',
            year=2022
        )
        with self.assertRaises(Exception):
            Course.objects.create(
                code='CS101',
                title='Intro to CS 2',
                description='This is another test course.',
                instructor=self.user1,
                semester='Fall',
                year=2022
            )

    def test_instructor_can_be_none(self):
        course = Course.objects.create(
            code='CS101',
            title='Intro to CS',
            description='This is a test course.',
            instructor=None,
            semester='Fall',
            year=2022
        )
        self.assertIsNone(course.instructor)

    def test_tas_can_have_multiple_users(self):
        course = Course.objects.create(
            code='CS101',
            title='Intro to CS',
            description='This is a test course.',
            instructor=self.user1,
            semester='Fall',
            year=2022
        )
        course.tas.add(self.user2, self.user3)
        self.assertEqual(list(course.tas.all()), [self.user2, self.user3])


class CourseDetailViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(email='test@test.com', password='testpassword')
        self.course = Course.objects.create(
            code='CS101',
            title='Intro to CS',
            description='This is a test course.',
            instructor=self.user,
            semester='Fall',
            year=2022
        )

    def test_get_context_data(self):
        request = self.factory.get('/')
        request.user = self.user
        view = CourseDetailView()
        view.setup(request, pk=self.course.pk)
        view.get(request, pk=self.course.pk)
        context = view.get_context_data()
        self.assertEqual(context['course'], self.course)


class CourseListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(email='test@test.com', password='testpassword')
        self.course1 = Course.objects.create(
            code='CS101',
            title='Intro to CS',
            description='This is a test course.',
            instructor=self.user,
            semester='Fall',
            year=2022
        )
        self.course2 = Course.objects.create(
            code='CS102',
            title='Intro to Python',
            description='This is another test course.',
            instructor=self.user,
            semester='Fall',
            year=2022
        )

    def test_get_queryset(self):
        request = self.factory.get('/', {'search': 'Python'})
        request.user = self.user
        view = CourseListView()
        view.setup(request)
        queryset = view.get_queryset()
        self.assertEqual(list(queryset), [self.course2])


class CourseCreateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(email='test@test.com', password='testpassword', role='Supervisor')

    def test_test_func(self):
        request = self.factory.get('/')
        request.user = self.user
        view = CourseCreateView()
        view.setup(request)
        self.assertTrue(view.test_func())


class CourseUpdateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(email='test@test.com', password='testpassword', role='Supervisor')

    def test_test_func(self):
        request = self.factory.get('/')
        request.user = self.user
        view = CourseUpdateView()
        view.setup(request)
        self.assertTrue(view.test_func())


class CourseDeleteViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(email='test@test.com', password='testpassword', role='Supervisor')

    def test_test_func(self):
        request = self.factory.get('/')
        request.user = self.user
        view = CourseDeleteView()
        view.setup(request)
        self.assertTrue(view.test_func())


class CourseFormTest(TestCase):
    def setUp(self):
        self.instructor = User.objects.create(email='instructor@test.com', password='testpassword', role='Instructor')
        self.ta = User.objects.create(email='ta@test.com', password='testpassword', role='TA')

    def test_form_with_valid_data(self):
        form = CourseForm(data={
            'code': 'CS101',
            'title': 'Intro to CS',
            'description': 'This is a test course.',
            'instructor': self.instructor.id,
            'tas': [self.ta.id],
            'semester': 'Fall',
            'year': 2022
        })
        self.assertTrue(form.is_valid())

    def test_form_with_missing_fields(self):
        form = CourseForm(data={})
        self.assertFalse(form.is_valid())

    def test_clean_code_with_non_alphanumeric_code(self):
        form = CourseForm(data={
            'code': 'CS-101',
            'title': 'Intro to CS',
            'description': 'This is a test course.',
            'instructor': self.instructor.id,
            'tas': [self.ta.id],
            'semester': 'Fall',
            'year': 2022
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['code'], ['Course code must be alphanumeric.'])

    def test_clean_year_with_year_less_than_1900(self):
        form = CourseForm(data={
            'code': 'CS101',
            'title': 'Intro to CS',
            'description': 'This is a test course.',
            'instructor': self.instructor.id,
            'tas': [self.ta.id],
            'semester': 'Fall',
            'year': 1899
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['year'], ['Ensure this value is greater than or equal to 1900.'])


class CourseURLsTest(TestCase):
    def test_course_list_url_resolves(self):
        url = reverse('course_management:course_list')
        self.assertEqual(resolve(url).func.view_class, CourseListView)

    def test_course_create_url_resolves(self):
        url = reverse('course_management:course_create')
        self.assertEqual(resolve(url).func.view_class, CourseCreateView)

    def test_course_detail_url_resolves(self):
        url = reverse('course_management:course_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, CourseDetailView)

    def test_course_update_url_resolves(self):
        url = reverse('course_management:course_update', args=[1])
        self.assertEqual(resolve(url).func.view_class, CourseUpdateView)

    def test_course_delete_url_resolves(self):
        url = reverse('course_management:course_delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, CourseDeleteView)


class CourseAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = CourseAdmin(Course, self.site)
        self.instructor = User.objects.create(email='instructor@test.com', password='testpassword', role='Instructor')
        self.ta1 = User.objects.create(email='ta1@test.com', password='testpassword', role='TA')
        self.ta2 = User.objects.create(email='ta2@test.com', password='testpassword', role='TA')
        self.course = Course.objects.create(
            code='CS101',
            title='Intro to CS',
            description='This is a test course.',
            instructor=self.instructor,
            semester='Fall',
            year=2022
        )
        self.course.tas.add(self.ta1, self.ta2)

    def test_list_display(self):
        self.assertEqual(self.admin.list_display, ('code', 'title', 'instructor_name', 'number_of_tas'))

    def test_search_fields(self):
        self.assertEqual(self.admin.search_fields, ('code', 'title', 'instructor__username', 'tas__username'))

    def test_list_filter(self):
        self.assertEqual(self.admin.list_filter, ('instructor', 'tas'))

    def test_instructor_name(self):
        self.assertEqual(self.admin.instructor_name(self.course), 'instructor@test.com')

    def test_number_of_tas(self):
        self.assertEqual(self.admin.number_of_tas(self.course), 2)

# END OF UNIT TESTS
# ACCEPTANCE TESTS


class CourseManagementTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(email='test@test.com', password='testpassword', role='Instructor')
        self.course = Course.objects.create(
            code='101',
            title='Intro to CS',
            description='This is a test course.',
            instructor=self.user,
            semester='Fall',
            year=2022
        )

    def test_course_list_view(self):
        self.client.login(email='test@test.com', password='testpassword')
        response = self.client.get(reverse('course_management:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '101')
        self.assertQuerysetEqual(response.context['courses'], [str(self.course)], transform=str)

    def test_course_create_view(self):
        self.client.login(email='test@test.com', password='testpassword')
        add_course_permission = Permission.objects.get(codename='add_course')
        self.user.user_permissions.add(add_course_permission)
        response = self.client.get(reverse('course_management:course_create'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CourseForm)

    def test_course_update_view(self):
        self.client.login(email='test@test.com', password='testpassword')
        change_course_permission = Permission.objects.get(codename='change_course')
        self.user.user_permissions.add(change_course_permission)
        response = self.client.get(reverse('course_management:course_update', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CourseForm)
        self.assertEqual(response.context['course'], self.course)

    def test_course_delete_view(self):
        self.client.login(email='test@test.com', password='testpassword')
        delete_course_permission = Permission.objects.get(codename='delete_course')
        self.user.user_permissions.add(delete_course_permission)
        response = self.client.get(reverse('course_management:course_delete', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['course'], self.course)

# ACCEPTANCE TESTS END
