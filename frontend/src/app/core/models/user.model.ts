import { UserRole } from './enums';

export interface User {
  email: string;
  name: string;
  role: UserRole;
  token?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  user: User;
  token: string;
}
