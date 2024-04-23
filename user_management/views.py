from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CustomUserCreationForm, CustomUserUpdateForm, CustomPasswordChangeForm, EmailForm
from user_management.models import User
from django.core.mail import send_mail
from django.db.models import Q, Count


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'user_management/create_user.html'
    success_url = reverse_lazy('user_management:user_list')


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'user_management/update_user.html'
    success_url = reverse_lazy('user_management:user_list')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.id == self.kwargs['pk']


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'user_management/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get the query parameters
        role = self.request.GET.get('role')
        department = self.request.GET.get('department')
        num_lab_sections = self.request.GET.get('num_lab_sections')
        sort_order = self.request.GET.get('sort_order')

        # Apply the filters
        if role:
            queryset = queryset.filter(role=role)
        if department:
            queryset = queryset.filter(department=department)
        if num_lab_sections:
            queryset = queryset.annotate(num_lab_sections=Count('lab_sections')).filter(
                num_lab_sections=num_lab_sections)
        if sort_order == 'alphabetical':
            queryset = queryset.order_by('name')

        return queryset

    def test_func(self):
        return self.request.user.role in ['Supervisor', 'Instructor', 'TA']


class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    template_name = 'user_management/user_detail.html'
    context_object_name = 'user'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role == 'TA' or self.request.user.id == self.kwargs['pk'] or self.request.user.role == 'Instructor' or self.request.user.role == 'Supervisor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == 'Instructor':
            context['courses'] = self.object.taught_courses.all()
            context['tas'] = User.objects.filter(role='TA')
        elif self.request.user.role == 'TA':
            context['tas'] = User.objects.filter(role='TA')
        return context


class PasswordChangeView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomPasswordChangeForm
    template_name = 'user_management/change_password.html'
    success_url = reverse_lazy('core:login')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = self.request.user
        if user.check_password(form.cleaned_data['old_password']):
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            return super().form_valid(form)
        form.add_error(None, 'Old password is incorrect')
        return self.form_invalid(form)


class SendEmailView(LoginRequiredMixin, FormView):
    template_name = 'user_management/email/send_email.html'
    form_class = EmailForm
    success_url = reverse_lazy('user_management:user_list')

    def get_form_kwargs(self):
        kwargs = super(SendEmailView, self).get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        recipients = []

        if 'send_to_all' in form.cleaned_data and form.cleaned_data.get('send_to_all'):
            recipients = [user.email for user in User.objects.all()]
        else:
            if 'send_to_all_instructors' in form.cleaned_data and form.cleaned_data.get('send_to_all_instructors'):
                instructors = User.objects.filter(role='Instructor')
                instructor_emails = [user.email for user in instructors]
                recipients.extend(instructor_emails)
            if 'send_to_all_tas_in_one_course' in form.cleaned_data and form.cleaned_data.get(
                    'send_to_all_tas_in_one_course'):
                course = form.cleaned_data.get('course')
                tas = User.objects.filter(role='TA', assigned_courses=course)
                recipients.extend([user.email for user in tas])
            elif 'send_to_all_tas' in form.cleaned_data and form.cleaned_data.get('send_to_all_tas'):
                if self.request.user.role == 'Supervisor':
                    tas = User.objects.filter(role='TA')
                else:  # For instructors
                    instructor_courses = self.request.user.taught_courses.all()
                    tas = User.objects.filter(role='TA', assigned_courses__in=instructor_courses)
                recipients.extend([user.email for user in tas])
            if not recipients and 'recipient' in form.cleaned_data and form.cleaned_data.get('recipient'):
                recipients = [form.cleaned_data['recipient']]

        result = send_mail(subject, message, 'your-email@uwm.edu', recipients, fail_silently=False)

        return super(SendEmailView, self).form_valid(form)
