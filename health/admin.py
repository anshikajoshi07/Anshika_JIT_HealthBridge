from django.contrib import admin
from .models import HealthRecord, PatientProfile, DoctorProfile, Appointment


@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'age', 'blood_group', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('blood_group',)


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'clinic_name', 'is_available', 'created_at')
    search_fields = ('user__username', 'user__email', 'specialization', 'clinic_name')
    list_filter = ('specialization', 'is_available')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_time', 'status')
    search_fields = ('patient__user__username', 'doctor__user__username', 'status')
    list_filter = ('status', 'appointment_date')
