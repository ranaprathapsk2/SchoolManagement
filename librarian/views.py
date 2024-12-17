from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from accounts.models import Librarian
from .serializers import LibrarianLoginSerializer, LibrarianSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import messages
from rest_framework.exceptions import PermissionDenied

class LIbrarianLoginView(APIView):
    
    def post(self, request):
        # Serialize and validate the incoming data
        serializer = LibrarianLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get the user from validated data
        user = serializer.validated_data['user']

        if user:
            #token for the authenticated user 
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Authentication failed.'}, status=status.HTTP_401_UNAUTHORIZED)
    

class LibrarianCreateView(generics.CreateAPIView):
    queryset = Librarian.objects.all()  # Use Librarian model
    serializer_class = LibrarianSerializer  # Use Librarian serializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    def perform_create(self, serializer):
        user_data = self.request.data.get('user')  # Extract user data
        
        if user_data is None:
            raise ValueError("User data is required")

        # Serialize the user data first
        user_serializer = UserSerializer(data=user_data)
        
        # Check if user data is valid
        if user_serializer.is_valid():
            user = user_serializer.save()  # Save the user instance and get its pk

            # Now, create the Librarian instance and associate it with the user pk
            serializer.save(user=user)  # Save the librarian and associate with user
        else:
            raise ValueError("User data is invalid")

    def create(self, request, *args, **kwargs):
        try:
            # Call the parent class's create method to save the data
            return super().create(request, *args, **kwargs)
        except ValueError as e:
            # Return error if there is an invalid value
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class LibrarianView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request, pk=None):
        if pk:
            # Retrieve a single librarian by primary key (pk)
            try:
                librarian = Librarian.objects.get(pk=pk)  # Changed from Student to Librarian
                serializer = LibrarianSerializer(librarian)  # Changed from StudentSerializer to LibrarianSerializer
                return Response(serializer.data)
            except Librarian.DoesNotExist:  # Changed from Student to Librarian
                return Response({"detail": "Librarian not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Retrieve all librarians
            librarians = Librarian.objects.all()  # Changed from Student to Librarian
            serializer = LibrarianSerializer(librarians, many=True)  # Changed from StudentSerializer to LibrarianSerializer
            return Response(serializer.data)

    def put(self, request, pk=None):
        # Full update of a librarian (including related user data if provided)
        try:
            librarian = Librarian.objects.get(pk=pk)  # Changed from Student to Librarian
        except Librarian.DoesNotExist:  # Changed from Student to Librarian
            return Response({"detail": "Librarian not found."}, status=status.HTTP_404_NOT_FOUND)

        # Pass data to the serializer
        librarian_serializer = LibrarianSerializer(librarian, data=request.data)  # Changed from StudentSerializer to LibrarianSerializer
        if librarian_serializer.is_valid():
            librarian_serializer.save()  # The custom update() method in the serializer will handle the update
            return Response(librarian_serializer.data)
        return Response(librarian_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        # Partial update of a librarian (including related user data if provided)
        try:
            librarian = Librarian.objects.get(pk=pk)  # Changed from Student to Librarian
        except Librarian.DoesNotExist:  # Changed from Student to Librarian
            return Response({"detail": "Librarian not found."}, status=status.HTTP_404_NOT_FOUND)

        librarian_serializer = LibrarianSerializer(librarian, data=request.data, partial=True)  # partial=True for PATCH, changed to LibrarianSerializer
        if librarian_serializer.is_valid():
            librarian_serializer.save()  # The custom update() method in the serializer will handle the update
            return Response(librarian_serializer.data)
        return Response(librarian_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            # Retrieve the librarian object
            librarian = Librarian.objects.get(pk=pk)  # Changed from Student to Librarian
            
            # Delete the librarian record
            librarian.delete()

            # Return a success response with a custom message
            return Response({"detail": "Librarian has been deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        
        except Librarian.DoesNotExist:  # Changed from Student to Librarian
            return Response({"detail": "Librarian not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        if request.query_params.get('confirm') != 'true':
            messages.warning(request, "Confirmation required to delete the Librarian.")
            raise PermissionDenied("Confirmation required to delete.")

        try:
            librarian = Librarian.objects.get(pk=pk)
            librarian.delete()

            messages.success(request, "Librarian has been deleted successfully.")

            return Response(
                {"detail": "Librarian has been deleted successfully."},
                status=status.HTTP_204_NO_CONTENT
            )

        except Librarian.DoesNotExist:
            messages.error(request, "Librarian not found.")
            return Response(
                {"detail": "Librarian not found."},
                status=status.HTTP_404_NOT_FOUND
            )        