from django.contrib import admin
from accounts.models import User, Librarian, OfficeStaff, Student, LibraryHistory
# Register your models here.

admin.site.register(Student)
admin.site.register(User)
admin.site.register(Librarian)
admin.site.register(OfficeStaff)
admin.site.register(LibraryHistory)
