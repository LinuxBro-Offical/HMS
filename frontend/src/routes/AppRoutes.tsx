import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import PrivateRoute from './PrivateRoute';
import Login from '../pages/auth/Login';
import Dashboard from '../pages/dashboard/Dashboard';
import PatientsPage from '../pages/patients/PatientsPage';
import PatientDetailsPage from '../pages/patients/PatientDetailsPage';
import AddPatientPage from '../pages/patients/AddPatientPage';
import AppointmentsPage from '../pages/appointments/AppointmentsPage';

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/dashboard"
        element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        }
      />
      <Route
        path="/patients"
        element={
          <PrivateRoute>
            <PatientsPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/patients/new"
        element={
          <PrivateRoute>
            <AddPatientPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/patients/:id"
        element={
          <PrivateRoute>
            <PatientDetailsPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/appointments"
        element={
          <PrivateRoute>
            <AppointmentsPage />
          </PrivateRoute>
        }
      />
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
};

export default AppRoutes;
