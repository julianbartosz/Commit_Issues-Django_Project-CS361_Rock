from django.urls import path
from TAScheduler import views

from TAScheduler.views import LogInPage, Homepage, EditAccountView, CreateUserView

urlpatterns = [
path('users/edit-account/', EditAccountView.as_view(), name='edit_account'),
path('create/', CreateUserView, name='create_user')
]