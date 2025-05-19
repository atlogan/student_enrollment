from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Student # Import your specific model

# Create your views here.
class StudentListView(LoginRequiredMixin, ListView):
    model = Student    

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    template_name = 'myapp/student_form.html' # Optional: Defaults to myapp/student_form.html
    fields = ['name', 'major', 'enrollment_date'] # Specify fields to include in the form OR use form_class
    success_url = reverse_lazy('student_list') # Redirect after successful creation
    # Alternatively define get_success_url(self) method
    def form_valid(self, form):
        # Assuming your model has an 'owner' ForeignKey to User
        # Make sure 'owner' is NOT in the 'fields' attribute of the view
        form.instance.owner = self.request.user
        return super().form_valid(form)


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    template_name = 'myapp/student_form.html' # Can reuse the create form template
    fields = ['name', 'major', 'enrollment_date'] # Specify fields
    success_url = reverse_lazy('student_list') # Redirect after successful update

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'myapp/student_confirm_delete.html' # Optional: Defaults to myapp/student_confirm_delete.html
    success_url = reverse_lazy('student_list') # Redirect after successful deletion
