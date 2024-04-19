from django.contrib import admin
from .models import MyUser, Course, Lab

admin.site.register(MyUser)
admin.site.register(Course)
admin.site.register(Lab)