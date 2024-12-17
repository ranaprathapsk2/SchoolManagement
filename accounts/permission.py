from rest_framework.permissions import BasePermission

class IsAdminorStafforLibrarian(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and (request.user.is_officestaff or request.user.is_superuser or request.user.is_librarian)


class IsAdminorStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_officestaff or request.user.is_superuser) 
    

class IsAdminorLibrarian(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and (request.user.is_librarian or request.user.is_superuser) 
