from django.shortcuts import render
from accounts.models import FeesHistory, LibraryHistory
from .serializers import FeesHistorySerializer, LibraryHistorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from accounts.permission import IsAdminorStafforLibrarian, IsAdminorStaff, IsAdminorLibrarian


class LibraryHistoryViewSet(viewsets.ModelViewSet):
    queryset = LibraryHistory.objects.all()
    serializer_class = LibraryHistorySerializer

    def get_permissions(self):

        if self.request.method == 'GET':  
            permission_classes = [IsAuthenticated,IsAdminorStafforLibrarian]
        elif self.request.method in ['POST','PUT','PATCH', 'DELETE']:  
            permission_classes = [IsAuthenticated, IsAdminorLibrarian]
        return [permission() for permission in permission_classes]
    

class FeesHistoryViewSet(viewsets.ModelViewSet):
    queryset = FeesHistory.objects.all()
    serializer_class = FeesHistorySerializer
    permission_classes = [IsAuthenticated,IsAdminorStaff]

    