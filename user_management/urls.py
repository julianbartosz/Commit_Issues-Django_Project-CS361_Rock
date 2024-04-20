from django.urls import path
from user_management import views
from user_management.views import UserCreateView, UserUpdateView

urlpatterns = [
path('edit-account/', UserUpdateView.as_view(), name='edit_account'),
path('create/', UserCreateView, name='create_user')
]