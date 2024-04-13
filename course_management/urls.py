# course_management/urls.py
from django.urls import path
from .views import CourseListView, CourseCreateView, CourseDetailView, CourseUpdateView, CourseDeleteView

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),  # List view of courses
    path('create/', CourseCreateView.as_view(), name='course_create'),  # Create a new course
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),  # Detail view of a specific course
    path('courses/<int:pk>/update/', CourseUpdateView.as_view(), name='course_update'),
    path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
]
