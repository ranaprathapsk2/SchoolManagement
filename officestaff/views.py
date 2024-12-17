from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from accounts.models import OfficeStaff
from student.serializers import UserSerializer
from .serializers import OfficeStaffSerializer, OfficeStaffinSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import messages
from rest_framework.exceptions import PermissionDenied

#login for office satff 
class OfficeStaffLoginView(APIView):
    
    def post(self, request):
        serializer = OfficeStaffinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']

        if user:
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Authentication failed.'}, status=status.HTTP_401_UNAUTHORIZED)
     
#office staff user create
class OfficeStaffCreateView(generics.CreateAPIView):
    queryset = OfficeStaff.objects.all() 
    serializer_class = OfficeStaffSerializer  #
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def perform_create(self, serializer):
        user_data = self.request.data.get('user')  
        
        if user_data is None:
            raise ValueError("User data is required")
        
        user_serializer = UserSerializer(data=user_data)
               
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
        
#office staff user get, update, delete
class OfficeStaffView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk=None):
        if pk:
            try:
                office_staff = OfficeStaff.objects.get(pk=pk)
                serializer = OfficeStaffSerializer(office_staff)
                return Response(serializer.data)
            except OfficeStaff.DoesNotExist:
                return Response({"detail": "Office staff not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            office_staff = OfficeStaff.objects.all()
            serializer = OfficeStaffSerializer(office_staff, many=True)
            return Response(serializer.data)

    def put(self, request, pk=None):
        try:
            office_staff = OfficeStaff.objects.get(pk=pk)
        except OfficeStaff.DoesNotExist:
            return Response({"detail": "Office staff not found."}, status=status.HTTP_404_NOT_FOUND)

        office_staff_serializer = OfficeStaffSerializer(office_staff, data=request.data)
        if office_staff_serializer.is_valid():
            office_staff_serializer.save()  
            return Response(office_staff_serializer.data)
        return Response(office_staff_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        try:
            office_staff = OfficeStaff.objects.get(pk=pk)
        except OfficeStaff.DoesNotExist:
            return Response({"detail": "Office staff not found."}, status=status.HTTP_404_NOT_FOUND)

        office_staff_serializer = OfficeStaffSerializer(office_staff, data=request.data, partial=True)  
        if office_staff_serializer.is_valid():
            office_staff_serializer.save()  
            return Response(office_staff_serializer.data)
        return Response(office_staff_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if request.query_params.get('confirm') != 'true':
            messages.warning(request, "Confirmation required to delete the Office Staff.")
            raise PermissionDenied("Confirmation required to delete.")

        try:
            officestaff = OfficeStaff.objects.get(pk=pk)
            officestaff.delete()

            messages.success(request, "Office Staff has been deleted successfully.")

            return Response(
                {"detail": "Office Staff has been deleted successfully."},
                status=status.HTTP_204_NO_CONTENT
            )

        except OfficeStaff.DoesNotExist:
            messages.error(request, "Office Staff not found.")
            return Response(
                {"detail": "Office Staff not found."},
                status=status.HTTP_404_NOT_FOUND
            )        
 
