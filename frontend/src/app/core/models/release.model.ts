import { Environment, ReleaseStatus } from './enums';
import { Approval } from './approval.model';

export interface Release {
  release_id?: number;
  application_id: number;
  version: string;
  env: Environment;
  status: ReleaseStatus;
  evidence_url?: string;
  created_at?: string;
  deployed_at?: string;
  logs?: string;
  deployment_logs?: string;
  application_name?: string;
  approvals?: Approval[];

  id?: number;
  releaseId?: number;
  applicationId?: number;
  evidenceUrl?: string;
  createdAt?: Date;
  deployedAt?: Date;
  applicationName?: string;
}

export interface CreateReleaseRequest {
  application_id: number;
  version: string;
}

export interface PromoteReleaseResponse {
  success: boolean;
  message: string;
  release: Release;
}
