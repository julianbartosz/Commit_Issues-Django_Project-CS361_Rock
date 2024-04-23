from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('users/', include(('user_management.urls', 'user_management'), namespace='user_management')),
    path('courses/', include(('course_management.urls', 'course_management'), namespace='course_management')),
    path('lab_section_management/', include(('lab_section_management.urls', 'lab_section_management'), namespace='lab_section_management')),
]
