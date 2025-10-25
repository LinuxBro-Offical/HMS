#!/usr/bin/env python3
"""
HMS Sample Data Seeding Script
This script creates sample data for all models in the HMS project.
Run this script from the project root: python scripts/seed_data.py
"""

import os
import sys
import django
from datetime import datetime, date, timedelta
from decimal import Decimal
import random
from django.utils import timezone

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMS_Project.settings')
django.setup()

# Import all models
from tenants.models import Organization, Branch, Plan, Subscription, Domain
from users.models import User, Role, StaffProfile
from patients.models import Patient, PatientCondition, PatientAllergy, PatientReport
from appointments.models import Appointment, DoctorSchedule, TokenCounter, AppointmentStatusHistory
from encounters.models import Encounter, Prescription, PrescriptionItem, EncounterReport
from billing.models import ChargeType, Invoice, InvoiceItem, Payment, PaymentAllocation, Refund, InvoiceCounter
from notifications.models import TenantNotificationSetting, NotificationTemplate, NotificationEvent, NotificationLog


def create_sample_data():
    """Create sample data for all models"""
    
    print("🌱 Starting HMS Sample Data Seeding...")
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    # clear_existing_data()
    
    # Create data in dependency order
    create_organizations()
    create_plans()
    create_subscriptions()
    create_branches()
    create_users()
    create_roles()
    create_staff_profiles()
    create_patients()
    create_patient_conditions()
    create_patient_allergies()
    create_patient_reports()
    create_charge_types()
    create_doctor_schedules()
    create_appointments()
    create_encounters()
    create_prescriptions()
    create_prescription_items()
    create_encounter_reports()
    create_invoices()
    create_invoice_items()
    create_payments()
    create_payment_allocations()
    create_notification_settings()
    create_notification_templates()
    create_notification_events()
    
    print("✅ Sample data seeding completed successfully!")
    print(f"📊 Created:")
    print(f"   - Organizations: {Organization.objects.count()}")
    print(f"   - Branches: {Branch.objects.count()}")
    print(f"   - Users: {User.objects.count()}")
    print(f"   - Patients: {Patient.objects.count()}")
    print(f"   - Appointments: {Appointment.objects.count()}")
    print(f"   - Encounters: {Encounter.objects.count()}")
    print(f"   - Invoices: {Invoice.objects.count()}")
    print(f"   - Payments: {Payment.objects.count()}")


def clear_existing_data():
    """Clear existing sample data"""
    print("🗑️  Clearing existing data...")
    
    # Delete in reverse dependency order
    NotificationLog.objects.all().delete()
    NotificationEvent.objects.all().delete()
    NotificationTemplate.objects.all().delete()
    TenantNotificationSetting.objects.all().delete()
    PaymentAllocation.objects.all().delete()
    Payment.objects.all().delete()
    Refund.objects.all().delete()
    InvoiceItem.objects.all().delete()
    Invoice.objects.all().delete()
    InvoiceCounter.objects.all().delete()
    EncounterReport.objects.all().delete()
    PrescriptionItem.objects.all().delete()
    Prescription.objects.all().delete()
    Encounter.objects.all().delete()
    AppointmentStatusHistory.objects.all().delete()
    Appointment.objects.all().delete()
    TokenCounter.objects.all().delete()
    DoctorSchedule.objects.all().delete()
    PatientReport.objects.all().delete()
    PatientAllergy.objects.all().delete()
    PatientCondition.objects.all().delete()
    Patient.objects.all().delete()
    StaffProfile.objects.all().delete()
    Role.objects.all().delete()
    User.objects.all().delete()
    Branch.objects.all().delete()
    Subscription.objects.all().delete()
    Plan.objects.all().delete()
    Domain.objects.all().delete()
    Organization.objects.all().delete()


