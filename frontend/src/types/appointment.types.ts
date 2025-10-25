export interface Appointment {
  id: string;
  patient: string;
  patient_name?: string;
  doctor: string;
  doctor_name?: string;
  appointment_date: string;
  appointment_time: string;
  status: 'scheduled' | 'confirmed' | 'in_progress' | 'completed' | 'cancelled' | 'no_show';
  reason: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface AppointmentFormData {
  patient: string;
  doctor: string;
  appointment_date: string;
  appointment_time: string;
  reason: string;
  notes?: string;
}
