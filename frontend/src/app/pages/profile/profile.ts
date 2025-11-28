import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { finalize, timeout } from 'rxjs/operators';
import { FormBuilder, FormGroup, FormArray, Validators, ReactiveFormsModule, FormsModule } from '@angular/forms';
import { ProfileService, Profile, ProfileUpdateRequest, Post } from '../../services/profile.service';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-profile',
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  templateUrl: './profile.html',
  styleUrl: './profile.css',
})
export class ProfileComponent implements OnInit {
  profile: Profile | null = null;
  isEditing: boolean = false;
  isLoading: boolean = false;
  error: string | null = null;
  profileForm: FormGroup;
  currentUserId: string | null = null;

  profileImagePreview: string | null = null;
  coverImagePreview: string | null = null;
  selectedProfileImage: File | null = null;
  selectedCoverImage: File | null = null;

  // Posts
  posts: Post[] = [];
  newPostContent: string = '';
  selectedMedia: File | null = null;
  mediaPreview: string | null = null;
  isPosting: boolean = false;

  constructor(
    private profileService: ProfileService,
    private authService: AuthService,
    private fb: FormBuilder,
    private cdr: ChangeDetectorRef,
    private sanitizer: DomSanitizer,
    private router: Router
  ) {
    this.profileForm = this.fb.group({
      name: ['', Validators.required],
      headline: [''],
      bio: [''],
      location: [''],
      category: [''],
      role: [''],
      sport: [''],
      // Sport-specific player information
      age: [null],
      weight: [''],
      height: [''],
      playing_hand: [''],
      years_of_experience: [null],
      age_category: [''],
      academy: [''],
      // Coach-specific information
      coaching_license: [''],
      coaching_experience_years: [null],
      coaching_specialization: [''],
      current_organization: [''],
      coaching_philosophy: [''],
      age_groups_coached: [''],
      coaching_achievements: [''],

      skills: this.fb.array([]),
      experience: this.fb.array([])
    });
  }

  ngOnInit() {
    // Get current user from auth service
    this.currentUserId = this.authService.getUserId();

    if (!this.currentUserId) {
      // No user logged in, redirect to auth
      this.router.navigate(['/auth']);
      return;
    }

    this.loadProfile();
    this.loadPosts();
  }

  loadProfile() {
    console.log('Loading profile for user:', this.currentUserId);
    this.isLoading = true;
    this.error = null;

    this.profileService.getProfile(this.currentUserId!).pipe(
      timeout(5000), // Timeout after 5 seconds
      finalize(() => {
        this.isLoading = false;
        console.log('Profile loading finalized');
        this.cdr.detectChanges();
      })
    ).subscribe({
      next: (profile: Profile) => {
        console.log('Profile loaded successfully:', profile);
        this.profile = profile;
        // Ensure skills and experience are always arrays
        this.profile.skills = this.profile.skills || [];
        this.profile.experience = this.profile.experience || [];
        this.populateForm(profile);
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Profile load error:', err);
        this.error = `Failed to load profile: ${err.message || 'Unknown error'}`;
      }
    });
  }

  populateForm(profile: Profile) {
    this.profileForm.patchValue({
      name: profile.name,
      headline: profile.headline || '',
      bio: profile.bio || '',
      location: profile.location || '',
      category: profile.category || '',
      role: profile.role,
      sport: profile.sport,
      // Sport-specific player information
      age: profile.age || null,
      weight: profile.weight || '',
      height: profile.height || '',
      playing_hand: profile.playing_hand || '',
      years_of_experience: profile.years_of_experience || null,
      age_category: profile.age_category || '',
      academy: profile.academy || '',
      // Coach fields
      coaching_license: profile.coaching_license || '',
      coaching_experience_years: profile.coaching_experience_years || null,
      coaching_specialization: profile.coaching_specialization || '',
      current_organization: profile.current_organization || '',
      coaching_philosophy: profile.coaching_philosophy || '',
      age_groups_coached: profile.age_groups_coached || '',
      coaching_achievements: profile.coaching_achievements || ''
    });

    // Populate Skills
    const skillFGs = (profile.skills || []).map(s => this.fb.group({
      name: [s.name, Validators.required],
      endorsements: [s.endorsements || 0]
    }));
    this.profileForm.setControl('skills', this.fb.array(skillFGs));

    // Populate Experience
    const expFGs = (profile.experience || []).map(e => this.fb.group({
      role: [e.role, Validators.required],
      org: [e.org, Validators.required],
      years: [e.years, Validators.required],
      description: [e.description || '']
    }));
    this.profileForm.setControl('experience', this.fb.array(expFGs));
  }

