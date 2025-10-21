import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { Application, Release } from '../../../core/models';
import { Environment, ReleaseStatus } from '../../../core/models/enums';
import { ApplicationService } from '../../../core/services/application.service';
import { MaterialModule } from '../../../shared/material.module';
import {
  getEnvironmentConfig,
  getStatusConfig,
} from '../../../shared/utils/status-helpers';

@Component({
  selector: 'app-application-detail',
  standalone: true,
  imports: [CommonModule, MaterialModule, RouterModule],
  templateUrl: './application-detail.component.html',
  styleUrl: './application-detail.component.css',
})
export class ApplicationDetailComponent implements OnInit {
  application: Application | null = null;
  releases: Release[] = [];
  loading = false;
  displayedColumns: string[] = [
    'id',
    'version',
    'env',
    'status',
    'createdAt',
    'actions',
  ];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private applicationService: ApplicationService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.params['id'];
    if (id) {
      this.loadApplication(+id);
    }
  }

  loadApplication(id: number): void {
    this.loading = true;
    this.applicationService.getApplicationById(id).subscribe({
      next: (data) => {
        this.application = data;
        this.releases = data.releases || [];
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading application:', error);
        this.loading = false;
        this.router.navigate(['/applications']);
      },
    });
  }

  goBack(): void {
    this.router.navigate(['/applications']);
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
}
