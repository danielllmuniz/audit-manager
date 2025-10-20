export interface Application {
  id?: number;
  name: string;
  ownerTeam: string;
  repoUrl: string;
  createdAt?: Date;
}

export interface CreateApplicationRequest {
  name: string;
  ownerTeam: string;
  repoUrl: string;
}
