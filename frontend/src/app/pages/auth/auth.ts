import { Component, AfterViewInit, NgZone, ChangeDetectorRef } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';
import { finalize } from 'rxjs/operators';

declare const google: any;

@Component({
  selector: 'app-auth',
  imports: [FormsModule, CommonModule],
  templateUrl: './auth.html',
  styleUrl: './auth.css',
})
export class AuthComponent implements AfterViewInit {
  email: string = '';
  password: string = '';
  errorMessage: string = '';
  isLoading: boolean = false;
  isGoogleLoading: boolean = false;

  private readonly GOOGLE_CLIENT_ID = '874807563899-6fv6stnt81m92cmm6fedocojj0748fd3.apps.googleusercontent.com';

  constructor(
    private authService: AuthService,
    private router: Router,
    private ngZone: NgZone,
    private cdr: ChangeDetectorRef
  ) { }

  ngAfterViewInit() {
    // Initialize Google Sign-In after view is ready
    this.initializeGoogleSignIn();
  }

  private initializeGoogleSignIn() {
    // Wait for Google script to load
    if (typeof google === 'undefined') {
      setTimeout(() => this.initializeGoogleSignIn(), 100);
      return;
    }

    google.accounts.id.initialize({
      client_id: this.GOOGLE_CLIENT_ID,
      callback: (response: any) => this.handleGoogleCallback(response)
    });

    google.accounts.id.renderButton(
      document.getElementById('google-signin-button'),
      {
        theme: 'filled_black',
        size: 'large',
        width: 320,
        text: 'signin_with',
        shape: 'rectangular'
      }
    );
  }

  private handleGoogleCallback(response: any) {
    // Use NgZone to run Angular change detection
    this.ngZone.run(() => {
      this.isGoogleLoading = true;
      this.errorMessage = '';

      this.authService.loginWithGoogle(response.credential).subscribe({
        next: (user) => {
          console.log('Google login successful', user);
          this.router.navigate(['/app/feed']);
        },
        error: (error) => {
          console.error('Google login failed', error);
          this.errorMessage = 'Google sign-in failed. Please try again.';
          this.isGoogleLoading = false;
        },
        complete: () => {
          this.isGoogleLoading = false;
        }
      });
    });
  }

  login() {
    if (!this.email || !this.password) {
      this.errorMessage = 'Please enter email and password';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    this.authService.login(this.email, this.password)
    .pipe(finalize(() => {
        this.isLoading = false;
        this.cdr.detectChanges();
    }))
    .subscribe({
      next: (user) => {
        console.log('Login successful', user);
        this.router.navigate(['/app/feed']);
      },
      error: (error) => {
        console.error('Login failed', error);
        this.errorMessage = 'Invalid email or password. Try password123 for any user.';
      }
    });
  }
}
