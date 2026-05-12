import os

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.db import models
from .models import PatientProfile, DoctorProfile, Appointment


def get_user_role(user):
    if user.is_superuser or user.is_staff:
        return 'admin'
    if hasattr(user, 'doctor_profile'):
        return 'doctor'
    if hasattr(user, 'patient_profile'):
        return 'patient'
    return 'user'


def role_redirect(user):
    role = get_user_role(user)
    if role == 'admin':
        return redirect('health:admin_dashboard')
    if role == 'doctor':
        return redirect('health:index')
    if role == 'patient':
        return redirect('health:index')
    return redirect('health:index')


def index(request):
    """Health app home page."""
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('health:admin_dashboard')
        
        # Check if user has doctor profile
        has_doctor_profile = False
        try:
            has_doctor_profile = hasattr(request.user, 'doctor_profile')
        except Exception:
            pass
        
        if has_doctor_profile:
            return render(request, 'health/indexdoctor.html', {
                'title': 'HealthBridge - Doctor Dashboard'
            })
        
        return render(request, 'health/indexpatient.html', {
            'title': 'HealthBridge - Your Dashboard'
        })

    return render(request, 'health/index.html', {
        'title': 'HealthBridge - Welcome'
    })


@login_required
def admin_dashboard(request):
    """Admin dashboard view."""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('health:index')
    
    # Get system statistics
    total_patients = PatientProfile.objects.count()
    total_doctors = DoctorProfile.objects.count()
    total_appointments = Appointment.objects.count()
    
    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
    }
    
    return render(request, 'health/admin_dashboard.html', context)


@login_required
def manage_patients(request):
    """Manage patients view."""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('health:index')
    
    patients = PatientProfile.objects.all().order_by('-created_at')
    context = {
        'patients': patients,
    }
    
    return render(request, 'health/manage_patients.html', context)


@login_required
def manage_doctors(request):
    """Manage doctors view."""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('health:index')
    
    doctors = DoctorProfile.objects.all().order_by('-created_at')
    context = {
        'doctors': doctors,
    }
    
    return render(request, 'health/manage_doctors.html', context)


@login_required
def view_appointments(request):
    """View all appointments view."""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('health:index')
    
    appointments = Appointment.objects.all().order_by('-appointment_date', '-appointment_time')
    context = {
        'appointments': appointments,
    }
    
    return render(request, 'health/view_appointments.html', context)


@login_required
def manage_system(request):
    """Manage system data view."""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('health:index')
    
    # Placeholder for system management
    context = {}
    
    return render(request, 'health/manage_system.html', context)


@login_required
def view_patient(request, patient_id):
    """View patient details."""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('health:index')
    
    try:
        patient = PatientProfile.objects.get(id=patient_id)
        context = {
            'patient': patient,
        }
        return render(request, 'health/view_patient.html', context)
    except PatientProfile.DoesNotExist:
        messages.error(request, 'Patient not found.')
        return redirect('health:manage_patients')


@login_required
def edit_patient(request, patient_id):
    """Edit patient details."""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('health:index')
    
    try:
        patient = PatientProfile.objects.get(id=patient_id)
        
        if request.method == 'POST':
            # Update user fields
            patient.user.first_name = request.POST.get('first_name', patient.user.first_name)
            patient.user.last_name = request.POST.get('last_name', patient.user.last_name)
            patient.user.email = request.POST.get('email', patient.user.email)
            patient.user.save()
            
            # Update patient fields
            patient.phone = request.POST.get('phone') or None
            patient.age = int(request.POST.get('age')) if request.POST.get('age') and request.POST.get('age').isdigit() else None
            patient.blood_group = request.POST.get('blood_group') or None
            patient.bio = request.POST.get('bio') or None
            patient.save()
            
            messages.success(request, 'Patient updated successfully.')
            return redirect('health:view_patient', patient_id=patient.id)
        
        context = {
            'patient': patient,
        }
        return render(request, 'health/edit_patient.html', context)
    except PatientProfile.DoesNotExist:
        messages.error(request, 'Patient not found.')
        return redirect('health:manage_patients')


