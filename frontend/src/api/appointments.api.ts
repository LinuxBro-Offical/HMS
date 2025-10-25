import axiosInstance from './axios.config';
import { Appointment, AppointmentFormData } from '../types/appointment.types';
import { PaginatedResponse } from '../types/common.types';

export const appointmentsAPI = {
  getAll: async (params?: {
    page?: number;
    status?: string;
    patient?: string;
    doctor?: string;
  }): Promise<PaginatedResponse<Appointment>> => {
    const response = await axiosInstance.get('/appointments/', { params });
    return response.data;
  },

  getById: async (id: string): Promise<Appointment> => {
    const response = await axiosInstance.get(`/appointments/${id}/`);
    return response.data;
  },

  create: async (data: AppointmentFormData): Promise<Appointment> => {
    const response = await axiosInstance.post('/appointments/', data);
    return response.data;
  },

  update: async (id: string, data: Partial<AppointmentFormData>): Promise<Appointment> => {
    const response = await axiosInstance.patch(`/appointments/${id}/`, data);
    return response.data;
  },

  updateStatus: async (id: string, status: string): Promise<Appointment> => {
    const response = await axiosInstance.patch(`/appointments/${id}/`, { status });
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await axiosInstance.delete(`/appointments/${id}/`);
  },
};
