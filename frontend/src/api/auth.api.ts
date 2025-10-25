import axiosInstance from './axios.config';
import { LoginCredentials, AuthResponse, User } from '../types/auth.types';

export const authAPI = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await axiosInstance.post('/users/token/', credentials);
    return response.data;
  },

  logout: async (): Promise<void> => {
    try {
      await axiosInstance.post('/users/logout/');
    } catch (error) {
      console.error('Logout error:', error);
    }
  },

  refreshToken: async (refreshToken: string): Promise<{ access: string }> => {
    const response = await axiosInstance.post('/users/token/refresh/', {
      refresh: refreshToken,
    });
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await axiosInstance.get('/users/me/');
    return response.data;
  },

  changePassword: async (data: {
    current_password: string;
    new_password: string;
  }): Promise<void> => {
    await axiosInstance.post('/users/change-password/', data);
  },
};
