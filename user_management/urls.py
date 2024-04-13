from django.urls import path
from .views import UserCreateView, UserUpdateView, UserListView, UserDetailView, PasswordChangeView

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='create_user'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='update_user'),
    path('', UserListView.as_view(), name='user_list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),
]