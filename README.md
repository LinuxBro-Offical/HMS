# HMS Backend API

A comprehensive, modern Hospital Management System Backend API built with Django REST Framework and designed for multi-tenant healthcare organizations.

## 🏥 Overview

HMS Backend API is a full-featured hospital management system backend that provides comprehensive REST API solutions for healthcare providers, from small clinics to large hospital networks. The system supports multi-tenant architecture, allowing multiple healthcare organizations to operate independently on the same platform.

## ✨ Key Features

### 🏗️ **Core Modules**
- **Patient Management**: Complete patient records with medical history
- **Appointment System**: Scheduling and management with doctor availability
- **Clinical Encounters**: Doctor-patient consultations with structured notes
- **Billing & Payments**: Invoice generation, payment tracking, insurance management
- **Notifications**: Multi-channel communication system

### 🚀 **Modern Enhancements**
- **Clinical Decision Support**: Drug interactions, clinical guidelines, safety alerts
- **Laboratory Management**: Test ordering, result entry, report generation
- **Inventory Management**: Medicine stock tracking, purchase orders, expiry alerts
- **Telemedicine**: Video consultations, digital prescriptions, follow-up management
- **Analytics & Reporting**: Patient metrics, revenue tracking, performance analytics
- **Patient Portal**: Self-service portal with health goals and feedback
- **Compliance**: Audit logging, privacy consent, breach incident tracking
- **Integrations**: External system connectivity, data synchronization

### 🔧 **Technical Features**
- **Multi-tenant Architecture**: Isolated data per organization
- **RESTful API**: Complete API coverage for all modules
- **JWT Authentication**: Secure token-based authentication
- **Role-based Access Control**: Granular permissions system
- **Real-time Notifications**: SMS, Email, Push notifications
- **File Management**: Document and image uploads
- **Audit Trail**: Comprehensive activity logging

## 🛠️ Technology Stack

### Backend
- **Django 5.2.3**: Web framework
- **Django REST Framework**: API development
- **PostgreSQL**: Primary database (SQLite for development)
- **Redis**: Caching and session storage
- **Celery**: Background task processing
- **JWT**: Authentication tokens

### Frontend (Ready for Integration)
- **React 18+**: Frontend framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **Redux Toolkit**: State management
- **Chart.js**: Data visualization

## 📁 Project Structure

```
HMS_Backend_API/
├── HMS_API/                    # Main Django project
│   ├── settings.py             # Configuration
│   ├── urls.py                 # URL routing
│   └── wsgi.py                 # WSGI configuration
├── tenants/                    # Multi-tenant management
├── users/                      # User management & authentication
├── patients/                   # Patient records & management
├── appointments/               # Appointment scheduling
├── encounters/                 # Clinical consultations
├── billing/                    # Financial management
├── notifications/              # Communication system
├── clinical_decision_support/  # Clinical guidelines & alerts
├── laboratory/                 # Lab test management
├── inventory/                  # Medicine & stock management
├── telemedicine/               # Remote consultations
├── analytics/                  # Performance & revenue analytics
├── patient_portal/             # Patient self-service
├── compliance/                 # Audit & privacy management
├── integrations/               # External system connectivity
├── scripts/                    # Utility scripts
│   ├── seed_data.py           # Sample data generation
│   └── README.md              # Scripts documentation
├── logs/                       # Application logs
├── media/                      # File uploads
└── requirements.txt            # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd HMS_Backend_API
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Seed sample data**
   ```bash
   python scripts/seed_data.py
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the system**
   - Admin Interface: http://localhost:8000/admin/
   - API Documentation: http://localhost:8000/api/

## 📊 Sample Data

The system comes with comprehensive sample data:

- **5 Organizations** with different subscription plans
- **7 Branches** across organizations
- **11 Users** (admin, doctors, nurses, staff)
- **5 Patients** with complete medical profiles
- **30 Appointments** with various statuses
- **22 Clinical Encounters** with prescriptions
- **6 Invoices** with payment tracking
- **4 Payment Records** with different methods

## 🔐 Authentication

The system uses JWT (JSON Web Tokens) for authentication:

### Login
```bash
POST /api/auth/login/
{
    "username": "your_username",
    "password": "your_password"
}
```

### Response
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Using Tokens
Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## 👥 User Roles

- **Super Admin**: Full system access
- **Tenant Admin**: Organization-level administration
- **Doctor**: Patient care and clinical management
- **Nurse**: Patient care support
- **Receptionist**: Appointment and patient management
- **Lab Technician**: Laboratory operations
- **Pharmacist**: Inventory management
- **Accountant**: Billing and financial management

## 🏥 Multi-Tenant Architecture

Each organization operates in complete isolation:

- **Separate Data**: All data is tenant-specific
- **Custom Branding**: Organization-specific settings
- **Independent Users**: User accounts are tenant-scoped
- **Isolated Billing**: Separate financial tracking
- **Custom Workflows**: Tenant-specific configurations

## 📱 API Endpoints

### Core Resources
- **Patients**: `/api/patients/`
- **Appointments**: `/api/appointments/`
- **Encounters**: `/api/encounters/`
- **Billing**: `/api/billing/`
- **Notifications**: `/api/notifications/`

### Enhanced Modules
- **Clinical Decision Support**: `/api/clinical-decision-support/`
- **Laboratory**: `/api/laboratory/`
- **Inventory**: `/api/inventory/`
- **Telemedicine**: `/api/telemedicine/`
- **Analytics**: `/api/analytics/`
- **Patient Portal**: `/api/patient-portal/`
- **Compliance**: `/api/compliance/`
- **Integrations**: `/api/integrations/`

## 🔧 Configuration

### Environment Variables
```bash
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### CORS Settings
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

## 📈 Analytics & Reporting

The system provides comprehensive analytics:

- **Patient Analytics**: Visit patterns, risk scores, satisfaction metrics
- **Revenue Analytics**: Financial performance, payment trends
- **Doctor Performance**: Productivity metrics, patient satisfaction
- **Operational Metrics**: Appointment efficiency, resource utilization
- **Custom Reports**: Configurable report builder

## 🔒 Security & Compliance

- **Data Encryption**: Sensitive data encryption at rest
- **Audit Logging**: Complete activity tracking
- **Privacy Controls**: GDPR-compliant consent management
- **Access Controls**: Role-based permissions
- **Data Breach Management**: Incident tracking and reporting

## 🚀 Deployment

### Production Setup
1. Configure PostgreSQL database
2. Set up Redis for caching
3. Configure Celery for background tasks
4. Set up file storage (AWS S3, etc.)
5. Configure email/SMS providers
6. Set up monitoring and logging

### Docker Deployment
```bash
docker-compose up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Version History

- **v1.0.0**: Initial release with core HMS functionality
- **v2.0.0**: Enhanced with modern HMS features
  - Clinical Decision Support
  - Laboratory Management
  - Inventory Management
  - Telemedicine
  - Analytics & Reporting
  - Patient Portal
  - Compliance Management
  - Integration Framework

---

Built with ❤️ by Ananthu (Linux Bro)