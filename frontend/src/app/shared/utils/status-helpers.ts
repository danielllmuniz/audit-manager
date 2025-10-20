import { Environment, ReleaseStatus } from '../../core/models/enums';

export interface StatusConfig {
  label: string;
  color: string;
  icon: string;
}

export interface EnvironmentConfig {
  label: string;
  color: string;
  icon: string;
}

export const STATUS_CONFIG: Record<ReleaseStatus, StatusConfig> = {
  [ReleaseStatus.CREATED]: {
    label: 'Criado',
    color: 'primary',
    icon: 'schedule',
  },
  [ReleaseStatus.PENDING_PREPROD]: {
    label: 'Aguardando PRE-PROD',
    color: 'accent',
    icon: 'pending',
  },
  [ReleaseStatus.PENDING_PROD]: {
    label: 'Aguardando PROD',
    color: 'accent',
    icon: 'pending',
  },
  [ReleaseStatus.APPROVED_PREPROD]: {
    label: 'Aprovado PRE-PROD',
    color: 'primary',
    icon: 'check_circle',
  },
  [ReleaseStatus.APPROVED_PROD]: {
    label: 'Aprovado PROD',
    color: 'primary',
    icon: 'check_circle',
  },
  [ReleaseStatus.REJECTED]: {
    label: 'Rejeitado',
    color: 'warn',
    icon: 'cancel',
  },
  [ReleaseStatus.DEPLOYED]: {
    label: 'Implantado',
    color: 'accent',
    icon: 'cloud_done',
  },
};

export const ENVIRONMENT_CONFIG: Record<Environment, EnvironmentConfig> = {
  [Environment.DEV]: {
    label: 'DEV',
    color: 'primary',
    icon: 'code',
  },
  [Environment.PREPROD]: {
    label: 'PRE-PROD',
    color: 'accent',
    icon: 'backup',
  },
  [Environment.PROD]: {
    label: 'PROD',
    color: 'warn',
    icon: 'cloud',
  },
};

export function getStatusConfig(status: ReleaseStatus): StatusConfig {
  return STATUS_CONFIG[status];
}

export function getEnvironmentConfig(env: Environment): EnvironmentConfig {
  return ENVIRONMENT_CONFIG[env];
}
