from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Course
from .forms import CourseForm
from lab_section_management.models import LabSection
from django.db.models import Q


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'course_management/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lab_sections'] = LabSection.objects.filter(course=self.object)
        return context


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'course_management/course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(code__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset


class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'course_management/course_form.html'
    success_url = reverse_lazy('course_management:course_list')

    def test_func(self):
        return self.request.user.role == 'Supervisor' or self.request.user.is_superuser


class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'course_management/course_form.html'

    def get_success_url(self):
        return reverse_lazy('course_management:course_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        # Allow only supervisors or superusers to update courses
        return self.request.user.role == 'Supervisor' or self.request.user.is_superuser


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    template_name = 'course_management/course_confirm_delete.html'
    success_url = reverse_lazy('course_management:course_list')

    def test_func(self):
        # Allow only supervisors to delete courses
        return self.request.user.role == 'Supervisor' or self.request.user.is_superuser
