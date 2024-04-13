from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from user_management.forms import CustomUserLoginForm


def home(request):
    return render(request, 'core/home.html')


def login_view(request):
    form = CustomUserLoginForm(data=request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('user_management:user_list')
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
