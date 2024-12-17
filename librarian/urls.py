from django.urls import path
from librarian.views import LIbrarianLoginView, LibrarianCreateView, LibrarianView

urlpatterns = [

    path('add_librarian/', LibrarianCreateView.as_view(), name='librarian-create'),
    path('librarian/', LibrarianView.as_view(), name='librarian-list-create'),
    path('librarian/<int:pk>/', LibrarianView.as_view(), name='librarian-detail'),

    path('login/', LIbrarianLoginView.as_view(), name='student-login'),

  
]
