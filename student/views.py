from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from accounts.models import Student
from .serializers import StudentSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from accounts.permission import IsAdminorStafforLibrarian
from django.contrib import messages
from rest_framework.exceptions import PermissionDenied

class StudentCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def perform_create(self, serializer):
        user_data = self.request.data.get('user')  
        
        if user_data is None:
            raise ValueError("User data is required")

        user_serializer = UserSerializer(data=user_data)
        is_student = True
        if user_serializer.is_valid():
            user = user_serializer.save()  

            serializer.save(user=user) 
        else:
            raise ValueError("User data is invalid")

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class StudentView(APIView):

    def get(self, request, pk=None):
        if pk:
            # Retrieve a single student by primary key (pk)
            try:
                student = Student.objects.get(pk=pk)
                serializer = StudentSerializer(student)
                return Response(serializer.data)
            except Student.DoesNotExist:
                return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Retrieve all students
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data)

    def put(self, request, pk=None):
        # Full update of a student (including related user data if provided)
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        # Pass data to the serializer
        student_serializer = StudentSerializer(student, data=request.data)
        if student_serializer.is_valid():
            student_serializer.save()  # The custom update() method in the serializer will handle the update
            return Response(student_serializer.data)
        return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        # Partial update of a student (including related user data if provided)
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        student_serializer = StudentSerializer(student, data=request.data, partial=True)  # partial=True for PATCH
        if student_serializer.is_valid():
            student_serializer.save()  # The custom update() method in the serializer will handle the update
            return Response(student_serializer.data)
        return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        if request.query_params.get('confirm') != 'true':
            messages.warning(request, "Confirmation required to delete the student.")
            raise PermissionDenied("Confirmation required to delete.")

        try:
            student = Student.objects.get(pk=pk)
            student.delete()

            messages.success(request, "Student has been deleted successfully.")

            return Response(
                {"detail": "Student has been deleted successfully."},
                status=status.HTTP_204_NO_CONTENT
            )

        except Student.DoesNotExist:
            messages.error(request, "Student not found.")
            return Response(
                {"detail": "Student not found."},
                status=status.HTTP_404_NOT_FOUND
            )        
        
    def get_permissions(self):

        if self.request.method == 'GET':  
            permission_classes = [IsAuthenticated, IsAdminorStafforLibrarian]
        elif self.request.method in ['PUT','PATCH', 'DELETE']:  
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
