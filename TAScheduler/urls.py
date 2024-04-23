from django.urls import path
from TAScheduler import views

#from TAScheduler.views import LogInPage, Homepage, EditAccountView, CreateUserView
from course_management.views import CreateCoursesView

urlpatterns = [
#path('edit-account/', EditAccountView.as_view(), name='edit_account'),
#path('create/', CreateUserView, name='create_user')
path('/create_course/', CreateCoursesView.as_view())
]