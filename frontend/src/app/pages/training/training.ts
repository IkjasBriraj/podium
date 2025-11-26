import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { SafePipe } from '../../pipes/safe.pipe';
import { ApiService } from '../../services/api.service';

@Component({
    selector: 'app-training',
    imports: [CommonModule, SafePipe, FormsModule],
    templateUrl: './training.html',
    styleUrl: './training.css',
})
export class TrainingComponent implements OnInit {
    constructor(
        private router: Router,
        private apiService: ApiService
    ) { }

    trainingCategories = [
        { title: 'Technique Drills', icon: '🏸', count: 24, route: 'technique' },
        { title: 'Footwork Training', icon: '👟', count: 18, route: 'footwork' },
        { title: 'Strength & Conditioning', icon: '💪', count: 32, route: 'strength' },
        { title: 'Match Analysis', icon: '📊', count: 15, route: 'analysis' }
    ];

    selectedVideo: any = null;
    showUploadForm: boolean = false;
    uploadType: 'link' | 'file' = 'link';
    selectedFile: File | null = null;

    // Upload & Analysis State
    isUploading: boolean = false;
    uploadProgress: number = 0;
    isAnalyzing: boolean = false;
    analysisResult: any = null;

    newVideo = {
        title: '',
        author: '',
        description: '',
        video_url: ''
    };

    recentVideos: any[] = [];

    ngOnInit() {
        this.loadVideos();
    }

    loadVideos() {
        this.apiService.getTrainingVideos().subscribe({
            next: (videos) => {
                this.recentVideos = videos;
            },
            error: (err) => console.error('Failed to load videos', err)
        });
    }

    onVideoClick(video: any) {
        this.selectedVideo = video;
    }

    closeVideo() {
        this.selectedVideo = null;
    }

    onCategoryClick(category: any) {
        if (category.title === 'Match Analysis') {
            this.router.navigate(['/app/training/analysis']);
        } else {
            console.log('Clicked category:', category.title);
            alert(`Opening ${category.title} section... (Coming Soon)`);
        }
    }

    onUploadClick() {
        this.showUploadForm = !this.showUploadForm;
        // Reset analysis state when opening/closing form
        if (!this.showUploadForm) {
            this.resetForm();
        }
    }

    onFileSelected(event: any) {
        const file = event.target.files[0];
        if (file) {
            this.selectedFile = file;
        }
    }

    submitVideo() {
        const formData = new FormData();
        formData.append('title', this.newVideo.title);
        formData.append('author', this.newVideo.author);
        formData.append('description', this.newVideo.description);
        formData.append('type', this.uploadType);

        if (this.uploadType === 'link') {
            formData.append('video_url', this.newVideo.video_url);
        } else if (this.uploadType === 'file' && this.selectedFile) {
            formData.append('file', this.selectedFile);
        } else if (this.uploadType === 'file' && !this.selectedFile) {
            alert('Please select a file to upload');
            return;
        }

        this.isUploading = true;

        this.apiService.addTrainingVideo(formData).subscribe({
            next: (video) => {
                console.log('Video added successfully', video);
                this.isUploading = false;
                this.showUploadForm = false;
                this.resetForm();
                this.loadVideos(); // Refresh list
                alert('Video uploaded successfully!');
            },
            error: (err) => {
                console.error('Failed to add video', err);
                this.isUploading = false;
                alert('Failed to upload video. Please try again.');
            }
        });
    }

    resetForm() {
        this.newVideo = {
            title: '',
            author: '',
            description: '',
            video_url: ''
        };
        this.selectedFile = null;
        this.uploadType = 'link';
        this.isUploading = false;
    }
}
