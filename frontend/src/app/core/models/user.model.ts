import { UserRole } from './enums';

export interface User {
  id: number;
  email: string;
  name: string;
  role: UserRole;
}

export interface LoginResponse {
  data: {
    type: string;
    attributes: {
      token: string;
      user: User;
    };
  };
}
