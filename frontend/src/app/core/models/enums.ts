export enum Environment {
  DEV = 'DEV',
  PREPROD = 'PREPROD',
  PROD = 'PROD',
}

export enum ReleaseStatus {
  CREATED = 'CREATED',
  PENDING_PREPROD = 'PENDING_PREPROD',
  PENDING_PROD = 'PENDING_PROD',
  APPROVED_PREPROD = 'APPROVED_PREPROD',
  APPROVED_PROD = 'APPROVED_PROD',
  REJECTED = 'REJECTED',
  DEPLOYED = 'DEPLOYED',
}

export enum ApprovalOutcome {
  APPROVED = 'APPROVED',
  REJECTED = 'REJECTED',
}

export enum UserRole {
  DEV = 'DEV',
  APPROVER = 'APPROVER',
  DEVOPS = 'DEVOPS',
}
