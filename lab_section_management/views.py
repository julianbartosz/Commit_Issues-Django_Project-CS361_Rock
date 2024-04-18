from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import LabSection
from .forms import LabSectionForm


class LabSectionListView(LoginRequiredMixin, ListView):
    model = LabSection
    template_name = 'lab_section_management/lab_section_list.html'
    context_object_name = 'lab_sections'


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


class LabSectionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LabSection
    form_class = LabSectionForm
    template_name = 'lab_section_management/lab_section_form.html'
    success_url = reverse_lazy('lab_section_list')

    def test_func(self):
        return self.request.user.role in ['Supervisor', 'Instructor']


class LabSectionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LabSection
    template_name = 'lab_section_management/lab_section_confirm_delete.html'
    success_url = reverse_lazy('lab_section_list')

    def test_func(self):
        return self.request.user.role == 'Supervisor'
