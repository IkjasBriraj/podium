import { Directive, ElementRef, HostListener, Renderer2 } from '@angular/core';

@Directive({
  selector: '[appRipple]',
  standalone: true
})
export class RippleDirective {
  constructor(private el: ElementRef, private renderer: Renderer2) {
    // Ensure the host acts as the absolute positioning boundary
    this.renderer.setStyle(this.el.nativeElement, 'position', 'relative');
    this.renderer.setStyle(this.el.nativeElement, 'overflow', 'hidden');
  }

  @HostListener('mousedown', ['$event'])
  onClick(event: MouseEvent) {
    const circle = this.renderer.createElement('span');
    const diameter = Math.max(this.el.nativeElement.clientWidth, this.el.nativeElement.clientHeight);
    const radius = diameter / 2;
    const rect = this.el.nativeElement.getBoundingClientRect();
    
    this.renderer.setStyle(circle, 'width', `${diameter}px`);
    this.renderer.setStyle(circle, 'height', `${diameter}px`);
    this.renderer.setStyle(circle, 'left', `${event.clientX - rect.left - radius}px`);
    this.renderer.setStyle(circle, 'top', `${event.clientY - rect.top - radius}px`);
    this.renderer.addClass(circle, 'water-ripple');

    this.renderer.appendChild(this.el.nativeElement, circle);

    // Remove the ripple element after animation completes
    setTimeout(() => {
      try {
        this.renderer.removeChild(this.el.nativeElement, circle);
      } catch (e) {
        // Ignored if element was already removed
      }
    }, 800);
  }
}
