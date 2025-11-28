import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { finalize } from 'rxjs/operators';
import { ProfileService, Post } from '../../services/profile.service';
import { AuthService, User } from '../../services/auth.service';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-feed',
  imports: [RouterModule, CommonModule, FormsModule],
  templateUrl: './feed.html',
  styleUrl: './feed.css',
})
export class FeedComponent implements OnInit {
  currentUser: User | null = null;
  posts: Post[] = [];
  isLoading: boolean = false;

  // New Post
  newPostContent: string = '';
  selectedMedia: File | null = null;
  mediaPreview: string | null = null;
  isPosting: boolean = false;

  constructor(
    private profileService: ProfileService,
    private authService: AuthService,
    private apiService: ApiService,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit() {
    this.authService.currentUser.subscribe(user => {
      this.currentUser = user;
    });
    this.loadFeed();
  }

  loadFeed() {
    this.isLoading = true;
    this.apiService.get<Post[]>('/feed').pipe(
      finalize(() => {
        this.isLoading = false;
        this.cdr.detectChanges();
      })
    ).subscribe({
      next: (posts) => {
        this.posts = posts;
      },
      error: (err) => console.error('Error loading feed:', err)
    });
  }

  triggerFileInput(type: 'image' | 'video') {
    const fileInput = document.getElementById('feed-media-input') as HTMLInputElement;
    if (fileInput) {
      fileInput.accept = type === 'video' ? 'video/*' : 'image/*';
      fileInput.click();
    }
  }

  onMediaSelect(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const file = input.files[0];
      this.selectedMedia = file;

      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        this.mediaPreview = e.target?.result as string;
        this.cdr.detectChanges();
      };
      reader.readAsDataURL(file);
    }
  }

  removeMedia() {
    this.selectedMedia = null;
    this.mediaPreview = null;
    const fileInput = document.getElementById('feed-media-input') as HTMLInputElement;
    if (fileInput) {
      fileInput.value = '';
    }
  }

  createPost() {
    if (!this.newPostContent && !this.selectedMedia) return;
    if (!this.currentUser) return;

    this.isPosting = true;
    const type = this.selectedMedia?.type.startsWith('video') ? 'video' : (this.selectedMedia ? 'image' : 'text');

    this.profileService.createPost(this.currentUser.id, this.newPostContent, type, this.selectedMedia || undefined)
      .pipe(finalize(() => {
        this.isPosting = false;
        this.cdr.detectChanges();
      }))
      .subscribe({
        next: (post) => {
          this.posts.unshift(post);
          this.newPostContent = '';
          this.removeMedia();
        },
        error: (err) => console.error('Error creating post:', err)
      });
  }
}