def create_organizations():
    """Create sample organizations"""
    print("🏢 Creating Organizations...")
    
    orgs_data = [
        {
            'name': 'City General Hospital',
            'slug': 'city-general',
            'owner_name': 'Dr. John Smith',
            'owner_email': 'owner@citygeneral.com',
            'contact_phone': '+91-9876543210',
            'address': '123 Medical Street, City Center',
            'is_active': True,
            'settings': {'theme_color': '#2E8B57', 'features': {'appointments': True, 'billing': True}}
        },
        {
            'name': 'Metro Health Clinic',
            'slug': 'metro-health',
            'owner_name': 'Dr. Sarah Johnson',
            'owner_email': 'owner@metrohealth.com',
            'contact_phone': '+91-9876543211',
            'address': '456 Health Avenue, Metro City',
            'is_active': True,
            'settings': {'theme_color': '#4169E1', 'features': {'appointments': True, 'telemedicine': True}}
        },
        {
            'name': 'Sunrise Medical Center',
            'slug': 'sunrise-medical',
            'owner_name': 'Dr. Michael Brown',
            'owner_email': 'owner@sunrise.com',
            'contact_phone': '+91-9876543212',
            'address': '789 Wellness Road, Sunrise City',
            'is_active': True,
            'settings': {'theme_color': '#FF6347', 'features': {'appointments': True, 'lab': True}}
        },
        {
            'name': 'Prime Care Hospital',
            'slug': 'prime-care',
            'owner_name': 'Dr. Emily Davis',
            'owner_email': 'owner@primecare.com',
            'contact_phone': '+91-9876543213',
            'address': '321 Care Boulevard, Prime City',
            'is_active': True,
            'settings': {'theme_color': '#9370DB', 'features': {'appointments': True, 'pharmacy': True}}
        },
        {
            'name': 'Elite Healthcare',
            'slug': 'elite-healthcare',
            'owner_name': 'Dr. Robert Wilson',
            'owner_email': 'owner@elitehealth.com',
            'contact_phone': '+91-9876543214',
            'address': '654 Elite Street, Elite City',
            'is_active': True,
            'settings': {'theme_color': '#DC143C', 'features': {'appointments': True, 'emergency': True}}
        }
    ]
    
    for org_data in orgs_data:
        Organization.objects.get_or_create(
            slug=org_data['slug'],
            defaults=org_data
        )


def create_plans():
    """Create sample plans"""
    print("📋 Creating Plans...")
    
    plans_data = [
        {
            'name': 'Free Plan',
            'code': 'free',
            'description': 'Basic plan with limited features',
            'price_monthly': Decimal('0.00'),
            'price_yearly': Decimal('0.00'),
            'max_branches': 1,
            'max_doctors': 2,
            'max_staff': 5,
            'max_patients': 100,
            'allow_patient_portal': False,
            'allow_sms': False,
            'allow_whatsapp': False
        },
        {
            'name': 'Starter Plan',
            'code': 'starter',
            'description': 'Perfect for small clinics',
            'price_monthly': Decimal('2999.00'),
            'price_yearly': Decimal('29999.00'),
            'max_branches': 2,
            'max_doctors': 5,
            'max_staff': 10,
            'max_patients': 500,
            'allow_patient_portal': True,
            'allow_sms': True,
            'allow_whatsapp': False
        },
        {
            'name': 'Professional Plan',
            'code': 'professional',
            'description': 'Ideal for medium-sized hospitals',
            'price_monthly': Decimal('5999.00'),
            'price_yearly': Decimal('59999.00'),
            'max_branches': 5,
            'max_doctors': 15,
            'max_staff': 30,
            'max_patients': 2000,
            'allow_patient_portal': True,
            'allow_sms': True,
            'allow_whatsapp': True
        },
        {
            'name': 'Enterprise Plan',
            'code': 'enterprise',
            'description': 'Complete solution for large hospitals',
            'price_monthly': Decimal('9999.00'),
            'price_yearly': Decimal('99999.00'),
            'max_branches': 10,
            'max_doctors': 50,
            'max_staff': 100,
            'max_patients': 10000,
            'allow_patient_portal': True,
            'allow_sms': True,
            'allow_whatsapp': True,
            'allow_inventory': True,
            'allow_insurance': True
        },
        {
            'name': 'Custom Plan',
            'code': 'custom',
            'description': 'Tailored solution for specific needs',
            'price_monthly': Decimal('14999.00'),
            'price_yearly': Decimal('149999.00'),
            'max_branches': 20,
            'max_doctors': 100,
            'max_staff': 200,
            'max_patients': 50000,
            'allow_patient_portal': True,
            'allow_sms': True,
            'allow_whatsapp': True,
            'allow_inventory': True,
            'allow_insurance': True,
            'allow_reports': True
        }
    ]
    
    for plan_data in plans_data:
        Plan.objects.get_or_create(
            code=plan_data['code'],
            defaults=plan_data
        )


def create_subscriptions():
    """Create sample subscriptions"""
    print("💳 Creating Subscriptions...")
    
    organizations = Organization.objects.all()
    plans = Plan.objects.all()
    
    for i, org in enumerate(organizations):
        plan = plans[i % len(plans)]
        Subscription.objects.get_or_create(
            organization=org,
            defaults={
                'plan': plan,
                'start_date': date.today(),
                'end_date': date.today() + timedelta(days=365),
                'is_trial': i < 2,
                'trial_ends_at': date.today() + timedelta(days=14) if i < 2 else None,
                'is_active': True
            }
        )


