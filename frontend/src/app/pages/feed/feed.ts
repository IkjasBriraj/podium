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

  // Comments State
  expandedComments: Set<string> = new Set();
  postComments: { [postId: string]: any[] } = {};
  commentInputs: { [postId: string]: string } = {};
  loadingComments: Set<string> = new Set();

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
        this.posts = posts.map(p => ({ ...p, id: p.id || p._id! }));
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
          const newPost = { ...post, id: post.id || post._id! };
          this.posts.unshift(newPost);
          this.newPostContent = '';
          this.removeMedia();
        },
        error: (err) => console.error('Error creating post:', err)
      });
  }

  likePost(post: Post) {
    this.profileService.likePost(post.id).subscribe({
      next: (response) => {
        post.likes = response.likes;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Error liking post:', err);
        alert('Failed to like post. Please try again.');
      }
    });
  }

  toggleComments(post: Post) {
    if (this.expandedComments.has(post.id)) {
      this.expandedComments.delete(post.id);
    } else {
      this.expandedComments.add(post.id);
      if (!this.postComments[post.id]) {
        this.loadComments(post.id);
      }
    }
  }

  loadComments(postId: string) {
    this.loadingComments.add(postId);
    this.profileService.getComments(postId)
      .pipe(finalize(() => {
        this.loadingComments.delete(postId);
        this.cdr.detectChanges();
      }))
      .subscribe({
        next: (comments) => {
          this.postComments[postId] = comments;
        },
        error: (err) => console.error('Error loading comments:', err)
      });
  }

  submitComment(post: Post) {
    if (!this.currentUser) {
      alert('Please login to comment.');
      return;
    }
    const content = this.commentInputs[post.id];
    if (!content || !content.trim()) return;

    this.profileService.addComment(post.id, this.currentUser.id, content).subscribe({
      next: (comment) => {
        if (!this.postComments[post.id]) {
          this.postComments[post.id] = [];
        }
        this.postComments[post.id].push(comment);
        post.comments++; // Increment comment count locally
        this.commentInputs[post.id] = ''; // Clear input
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Error adding comment:', err);
        alert('Failed to post comment. Please try again.');
      }
    });
  }

  isCommentsExpanded(postId: string): boolean {
    return this.expandedComments.has(postId);
  }
}
