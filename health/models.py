from django.db import models
from django.contrib.auth.models import User


class PatientProfile(models.Model):
    """Patient profile model extending User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True, choices=[
        ('O+', 'O+'), ('O-', 'O-'), ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-')
    ])
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Profile"

    class Meta:
        verbose_name = 'Patient Profile'
        verbose_name_plural = 'Patient Profiles'


class DoctorProfile(models.Model):
    """Doctor profile model extending User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    clinic_name = models.CharField(max_length=200, blank=True, null=True)
    experience = models.PositiveIntegerField(blank=True, null=True, help_text="Years of experience")
    profile_photo = models.ImageField(upload_to='doctor_photos/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True, max_length=500)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    available_days = models.CharField(max_length=100, blank=True, null=True, help_text="Comma separated days (e.g., Monday,Tuesday,Wednesday)")
    available_time_start = models.TimeField(blank=True, null=True)
    available_time_end = models.TimeField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} - {self.specialization}"

    class Meta:
        verbose_name = 'Doctor Profile'
        verbose_name_plural = 'Doctor Profiles'


class Appointment(models.Model):
    """Appointment model."""
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment: {self.patient.user.first_name} with Dr. {self.doctor.user.first_name} on {self.appointment_date}"

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['-appointment_date', '-appointment_time']


class HealthRecord(models.Model):
    """Health record model."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Health Record'
        verbose_name_plural = 'Health Records'