@login_required
def view_doctor(request, doctor_id):
    """View doctor details."""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('health:index')
    
    try:
        doctor = DoctorProfile.objects.get(id=doctor_id)
        context = {
            'doctor': doctor,
        }
        return render(request, 'health/view_doctor.html', context)
    except DoctorProfile.DoesNotExist:
        messages.error(request, 'Doctor not found.')
        return redirect('health:manage_doctors')


@login_required
def edit_doctor(request, doctor_id):
    """Edit doctor details."""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('health:index')
    
    try:
        doctor = DoctorProfile.objects.get(id=doctor_id)
        
        if request.method == 'POST':
            # Update user fields
            doctor.user.first_name = request.POST.get('first_name', doctor.user.first_name)
            doctor.user.last_name = request.POST.get('last_name', doctor.user.last_name)
            doctor.user.email = request.POST.get('email', doctor.user.email)
            doctor.user.save()
            
            # Update doctor fields
            doctor.phone = request.POST.get('phone') or None
            doctor.specialization = request.POST.get('specialization') or None
            doctor.license_number = request.POST.get('license_number') or None
            doctor.clinic_name = request.POST.get('clinic_name') or None
            doctor.experience = int(request.POST.get('experience')) if request.POST.get('experience') and request.POST.get('experience').isdigit() else None
            doctor.consultation_fee = request.POST.get('consultation_fee') or None
            doctor.available_days = request.POST.get('available_days') or None
            doctor.available_time_start = request.POST.get('available_time_start') or None
            doctor.available_time_end = request.POST.get('available_time_end') or None
            doctor.bio = request.POST.get('bio') or None
            doctor.save()
            
            messages.success(request, 'Doctor updated successfully.')
            return redirect('health:view_doctor', doctor_id=doctor.id)
        
        context = {
            'doctor': doctor,
        }
        return render(request, 'health/edit_doctor.html', context)
    except DoctorProfile.DoesNotExist:
        messages.error(request, 'Doctor not found.')
        return redirect('health:manage_doctors')


@login_required
def view_appointment(request, appointment_id):
    """View appointment details."""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('health:index')
    
    try:
        appointment = Appointment.objects.select_related('patient__user', 'doctor__user').get(id=appointment_id)
        context = {
            'appointment': appointment,
        }
        return render(request, 'health/view_appointment.html', context)
    except Appointment.DoesNotExist:
        messages.error(request, 'Appointment not found.')
        return redirect('health:view_appointments')


@login_required
def edit_appointment(request, appointment_id):
    """Edit appointment status."""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('health:index')
    
    try:
        appointment = Appointment.objects.select_related('patient__user', 'doctor__user').get(id=appointment_id)
        
        if request.method == 'POST':
            new_status = request.POST.get('status')
            if new_status in ['pending', 'confirmed', 'completed', 'cancelled']:
                appointment.status = new_status
                appointment.save()
                messages.success(request, f'Appointment status updated to {new_status.title()}.')
                return redirect('health:view_appointment', appointment_id=appointment.id)
            else:
                messages.error(request, 'Invalid status selected.')
        
        context = {
            'appointment': appointment,
        }
        return render(request, 'health/edit_appointment.html', context)
    except Appointment.DoesNotExist:
        messages.error(request, 'Appointment not found.')
        return redirect('health:view_appointments')


@login_required
def approve_appointment(request, appointment_id):
    """Approve an appointment (set to confirmed)."""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('health:index')
    
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        if appointment.status == 'pending':
            appointment.status = 'confirmed'
            appointment.save()
            messages.success(request, 'Appointment approved successfully.')
        else:
            messages.warning(request, f'Appointment is already {appointment.status}.')
        return redirect('health:view_appointment', appointment_id=appointment.id)
    except Appointment.DoesNotExist:
        messages.error(request, 'Appointment not found.')
        return redirect('health:view_appointments')


