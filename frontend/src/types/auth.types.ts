export interface User {
  id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role?: string;
  is_active: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
  user?: User;
}

export interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}
