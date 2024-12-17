from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import SchoolAdminLoginSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken



#login school admin function
class SchoolAdminLoginView(APIView):
    
    def post(self, request):
        serializer = SchoolAdminLoginSerializer(data=request.data)
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
        