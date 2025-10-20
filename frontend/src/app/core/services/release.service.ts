import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
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

@Injectable({
  providedIn: 'root',
})
export class ReleaseService {
  private apiUrl = `${environment.apiUrl}/api/v1/releases`;

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

    return this.http.get<Release[]>(this.apiUrl, { params });
  }

  getReleaseById(id: number): Observable<Release> {
    return this.http.get<Release>(`${this.apiUrl}/${id}`);
  }

  createRelease(request: CreateReleaseRequest): Observable<Release> {
    return this.http.post<Release>(this.apiUrl, request);
  }

  approveRelease(id: number, request: ApprovalRequest): Observable<Release> {
    return this.http.post<Release>(`${this.apiUrl}/${id}/approve`, request);
  }

  disapproveRelease(id: number, request: ApprovalRequest): Observable<Release> {
    return this.http.post<Release>(`${this.apiUrl}/${id}/disapprove`, request);
  }

  promoteRelease(id: number): Observable<PromoteReleaseResponse> {
    return this.http.post<PromoteReleaseResponse>(
      `${this.apiUrl}/${id}/promote`,
      {}
    );
  }
}
