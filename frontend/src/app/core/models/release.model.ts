import { Environment, ReleaseStatus } from './enums';

export interface Release {
  id?: number;
  applicationId: number;
  version: string;
  env: Environment;
  status: ReleaseStatus;
  evidenceUrl?: string;
  createdAt?: Date;
  deployedAt?: Date;
  logs?: string;
  applicationName?: string;
}

export interface CreateReleaseRequest {
  applicationId: number;
  version: string;
}

export interface PromoteReleaseResponse {
  success: boolean;
  message: string;
  release: Release;
}