def create_branches():
    """Create sample branches"""
    print("🏥 Creating Branches...")
    
    organizations = Organization.objects.all()
    
    for org in organizations:
        # Create primary branch
        Branch.objects.get_or_create(
            name=f"{org.name} - Main Branch",
            defaults={
                'code': f"{org.slug.upper()}-01",
                'address': org.address,
                'phone': org.contact_phone,
                'email': f"main@{org.slug}.com",
                'is_primary': True,
                'timezone': 'Asia/Kolkata',
                'working_hours': {
                    'monday': {'start': '09:00', 'end': '18:00'},
                    'tuesday': {'start': '09:00', 'end': '18:00'},
                    'wednesday': {'start': '09:00', 'end': '18:00'},
                    'thursday': {'start': '09:00', 'end': '18:00'},
                    'friday': {'start': '09:00', 'end': '18:00'},
                    'saturday': {'start': '09:00', 'end': '14:00'},
                    'sunday': {'closed': True}
                }
            }
        )
        
        # Create additional branch for some organizations
        if org.slug in ['city-general', 'metro-health']:
            Branch.objects.get_or_create(
                name=f"{org.name} - Emergency Wing",
                defaults={
                    'code': f"{org.slug.upper()}-02",
                    'address': f"Emergency Wing, {org.address}",
                    'phone': f"+91-{random.randint(9000000000, 9999999999)}",
                    'email': f"emergency@{org.slug}.com",
                    'is_primary': False,
                    'timezone': 'Asia/Kolkata',
                    'working_hours': {'24x7': True}
                }
            )


