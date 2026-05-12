from django.urls import path
from . import views

app_name = 'health'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-patients/', views.manage_patients, name='manage_patients'),
    path('manage-doctors/', views.manage_doctors, name='manage_doctors'),
    path('view-appointments/', views.view_appointments, name='view_appointments'),
    path('manage-system/', views.manage_system, name='manage_system'),
    path('patient/<int:patient_id>/view/', views.view_patient, name='view_patient'),
    path('patient/<int:patient_id>/edit/', views.edit_patient, name='edit_patient'),
    path('doctor/<int:doctor_id>/view/', views.view_doctor, name='view_doctor'),
    path('doctor/<int:doctor_id>/edit/', views.edit_doctor, name='edit_doctor'),
    path('appointment/<int:appointment_id>/view/', views.view_appointment, name='view_appointment'),
    path('appointment/<int:appointment_id>/edit/', views.edit_appointment, name='edit_appointment'),
    path('appointment/<int:appointment_id>/approve/', views.approve_appointment, name='approve_appointment'),
    path('appointment/<int:appointment_id>/reject/', views.reject_appointment, name='reject_appointment'),
    path('signin/', views.signin, name='signin'),
    path('login/', views.signin, name='login'),
    path('signup/', views.signup, name='signup'),
    path('signup/patient/', views.signup_patient, name='signup_patient'),
    path('signup/doctor/', views.signup_doctor, name='signup_doctor'),
    path('signup/admin/', views.signup_admin, name='signup_admin'),
    path('signout/', views.signout, name='signout'),
    path('logout/', views.signout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('search-doctors/', views.search_doctors, name='search_doctors'),
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('book-appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment_with_doctor'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('health-records/', views.health_records, name='health_records'),
    path('my-prescriptions/', views.my_prescriptions, name='my_prescriptions'),
]
