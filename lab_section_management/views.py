#tfrom django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from .models import LabSection
from .forms import LabSectionForm


class LabSectionListView(LoginRequiredMixin, ListView):
    model = LabSection
    template_name = 'lab_section_management/lab_section_list.html'
    context_object_name = 'lab_sections'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(course__title__icontains=search_query) |
                Q(number__icontains=search_query)
            )
        return queryset


class LabSectionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = LabSection
    form_class = LabSectionForm
    template_name = 'lab_section_management/lab_section_form.html'
    success_url = reverse_lazy('lab_section_list')

    def test_func(self):
        return self.request.user.role in ['Supervisor', 'Instructor']


class LabSectionDetailView(LoginRequiredMixin, DetailView):
    model = LabSection
    template_name = 'lab_section_management/lab_section_detail.html'
    context_object_name = 'lab_section'

    def test_func(self):
        return True  # All roles can view lab section details


class LabSectionUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    permission_required = 'lab_section_management.view_labsection'
    model = LabSection
    form_class = LabSectionForm
    template_name = 'lab_section_management/lab_section_form.html'

    def get_success_url(self):
        return reverse_lazy('lab_section_management:lab_section_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        lab_section = self.get_object()
        if self.request.user.role == 'Supervisor':
            return True
        elif self.request.user.role == 'Instructor':
            return lab_section.course.instructor == self.request.user
        else:  # For TAs
            return False

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            if 'course' in form.fields:
                del form.fields['course']
            if 'number' in form.fields:
                del form.fields['number']
        if not self.request.user.is_superuser and not self.request.user.groups.filter(name='Instructors').exists():
            if 'schedule' in form.fields:
                del form.fields['schedule']
            if 'TAs' in form.fields:
                del form.fields['TAs']
        return form


class LabSectionDeleteView(PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    permission_required = 'lab_section_management.view_labsection'
    model = LabSection
    template_name = 'lab_section_management/lab_section_confirm_delete.html'
    success_url = reverse_lazy('lab_section_management:lab_section_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lab_section'] = self.object
        return context

    def test_func(self):
        lab_section = self.get_object()
        if self.request.user.role == 'Supervisor':
            return True
        elif self.request.user.role == 'Instructor':
            return lab_section.course.instructor == self.request.user
        else: # For TAs
            return False
