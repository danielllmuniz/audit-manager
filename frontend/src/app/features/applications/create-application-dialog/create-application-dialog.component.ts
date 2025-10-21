import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { CreateApplicationRequest } from '../../../core/models';
import { ApplicationService } from '../../../core/services/application.service';
import { NotificationService } from '../../../core/services/notification.service';
import { MaterialModule } from '../../../shared/material.module';

@Component({
  selector: 'app-create-application-dialog',
  standalone: true,
  imports: [CommonModule, MaterialModule, ReactiveFormsModule],
  templateUrl: './create-application-dialog.component.html',
  styleUrl: './create-application-dialog.component.css',
})
export class CreateApplicationDialogComponent {
  applicationForm: FormGroup;
  saving = false;

  constructor(
    private fb: FormBuilder,
    private applicationService: ApplicationService,
    private notificationService: NotificationService,
    private dialogRef: MatDialogRef<CreateApplicationDialogComponent>
  ) {
    this.applicationForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      ownerTeam: ['', [Validators.required]],
      repoUrl: [
        '',
        [Validators.required, Validators.pattern(/^https?:\/\/.+/)],
      ],
    });
  }

  onSubmit(): void {
    if (this.applicationForm.invalid) {
      this.applicationForm.markAllAsTouched();
      return;
    }

    this.saving = true;

    const request: CreateApplicationRequest = {
      name: this.applicationForm.value.name,
      owner_team: this.applicationForm.value.ownerTeam,
      repo_url: this.applicationForm.value.repoUrl,
    };

    this.applicationService.createApplication(request).subscribe({
      next: (application) => {
        this.notificationService.showSuccess(
          `Application "${application.name}" created successfully!`
        );
        this.dialogRef.close(true);
      },
      error: (error) => {
        console.error('Error creating application:', error);
        this.saving = false;
      },
    });
  }
}
