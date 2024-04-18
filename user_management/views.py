from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CustomUserCreationForm, CustomUserUpdateForm, CustomPasswordChangeForm, EmailForm
from .models import User
from django.core.mail import send_mail


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
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        recipients = []

        if form.cleaned_data.get('send_to_all'):
            recipients = [user.email for user in User.objects.all()]
        elif form.cleaned_data.get('send_to_all_tas'):
            recipients = [user.email for user in User.objects.filter(role='TA')]
        else:
            recipients = [form.cleaned_data['recipient']]

        send_mail(subject, message, 'your-email@uwm.edu', recipients, fail_silently=False)
        return super(SendEmailView, self).form_valid(form)
