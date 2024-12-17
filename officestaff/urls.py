from django.urls import path
from officestaff.views import OfficeStaffCreateView, OfficeStaffLoginView, OfficeStaffView


urlpatterns = [
    path('add_officestaff/', OfficeStaffCreateView.as_view(), name='officestaff-create'),
    path('officestaff/', OfficeStaffView.as_view(), name='officestaff-list-create'),
    path('officestaff/<int:pk>/', OfficeStaffView.as_view(), name='officestaff-detail'),

    path('login/', OfficeStaffLoginView.as_view(), name='student-login'),


 
]
