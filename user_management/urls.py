from django.urls import path
from user_management import views

from .views import UserCreateView, UserListView, UserDetailView, PasswordChangeView

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='create_user'),
    path('users/edit-account/<int:pk>/', views.EditAccountView.as_view(), name='edit_account'),
    path('', UserListView.as_view(), name='user_list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),
]# t