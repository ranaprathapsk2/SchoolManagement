from django.urls import path
from .views import SchoolAdminLoginView


urlpatterns = [
   
    path('login/', SchoolAdminLoginView.as_view(), name='student-login'),

   
 
]
