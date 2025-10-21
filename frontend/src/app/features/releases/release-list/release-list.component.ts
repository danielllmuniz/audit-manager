import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { Application, Release } from '../../../core/models';
import {
  Environment,
  ReleaseStatus,
  UserRole,
} from '../../../core/models/enums';
import { AuthService } from '../../../core/services/auth.service';
import { NotificationService } from '../../../core/services/notification.service';
import { ReleaseService } from '../../../core/services/release.service';
import { MaterialModule } from '../../../shared/material.module';
import {
  getEnvironmentConfig,
  getStatusConfig,
} from '../../../shared/utils/status-helpers';
import { ApprovalDialogComponent } from '../approval-dialog/approval-dialog.component';
import { CreateReleaseDialogComponent } from '../create-release-dialog/create-release-dialog.component';

@Component({
  selector: 'app-release-list',
  standalone: true,
  imports: [CommonModule, MaterialModule, ReactiveFormsModule],
  templateUrl: './release-list.component.html',
  styleUrl: './release-list.component.css',
})
export class ReleaseListComponent implements OnInit {
  releases: Release[] = [];
  applications: Application[] = [];
  loading = false;
  filterForm: FormGroup;
  displayedColumns: string[] = [
    'id',
    'application',
    'version',
    'env',
    'status',
    'createdAt',
    'evidence',
    'actions',
  ];

  constructor(
    private releaseService: ReleaseService,
    private authService: AuthService,
    private notificationService: NotificationService,
    private dialog: MatDialog,
    private fb: FormBuilder
  ) {
    this.filterForm = this.fb.group({
      applicationId: [null],
      env: [null],
      status: [null],
      version: [''],
    });
  }

  ngOnInit(): void {
    this.loadReleases();
  }

  loadReleases(): void {
    this.loading = true;
    const filters = this.filterForm.value;

    const cleanFilters: any = {};
    if (filters.applicationId)
      cleanFilters.applicationId = filters.applicationId;
    if (filters.env) cleanFilters.env = filters.env;
    if (filters.status) cleanFilters.status = filters.status;
    if (filters.version) cleanFilters.version = filters.version;

    this.releaseService.getReleases(cleanFilters).subscribe({
      next: (data) => {
        this.releases = data;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading releases:', error);
        this.loading = false;
      },
    });
  }

  applyFilters(): void {
    this.loadReleases();
  }

  clearFilters(): void {
    this.filterForm.reset({
      applicationId: null,
      env: null,
      status: null,
      version: '',
    });
    this.loadReleases();
  }

  openCreateDialog(): void {
    const dialogRef = this.dialog.open(CreateReleaseDialogComponent, {
      width: '600px',
      data: { applications: this.applications },
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.loadReleases();
      }
    });
  }

  openApprovalDialog(release: Release, isApproval: boolean): void {
    const dialogRef = this.dialog.open(ApprovalDialogComponent, {
      width: '500px',
      data: { release, isApproval },
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.loadReleases();
      }
    });
  }

  promoteRelease(release: Release): void {
    const releaseId = release.id || release.release_id;
    if (!releaseId) return;

    this.releaseService.promoteRelease(releaseId).subscribe({
      next: (response) => {
        this.notificationService.showSuccess(
          `Release ${release.version} promoted successfully!`
        );
        this.loadReleases();
      },
      error: (error) => {
        console.error('Error promoting release:', error);
      },
    });
  }

  viewLogs(release: Release): void {
    alert(`Logs for Release ${release.version}:\n\n${release.logs}`);
  }

  canApprove(release: Release): boolean {
    const user = this.authService.currentUserValue;
    if (!user || user.role !== UserRole.APPROVER) return false;

    return (
      release.status === ReleaseStatus.PENDING_PREPROD ||
      release.status === ReleaseStatus.PENDING_PROD
    );
  }

  canReject(release: Release): boolean {
    return this.canApprove(release);
  }

  canPromote(release: Release): boolean {
    const user = this.authService.currentUserValue;
    if (!user || user.role !== UserRole.DEVOPS) return false;

    return (
      release.status === ReleaseStatus.APPROVED_PREPROD ||
      release.status === ReleaseStatus.APPROVED_PROD
    );
  }

  getStatusLabel(status: ReleaseStatus): string {
    return getStatusConfig(status).label;
  }

  getStatusIcon(status: ReleaseStatus): string {
    return getStatusConfig(status).icon;
  }

  getStatusClass(status: ReleaseStatus): string {
    const statusMap: Record<ReleaseStatus, string> = {
      [ReleaseStatus.CREATED]: 'created',
      [ReleaseStatus.PENDING_PREPROD]: 'pending',
      [ReleaseStatus.PENDING_PROD]: 'pending',
      [ReleaseStatus.APPROVED_PREPROD]: 'approved',
      [ReleaseStatus.APPROVED_PROD]: 'approved',
      [ReleaseStatus.REJECTED]: 'rejected',
      [ReleaseStatus.DEPLOYED]: 'deployed',
    };
    return statusMap[status];
  }

  getEnvironmentIcon(env: Environment): string {
    return getEnvironmentConfig(env).icon;
  }

  canCreateReleases(): boolean {
    return this.authService.hasRole('DEV');
  }
}
