from django.db import models
from django.conf import settings

class Student(models.Model):
    name = models.CharField(max_length=100)
    major = models.CharField(max_length=50)
    enrollment_date = models.DateField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name}"


class Instructor(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    credits = models.IntegerField()

    def __str__(self):
        return f"{self.course_name}"


class Class(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    schedule = models.CharField(max_length=100)
    semester = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.course.course_name} - {self.semester}"


class Enrollment(models.Model):
    # Using Django's default auto-incrementing id field instead of SERIAL
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE)  # Using class_field since 'class' is a Python keyword
    grade = models.CharField(max_length=2, null=True, blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    class Meta:
        # Ensuring a student can't enroll in the same class twice
        unique_together = ['student', 'class_field']

    def __str__(self):
        return f"{self.student.name} in {self.class_field.course.course_name}"