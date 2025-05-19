from rest_framework import serializers
from .models import Student # Import your model

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # Option 1: Include all fields
        fields = '__all__'
        # Option 2: Specify fields to include
        # fields = ['id', 'field1', 'field2', 'related_field']
        # Option 3: Specify fields to exclude
        # exclude = ['internal_field']
        
        # Optional: Make some fields read-only (e.g., id, owner)
        read_only_fields = ['id', 'owner']