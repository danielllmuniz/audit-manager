import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { Release, Approval } from '../../../core/models';
import { Environment, ReleaseStatus } from '../../../core/models/enums';
import { ReleaseService } from '../../../core/services/release.service';
import { NotificationService } from '../../../core/services/notification.service';
import { MaterialModule } from '../../../shared/material.module';
import {
  getEnvironmentConfig,
  getStatusConfig,
} from '../../../shared/utils/status-helpers';

interface TimelineEvent {
  title: string;
  description: string;
  timestamp: Date;
  icon: string;
  type: 'created' | 'pending' | 'approved' | 'rejected' | 'deployed';
}

@Component({
  selector: 'app-release-detail',
  standalone: true,
  imports: [CommonModule, MaterialModule, RouterModule],
  templateUrl: './release-detail.component.html',
  styleUrl: './release-detail.component.css',
})
export class ReleaseDetailComponent implements OnInit {
  release: Release | null = null;
  approvals: Approval[] = [];
  timelineEvents: TimelineEvent[] = [];
  loading = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private releaseService: ReleaseService,
    private notificationService: NotificationService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.params['id'];
    if (id) {
      this.loadRelease(+id);
    }
  }

  loadRelease(id: number): void {
    this.loading = true;
    this.releaseService.getReleaseById(id).subscribe({
      next: (data: any) => {
        this.release = data;
        this.approvals = data.approvals || [];
        this.buildTimeline();
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading release:', error);
        this.notificationService.showError('Error loading release details');
        this.loading = false;
        this.router.navigate(['/releases']);
      },
    });
  }

  buildTimeline(): void {
    if (!this.release) return;

    this.timelineEvents = [];

    // Created event
    const createdDate = this.release.created_at || this.release.createdAt;
    if (createdDate) {
      this.timelineEvents.push({
        title: 'Release Created',
        description: `Version ${this.release.version} created for ${this.release.env} environment`,
        timestamp: new Date(createdDate),
        icon: 'add_circle',
        type: 'created',
      });
    }

    // Approval/Rejection events
    if (this.approvals && this.approvals.length > 0) {
      this.approvals.forEach((approval) => {
        const email = approval.approver_email || approval.approverEmail || 'Unknown';
        const outcome = String(approval.outcome);
        const timestampValue = approval.timestamp;

        if (timestampValue) {
          this.timelineEvents.push({
            title:
              outcome === 'APPROVED'
                ? 'Release Approved'
                : 'Release Rejected',
            description: `${outcome.toLowerCase()} by ${email}${approval.notes ? `: ${approval.notes}` : ''}`,
            timestamp: new Date(timestampValue),
            icon:
              outcome === 'APPROVED' ? 'check_circle' : 'cancel',
            type: outcome === 'APPROVED' ? 'approved' : 'rejected',
          });
        }
      });
    }

    // Deployed to PREPROD event
    const deployedPreprodDate = this.release.deployed_preprod_at || this.release.deployedPreprodAt;
    if (deployedPreprodDate) {
      this.timelineEvents.push({
        title: 'Deployed to PREPROD',
        description: 'Successfully deployed to PREPROD environment',
        timestamp: new Date(deployedPreprodDate),
        icon: 'rocket_launch',
        type: 'deployed',
      });
    }

    // Deployed to PROD event
    const deployedProdDate = this.release.deployed_prod_at || this.release.deployedProdAt;
    if (deployedProdDate) {
      this.timelineEvents.push({
        title: 'Deployed to PROD',
        description: 'Successfully deployed to PRODUCTION environment',
        timestamp: new Date(deployedProdDate),
        icon: 'rocket_launch',
        type: 'deployed',
      });
    }

    // Sort by timestamp (newest first)
    this.timelineEvents.sort(
      (a, b) => b.timestamp.getTime() - a.timestamp.getTime()
    );
  }

  goBack(): void {
    this.router.navigate(['/releases']);
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

  downloadEvidence(release: Release): void {
    const evidenceUrl = release.evidence_url || release.evidenceUrl;
    if (!evidenceUrl) return;

    this.releaseService.downloadEvidence(evidenceUrl).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `evidence_${release.version}.txt`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      },
      error: (error) => {
        console.error('Error downloading evidence:', error);
        this.notificationService.showError('Error downloading evidence file');
      },
    });
  }
}
