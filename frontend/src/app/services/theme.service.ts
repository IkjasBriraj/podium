import { Injectable, signal, effect } from '@angular/core';

export type Theme = 'light' | 'dark' | 'glass';

@Injectable({
    providedIn: 'root'
})
export class ThemeService {
    private readonly STORAGE_KEY = 'podium-theme';

    // Using signal for reactive state management
    currentTheme = signal<Theme>(this.getStoredTheme());

    constructor() {
        // Apply theme on initialization
        this.applyTheme(this.currentTheme());

        // Set up effect to apply theme whenever it changes
        effect(() => {
            this.applyTheme(this.currentTheme());
        });
    }

    private getStoredTheme(): Theme {
        if (typeof window !== 'undefined') {
            const stored = localStorage.getItem(this.STORAGE_KEY) as Theme;
            if (stored === 'light' || stored === 'dark' || stored === 'glass') {
                return stored;
            }
            // Check system preference
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
                return 'light';
            }
        }
        return 'dark'; // Default to dark
    }

    setTheme(theme: Theme): void {
        this.currentTheme.set(theme);
        if (typeof window !== 'undefined') {
            localStorage.setItem(this.STORAGE_KEY, theme);
        }
    }

    toggleTheme(): void {
        const themes: Theme[] = ['dark', 'light', 'glass'];
        const currentIndex = themes.indexOf(this.currentTheme());
        const nextIndex = (currentIndex + 1) % themes.length;
        this.setTheme(themes[nextIndex]);
    }

    private applyTheme(theme: Theme): void {
        if (typeof document !== 'undefined') {
            document.documentElement.setAttribute('data-theme', theme);
            document.body.classList.remove('light-theme', 'dark-theme', 'glass-theme');
            document.body.classList.add(`${theme}-theme`);
        }
    }

    isDarkMode(): boolean {
        return this.currentTheme() === 'dark';
    }

    isGlassMode(): boolean {
        return this.currentTheme() === 'glass';
    }
}
