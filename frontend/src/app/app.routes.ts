import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { ApplicationDetailComponent } from './features/applications/application-detail/application-detail.component';
import { ApplicationListComponent } from './features/applications/application-list/application-list.component';
import { LoginComponent } from './features/auth/login/login.component';
import { ReleaseListComponent } from './features/releases/release-list/release-list.component';
import { LayoutComponent } from './shared/layout/layout.component';

export const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent,
  },
  {
    path: '',
    component: LayoutComponent,
    canActivate: [authGuard],
    children: [
      {
        path: '',
        redirectTo: 'applications',
        pathMatch: 'full',
      },
      {
        path: 'applications',
        component: ApplicationListComponent,
      },
      {
        path: 'applications/:id',
        component: ApplicationDetailComponent,
      },
      {
        path: 'releases',
        component: ReleaseListComponent,
      },
    ],
  },
  {
    path: '**',
    redirectTo: 'login',
  },
];
