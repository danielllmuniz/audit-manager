import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { NotificationService } from '../../../core/services/notification.service';
import { MaterialModule } from '../../../shared/material.module';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, MaterialModule, MatProgressBarModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
})
export class LoginComponent {
  loading = false;

  constructor(
    private authService: AuthService,
    private notificationService: NotificationService,
    private router: Router
  ) {
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/applications']);
    }
  }

  loginAs(role: 'dev' | 'approver' | 'devops'): void {
    this.loading = true;

    let loginObservable;

    switch (role) {
      case 'dev':
        loginObservable = this.authService.loginAsDev();
        break;
      case 'approver':
        loginObservable = this.authService.loginAsApprover();
        break;
      case 'devops':
        loginObservable = this.authService.loginAsDevOps();
        break;
    }

    loginObservable.subscribe({
      next: (response) => {
        const userName = response.data.attributes.user.name;
        const userRole = response.data.attributes.user.role;

        this.notificationService.showSuccess(
          `Bem-vindo, ${userName}! (${userRole})`
        );
        this.router.navigate(['/']);
      },
      error: (error) => {
        console.error('Erro no login:', error);
        this.loading = false;
      },
      complete: () => {
        this.loading = false;
      },
    });
  }
}
