from django.urls import path
from student.views import StudentCreateView, StudentView

urlpatterns = [
    path('add_students/', StudentCreateView.as_view(), name='student-create'),
    path('students/', StudentView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentView.as_view(), name='student-detail'),

]
