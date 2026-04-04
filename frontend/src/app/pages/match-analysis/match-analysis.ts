import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';

interface AnalysisIssue {
    title: string;
    severity: 'Critical' | 'High' | 'Medium' | 'Low' | 'Positive';
    timestamp: string;
    description: string;
    recommendation: string;
    category: 'footwork' | 'technique' | 'positioning' | 'tactical' | 'physical';
    confidence?: 'High' | 'Medium' | 'Low';
    player?: string;
}

interface TopRecommendation {
    category: string;
    issue: string;
    recommendation: string;
    priority: number;
}

interface AnalysisResult {
    score: number;
    summary: string;
    footworkScore: number;
    techniqueScore: number;
    positioningScore: number;
    tacticalScore: number;
    physicalScore: number;
    issues: AnalysisIssue[];
    topRecommendations?: TopRecommendation[];
    framesAnalyzed?: number;
    issuesFound?: number;
}

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
    analysisStep = 'Initializing AI Analysis Engine...';
    videoDuration = 0;
    videoName = '';

    analysisResults: AnalysisResult = {
        score: 0,
        summary: '',
        footworkScore: 0,
        techniqueScore: 0,
        positioningScore: 0,
        tacticalScore: 0,
        physicalScore: 0,
        issues: [],
        topRecommendations: []
    };





    constructor(
        private cdr: ChangeDetectorRef,
        private apiService: ApiService
    ) { }

    onFileSelected(event: any) {
        this.selectedFile = event.target.files[0];
        if (this.selectedFile) {
            this.videoName = this.selectedFile.name;
            // Get actual video duration
            this.getVideoDuration(this.selectedFile).then(duration => {
                this.videoDuration = duration;
                console.log(`Video duration: ${duration} seconds`);
                this.startRealAnalysis();
            });
        }
    }

    private getVideoDuration(file: File): Promise<number> {
        return new Promise((resolve) => {
            const video = document.createElement('video');
            video.preload = 'metadata';

            video.onloadedmetadata = () => {
                window.URL.revokeObjectURL(video.src);
                const duration = Math.floor(video.duration);
                resolve(duration > 0 ? duration : 180); // Default to 3 min if can't read
            };

            video.onerror = () => {
                resolve(180); // Default to 3 minutes on error
            };

            video.src = URL.createObjectURL(file);
        });
    }

    startRealAnalysis() {
        if (!this.selectedFile) return;

        this.isUploading = true;
        this.isAnalyzing = true;
        this.analysisStep = 'Uploading & Analyzing with LLaVA (this may take a minute)...';
        this.uploadProgress = 0;
        this.analysisProgress = 0;

        // Simulate progress while waiting for real response
        const progressInterval = setInterval(() => {
            if (this.uploadProgress < 90) {
                this.uploadProgress += 1;
                this.analysisProgress = this.uploadProgress;
                this.cdr.detectChanges();
            }
        }, 500);

        this.apiService.uploadFile<AnalysisResult>('/training/analyze-video', this.selectedFile)
            .subscribe({
                next: (result) => {
                    clearInterval(progressInterval);
                    this.uploadProgress = 100;
                    this.analysisProgress = 100;
                    this.isUploading = false;
                    this.isAnalyzing = false;
                    this.analysisComplete = true;

                    // Assign results
                    this.analysisResults = result;
                    this.cdr.detectChanges();
                    console.log('Analysis result:', result);
                },
                error: (err) => {
                    clearInterval(progressInterval);
                    console.error('Analysis failed:', err);
                    this.isUploading = false;
                    this.isAnalyzing = false;
                    this.analysisStep = 'Analysis Failed. Please try again.';
                    alert('Failed to analyze video. Ensure Ollama is running.');
                    this.cdr.detectChanges();
                }
            });
    }



    getSeverityClass(severity: string): string {
        switch (severity) {
            case 'Critical': return 'severity-critical';
            case 'High': return 'severity-high';
            case 'Medium': return 'severity-medium';
            case 'Low': return 'severity-low';
            case 'Positive': return 'severity-positive';
            default: return '';
        }
    }

    resetAnalysis() {
        this.selectedFile = null;
        this.analysisComplete = false;
        this.uploadProgress = 0;
        this.analysisProgress = 0;
        this.analysisStep = 'Initializing Gemini 3 AI Model...';
    }
}
