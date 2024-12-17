from django.urls import path
from library.views import FeesHistoryViewSet, LibraryHistoryViewSet


urlpatterns = [
   
    path('library-history/', LibraryHistoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='library-history-list'),
    path('library-history/<int:pk>/', LibraryHistoryViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='library-history-detail'),
    
    path('fees-history/', FeesHistoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='fee-history-list'),
    path('fees-history/<int:pk>/', FeesHistoryViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='fees-history-detail'),

 
]