@login_required
def reject_appointment(request, appointment_id):
    """Reject an appointment (set to cancelled)."""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('health:index')
    
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        if appointment.status == 'pending':
            appointment.status = 'cancelled'
            appointment.save()
            messages.success(request, 'Appointment rejected.')
        else:
            messages.warning(request, f'Appointment is already {appointment.status}.')
        return redirect('health:view_appointment', appointment_id=appointment.id)
    except Appointment.DoesNotExist:
        messages.error(request, 'Appointment not found.')
        return redirect('health:view_appointments')


def signin(request):
    """Sign in view."""
    if request.user.is_authenticated:
        return role_redirect(request.user)

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, 'Please enter both email and password.')
            return render(request, 'health/signin.html')

        user = User.objects.filter(email__iexact=email).first()
        if user:
            authenticated_user = authenticate(request, username=user.username, password=password)
            if authenticated_user is not None:
                if not authenticated_user.is_active:
                    messages.error(request, 'Account is disabled. Contact support.')
                    return render(request, 'health/signin.html')

                login(request, authenticated_user)
                messages.success(request, 'Successfully signed in!')
                return role_redirect(authenticated_user)

        messages.error(request, 'Invalid email or password.')

    return render(request, 'health/signin.html')


def signup(request):
    """Account type selection page."""
    return render(request, 'health/signup.html')


def signup_patient(request):
    """Patient signup view."""
    if request.method == 'POST':
        print("DEBUG: Signup patient POST received")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        blood_group = request.POST.get('blood_group')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print(f"DEBUG: Email: {email}, First: {first_name}")
        
        # Validations
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'health/signup_patient.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'health/signup_patient.html')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'health/signup_patient.html')
        
        # Create user
        try:
            print("DEBUG: Creating user")
            username = email.split('@')[0]
            # Make username unique if needed
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            print(f"DEBUG: User created: {user.username}")
            
            # Create patient profile
            from .models import PatientProfile
            PatientProfile.objects.create(
                user=user,
                phone=phone if phone else None,
                age=int(age) if age and age.isdigit() else None,
                blood_group=blood_group if blood_group else None
            )
            print("DEBUG: Patient profile created")
            
            # Log in the user
            login(request, user)
            messages.success(request, 'Patient account created successfully!')
            return redirect('health:index')
            
        except Exception as e:
            print(f"DEBUG: Exception in signup_patient: {e}")
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'health/signup_patient.html')
    
    return render(request, 'health/signup_patient.html')


def signup_doctor(request):
    """Doctor signup view."""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        specialization = request.POST.get('specialization')
        license_number = request.POST.get('license_number')
        clinic_name = request.POST.get('clinic_name')
        experience = request.POST.get('experience')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validations
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'health/signup_doctor.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'health/signup_doctor.html')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'health/signup_doctor.html')
        
        # Create user
        try:
            username = email.split('@')[0]
            # Make username unique if needed
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create doctor profile
            from .models import DoctorProfile
            DoctorProfile.objects.create(
                user=user,
                phone=phone if phone else None,
                specialization=specialization if specialization else None,
                license_number=license_number if license_number else None,
                clinic_name=clinic_name if clinic_name else None,
                experience=int(experience) if experience and experience.isdigit() else None
            )
            
            # Log in the user
            login(request, user)
            messages.success(request, 'Doctor account created successfully!')
            return redirect('health:index')
            
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'health/signup_doctor.html')
    
    return render(request, 'health/signup_doctor.html')


