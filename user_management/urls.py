from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import UserCreateView, UserUpdateView, UserListView, UserDetailView, PasswordChangeView, SendEmailView

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='create_user'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='update_user'),
    path('', UserListView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),
]
