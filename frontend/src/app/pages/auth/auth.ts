import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-auth',
  imports: [],
  templateUrl: './auth.html',
  styleUrl: './auth.css',
})
export class AuthComponent {
  constructor(private router: Router) { }

  login() {
    // Mock login - navigate to app shell
    this.router.navigate(['/app']);
  }
}
