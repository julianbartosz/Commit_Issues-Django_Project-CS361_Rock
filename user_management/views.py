from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from .forms import CreateUserForm, MyUserUpdateForm
from .models import MyUser
from .classes import Auth

class UserCreateView(View):
    model = MyUser
    form_class = CreateUserForm
    template_name = 'user_management/create_user.html'
    success_url = reverse_lazy('user_management:user_list')


class UserUpdateView(View):
    model = MyUser
    form_class = MyUserUpdateForm
    template_name = 'user_management/update_user.html'
    success_url = reverse_lazy('user_management:user_list')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.id == self.kwargs['pk']