def create_users():
    """Create sample users"""
    print("👥 Creating Users...")
    
    # Create superuser if not exists
    User.objects.get_or_create(
        email='admin@hms.com',
        defaults={
            'full_name': 'System Administrator',
            'phone': '+91-9876543210',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    # Create sample users for each organization
    organizations = Organization.objects.all()
    
    user_data = [
        {'email': 'doctor1@citygeneral.com', 'full_name': 'Dr. John Smith', 'phone': '+91-9876543210'},
        {'email': 'doctor2@citygeneral.com', 'full_name': 'Dr. Jane Doe', 'phone': '+91-9876543211'},
        {'email': 'receptionist@citygeneral.com', 'full_name': 'Sarah Wilson', 'phone': '+91-9876543212'},
        {'email': 'nurse@citygeneral.com', 'full_name': 'Mary Johnson', 'phone': '+91-9876543213'},
        {'email': 'labtech@citygeneral.com', 'full_name': 'David Brown', 'phone': '+91-9876543214'},
        {'email': 'doctor1@metrohealth.com', 'full_name': 'Dr. Sarah Johnson', 'phone': '+91-9876543215'},
        {'email': 'doctor2@metrohealth.com', 'full_name': 'Dr. Michael Davis', 'phone': '+91-9876543216'},
        {'email': 'receptionist@metrohealth.com', 'full_name': 'Lisa Anderson', 'phone': '+91-9876543217'},
        {'email': 'nurse@metrohealth.com', 'full_name': 'Jennifer Taylor', 'phone': '+91-9876543218'},
        {'email': 'labtech@metrohealth.com', 'full_name': 'Robert Wilson', 'phone': '+91-9876543219'},
    ]
    
    for user_info in user_data:
        User.objects.get_or_create(
            email=user_info['email'],
            defaults={
                'full_name': user_info['full_name'],
                'phone': user_info['phone'],
                'is_active': True
            }
        )


def create_roles():
    """Create sample roles"""
    print("🎭 Creating Roles...")
    
    roles_data = [
        {'name': 'tenant_admin', 'description': 'Tenant Administrator', 'default': False},
        {'name': 'branch_admin', 'description': 'Branch Administrator', 'default': False},
        {'name': 'doctor', 'description': 'Medical Doctor', 'default': True},
        {'name': 'nurse', 'description': 'Nursing Staff', 'default': True},
        {'name': 'receptionist', 'description': 'Reception Staff', 'default': True},
        {'name': 'lab_technician', 'description': 'Laboratory Technician', 'default': True},
        {'name': 'pharmacist', 'description': 'Pharmacy Staff', 'default': True},
        {'name': 'cashier', 'description': 'Billing and Cashier', 'default': True},
    ]
    
    for role_data in roles_data:
        Role.objects.get_or_create(
            name=role_data['name'],
            defaults=role_data
        )


def create_staff_profiles():
    """Create sample staff profiles"""
    print("👨‍⚕️ Creating Staff Profiles...")
    
    users = User.objects.filter(is_superuser=False)
    branches = Branch.objects.all()
    roles = Role.objects.all()
    
    designations = ['Doctor', 'Nurse', 'Receptionist', 'Lab Technician', 'Pharmacist', 'Cashier']
    specializations = ['General Medicine', 'Cardiology', 'Pediatrics', 'Orthopedics', 'Dermatology', 'Neurology']
    
    for i, user in enumerate(users):
        # Assign random branch
        branch = random.choice(branches)
        
        # Determine designation based on email
        if 'doctor' in user.email:
            designation = 'Doctor'
            specialization = random.choice(specializations)
        elif 'nurse' in user.email:
            designation = 'Nurse'
            specialization = None
        elif 'receptionist' in user.email:
            designation = 'Receptionist'
            specialization = None
        elif 'labtech' in user.email:
            designation = 'Lab Technician'
            specialization = None
        else:
            designation = random.choice(designations)
            specialization = random.choice(specializations) if designation == 'Doctor' else None
        
        staff_profile, created = StaffProfile.objects.get_or_create(
            user=user,
            defaults={
                'employee_id': f"EMP{random.randint(1000, 9999)}",
                'designation': designation,
                'specialization': specialization,
                'is_consulting': designation == 'Doctor'
            }
        )
        
        if created:
            # Assign branch
            staff_profile.assigned_branches.add(branch)
            
            # Assign role based on designation
            if designation == 'Doctor':
                role = roles.get(name='doctor')
            elif designation == 'Nurse':
                role = roles.get(name='nurse')
            elif designation == 'Receptionist':
                role = roles.get(name='receptionist')
            elif designation == 'Lab Technician':
                role = roles.get(name='lab_technician')
            else:
                role = roles.get(name='cashier')
            
            staff_profile.roles.add(role)


def create_patients():
    """Create sample patients"""
    print("🏥 Creating Patients...")
    
    branches = Branch.objects.all()
    users = User.objects.filter(is_superuser=False)
    
    patient_data = [
        {
            'patient_code': 'PAT001',
            'full_name': 'Rajesh Kumar',
            'date_of_birth': date(1985, 5, 15),
            'gender': 'M',
            'phone': '+91-9876543210',
            'email': 'rajesh.kumar@email.com',
            'address': '123 Main Street, Mumbai',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'pin_code': '400001',
            'referral_source': 'Self',
            'is_vip': False
        },
        {
            'patient_code': 'PAT002',
            'full_name': 'Priya Sharma',
            'date_of_birth': date(1990, 8, 22),
            'gender': 'F',
            'phone': '+91-9876543211',
            'email': 'priya.sharma@email.com',
            'address': '456 Park Avenue, Delhi',
            'city': 'Delhi',
            'state': 'Delhi',
            'pin_code': '110001',
            'referral_source': 'Doctor Referral',
            'is_vip': True
        },
        {
            'patient_code': 'PAT003',
            'full_name': 'Amit Patel',
            'date_of_birth': date(1978, 12, 10),
            'gender': 'M',
            'phone': '+91-9876543212',
            'email': 'amit.patel@email.com',
            'address': '789 Garden Road, Bangalore',
            'city': 'Bangalore',
            'state': 'Karnataka',
            'pin_code': '560001',
            'referral_source': 'Insurance',
            'is_vip': False
        },
        {
            'patient_code': 'PAT004',
            'full_name': 'Sneha Reddy',
            'date_of_birth': date(1992, 3, 18),
            'gender': 'F',
            'phone': '+91-9876543213',
            'email': 'sneha.reddy@email.com',
            'address': '321 Tech Park, Hyderabad',
            'city': 'Hyderabad',
            'state': 'Telangana',
            'pin_code': '500001',
            'referral_source': 'Online',
            'is_vip': False
        },
        {
            'patient_code': 'PAT005',
            'full_name': 'Vikram Singh',
            'date_of_birth': date(1982, 7, 25),
            'gender': 'M',
            'phone': '+91-9876543214',
            'email': 'vikram.singh@email.com',
            'address': '654 Business District, Pune',
            'city': 'Pune',
            'state': 'Maharashtra',
            'pin_code': '411001',
            'referral_source': 'Corporate',
            'is_vip': True
        }
    ]
    
    for i, patient_info in enumerate(patient_data):
        patient, created = Patient.objects.get_or_create(
            patient_code=patient_info['patient_code'],
            defaults={
                **patient_info,
                'date_registered': date.today() - timedelta(days=random.randint(1, 365)),
                'last_visit_date': date.today() - timedelta(days=random.randint(1, 30)),
                'total_visits': random.randint(1, 10),
                'registered_by': random.choice(users),
                'last_updated_by': random.choice(users)
            }
        )
        
        if created:
            # Assign to random branch
            patient.branches.add(random.choice(branches))


def create_patient_conditions():
    """Create sample patient conditions"""
    print("🩺 Creating Patient Conditions...")
    
    patients = Patient.objects.all()
    conditions = [
        'Hypertension', 'Diabetes Type 2', 'Asthma', 'Arthritis', 'Migraine',
        'High Cholesterol', 'Anxiety', 'Depression', 'Sleep Apnea', 'GERD'
    ]
    
    for patient in patients:
        # Create 1-3 conditions per patient
        num_conditions = random.randint(1, 3)
        selected_conditions = random.sample(conditions, num_conditions)
        
        for condition in selected_conditions:
            PatientCondition.objects.get_or_create(
                patient=patient,
                name=condition,
                defaults={
                    'diagnosed_date': date.today() - timedelta(days=random.randint(30, 1000)),
                    'notes': f'Diagnosed with {condition}',
                    'active': random.choice([True, False])
                }
            )


def create_patient_allergies():
    """Create sample patient allergies"""
    print("🤧 Creating Patient Allergies...")
    
    patients = Patient.objects.all()
    allergens = [
        'Penicillin', 'Aspirin', 'Sulfa Drugs', 'Latex', 'Shellfish',
        'Peanuts', 'Dust Mites', 'Pollen', 'Mold', 'Eggs'
    ]
    reactions = ['Rash', 'Swelling', 'Difficulty Breathing', 'Nausea', 'Hives']
    severities = ['Mild', 'Moderate', 'Severe']
    
    for patient in patients:
        # Create 0-2 allergies per patient
        num_allergies = random.randint(0, 2)
        if num_allergies > 0:
            selected_allergens = random.sample(allergens, num_allergies)
            
            for allergen in selected_allergens:
                PatientAllergy.objects.get_or_create(
                    patient=patient,
                    allergen=allergen,
                    defaults={
                        'reaction': random.choice(reactions),
                        'severity': random.choice(severities)
                    }
                )


def create_patient_reports():
    """Create sample patient reports"""
    print("📄 Creating Patient Reports...")
    
    patients = Patient.objects.all()
    users = User.objects.filter(is_superuser=False)
    
    report_titles = [
        'Blood Test Report', 'X-Ray Report', 'MRI Scan Report', 'ECG Report', 'Ultrasound Report',
        'CT Scan Report', 'Pathology Report', 'Cardiology Report', 'Neurology Report', 'Lab Results'
    ]
    
    for patient in patients:
        # Create 1-2 reports per patient
        num_reports = random.randint(1, 2)
        selected_reports = random.sample(report_titles, num_reports)
        
        for report_title in selected_reports:
            PatientReport.objects.get_or_create(
                patient=patient,
                title=report_title,
                defaults={
                    'file': f'reports/{patient.patient_code}_{report_title.replace(" ", "_")}.pdf',
                    'uploaded_by': random.choice(users)
                }
            )


def create_charge_types():
    """Create sample charge types"""
    print("💰 Creating Charge Types...")
    
    charge_types_data = [
        {
            'code': 'consultation',
            'name': 'Doctor Consultation',
            'category': 'Consultation',
            'default_price': Decimal('500.00'),
            'is_taxable': True,
            'taxable_rate': Decimal('18.00'),
            'description': 'General consultation fee'
        },
        {
            'code': 'followup',
            'name': 'Follow-up Visit',
            'category': 'Consultation',
            'default_price': Decimal('300.00'),
            'is_taxable': True,
            'taxable_rate': Decimal('18.00'),
            'description': 'Follow-up consultation fee'
        },
        {
            'code': 'emergency',
            'name': 'Emergency Consultation',
            'category': 'Emergency',
            'default_price': Decimal('1000.00'),
            'is_taxable': True,
            'taxable_rate': Decimal('18.00'),
            'description': 'Emergency consultation fee'
        },
        {
            'code': 'lab_test',
            'name': 'Laboratory Test',
            'category': 'Diagnostics',
            'default_price': Decimal('200.00'),
            'is_taxable': True,
            'taxable_rate': Decimal('18.00'),
            'description': 'General laboratory test fee'
        },
        {
            'code': 'xray',
            'name': 'X-Ray',
            'category': 'Radiology',
            'default_price': Decimal('400.00'),
            'is_taxable': True,
            'taxable_rate': Decimal('18.00'),
            'description': 'X-Ray imaging fee'
        }
    ]
    
    for charge_data in charge_types_data:
        ChargeType.objects.get_or_create(
            code=charge_data['code'],
            defaults=charge_data
        )


def create_doctor_schedules():
    """Create sample doctor schedules"""
    print("📅 Creating Doctor Schedules...")
    
    doctors = StaffProfile.objects.filter(designation='Doctor')
    branches = Branch.objects.all()
    
    weekdays = [0, 1, 2, 3, 4, 5, 6]  # Monday to Sunday
    
    for doctor in doctors:
        branch = random.choice(branches)
        
        # Create schedule for weekdays (Monday to Friday)
        for weekday in weekdays[:5]:
            DoctorSchedule.objects.get_or_create(
                doctor=doctor,
                branch=branch,
                weekday=weekday,
                defaults={
                    'start_time': '09:00:00',
                    'end_time': '17:00:00',
                    'slot_duration_minutes': 15,
                    'is_active': True
                }
            )


def create_appointments():
    """Create sample appointments"""
    print("📝 Creating Appointments...")
    
    patients = Patient.objects.all()
    doctors = StaffProfile.objects.filter(designation='Doctor')
    branches = Branch.objects.all()
    
    sources = ['CALL', 'WHATSAPP', 'DIRECT']
    statuses = ['BOOKED', 'CONFIRMED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED']
    
    for i in range(10):  # Create 10 appointments
        patient = random.choice(patients)
        doctor = random.choice(doctors)
        branch = random.choice(branches)
        
        appointment_date = date.today() + timedelta(days=random.randint(-30, 30))
        appointment_time = f"{random.randint(9, 17):02d}:{random.choice(['00', '15', '30', '45'])}:00"
        
        Appointment.objects.get_or_create(
            patient=patient,
            doctor=doctor,
            branch=branch,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            defaults={
                'token_number': random.randint(1, 50),
                'source': random.choice(sources),
                'status': random.choice(statuses),
                'remarks': f'Appointment for {patient.full_name}',
                'notified': random.choice([True, False])
            }
        )


def create_encounters():
    """Create sample encounters"""
    print("🩺 Creating Encounters...")
    
    appointments = Appointment.objects.all()
    patients = Patient.objects.all()
    doctors = StaffProfile.objects.filter(designation='Doctor')
    branches = Branch.objects.all()
    
    chief_complaints = [
        'Headache', 'Fever', 'Cough', 'Chest Pain', 'Abdominal Pain',
        'Back Pain', 'Joint Pain', 'Shortness of Breath', 'Nausea', 'Dizziness'
    ]
    
    diagnoses = [
        'Common Cold', 'Hypertension', 'Diabetes', 'Migraine', 'Gastritis',
        'Bronchitis', 'Arthritis', 'Anxiety', 'Depression', 'Insomnia'
    ]
    
    for i in range(8):  # Create 8 encounters
        patient = random.choice(patients)
        doctor = random.choice(doctors)
        branch = random.choice(branches)
        
        encounter_date = timezone.now() - timedelta(days=random.randint(1, 30))
        
        encounter, created = Encounter.objects.get_or_create(
            patient=patient,
            doctor=doctor,
            branch=branch,
            encounter_date=encounter_date,
            defaults={
                'chief_complaint': random.choice(chief_complaints),
                'diagnosis': random.choice(diagnoses),
                'notes': f'Patient consultation notes for {patient.full_name}',
                'height_cm': Decimal(str(random.uniform(150, 190))),
                'weight_kg': Decimal(str(random.uniform(50, 100))),
                'temperature_c': Decimal(str(random.uniform(36, 39))),
                'blood_pressure': f"{random.randint(100, 140)}/{random.randint(60, 90)}",
                'pulse_rate': random.randint(60, 100),
                'oxygen_saturation': random.randint(95, 100),
                'follow_up_required': random.choice([True, False]),
                'follow_up_in_days': random.randint(7, 30) if random.choice([True, False]) else None
            }
        )
        
        if created and appointments.exists():
            # Link to random appointment that doesn't already have an encounter
            available_appointments = appointments.filter(encounter_link__isnull=True)
            if available_appointments.exists():
                appointment = random.choice(available_appointments)
                encounter.appointment = appointment
                encounter.save()


def create_prescriptions():
    """Create sample prescriptions"""
    print("💊 Creating Prescriptions...")
    
    encounters = Encounter.objects.all()
    
    for encounter in encounters:
        Prescription.objects.get_or_create(
            encounter=encounter,
            defaults={
                'notes': f'Prescription for {encounter.patient.full_name}'
            }
        )


def create_prescription_items():
    """Create sample prescription items"""
    print("💊 Creating Prescription Items...")
    
    prescriptions = Prescription.objects.all()
    
    medicines = [
        {'name': 'Paracetamol', 'dosage': '500mg', 'frequency': 'Twice daily', 'duration': 5},
        {'name': 'Amoxicillin', 'dosage': '250mg', 'frequency': 'Three times daily', 'duration': 7},
        {'name': 'Omeprazole', 'dosage': '20mg', 'frequency': 'Once daily', 'duration': 14},
        {'name': 'Metformin', 'dosage': '500mg', 'frequency': 'Twice daily', 'duration': 30},
        {'name': 'Lisinopril', 'dosage': '10mg', 'frequency': 'Once daily', 'duration': 30}
    ]
    
    for prescription in prescriptions:
        # Create 1-3 prescription items per prescription
        num_items = random.randint(1, 3)
        selected_medicines = random.sample(medicines, num_items)
        
        for medicine in selected_medicines:
            PrescriptionItem.objects.get_or_create(
                prescription=prescription,
                medicine_name=medicine['name'],
                defaults={
                    'dosage': medicine['dosage'],
                    'frequency': medicine['frequency'],
                    'duration_days': medicine['duration'],
                    'instructions': f'Take {medicine["dosage"]} {medicine["frequency"].lower()}',
                    'is_conflicting': random.choice([True, False])
                }
            )


def create_encounter_reports():
    """Create sample encounter reports"""
    print("📋 Creating Encounter Reports...")
    
    encounters = Encounter.objects.all()
    
    report_titles = [
        'Blood Test Results', 'X-Ray Report', 'ECG Report', 'Ultrasound Report',
        'Pathology Report', 'Cardiology Report', 'Neurology Report'
    ]
    
    for encounter in encounters:
        # Create 0-2 reports per encounter
        num_reports = random.randint(0, 2)
        if num_reports > 0:
            selected_reports = random.sample(report_titles, num_reports)
            
            for report_title in selected_reports:
                EncounterReport.objects.get_or_create(
                    encounter=encounter,
                    title=report_title,
                    defaults={
                        'file': f'encounter_reports/{encounter.id}/{report_title.replace(" ", "_")}.pdf'
                    }
                )


def create_invoices():
    """Create sample invoices"""
    print("🧾 Creating Invoices...")
    
    patients = Patient.objects.all()
    encounters = Encounter.objects.all()
    users = User.objects.filter(is_superuser=False)
    
    # Create invoice counter
    counter, created = InvoiceCounter.objects.get_or_create(
        defaults={
            'prefix': 'INV',
            'counter': 0
        }
    )
    
    for i in range(6):  # Create 6 invoices
        patient = random.choice(patients)
        encounter = random.choice(encounters) if encounters.exists() else None
        user = random.choice(users)
        
        # Generate invoice number
        invoice_no = f"INV-{str(counter.next()).zfill(4)}"
        
        Invoice.objects.get_or_create(
            invoice_no=invoice_no,
            defaults={
                'patient': patient,
                'created_by': user,
                'encounter': encounter,
                'date': timezone.now() - timedelta(days=random.randint(1, 30)),
                'subtotal': Decimal(str(random.uniform(500, 2000))),
                'tax_total': Decimal(str(random.uniform(50, 200))),
                'discount': Decimal(str(random.uniform(0, 100))),
                'total': Decimal(str(random.uniform(600, 2200))),
                'status': random.choice(['DRAFT', 'ISSUED', 'PAID']),
                'notes': f'Invoice for {patient.full_name}'
            }
        )


def create_invoice_items():
    """Create sample invoice items"""
    print("📝 Creating Invoice Items...")
    
    invoices = Invoice.objects.all()
    charge_types = ChargeType.objects.all()
    
    for invoice in invoices:
        # Create 1-3 items per invoice
        num_items = random.randint(1, 3)
        selected_charges = random.sample(list(charge_types), num_items)
        
        for charge_type in selected_charges:
            quantity = random.randint(1, 3)
            unit_price = charge_type.default_price
            amount = unit_price * quantity
            
            InvoiceItem.objects.get_or_create(
                invoice=invoice,
                charge_type=charge_type,
                description=f'{charge_type.name} - {invoice.patient.full_name}',
                defaults={
                    'unit_price': unit_price,
                    'quantity': quantity,
                    'amount': amount,
                    'tax_amount': amount * (charge_type.taxable_rate / 100) if charge_type.taxable_rate else 0,
                    'discount': Decimal('0.00'),
                    'validity_days': 30,
                    'valid_until': date.today() + timedelta(days=30)
                }
            )


def create_payments():
    """Create sample payments"""
    print("💳 Creating Payments...")
    
    invoices = Invoice.objects.all()
    users = User.objects.filter(is_superuser=False)
    
    payment_methods = ['CASH', 'CARD', 'UPI', 'WALLET', 'NETBANK']
    
    for i in range(4):  # Create 4 payments
        invoice = random.choice(invoices)
        user = random.choice(users)
        
        Payment.objects.get_or_create(
            paid_by=user,
            payment_method=random.choice(payment_methods),
            amount=invoice.total,
            paid_at=timezone.now() - timedelta(days=random.randint(1, 30)),
            defaults={
                'payer_name': invoice.patient.full_name,
                'transaction_ref': f"TXN{random.randint(100000, 999999)}",
                'is_advance': random.choice([True, False])
            }
        )


def create_payment_allocations():
    """Create sample payment allocations"""
    print("💰 Creating Payment Allocations...")
    
    payments = Payment.objects.all()
    invoices = Invoice.objects.all()
    
    for payment in payments:
        # Allocate payment to random invoice
        invoice = random.choice(invoices)
        
        PaymentAllocation.objects.get_or_create(
            payment=payment,
            invoice=invoice,
            defaults={
                'amount': min(payment.amount, invoice.total)
            }
        )


def create_notification_settings():
    """Create sample notification settings"""
    print("📱 Creating Notification Settings...")
    
    organizations = Organization.objects.all()
    
    for org in organizations:
        TenantNotificationSetting.objects.get_or_create(
            tenant=org.slug,
            defaults={
                'sms_enabled': True,
                'whatsapp_enabled': True,
                'sms_provider': 'twilio',
                'whatsapp_provider': 'twilio_whatsapp',
                'default_from_number': '+91-9876543210'
            }
        )


def create_notification_templates():
    """Create sample notification templates"""
    print("📧 Creating Notification Templates...")
    
    organizations = Organization.objects.all()
    
    templates_data = [
        {
            'event': 'appointment_booked',
            'channel': 'SMS',
            'subject': 'Appointment Confirmed',
            'template': 'Dear {{patient_name}}, your appointment with Dr {{doctor_name}} is confirmed for {{appointment_date}} at {{appointment_time}}. Token: {{token_number}}'
        },
        {
            'event': 'appointment_reminder',
            'channel': 'SMS',
            'subject': 'Appointment Reminder',
            'template': 'Reminder: You have an appointment with Dr {{doctor_name}} tomorrow at {{appointment_time}}. Please arrive 15 minutes early.'
        },
        {
            'event': 'invoice_issued',
            'channel': 'SMS',
            'subject': 'Invoice Generated',
            'template': 'Dear {{patient_name}}, your invoice {{invoice_no}} for amount ₹{{amount}} has been generated. Please make payment at your earliest convenience.'
        }
    ]
    
    for org in organizations:
        for template_data in templates_data:
            NotificationTemplate.objects.get_or_create(
                tenant=org.slug,
                event=template_data['event'],
                channel=template_data['channel'],
                defaults={
                    'subject': template_data['subject'],
                    'template': template_data['template'],
                    'is_active': True
                }
            )


def create_notification_events():
    """Create sample notification events"""
    print("📨 Creating Notification Events...")
    
    organizations = Organization.objects.all()
    patients = Patient.objects.all()
    
    events = ['appointment_booked', 'appointment_reminder', 'invoice_issued']
    channels = ['SMS', 'WHATSAPP']
    statuses = ['PENDING', 'SENT', 'FAILED']
    
    for i in range(10):  # Create 10 notification events
        org = random.choice(organizations)
        patient = random.choice(patients)
        
        NotificationEvent.objects.get_or_create(
            tenant=org.slug,
            event=random.choice(events),
            channel=random.choice(channels),
            to=patient.phone,
            defaults={
                'subject': f'Notification from {org.name}',
                'message': f'Test message for {patient.full_name}',
                'payload': {
                    'patient_name': patient.full_name,
                    'clinic_name': org.name
                },
                'scheduled_at': timezone.now() - timedelta(days=random.randint(1, 30)),
                'status': random.choice(statuses),
                'attempts': random.randint(0, 3)
            }
        )


if __name__ == '__main__':
    create_sample_data()
