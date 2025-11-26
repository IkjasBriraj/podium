import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
    selector: 'app-match-analysis',
    imports: [CommonModule, FormsModule],
    templateUrl: './match-analysis.html',
    styleUrl: './match-analysis.css',
})
export class MatchAnalysisComponent {
    isUploading = false;
    isAnalyzing = false;
    analysisComplete = false;
    selectedFile: File | null = null;
    uploadProgress = 0;
    analysisProgress = 0;
    analysisStep = 'Initializing Gemini 3 AI Model...';

    analysisResults = {
        score: 78,
        summary: "Good overall performance, but footwork efficiency needs improvement during rear-court transitions.",
        issues: [
            {
                title: 'Slow Rear Court Recovery',
                severity: 'High',
                timestamp: '00:45',
                description: 'Recovery to center after smash is 0.5s slower than optimal. Try to split-step immediately after landing.',
                recommendation: 'Practice "China Jump" drills.'
            },
            {
                title: 'Smash Angle Too Flat',
                severity: 'Medium',
                timestamp: '01:12',
                description: 'Smash trajectory is -5 degrees. Optimal is -12 to -15 degrees for this position.',
                recommendation: 'Contact the shuttle higher and further in front of your body.'
            },
            {
                title: 'Good Net Play',
                severity: 'Low', // Actually a positive
                timestamp: '02:30',
                description: 'Excellent tumbling net shot execution. Spin rate is high.',
                recommendation: 'Maintain this technique.'
            }
        ]
    };

    constructor(private cdr: ChangeDetectorRef) { }

    onFileSelected(event: any) {
        this.selectedFile = event.target.files[0];
        if (this.selectedFile) {
            this.simulateUpload();
        }
    }

    simulateUpload() {
        this.isUploading = true;
        let progress = 0;
        console.log('Starting upload simulation...');

        const interval = setInterval(() => {
            progress += 5;
            this.uploadProgress = progress;
            this.cdr.detectChanges(); // Force UI update

            if (progress >= 100) {
                clearInterval(interval);
                this.isUploading = false;
                this.startAnalysis();
            }
        }, 100);
    }

    startAnalysis() {
        this.isAnalyzing = true;
        let progress = 0;
        const steps = [
            'Initializing Gemini 3 AI Model...',
            'Detecting Player Skeleton...',
            'Analyzing Footwork Patterns...',
            'Calculating Shot Trajectories...',
            'Generating Tactical Insights...',
            'Finalizing Report...'
        ];

        const interval = setInterval(() => {
            progress += 2;
            this.analysisProgress = progress;

            // Update step text based on progress
            const stepIndex = Math.floor((progress / 100) * steps.length);
            if (stepIndex < steps.length) {
                this.analysisStep = steps[stepIndex];
            }

            this.cdr.detectChanges(); // Force UI update

            if (progress >= 100) {
                clearInterval(interval);
                this.isAnalyzing = false;
                this.analysisComplete = true;
                this.cdr.detectChanges();
            }
        }, 150);
    }

    resetAnalysis() {
        this.selectedFile = null;
        this.analysisComplete = false;
        this.uploadProgress = 0;
        this.analysisProgress = 0;
    }
}
