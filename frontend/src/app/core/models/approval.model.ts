import { ApprovalOutcome } from './enums';

export interface Approval {
  id?: number;
  releaseId: number;
  approverEmail: string;
  outcome: ApprovalOutcome;
  notes?: string;
  timestamp?: Date;
}

export interface ApprovalRequest {
  notes?: string;
}
