import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';

export interface Skill {
    name: string;
    endorsements: number;
}

export interface Experience {
    role: string;
    org: string;
    years: string;
    description?: string;
}

export interface Profile {
    id: string;
    name: string;
    role: string;
    sport: string;
    headline?: string;
    bio?: string;
    location?: string;
    category?: string;
    profile_image?: string;
    cover_image?: string;
    skills: Skill[];
    experience: Experience[];
}

export interface ProfileCreateRequest {
    name: string;
    role: string;
    sport: string;
    headline?: string;
    bio?: string;
    location?: string;
    category?: string;
}

export interface ProfileUpdateRequest {
    name?: string;
    headline?: string;
    bio?: string;
    location?: string;
    category?: string;
    role?: string;
    sport?: string;
}

export interface ImageUploadResponse {
    message: string;
    image_url: string;
}

export interface Post {
    id: string;
    author_id: string;
    content: string;
    media_url?: string;
    type: string;
    likes: number;
    comments: number;
}

@Injectable({
    providedIn: 'root'
})
export class ProfileService {

    constructor(private apiService: ApiService) { }

    getProfile(userId: string): Observable<Profile> {
        return this.apiService.get<Profile>(`/profiles/${userId}`);
    }

    createProfile(profile: ProfileCreateRequest): Observable<Profile> {
        return this.apiService.post<Profile>('/profiles', profile);
    }

    updateProfile(userId: string, profile: ProfileUpdateRequest): Observable<Profile> {
        return this.apiService.put<Profile>(`/profiles/${userId}`, profile);
    }

    uploadProfileImage(userId: string, file: File): Observable<ImageUploadResponse> {
        return this.apiService.uploadFile<ImageUploadResponse>(
            `/profiles/${userId}/image`,
            file
        );
    }

    uploadCoverImage(userId: string, file: File): Observable<ImageUploadResponse> {
        return this.apiService.uploadFile<ImageUploadResponse>(
            `/profiles/${userId}/cover`,
            file
        );
    }

    createPost(userId: string, content: string, type: string, file?: File): Observable<Post> {
        const formData = new FormData();
        formData.append('user_id', userId);
        formData.append('content', content);
        formData.append('type', type);
        if (file) {
            formData.append('file', file);
        }
        return this.apiService.post<Post>('/posts', formData);
    }

    getUserPosts(userId: string): Observable<Post[]> {
        return this.apiService.get<Post[]>(`/users/${userId}/posts`);
    }
}