def signup_admin(request):
    """Admin signup view for auto-creating the superuser."""
    User = get_user_model()

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        admin_email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'anshika@gmail.com')
        admin_username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'anshika')
        admin_password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'anshika')

        if email.lower() != admin_email.lower():
            messages.error(request, 'Admin signup is only allowed for the configured admin email.')
            return render(request, 'health/signup_admin.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'health/signup_admin.html')

        if password != admin_password:
            messages.error(request, 'Password does not match the configured admin password.')
            return render(request, 'health/signup_admin.html')

        username_field = getattr(User, 'USERNAME_FIELD', 'username')
        identifier = {username_field: admin_username}
        if hasattr(User, 'email'):
            identifier['email'] = admin_email

        if User.objects.filter(**identifier).exists():
            messages.success(request, 'Admin account already exists. Please sign in.')
            return redirect('health:signin')

        try:
            create_kwargs = {'password': admin_password}
            if username_field != 'email':
                create_kwargs[username_field] = admin_username
                if hasattr(User, 'email'):
                    create_kwargs['email'] = admin_email
            else:
                create_kwargs['email'] = admin_email

            if hasattr(User, 'first_name'):
                create_kwargs['first_name'] = first_name
            if hasattr(User, 'last_name'):
                create_kwargs['last_name'] = last_name

            user = User.objects.create_superuser(**create_kwargs)
            login(request, user)
            messages.success(request, 'Admin account created successfully!')
            return redirect('health:admin_dashboard')
        except Exception as e:
            messages.error(request, f'Error creating admin account: {str(e)}')
            return render(request, 'health/signup_admin.html')

    return render(request, 'health/signup_admin.html')


@login_required(login_url='health:signin')
def patient_index(request):
    """Patient dashboard home page."""
    return render(request, 'health/indexpatient.html')


@login_required(login_url='health:signin')
def profile(request):
    """Profile page with edit functionality."""
    from .models import PatientProfile, DoctorProfile

    if hasattr(request.user, 'doctor_profile'):
        doctor_profile = request.user.doctor_profile

        if request.method == 'POST':
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            phone = request.POST.get('phone', '').strip()
            specialization = request.POST.get('specialization', '').strip()
            license_number = request.POST.get('license_number', '').strip()
            clinic_name = request.POST.get('clinic_name', '').strip()
            experience = request.POST.get('experience', '').strip()
            consultation_fee = request.POST.get('consultation_fee', '').strip()
            available_days = request.POST.get('available_days', '').strip()
            available_time_start = request.POST.get('available_time_start', '').strip()
            available_time_end = request.POST.get('available_time_end', '').strip()
            bio = request.POST.get('bio', '').strip()

            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()

            doctor_profile.phone = phone if phone else None
            doctor_profile.specialization = specialization if specialization else None
            doctor_profile.license_number = license_number if license_number else None
            doctor_profile.clinic_name = clinic_name if clinic_name else None
            doctor_profile.experience = int(experience) if experience.isdigit() else None
            if consultation_fee.replace('.', '', 1).isdigit():
                doctor_profile.consultation_fee = float(consultation_fee)
            doctor_profile.available_days = available_days if available_days else None
            doctor_profile.available_time_start = available_time_start if available_time_start else None
            doctor_profile.available_time_end = available_time_end if available_time_end else None
            doctor_profile.bio = bio if bio else None

            if request.FILES.get('profile_photo'):
                doctor_profile.profile_photo = request.FILES['profile_photo']

            doctor_profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('health:profile')

        context = {
            'doctor_profile': doctor_profile,
        }
        return render(request, 'health/profile_doctor.html', context)

    # Patient path
    patient_profile, created = PatientProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'phone': '',
            'age': None,
            'blood_group': '',
            'bio': ''
        }
    )

    if request.method == 'POST':
        # Handle profile update
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        age = request.POST.get('age', '').strip()
        blood_group = request.POST.get('blood_group', '').strip()
        bio = request.POST.get('bio', '').strip()

        # Update user model
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()

        # Update patient profile
        patient_profile.phone = phone if phone else None
        patient_profile.age = int(age) if age.isdigit() else None
        patient_profile.blood_group = blood_group if blood_group else None
        patient_profile.bio = bio if bio else None

        # Handle profile photo upload
        if request.FILES.get('profile_photo'):
            patient_profile.profile_photo = request.FILES['profile_photo']

        patient_profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('health:profile')

    context = {
        'patient_profile': patient_profile,
    }
    return render(request, 'health/profile.html', context)


@login_required(login_url='health:signin')
def search_doctors(request):
    """Search doctors page."""
    from .models import DoctorProfile

    query = request.GET.get('q', '')
    specialization = request.GET.get('specialization', '')

    doctors = DoctorProfile.objects.filter(is_available=True)

    if query:
        doctors = doctors.filter(
            models.Q(user__first_name__icontains=query) |
            models.Q(user__last_name__icontains=query) |
            models.Q(clinic_name__icontains=query)
        )

    if specialization:
        doctors = doctors.filter(specialization__icontains=specialization)

    # Get unique specializations for filter dropdown
    specializations = DoctorProfile.objects.filter(
        is_available=True
    ).exclude(specialization__isnull=True).exclude(specialization='').values_list(
        'specialization', flat=True
    ).distinct()

    context = {
        'doctors': doctors,
        'query': query,
        'specialization': specialization,
        'specializations': specializations,
    }
    return render(request, 'health/searchpatient.html', context)


