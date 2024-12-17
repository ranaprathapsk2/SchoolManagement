from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.contrib.auth.models import Permission,Group



class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')


        # Create and return the user object
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if email is None:
            raise ValueError('Superuser must have an email address.')

        return self.create_user(email=email, password=password, **extra_fields)

class User(AbstractBaseUser):

    # Role-based fields
    is_student = models.BooleanField(default=False)
    is_officestaff = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)

    # Admin-related fields
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    #common field details for all roles
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True)
    date_of_birth = models.DateField()
    remarks = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['full_name','date_of_birth']

    objects = UserManager()
    
    groups = models.ManyToManyField(
        Group,
        related_name='library_user_groups',  
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='library_user_permissions' 
    )
    
    def __str__(self):
        return self.email or "No email provided"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
class Student(models.Model):

    #student details
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')
    studnet_class = models.IntegerField(blank=True, null=True)
    student_division = models.CharField(max_length=2, null=True, blank=True)
    address = models.CharField(max_length=100, blank=True)

class OfficeStaff(models.Model):
    #office staff details
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='officestaff')
    staff_id = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    position = models.CharField(max_length=50, null=True, blank=True)


    def __str__(self):
        return self.user.full_name

class Librarian(models.Model):
    #librarian details
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='librarian')
    librarian_id = models.CharField(max_length=10, unique=True)


    def __str__(self):
        return self.user.full_name
    
class LibraryHistory(models.Model):

    #library History
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='student_detils')
    book_name = models.CharField(max_length=300)
    retrun_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('borrowed', 'Borrowed'), ('returned', 'Returned')], default='borrowed')

class FeesHistory(models.Model):
    
    PAYMENT_CHOICES = [
        ('upi', 'UPI'),
        ('cash', 'Cash'),
    ]
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='student_detils_fee')
    fee_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paymnet_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

