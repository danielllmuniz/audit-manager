export interface Application {
  application_id?: number;
  name: string;
  owner_team: string;
  repo_url: string;
  created_at?: string;

  id?: number;
  ownerTeam?: string;
  repoUrl?: string;
  createdAt?: Date;
}

export interface CreateApplicationRequest {
  name: string;
  owner_team: string;
  repo_url: string;
}
