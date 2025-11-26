import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SafePipe } from '../../pipes/safe.pipe';

@Component({
    selector: 'app-highlights',
    imports: [CommonModule, SafePipe],
    templateUrl: './highlights.html',
    styleUrl: './highlights.css',
})
export class HighlightsComponent {
    activeFilter = 'All';
    selectedVideo: any = null;

    filters = ['All', 'Singles', 'Doubles', 'Mixed', 'Super Smashes', 'Amazing Rallies'];

    allHighlights = [
        {
            title: 'Epic Rally - All England 2023',
            player: 'Viktor Axelsen vs Kento Momota',
            duration: '2:34',
            views: '1.2M',
            likes: '45K',
            category: 'Singles',
            videoId: 'L1d8_r1x_w0', // Placeholder valid ID
            description: 'An incredible display of endurance and skill from two legends.'
        },
        {
            title: 'Championship Winning Point',
            player: 'Carolina Marin',
            duration: '1:15',
            views: '890K',
            likes: '32K',
            category: 'Singles',
            videoId: 's3cMVBRmySc', // Lee Chong Wei smash (reused for demo)
            description: 'The moment that decided the championship.'
        },
        {
            title: 'Amazing Saves Compilation',
            player: 'Mixed Highlights',
            duration: '5:42',
            views: '2.1M',
            likes: '78K',
            category: 'Amazing Rallies',
            videoId: 'SjX7_r1i3jE', // Net shots (reused for demo)
            description: 'Impossible saves that defied gravity.'
        },
        {
            title: 'Best Smashes of 2023',
            player: 'World Tour Highlights',
            duration: '4:18',
            views: '1.5M',
            likes: '56K',
            category: 'Super Smashes',
            videoId: 'rI7t1h5x6xs', // Smash compilation (reused for demo)
            description: 'The most powerful smashes from the 2023 season.'
        },
        {
            title: 'Deceptive Net Play',
            player: 'Lee Chong Wei',
            duration: '3:22',
            views: '980K',
            likes: '41K',
            category: 'Singles',
            videoId: '1w8qB2vGCOs', // Footwork (reused for demo)
            description: 'Masterclass in net play deception.'
        },
        {
            title: 'Tournament Finals Highlights',
            player: 'BWF Championships',
            duration: '8:45',
            views: '3.4M',
            likes: '125K',
            category: 'Doubles',
            videoId: 'L1d8_r1x_w0', // Placeholder
            description: 'Full highlights from the finals.'
        }
    ];

    get filteredHighlights() {
        if (this.activeFilter === 'All') {
            return this.allHighlights;
        }
        return this.allHighlights.filter(h => h.category === this.activeFilter);
    }

    setFilter(filter: string) {
        this.activeFilter = filter;
    }

    onVideoClick(video: any) {
        this.selectedVideo = video;
    }

    closeVideo() {
        this.selectedVideo = null;
    }
}
