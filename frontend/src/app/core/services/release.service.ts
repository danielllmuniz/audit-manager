import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map, tap } from 'rxjs';
import { environment } from '../../../environments/environment';
import {
  ApprovalRequest,
  CreateReleaseRequest,
  PromoteReleaseResponse,
  Release,
} from '../models';
import { Environment, ReleaseStatus } from '../models/enums';

export interface ReleaseFilters {
  env?: Environment;
  applicationId?: number;
  version?: string;
  status?: ReleaseStatus;
}

interface ReleaseListResponse {
  data: Release[];
}

interface ReleaseResponse {
  data: Release;
}

@Injectable({
  providedIn: 'root',
})
export class ReleaseService {
  private apiUrl = `${environment.apiUrl}/api/v1/audit/releases`;

  constructor(private http: HttpClient) {}

  getReleases(filters?: ReleaseFilters): Observable<Release[]> {
    let params = new HttpParams();

    if (filters) {
      if (filters.env) {
        params = params.set('env', filters.env);
      }
      if (filters.applicationId) {
        params = params.set('applicationId', filters.applicationId.toString());
      }
      if (filters.version) {
        params = params.set('version', filters.version);
      }
      if (filters.status) {
        params = params.set('status', filters.status);
      }
    }

    return this.http.get<ReleaseListResponse>(this.apiUrl, { params }).pipe(
      map((response) => {
        const releases = response.data
          ? response.data.map((r) => this.mapRelease(r))
          : [];
        return releases;
      }),
      tap((data) => console.log('Releases received:', data))
    );
  }

  getReleaseById(id: number): Observable<Release> {
    return this.http
      .get<ReleaseResponse>(`${this.apiUrl}/${id}`)
      .pipe(map((response) => this.mapRelease(response.data)));
  }

  createRelease(request: CreateReleaseRequest): Observable<Release> {
    console.log('Creating release:', request);
    return this.http.post<ReleaseResponse>(this.apiUrl, request).pipe(
      map((response) => this.mapRelease(response.data)),
      tap((data) => console.log('Release created:', data))
    );
  }

  approveRelease(id: number, request: ApprovalRequest): Observable<Release> {
    return this.http
      .post<ReleaseResponse>(`${this.apiUrl}/${id}/approve`, request)
      .pipe(map((response) => this.mapRelease(response.data)));
  }

  disapproveRelease(id: number, request: ApprovalRequest): Observable<Release> {
    return this.http
      .post<ReleaseResponse>(`${this.apiUrl}/${id}/disapprove`, request)
      .pipe(map((response) => this.mapRelease(response.data)));
  }

  promoteRelease(id: number): Observable<PromoteReleaseResponse> {
    return this.http.post<any>(`${this.apiUrl}/${id}/promote`, {}).pipe(
      map((response) => {
        if (response.data) {
          return {
            success: true,
            message: 'Release promovido com sucesso',
            release: this.mapRelease(response.data),
          };
        }
        return response;
      })
    );
  }

  downloadEvidence(evidenceUrl: string): Observable<Blob> {
    const url = evidenceUrl.startsWith('http')
      ? evidenceUrl
      : `${environment.apiUrl}/api/v1${evidenceUrl}`;

    return this.http.get(url, {
      responseType: 'blob'
    });
  }

  private mapRelease(release: Release): Release {
    return {
      ...release,
      id: release.release_id,
      releaseId: release.release_id,
      applicationId: release.application_id,
      evidenceUrl: release.evidence_url,
      createdAt: release.created_at ? new Date(release.created_at) : undefined,
      deployedAt: release.deployed_at
        ? new Date(release.deployed_at)
        : undefined,
      applicationName: release.application_name,
    };
  }
}
