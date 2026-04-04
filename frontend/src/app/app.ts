import { Component, signal, HostListener, Renderer2 } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');

  constructor(private renderer: Renderer2) {}

  @HostListener('document:mousedown', ['$event'])
  onGlobalClick(event: MouseEvent) {
    // Only spawn ripple on left clicks
    if (event.button !== 0) return;
    
    // Create ripple globally for the "liquid glass" water effect
    const theme = document.documentElement.getAttribute('data-theme') || 'glass';
    // If you only want this in glass theme, you can check it. (Assuming glass by default)
    if (theme && theme !== 'glass') return; 

    const circle = this.renderer.createElement('span');
    const diameter = 120; // Size for global water ripples
    const radius = diameter / 2;

    this.renderer.setStyle(circle, 'position', 'fixed');
    this.renderer.setStyle(circle, 'width', `${diameter}px`);
    this.renderer.setStyle(circle, 'height', `${diameter}px`);
    this.renderer.setStyle(circle, 'left', `${event.clientX - radius}px`);
    this.renderer.setStyle(circle, 'top', `${event.clientY - radius}px`);
    this.renderer.setStyle(circle, 'pointer-events', 'none');
    this.renderer.setStyle(circle, 'z-index', '9999');
    this.renderer.addClass(circle, 'water-ripple');

    this.renderer.appendChild(document.body, circle);

    setTimeout(() => {
      try {
        this.renderer.removeChild(document.body, circle);
      } catch (e) {}
    }, 800);
  }
}
