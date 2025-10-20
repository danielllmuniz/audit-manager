import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map, tap } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Application, CreateApplicationRequest } from '../models';

interface ApplicationListResponse {
  data: Application[];
}

interface ApplicationResponse {
  data: Application;
}

@Injectable({
  providedIn: 'root',
})
export class ApplicationService {
  private apiUrl = `${environment.apiUrl}/api/v1/applications`;

  constructor(private http: HttpClient) {
    console.log('ApplicationService initialized. API URL:', this.apiUrl);
  }

  getApplications(): Observable<Application[]> {
    console.log('=== Getting Applications ===');
    console.log('URL:', this.apiUrl);

    return this.http.get<ApplicationListResponse>(this.apiUrl).pipe(
      map((response) => {
        // Extrair o array de dentro de 'data'
        const applications = response.data.map((app) =>
          this.mapApplication(app)
        );
        return applications;
      }),
      tap({
        next: (data) => {
          console.log('Applications received:', data);
          console.log('Number of applications:', data.length);
        },
        error: (error) => {
          console.error('Error getting applications:', error);
        },
      })
    );
  }

  getApplicationById(id: number): Observable<Application> {
    return this.http
      .get<ApplicationResponse>(`${this.apiUrl}/${id}`)
      .pipe(map((response) => this.mapApplication(response.data)));
  }

  createApplication(
    request: CreateApplicationRequest
  ): Observable<Application> {
    console.log('=== Creating Application ===');
    console.log('Request:', request);

    return this.http.post<ApplicationResponse>(this.apiUrl, request).pipe(
      map((response) => this.mapApplication(response.data)),
      tap({
        next: (data) => {
          console.log('Application created:', data);
        },
        error: (error) => {
          console.error('Error creating application:', error);
        },
      })
    );
  }

  // Método auxiliar para mapear os campos snake_case para camelCase
  private mapApplication(app: Application): Application {
    return {
      ...app,
      id: app.application_id,
      ownerTeam: app.owner_team,
      repoUrl: app.repo_url,
      createdAt: app.created_at ? new Date(app.created_at) : undefined,
    };
  }
}
