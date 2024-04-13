from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Course
from .forms import CourseForm


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'course_management/course_detail.html'
    context_object_name = 'course'


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'course_management/course_list.html'
    context_object_name = 'courses'


class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'course_management/course_form.html'
    success_url = reverse_lazy('course_management:course_list')

    def test_func(self):
        return self.request.user.role == 'Supervisor'


class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'course_management/course_form.html'
    success_url = reverse_lazy('course_management:course_list')

    def test_func(self):
        # Allow supervisors to update any course and instructors to update their own courses
        return self.request.user.role == 'Supervisor' or (self.request.user.role == 'Instructor' and self.request.user == self.get_object().instructor)


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    template_name = 'course_management/course_confirm_delete.html'
    success_url = reverse_lazy('course_management:course_list')

    def test_func(self):
        # Allow only supervisors to delete courses
        return self.request.user.role == 'Supervisor'
