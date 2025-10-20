import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { RouterModule } from '@angular/router';
import { Application } from '../../../core/models';
import { ApplicationService } from '../../../core/services/application.service';
import { NotificationService } from '../../../core/services/notification.service';
import { MaterialModule } from '../../../shared/material.module';
import { CreateApplicationDialogComponent } from '../create-application-dialog/create-application-dialog.component';

@Component({
  selector: 'app-application-list',
  standalone: true,
  imports: [CommonModule, MaterialModule, RouterModule],
  templateUrl: './application-list.component.html',
  styleUrl: './application-list.component.css',
})
export class ApplicationListComponent implements OnInit {
  applications: Application[] = [];
  loading = false;
  displayedColumns: string[] = [
    'id',
    'name',
    'ownerTeam',
    'repoUrl',
    'createdAt',
    'actions',
  ];

  constructor(
    private applicationService: ApplicationService,
    private notificationService: NotificationService,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.loadApplications();
  }

  loadApplications(): void {
    this.loading = true;
    this.applicationService.getApplications().subscribe({
      next: (data) => {
        this.applications = data;
        this.loading = false;
      },
      error: (error) => {
        console.error('Erro ao carregar applications:', error);
        this.loading = false;
      },
    });
  }

  openCreateDialog(): void {
    const dialogRef = this.dialog.open(CreateApplicationDialogComponent, {
      width: '600px',
      disableClose: false,
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.loadApplications();
      }
    });
  }
}
