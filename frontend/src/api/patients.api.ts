import axiosInstance from './axios.config';
import { Patient, PatientFormData } from '../types/patient.types';
import { PaginatedResponse } from '../types/common.types';

export const patientsAPI = {
  getAll: async (params?: {
    page?: number;
    search?: string;
  }): Promise<PaginatedResponse<Patient>> => {
    const response = await axiosInstance.get('/patients/', { params });
    return response.data;
  },

  getById: async (id: string): Promise<Patient> => {
    const response = await axiosInstance.get(`/patients/${id}/`);
    return response.data;
  },

  create: async (data: PatientFormData): Promise<Patient> => {
    const response = await axiosInstance.post('/patients/', data);
    return response.data;
  },

  update: async (id: string, data: Partial<PatientFormData>): Promise<Patient> => {
    const response = await axiosInstance.patch(`/patients/${id}/`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await axiosInstance.delete(`/patients/${id}/`);
  },

  search: async (query: string): Promise<Patient[]> => {
    const response = await axiosInstance.get(`/patients/`, {
      params: { search: query },
    });
    return response.data.results;
  },
};
