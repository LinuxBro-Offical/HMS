# HMS Backend API Scripts

This folder contains utility scripts for the HMS Backend API (Hospital Management System Backend API) project.

## Available Scripts

### `seed_data.py`
Comprehensive sample data seeding script that creates realistic test data for all models in the HMS system.

**Usage:**
```bash
cd /path/to/HMS_Backend_API
python scripts/seed_data.py
```

**What it creates:**
- 5 Organizations with different plans and settings
- 5 Subscription plans (Free, Starter, Professional, Enterprise, Custom)
- 7 Branches across organizations
- 11 Users (including admin and staff)
- 8 Roles (tenant_admin, doctor, nurse, etc.)
- 5 Patients with medical history
- Patient conditions, allergies, and reports
- Doctor schedules and appointments
- Clinical encounters with prescriptions
- Billing invoices and payments
- Notification settings and templates

**Features:**
- Creates realistic, interconnected data
- Handles foreign key relationships properly
- Uses timezone-aware datetime objects
- Prevents duplicate data creation
- Provides detailed progress output

**Data Volume:**
- Organizations: 5
- Branches: 7
- Users: 11
- Patients: 5
- Appointments: 30
- Encounters: 22
- Invoices: 6
- Payments: 4

## Running Scripts

All scripts are designed to be run from the project root directory:

```bash
cd /path/to/HMS_Backend_API
python scripts/script_name.py
```

## Requirements

- Django project must be properly configured
- Database migrations must be applied
- All required dependencies must be installed

## Notes

- Scripts use `get_or_create()` to prevent duplicate data
- Timezone-aware datetime objects are used throughout
- Scripts handle foreign key relationships carefully
- Progress is shown with emoji indicators for better UX
