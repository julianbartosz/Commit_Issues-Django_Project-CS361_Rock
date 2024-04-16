from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomAuthenticationForm


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(
        template_name='core/login.html',
        authentication_form=CustomAuthenticationForm
    ), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
