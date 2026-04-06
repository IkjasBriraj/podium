import { Component, OnDestroy, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { interval, Subject, Subscription } from 'rxjs';
import { takeWhile } from 'rxjs/operators';

export enum DrillState {
    IDLE = 'IDLE',
    RUNNING = 'RUNNING',
    RESTING = 'RESTING',
    PAUSED = 'PAUSED',
    COMPLETED = 'COMPLETED',
}

interface Drill {
    id: string;
    name: string;
    workInterval: number; // seconds
    restInterval: number; // seconds
}

@Component({
    selector: 'app-digital-coach',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './digital-coach.html',
    styleUrl: './digital-coach.css'
})
export class DigitalCoachComponent implements OnDestroy, OnInit {
    drills: Drill[] = [
        { id: '6-corner', name: '6-Corner Ghosting', workInterval: 30, restInterval: 15 },
        { id: 'front-back', name: 'Front-Back Agility', workInterval: 20, restInterval: 10 },
        { id: 'defense', name: 'Rapid Defense Smashes', workInterval: 40, restInterval: 20 }
    ];

    selectedDrill: Drill = this.drills[0];
    totalDurationMinutes: number = 5; // Configurable
    
    // State machine
    state: DrillState = DrillState.IDLE;
    DrillState = DrillState; // Expose to template
    
    // Timer details
    totalTimeRemaining: number = 0;
    currentStageRemaining: number = 0;
    
    private timerSub?: Subscription;
    private synth = window.speechSynthesis;
    private previousState: DrillState = DrillState.IDLE;
    private clockSub?: Subscription;
    
    currentTime: Date = new Date();

    constructor(private cdr: ChangeDetectorRef) {}

    ngOnInit() {
        this.clockSub = interval(1000).subscribe(() => {
            this.currentTime = new Date();
            this.cdr.detectChanges();
        });
    }

    startDrill() {
        if (this.state === DrillState.PAUSED) {
            this.state = this.previousState !== DrillState.IDLE ? this.previousState : DrillState.RUNNING;
            this.startTimerLoop();
            return;
        }

        // Fresh Start
        if (!this.selectedDrill) return;
        
        this.totalTimeRemaining = this.totalDurationMinutes * 60;
        this.state = DrillState.RUNNING;
        this.currentStageRemaining = this.selectedDrill.workInterval;
        
        this.speak("Starting drill. Go!");
        this.startTimerLoop();
    }

    pauseDrill() {
        this.previousState = this.state;
        this.state = DrillState.PAUSED;
        if (this.timerSub) {
            this.timerSub.unsubscribe();
            this.timerSub = undefined;
        }
        if (this.synth) {
            this.synth.cancel(); // Stop talking immediately
        }
    }

    resetDrill() {
        this.state = DrillState.IDLE;
        if (this.timerSub) {
            this.timerSub.unsubscribe();
            this.timerSub = undefined;
        }
        if (this.synth) this.synth.cancel();
        this.totalTimeRemaining = 0;
        this.currentStageRemaining = 0;
    }

    private startTimerLoop() {
        if (this.timerSub) this.timerSub.unsubscribe();
        
        this.timerSub = interval(1000).pipe(
            takeWhile(() => this.state === DrillState.RUNNING || this.state === DrillState.RESTING)
        ).subscribe(() => {
            this.tick();
        });
    }

    private tick() {
        this.totalTimeRemaining--;
        this.currentStageRemaining--;
        this.cdr.detectChanges(); // Ensure UI binds properly

        // Check if entire drill is done
        if (this.totalTimeRemaining <= 0) {
            this.state = DrillState.COMPLETED;
            if (this.timerSub) this.timerSub.unsubscribe();
            this.speak("Drill completed. Great job!");
            return;
        }

        // Halfway point motivation only if more than 1 minute left
        if (this.totalTimeRemaining === Math.floor((this.totalDurationMinutes * 60) / 2)) {
            this.speak("Halfway there! Come on!");
        }

        // Change stages (Work <-> Rest)
        if (this.currentStageRemaining <= 0) {
            if (this.state === DrillState.RUNNING) {
                this.state = DrillState.RESTING;
                this.currentStageRemaining = this.selectedDrill.restInterval;
                this.speak("Rest.");
            } else {
                this.state = DrillState.RUNNING;
                this.currentStageRemaining = this.selectedDrill.workInterval;
                this.speak("Go!");
            }
        }
    }

    private speak(text: string) {
        if (!this.synth) return;
        try {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 1.1; // Slightly faster for coaching
            utterance.pitch = 1.0;
            this.synth.speak(utterance);
        } catch(e) {
            console.error("Speech Synthesis Failed:", e);
        }
    }

    formatTime(seconds: number): string {
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    }

    ngOnDestroy() {
        if (this.clockSub) this.clockSub.unsubscribe();
        if (this.timerSub) this.timerSub.unsubscribe();
        if (this.synth) this.synth.cancel(); // Stop talking
    }
}
