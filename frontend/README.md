# HMS React Frontend

## Overview

A modern, production-ready React TypeScript frontend for the Hospital Management System (HMS). This application provides a comprehensive user interface for healthcare management with 14+ modules.

## Technology Stack

- **Framework:** React 18.2
- **Language:** TypeScript 4.9
- **State Management:** Redux Toolkit 2.0
- **UI Library:** Material-UI (MUI) v5
- **Routing:** React Router v6
- **Form Handling:** React Hook Form + Yup
- **API Client:** Axios
- **Charts:** Recharts
- **Notifications:** React Toastify
- **Styling:** Emotion (CSS-in-JS)

## Project Structure

```
frontend/
├── public/                  # Static files
├── src/
│   ├── api/                # API integration layer
│   │   ├── axios.config.ts # Axios instance with JWT interceptors
│   │   ├── auth.api.ts     # Authentication API
│   │   ├── patients.api.ts # Patient API
│   │   └── appointments.api.ts
│   ├── components/         # React components
│   │   ├── common/         # Shared components
│   │   ├── patients/       # Patient-specific components
│   │   └── ...
│   ├── pages/              # Page components
│   │   ├── auth/           # Login, register pages
│   │   ├── dashboard/      # Dashboard page
│   │   ├── patients/       # Patient management pages
│   │   └── ...
│   ├── store/              # Redux store
│   │   ├── slices/         # Redux slices
│   │   ├── index.ts        # Store configuration
│   │   └── hooks.ts        # Typed hooks
│   ├── types/              # TypeScript type definitions
│   ├── theme/              # MUI theme configuration
│   ├── routes/             # Routing configuration
│   ├── App.tsx             # Main app component
│   └── index.tsx           # Entry point
├── package.json
└── tsconfig.json
```

## Features

### Implemented

✅ **Authentication System**
- JWT-based authentication with automatic token refresh
- Secure login/logout flow
- Protected routes

✅ **Patient Management**
- Patient list with search and filters
- Patient details view
- Comprehensive patient information display

✅ **Dashboard**
- Overview statistics
- Quick actions
- Recent activity

✅ **Common Components**
- Responsive Navbar with user menu
- Sidebar navigation
- Material-UI theming

### Core Modules (Framework Ready)

The application has the framework in place for:
- Appointments
- Clinical Encounters
- Billing & Payments
- Laboratory Management
- Inventory Management
- Telemedicine
- Analytics & Reporting

## Getting Started

### Prerequisites

- Node.js 20+
- Backend API running on port 8000

### Installation

```bash
cd frontend
npm install --legacy-peer-deps
```

### Running the App

```bash
npm start
```

The app will start on `http://localhost:5000` (or the port specified in .env)

### Environment Variables

Create `.env.development` or `.env.production`:

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_NAME=HMS - Hospital Management System
PORT=5000
HOST=0.0.0.0
```

## API Integration

### Axios Configuration

The app uses Axios with interceptors for:
- Automatic JWT token attachment
- Token refresh on 401 errors
- Centralized error handling

### API Structure

```typescript
// Example: Using the patient API
import { patientsAPI } from '../api/patients.api';

// Fetch all patients
const patients = await patientsAPI.getAll({ page: 1, search: 'John' });

// Get patient by ID
const patient = await patientsAPI.getById('patient-id');

// Create patient
const newPatient = await patientsAPI.create(patientData);
```

## State Management

### Redux Store Structure

```typescript
{
  auth: {
    user: User | null,
    accessToken: string | null,
    isAuthenticated: boolean,
    loading: boolean,
    error: string | null
  },
  patients: {
    patients: Patient[],
    currentPatient: Patient | null,
    total: number,
    loading: LoadingState,
    error: string | null
  }
}
```

### Using Redux Hooks

```typescript
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { fetchPatients } from '../store/slices/patientsSlice';

// In component
const dispatch = useAppDispatch();
const { patients, loading } = useAppSelector((state) => state.patients);

useEffect(() => {
  dispatch(fetchPatients());
}, [dispatch]);
```

## Routing

The app uses React Router v6 with protected routes:

```
/login              - Public login page
/dashboard          - Protected dashboard
/patients           - Protected patients list
/patients/:id       - Protected patient details
/appointments       - Protected appointments
...
```

## Material-UI Theme

Custom theme with healthcare-friendly colors:
- Primary: Blue (`#1976d2`)
- Secondary: Purple (`#9c27b0`)
- Success: Green (`#2e7d32`)
- Error: Red (`#d32f2f`)

## Authentication Flow

1. User enters credentials on login page
2. Frontend calls `/api/users/token/` endpoint
3. Backend returns access + refresh tokens
4. Tokens stored in localStorage
5. Access token attached to all API requests
6. On 401 error, automatically refresh using refresh token
7. If refresh fails, redirect to login

## Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

## Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App (not recommended)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Next Steps

To expand the application:

1. **Complete remaining modules:**
   - Implement Appointments components
   - Build Encounters module
   - Add Billing functionality
   - Create Laboratory module
   - Build Inventory module

2. **Add features:**
   - Real-time notifications
   - File uploads
   - Print functionality
   - Advanced search/filters
   - Data export (PDF, Excel)

3. **Enhance UI/UX:**
   - Add loading skeletons
   - Implement pagination
   - Add form validation messages
   - Create confirmation dialogs
   - Add tooltips and help text

4. **Testing:**
   - Write unit tests
   - Add integration tests
   - E2E testing with Cypress

## Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## License

MIT
