from django.db import models
from users.managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from departments.models import Department
import uuid


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        DOCTOR = 'doctor', 'Doctor'
        PATIENT = 'patient', 'Patient'
        STAFF = 'staff', 'Staff'

    username = None
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PATIENT, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctors')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='departments', null=True, blank=True)
    specialization = models.CharField(max_length=100)
    lisence_no = models.CharField(max_length=100)
    consultation_fee = models.PositiveIntegerField()
    is_available = models.BooleanField()
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.user.first_name}'

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patients')
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=3, null=True, blank=True)
    emergency_contact = models.CharField(max_length=15, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user.email} - {self.user.first_name}'




