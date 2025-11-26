import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class ApiService {
    private baseUrl: string = 'http://192.168.1.4:8000';

    constructor(private http: HttpClient) { }

    get<T>(endpoint: string): Observable<T> {
        console.log(`[ApiService] GET request to ${endpoint}`);
        return this.http.get<T>(`${this.baseUrl}${endpoint}`).pipe(
            tap({
                next: () => console.log(`[ApiService] GET ${endpoint} completed`),
                error: (err) => console.error(`[ApiService] GET ${endpoint} failed`, err)
            })
        );
    }

    post<T>(endpoint: string, data: any): Observable<T> {
        console.log(`[ApiService] POST request to ${endpoint}`);
        return this.http.post<T>(`${this.baseUrl}${endpoint}`, data).pipe(
            tap({
                next: () => console.log(`[ApiService] POST ${endpoint} completed`),
                error: (err) => console.error(`[ApiService] POST ${endpoint} failed`, err)
            })
        );
    }

    put<T>(endpoint: string, data: any): Observable<T> {
        console.log(`[ApiService] PUT request to ${endpoint}`);
        return this.http.put<T>(`${this.baseUrl}${endpoint}`, data).pipe(
            tap({
                next: () => console.log(`[ApiService] PUT ${endpoint} completed`),
                error: (err) => console.error(`[ApiService] PUT ${endpoint} failed`, err)
            })
        );
    }

    delete<T>(endpoint: string): Observable<T> {
        console.log(`[ApiService] DELETE request to ${endpoint}`);
        return this.http.delete<T>(`${this.baseUrl}${endpoint}`).pipe(
            tap({
                next: () => console.log(`[ApiService] DELETE ${endpoint} completed`),
                error: (err) => console.error(`[ApiService] DELETE ${endpoint} failed`, err)
            })
        );
    }

    uploadFile<T>(endpoint: string, file: File, fieldName: string = 'file'): Observable<T> {
        console.log(`[ApiService] Upload request to ${endpoint}`);
        const formData = new FormData();
        formData.append(fieldName, file);

        return this.http.post<T>(`${this.baseUrl}${endpoint}`, formData).pipe(
            tap({
                next: () => console.log(`[ApiService] Upload ${endpoint} completed`),
                error: (err) => console.error(`[ApiService] Upload ${endpoint} failed`, err)
            })
        );
    }

    getTrainingVideos(): Observable<any[]> {
        return this.get<any[]>('/training/videos');
    }

    addTrainingVideo(formData: FormData): Observable<any> {
        return this.http.post<any>(`${this.baseUrl}/training/videos`, formData).pipe(
            tap({
                next: () => console.log(`[ApiService] Add training video completed`),
                error: (err) => console.error(`[ApiService] Add training video failed`, err)
            })
        );
    }
}
