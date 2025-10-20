import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { ApplicationListComponent } from './features/applications/application-list/application-list.component';
import { LoginComponent } from './features/auth/login/login.component';
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
      // Releases - vamos adicionar no próximo passo
      // {
      //   path: 'releases',
      //   component: ReleaseListComponent
      // },
      // {
      //   path: 'releases/new',
      //   component: CreateReleaseComponent
      // }
    ],
  },
  {
    path: '**',
    redirectTo: 'login',
  },
];