@login_required(login_url='health:signin')
def doctor_detail(request, doctor_id):
    """Doctor detail page."""
    from .models import DoctorProfile

    try:
        doctor = DoctorProfile.objects.get(id=doctor_id, is_available=True)
    except DoctorProfile.DoesNotExist:
        messages.error(request, 'Doctor not found.')
        return redirect('health:search_doctors')

    context = {
        'doctor': doctor,
    }
    return render(request, 'health/doctorpatient.html', context)


@login_required(login_url='health:signin')
def book_appointment(request, doctor_id=None):
    """Book appointment page."""
    from .models import DoctorProfile, PatientProfile, Appointment

    # Get patient profile
    try:
        patient_profile = PatientProfile.objects.get(user=request.user)
    except PatientProfile.DoesNotExist:
        messages.error(request, 'Patient profile not found. Please complete your profile.')
        return redirect('health:profile')

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason')

        try:
            doctor = DoctorProfile.objects.get(id=doctor_id, is_available=True)

            # Create appointment
            appointment = Appointment.objects.create(
                patient=patient_profile,
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                reason=reason,
                status='pending'
            )

            messages.success(request, f'Appointment booked successfully with Dr. {doctor.user.first_name} {doctor.user.last_name}!')
            return redirect('health:my_appointments')

        except DoctorProfile.DoesNotExist:
            messages.error(request, 'Doctor not found.')
        except Exception as e:
            messages.error(request, f'Error booking appointment: {str(e)}')

    # If doctor_id provided, get that doctor
    selected_doctor = None
    if doctor_id:
        try:
            selected_doctor = DoctorProfile.objects.get(id=doctor_id, is_available=True)
        except DoctorProfile.DoesNotExist:
            pass

    # Get all available doctors for selection
    doctors = DoctorProfile.objects.filter(is_available=True)

    context = {
        'doctors': doctors,
        'selected_doctor': selected_doctor,
        'patient_profile': patient_profile,
    }
    return render(request, 'health/bookappointmentpatient.html', context)


@login_required(login_url='health:signin')
def my_appointments(request):
    """My appointments page."""
    from .models import PatientProfile, Appointment

    try:
        patient_profile = PatientProfile.objects.get(user=request.user)
        appointments = Appointment.objects.filter(patient=patient_profile).order_by('-appointment_date', '-appointment_time')
    except PatientProfile.DoesNotExist:
        appointments = []

    context = {
        'appointments': appointments,
    }
    return render(request, 'health/myappointmentspatient.html', context)


@login_required(login_url='health:signin')
def doctor_appointments(request):
    """Doctor appointments page."""
    from .models import DoctorProfile, Appointment

    try:
        doctor_profile = request.user.doctor_profile
        appointments = Appointment.objects.filter(doctor=doctor_profile).order_by('-appointment_date', '-appointment_time')
    except DoctorProfile.DoesNotExist:
        messages.error(request, 'Doctor profile not found. Please sign in with your doctor account.')
        return redirect('health:index')

    context = {
        'appointments': appointments,
    }
    return render(request, 'health/doctorappointments.html', context)


@login_required(login_url='health:signin')
def health_records(request):
    """Health records page."""
    # For now, just show a placeholder
    context = {}
    return render(request, 'health/healthrecordspatient.html', context)


@login_required(login_url='health:signin')
def my_prescriptions(request):
    """My prescriptions page."""
    # For now, just show a placeholder
    context = {}
    return render(request, 'health/myprescriptionspatient.html', context)


def signout(request):
    """Sign out view."""
    logout(request)
    messages.success(request, 'Successfully signed out!')
    return redirect('health:index')
