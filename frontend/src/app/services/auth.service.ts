import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Router } from '@angular/router';

export interface User {
    id: string;
    name: string;
    email: string;
    role: string;
    sport: string;
    profile_image?: string;
}

@Injectable({
    providedIn: 'root'
})
export class AuthService {
    private apiUrl = 'http://localhost:8000';
    private currentUserSubject: BehaviorSubject<User | null>;
    public currentUser: Observable<User | null>;

    constructor(
        private http: HttpClient,
        private router: Router
    ) {
        // Load user from localStorage if exists
        const storedUser = localStorage.getItem('currentUser');
        this.currentUserSubject = new BehaviorSubject<User | null>(
            storedUser ? JSON.parse(storedUser) : null
        );
        this.currentUser = this.currentUserSubject.asObservable();
    }

    public get currentUserValue(): User | null {
        return this.currentUserSubject.value;
    }

    public get isLoggedIn(): boolean {
        return !!this.currentUserSubject.value;
    }

    login(emailOrUsername: string, password: string): Observable<User> {
        // In a real app, this would call a backend login endpoint
        // For now, we'll fetch all users and find a match
        return this.http.get<any[]>(`${this.apiUrl}/users`).pipe(
            map(users => {
                // Find user by email or username
                const user = users.find(u =>
                    u.email === emailOrUsername || u.username === emailOrUsername
                );

                if (!user) {
                    throw new Error('User not found');
                }

                // In a real app, password would be validated on backend
                // For mock data, we're using password123 for all users
                // You would validate the hashed password here

                const mappedUser: User = {
                    id: user._id,
                    name: user.name,
                    email: user.email,
                    role: user.role,
                    sport: user.sport,
                    profile_image: user.profile_image
                };

                // Store user in localStorage
                localStorage.setItem('currentUser', JSON.stringify(mappedUser));
                this.currentUserSubject.next(mappedUser);

                return mappedUser;
            })
        );
    }

    logout(): void {
        // Remove user from localStorage
        localStorage.removeItem('currentUser');
        this.currentUserSubject.next(null);
        this.router.navigate(['/auth']);
    }

    getUserId(): string | null {
        return this.currentUserValue?.id || null;
    }
}
