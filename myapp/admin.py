from django.contrib import admin
from .models import Student, Instructor, Course, Class, Enrollment

admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Class)
admin.site.register(Enrollment)