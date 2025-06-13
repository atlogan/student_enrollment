# myapp/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student # Import your specific model
from .serializers import StudentSerializer
from .permissions import IsOwnerOrReadOnly
# from django.views.decorators.csrf import csrf_exempt # Import this

# Create your views here.

# @csrf_exempt # Add this decorator
class HealthCheckView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)

class StudentListView(LoginRequiredMixin, ListView):
    model = Student    

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    template_name = 'myapp/student_form.html' # Optional: Defaults to myapp/student_form.html
    fields = ['name', 'major', 'enrollment_date'] # Specify fields to include in the form OR use form_class
    success_url = reverse_lazy('student_list') # Redirect after successful creation

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class StudentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Student
    template_name = 'myapp/student_form.html' # Can reuse the create form template
    fields = ['name', 'major', 'enrollment_date'] # Specify fields
    success_url = reverse_lazy('student_list') # Redirect after successful update
    
    def test_func(self):
        return self.request.user.is_staff
    
class StudentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Student
    template_name = 'myapp/student_confirm_delete.html' # Optional: Defaults to myapp/student_confirm_delete.html
    success_url = reverse_lazy('student_list') # Redirect after successful deletion

    def test_func(self):
        return self.request.user.is_staff
    

class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Student objects to be viewed or edited.
    Provides list, create, retrieve, update, partial_update, destroy actions.
    """
    queryset = Student.objects.all().order_by('-id') # Or appropriate ordering
    serializer_class = StudentSerializer
    
    # Apply permissions: User must be authenticated (global default) 
    # AND be owner for write operations (IsOwnerOrReadOnly check).
    # Read operations allowed if IsAuthenticated passes.
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly] 
    # Filtering configuration (uses global DEFAULT_FILTER_BACKENDS)
    filterset_fields = ['name', 'owner__username'] # Fields for exact matches (e.g., ?field1=value)
    search_fields = ['name', 'major']    # Fields for ?search=... parameter
    ordering_fields = ['major', 'enrollment_date'] # Fields for ?ordering=... parameter
    # Ensure Owner is set to the current user on creation
    def perform_create(self, serializer):
            # Assumes 'owner' field exists on YourModel and is linked to User
            serializer.save(owner=self.request.user)