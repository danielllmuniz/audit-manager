import { CommonModule } from '@angular/common';
import { Component, Inject } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ApprovalRequest, Release } from '../../../core/models';
import { ReleaseStatus } from '../../../core/models/enums';
import { NotificationService } from '../../../core/services/notification.service';
import { ReleaseService } from '../../../core/services/release.service';
import { MaterialModule } from '../../../shared/material.module';
import { getStatusConfig } from '../../../shared/utils/status-helpers';

@Component({
  selector: 'app-approval-dialog',
  standalone: true,
  imports: [CommonModule, MaterialModule, ReactiveFormsModule],
  templateUrl: './approval-dialog.component.html',
  styleUrl: './approval-dialog.component.css',
})
export class ApprovalDialogComponent {
  approvalForm: FormGroup;
  saving = false;
  release: Release;
  isApproval: boolean;

  constructor(
    private fb: FormBuilder,
    private releaseService: ReleaseService,
    private notificationService: NotificationService,
    private dialogRef: MatDialogRef<ApprovalDialogComponent>,
    @Inject(MAT_DIALOG_DATA)
    public data: { release: Release; isApproval: boolean }
  ) {
    this.release = data.release;
    this.isApproval = data.isApproval;

    this.approvalForm = this.fb.group({
      notes: ['', [Validators.maxLength(500)]],
    });
  }

  onSubmit(): void {
    if (this.approvalForm.invalid) {
      this.approvalForm.markAllAsTouched();
      return;
    }

    this.saving = true;

    const request: ApprovalRequest = {
      notes: this.approvalForm.value.notes || undefined,
    };

    const releaseId = this.release.id || this.release.release_id;
    if (!releaseId) {
      this.notificationService.showError('ID do release não encontrado');
      this.saving = false;
      return;
    }

    const serviceCall = this.isApproval
      ? this.releaseService.approveRelease(releaseId, request)
      : this.releaseService.disapproveRelease(releaseId, request);

    serviceCall.subscribe({
      next: (release) => {
        const action = this.isApproval ? 'aprovado' : 'rejeitado';
        this.notificationService.showSuccess(
          `Release ${this.release.version} ${action} com sucesso!`
        );
        this.dialogRef.close(true);
      },
      error: (error) => {
        console.error('Erro ao processar aprovação:', error);
        this.saving = false;
      },
    });
  }

  getStatusLabel(): string {
    return getStatusConfig(this.release.status).label;
  }

  getStatusClass(): string {
    const statusMap: Record<ReleaseStatus, string> = {
      [ReleaseStatus.CREATED]: 'created',
      [ReleaseStatus.PENDING_PREPROD]: 'pending',
      [ReleaseStatus.PENDING_PROD]: 'pending',
      [ReleaseStatus.APPROVED_PREPROD]: 'approved',
      [ReleaseStatus.APPROVED_PROD]: 'approved',
      [ReleaseStatus.REJECTED]: 'rejected',
      [ReleaseStatus.DEPLOYED]: 'deployed',
    };
    return statusMap[this.release.status];
  }
}
