from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm, CustomPasswordChangeForm
from .models import User


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'user_management/create_user.html'
    success_url = reverse_lazy('user_management:user_list')

class EditAccountView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['email', 'username', 'phone', 'address']  # Update with your desired fields
    template_name = 'user_management/edit_account.html'  # Update with your template
    success_url = reverse_lazy('home')  # Update with your success URL

    def get_object(self, queryset=None):
        return self.request.user

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.id == self.kwargs['pk']

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'user_management/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        if self.request.user.role == 'Supervisor':
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)


class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    template_name = 'user_management/user_detail.html'
    context_object_name = 'user'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.id == self.kwargs['pk']


class PasswordChangeView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomPasswordChangeForm
    template_name = 'user_management/change_password.html'
    success_url = reverse_lazy('user_management:login')

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
