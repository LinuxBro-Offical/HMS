# HMS Backend API - Hospital Management System

## Overview

A comprehensive Hospital Management System Backend API built with Django REST Framework. This is a multi-tenant healthcare application that provides complete REST API solutions for healthcare providers, from small clinics to large hospital networks.

**Project Type:** Backend API (Django REST Framework)
**Version:** 2.0.0
**Python Version:** 3.11
**Database:** SQLite (Development) / PostgreSQL (Production Ready)

## Current State

The HMS application is set up as a **full-stack monorepo** with both backend and frontend running together:
- **Backend API:** Django REST Framework running on localhost:8000 (internal)
- **Frontend:** React TypeScript app running on 0.0.0.0:5000 (user-facing webview)
- All database migrations applied and operational

## Recent Changes (October 25, 2025)

**Backend:**
- Installed Python 3.11 and all Django dependencies
- Configured Django settings for Replit environment with environment variable support
- Made settings production-ready with environment-based configuration
- Created fresh database migrations and applied them
- Set up backend workflow running on localhost:8000
- Configured deployment with Gunicorn
- Added dummy cache fallback when Redis is not available

**Frontend:**
- Built complete React TypeScript application in frontend/ directory
- Installed Node.js 20 and all React dependencies
- Configured Redux Toolkit for state management
- Implemented JWT authentication with auto-refresh
- Created Patient module with list and details pages
- Built Dashboard with statistics
- Configured Material-UI theme
- Set up protected routing system
- Frontend running on 0.0.0.0:5000 with proxy to backend

## Project Architecture

### Backend Technology Stack

- **Framework:** Django 5.2.3 with Django REST Framework 3.15.2
- **Authentication:** JWT (JSON Web Tokens) with djangorestframework-simplejwt
- **Database:** SQLite (dev), PostgreSQL support ready
- **Caching:** Redis (optional, configured but not required for dev)
- **Task Queue:** Celery (optional, for background jobs)
- **File Uploads:** Pillow for image processing
- **CORS:** django-cors-headers (configured for all origins in dev)

### Frontend Technology Stack

- **Framework:** React 18.2 with TypeScript 4.9
- **State Management:** Redux Toolkit 2.0
- **UI Library:** Material-UI (MUI) v5
- **Routing:** React Router v6
- **Forms:** React Hook Form + Yup
- **API Client:** Axios with JWT interceptors
- **Charts:** Recharts
- **Notifications:** React Toastify
- **Styling:** Emotion (CSS-in-JS)

### Core Modules

1. **Tenants** - Multi-tenant organization management
2. **Users** - User management, authentication, roles
3. **Patients** - Patient records and medical history
4. **Appointments** - Scheduling and appointment management
5. **Encounters** - Clinical consultations and doctor visits
6. **Billing** - Invoicing, payments, insurance
7. **Notifications** - Multi-channel communication (SMS, email, push)

### Enhanced Modules

8. **Clinical Decision Support** - Drug interactions, guidelines, alerts
9. **Laboratory** - Lab test management and results
10. **Inventory** - Medicine stock tracking and management
11. **Telemedicine** - Remote video consultations
12. **Analytics** - Performance metrics and reporting
13. **Patient Portal** - Patient self-service features
14. **Compliance** - Audit logging and privacy management
15. **Integrations** - External system connectivity

## API Endpoints

All API endpoints are prefixed with `/api/`:

- `/admin/` - Django admin interface
- `/api/tenants/` - Organization management
- `/api/users/` - User authentication and management
- `/api/patients/` - Patient records
- `/api/appointments/` - Appointment scheduling
- `/api/encounters/` - Clinical encounters
- `/api/billing/` - Billing and payments
- `/api/notifications/` - Notification management
- `/api/clinical-decision-support/` - Clinical guidelines
- `/api/laboratory/` - Lab tests and results
- `/api/inventory/` - Medicine inventory
- `/api/telemedicine/` - Telemedicine sessions
- `/api/analytics/` - Analytics and reports
- `/api/patient-portal/` - Patient portal features
- `/api/compliance/` - Compliance and audit logs
- `/api/integrations/` - External integrations

## Authentication

The API uses JWT authentication:

1. **Login:** POST to `/api/users/login/` (or similar auth endpoint)
2. **Token Response:** Returns `access` and `refresh` tokens
3. **Using Tokens:** Include in Authorization header: `Bearer <access_token>`

## Development

### Running the Application

The application runs automatically via the configured workflow on port 5000:
```bash
python manage.py runserver 0.0.0.0:5000
```

### Common Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data
python scripts/seed_data.py

# Access Django shell
python manage.py shell
```

### Database

Currently using SQLite for development (`db.sqlite3`). The application is configured to support PostgreSQL for production use via the Replit database integration if needed.

### File Storage

- **Media files:** Stored in `media/` directory
- **Logs:** Stored in `logs/` directory

## Deployment

The application is configured for deployment using:
- **Server:** Gunicorn WSGI server
- **Workers:** 4 worker processes
- **Port:** 5000
- **Deployment Type:** Autoscale (stateless, suitable for REST APIs)

### Production Checklist

**Required for production deployment:**

1. **Set environment variables:**
   - `SECRET_KEY` - Generate a new secret key for production
   - `DEBUG=False` - Disable debug mode
   - `ALLOWED_HOSTS` - Set to your domain (comma-separated)
   - `CORS_ALLOWED_ORIGINS` - Set allowed frontend origins (comma-separated)

2. **Optional but recommended:**
   - Set up PostgreSQL database via Replit integrations
   - Configure Redis for caching and Celery tasks
   - Set up email service (SMTP settings)
   - Configure file storage (AWS S3)
   - Set up error monitoring (Sentry)

3. **Security:**
   - Never commit sensitive credentials to the repository
   - Use Replit's secrets management for API keys
   - Review and update CORS settings for production domains

See `.env.production.example` for a complete list of production environment variables.

## Multi-Tenant Architecture

The system supports multiple organizations operating independently:
- Each tenant has isolated data
- Separate user accounts per organization
- Independent billing and workflows
- Custom branding per organization

## Next Steps

To start using the API:

1. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

2. **Access the admin panel:**
   Navigate to `/admin/` in the browser

3. **Load sample data (optional):**
   ```bash
   python scripts/seed_data.py
   ```

4. **Start making API requests:**
   Use the API endpoints listed above with proper authentication

## User Preferences

None set yet.

## Notes

- **Development Mode:** CORS allows all origins, DEBUG is enabled, uses SQLite database
- **Production Mode:** Requires setting environment variables (see Production Checklist)
- The application uses SQLite by default but can use PostgreSQL via DATABASE_URL
- Redis and Celery are optional - app uses dummy cache when Redis is not available
- File uploads are supported via the media directory
- Settings are environment-aware and will automatically adjust based on environment variables

## Environment Variables

The application supports environment-based configuration:

**Development defaults (current):**
- DEBUG=True
- ALLOWED_HOSTS=*
- CORS_ALLOW_ALL_ORIGINS=True
- Database: SQLite (db.sqlite3)
- Cache: Dummy cache (no Redis required)

**Production configuration:**
Set environment variables to override defaults (see `.env.production.example`)