  toggleEditMode() {
    this.isEditing = !this.isEditing;
    if (!this.isEditing) {
      // Reset form if canceling
      if (this.profile) {
        this.populateForm(this.profile);
      }
      this.selectedProfileImage = null;
      this.selectedCoverImage = null;
      this.profileImagePreview = null;
      this.coverImagePreview = null;
    }
  }

  async saveProfile() {
    if (this.profileForm.invalid) {
      return;
    }

    this.isLoading = true;
    this.error = null;

    try {
      // Upload images first if selected
      if (this.selectedProfileImage) {
        await this.uploadProfileImage(this.selectedProfileImage);
      }

      if (this.selectedCoverImage) {
        await this.uploadCoverImage(this.selectedCoverImage);
      }

      // Update profile data
      const updateData: ProfileUpdateRequest = this.profileForm.value;

      this.profileService.updateProfile(this.currentUserId!, updateData).subscribe({
        next: (updatedProfile) => {
          this.profile = updatedProfile;
          this.isEditing = false;
          this.isLoading = false;
          this.selectedProfileImage = null;
          this.selectedCoverImage = null;
          this.profileImagePreview = null;
          this.coverImagePreview = null;
        },
        error: (err) => {
          this.error = 'Failed to update profile. Please try again.';
          console.error('Profile update error:', err);
          this.isLoading = false;
        }
      });
    } catch (err) {
      this.error = 'Failed to upload images. Please try again.';
      console.error('Image upload error:', err);
      this.isLoading = false;
    }
  }

