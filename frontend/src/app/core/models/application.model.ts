import { Release } from './release.model';

export interface Application {
  application_id?: number;
  name: string;
  owner_team: string;
  repo_url: string;
  created_at?: string;
  releases?: Release[];

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
