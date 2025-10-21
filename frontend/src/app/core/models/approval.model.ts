import { ApprovalOutcome } from './enums';

export interface Approval {
  id?: number;
  releaseId?: number;
  release_id?: number;
  approverEmail?: string;
  approver_email?: string;
  outcome: ApprovalOutcome | string;
  notes?: string;
  timestamp?: Date | string;
}

export interface ApprovalRequest {
  notes?: string;
}