  async onProfileImageChange(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const file = input.files[0];

      // Optimistic update / Preview
      const reader = new FileReader();
      reader.onload = (e) => {
        this.profileImagePreview = e.target?.result as string;
        this.cdr.detectChanges();
      };
      reader.readAsDataURL(file);

      try {
        await this.uploadProfileImage(file);
        // Clear preview after successful upload as the profile data is updated
        this.profileImagePreview = null;
        this.cdr.detectChanges();
      } catch (error) {
        console.error('Failed to upload profile image', error);
        alert('Failed to upload profile image');
        this.profileImagePreview = null; // Revert on error
        this.cdr.detectChanges();
      }
    }
  }

  onProfileImageSelect(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const file = input.files[0];
      this.selectedProfileImage = file;

      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        this.profileImagePreview = e.target?.result as string;
      };
      reader.readAsDataURL(file);
    }
  }

  async onCoverImageChange(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const file = input.files[0];

      // Optimistic update / Preview
      const reader = new FileReader();
      reader.onload = (e) => {
        this.coverImagePreview = e.target?.result as string;
        this.cdr.detectChanges();
      };
      reader.readAsDataURL(file);

      try {
        await this.uploadCoverImage(file);
        // Clear preview after successful upload as the profile data is updated
        this.coverImagePreview = null;
        this.cdr.detectChanges();
      } catch (error) {
        console.error('Failed to upload cover image', error);
        alert('Failed to upload cover image');
        this.coverImagePreview = null; // Revert on error
        this.cdr.detectChanges();
      }
    }
  }

  onCoverImageSelect(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      const file = input.files[0];
      this.selectedCoverImage = file;

      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        this.coverImagePreview = e.target?.result as string;
      };
      reader.readAsDataURL(file);
    }
  }

  uploadProfileImage(file: File): Promise<void> {
    return new Promise((resolve, reject) => {
      this.profileService.uploadProfileImage(this.currentUserId!, file).subscribe({
        next: (response) => {
          if (this.profile) {
            this.profile.profile_image = response.image_url;
          }
          resolve();
        },
        error: (err) => {
          reject(err);
        }
      });
    });
  }

  uploadCoverImage(file: File): Promise<void> {
    return new Promise((resolve, reject) => {
      this.profileService.uploadCoverImage(this.currentUserId!, file).subscribe({
        next: (response) => {
          if (this.profile) {
            this.profile.cover_image = response.image_url;
          }
          resolve();
        },
        error: (err) => {
          reject(err);
        }
      });
    });
  }

  getProfileImageUrl(): string {
    if (this.profileImagePreview) {
      return this.profileImagePreview;
    }
    if (this.profile?.profile_image) {
      return `${this.profile.profile_image}`;
    }
    return '';
  }

  getCoverImageUrl(): string {
    if (this.coverImagePreview) {
      return this.coverImagePreview;
    }
    if (this.profile?.cover_image) {
      return `${this.profile.cover_image}`;
    }
    return '';
  }

  // --- Posts ---

  loadPosts() {
    this.profileService.getUserPosts(this.currentUserId!).subscribe({
      next: (posts) => {
        this.posts = posts;
        this.cdr.detectChanges();
      },
      error: (err) => console.error('Error loading posts:', err)
    });
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

  createPost() {
    if (!this.newPostContent && !this.selectedMedia) return;

    this.isPosting = true;
    const type = this.selectedMedia?.type.startsWith('video') ? 'video' : (this.selectedMedia ? 'image' : 'text');

    this.profileService.createPost(this.currentUserId!, this.newPostContent, type, this.selectedMedia || undefined)
      .pipe(finalize(() => {
        this.isPosting = false;
        this.cdr.detectChanges();
      }))
      .subscribe({
        next: (post) => {
          this.posts.unshift(post);
          this.newPostContent = '';
          this.selectedMedia = null;
          this.mediaPreview = null;
          this.profileForm.get('newPostContent')?.reset(); // If using form control
          this.playSuccessSound();
        },
        error: (err) => {
          console.error('Error creating post:', err);
          alert('Failed to create post');
        }
      });
  }

  playSuccessSound() {
    const AudioContext = (window as any).AudioContext || (window as any).webkitAudioContext;
    if (!AudioContext) return;

    const ctx = new AudioContext();
    const oscillator = ctx.createOscillator();
    const gainNode = ctx.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(ctx.destination);

    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(500, ctx.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(1000, ctx.currentTime + 0.1);

    gainNode.gain.setValueAtTime(0.1, ctx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5);

    oscillator.start(ctx.currentTime);
    oscillator.stop(ctx.currentTime + 0.5);
  }

  getSafeUrl(url: string): SafeUrl {
    return this.sanitizer.bypassSecurityTrustUrl(url);
  }

  // --- Helper Methods for Form Arrays ---

  get experienceArray() {
    return this.profileForm.get('experience') as FormArray;
  }

  get skillsArray() {
    return this.profileForm.get('skills') as FormArray;
  }

  addExperience() {
    const expGroup = this.fb.group({
      role: ['', Validators.required],
      org: ['', Validators.required],
      years: ['', Validators.required],
      description: ['']
    });
    this.experienceArray.push(expGroup);
  }

  removeExperience(index: number) {
    this.experienceArray.removeAt(index);
  }

  addSkill() {
    const skillGroup = this.fb.group({
      name: ['', Validators.required],
      endorsements: [0]
    });
    this.skillsArray.push(skillGroup);
  }

  removeSkill(index: number) {
    this.skillsArray.removeAt(index);
  }
}
