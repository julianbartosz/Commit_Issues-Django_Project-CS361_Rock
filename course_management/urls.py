from django.urls import path
from course_management.views import (
    CourseListView,
    CourseCreateView,
    CourseDetailView,
    CourseUpdateView,
    CourseDeleteView,
    SectionCreateView,
    SectionUpdateView,
    SectionDeleteView
)

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),  # List view of courses
    path('create/', CourseCreateView.as_view(), name='course_create'),  # Create a new course
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),  # Detail view of a specific course
    path('<int:pk>/update/', CourseUpdateView.as_view(), name='course_update'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),

    # Section paths
    path('sections/create/', SectionCreateView.as_view(), name='section_create'),
    path('sections/<int:pk>/update/', SectionUpdateView.as_view(), name='section_update'),
    path('sections/<int:pk>/delete/', SectionDeleteView.as_view(), name='section_delete')
]
