from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('users/', include(('user_management.urls', 'user_management'), namespace='user_management')),
    path('courses/', include('course_management.urls')),
    path('lab_sections/', include('lab_section_management.urls')),
]
