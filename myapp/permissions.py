# myapp/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        # Allow GET, HEAD or OPTIONS requests for anyone (authenticated or not based on global settings)
        # This method handles view-level permissions (e.g., list/create access)
        # Returning True delegates this check to other permission classes (like IsAuthenticated)
        return True 

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request (GET, HEAD or OPTIONS requests).
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        # Ensure your model has an 'owner' field linked to the User model.
        if not hasattr(obj, 'owner'):
            # Handle cases where the object doesn't have an owner field if necessary
            # For this example, we assume owner exists. Deny if not present.
            return False 
            
        # Instance must have an attribute named `owner`.
        return obj.owner == request.user