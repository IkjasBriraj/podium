import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../../../services/auth.service';

export interface Racket {
  id: string;
  brand: string;
  model: string;
  stringType: string;
  tension: number;
  tensionUnit: 'lbs' | 'kg';
  lastStringingDate: string;
}

@Component({
  selector: 'app-gear-manager',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './gear-manager.html',
})
export class GearManagerComponent implements OnInit {
  rackets: Racket[] = [];

  showAddForm = false;
  userId: string | null = null;

  constructor(private authService: AuthService) {}

  ngOnInit() {
      this.userId = this.authService.getUserId();
      if (this.userId) {
          const saved = localStorage.getItem(`podium_gear_${this.userId}`);
          if (saved) {
              this.rackets = JSON.parse(saved);
          } else {
              // Default mock data if empty
              this.rackets = [
                  {
                    id: 'r1', brand: 'Yonex', model: 'Astrox 99 Pro',
                    stringType: 'BG80 Power', tension: 28, tensionUnit: 'lbs',
                    lastStringingDate: '2025-11-15'
                  }
              ];
          }
      }
  }

  private saveToStorage() {
      if (this.userId) {
          localStorage.setItem(`podium_gear_${this.userId}`, JSON.stringify(this.rackets));
      }
  }
  
  newRacket: Racket = {
    id: '',
    brand: '',
    model: '',
    stringType: '',
    tension: 24,
    tensionUnit: 'lbs',
    lastStringingDate: new Date().toISOString().split('T')[0]
  };

  needsRestringing(dateString: string): boolean {
    const stringDate = new Date(dateString);
    const now = new Date();
    const diffInDays = Math.floor((now.getTime() - stringDate.getTime()) / (1000 * 60 * 60 * 24));
    return diffInDays > 90;
  }

  getDaysElapsed(dateString: string): number {
    const stringDate = new Date(dateString);
    const now = new Date();
    return Math.floor((now.getTime() - stringDate.getTime()) / (1000 * 60 * 60 * 24));
  }

  addRacket() {
    if (!this.newRacket.model || !this.newRacket.stringType) return;
    
    this.rackets.push({
      ...this.newRacket,
      id: Math.random().toString(36).substr(2, 9)
    });
    
    // Reset
    this.newRacket = {
      id: '', brand: '', model: '', stringType: '', tension: 24, tensionUnit: 'lbs', 
      lastStringingDate: new Date().toISOString().split('T')[0]
    };
    this.showAddForm = false;
    this.saveToStorage();
  }

  deleteRacket(id: string) {
    this.rackets = this.rackets.filter(r => r.id !== id);
    this.saveToStorage();
  }
}
