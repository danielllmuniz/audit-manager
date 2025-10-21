import { CommonModule } from '@angular/common';
import { Component, Inject, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Application, CreateReleaseRequest } from '../../../core/models';
import { NotificationService } from '../../../core/services/notification.service';
import { ReleaseService } from '../../../core/services/release.service';
import { MaterialModule } from '../../../shared/material.module';

@Component({
  selector: 'app-create-release-dialog',
  standalone: true,
  imports: [CommonModule, MaterialModule, ReactiveFormsModule],
  templateUrl: './create-release-dialog.component.html',
  styleUrl: './create-release-dialog.component.css',
})
export class CreateReleaseDialogComponent implements OnInit {
  releaseForm: FormGroup;
  saving = false;
  applications: Application[] = [];

  constructor(
    private fb: FormBuilder,
    private releaseService: ReleaseService,
    private notificationService: NotificationService,
    private dialogRef: MatDialogRef<CreateReleaseDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { applications: Application[] }
  ) {
    this.applications = data.applications || [];

    this.releaseForm = this.fb.group({
      applicationId: [null, [Validators.required]],
      version: [
        '',
        [Validators.required, Validators.pattern(/^v?\d+\.\d+\.\d+.*$/)],
      ],
    });
  }

  ngOnInit(): void {
    // Se houver apenas uma application, pré-seleciona
    if (this.applications.length === 1) {
      this.releaseForm.patchValue({
        applicationId:
          this.applications[0].id || this.applications[0].application_id,
      });
    }
  }

  onSubmit(): void {
    if (this.releaseForm.invalid) {
      this.releaseForm.markAllAsTouched();
      return;
    }

    this.saving = true;

    const request: CreateReleaseRequest = {
      application_id: this.releaseForm.value.applicationId,
      version: this.releaseForm.value.version,
    };

    this.releaseService.createRelease(request).subscribe({
      next: (release) => {
        this.notificationService.showSuccess(
          `Release ${release.version} created successfully! Status: ${release.status}`
        );
        this.dialogRef.close(true);
      },
      error: (error) => {
        console.error('Error creating release:', error);
        this.saving = false;
      },
    });
  }
}
