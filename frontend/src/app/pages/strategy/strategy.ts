import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-strategy',
    imports: [CommonModule],
    templateUrl: './strategy.html',
    styleUrl: './strategy.css',
})
export class StrategyComponent {
    strategies = [
        {
            title: 'Singles Positioning',
            author: 'Coach Mike Chen',
            category: 'Singles',
            comments: 24,
            likes: 156
        },
        {
            title: 'Doubles Rotation Tactics',
            author: 'Team Denmark',
            category: 'Doubles',
            comments: 18,
            likes: 132
        },
        {
            title: 'Serve and Attack Patterns',
            author: 'Lee Chong Wei',
            category: 'Strategy',
            comments: 42,
            likes: 289
        },
        {
            title: 'Defensive Strategy Guide',
            author: 'Carolina Marin',
            category: 'Defense',
            comments: 31,
            likes: 201
        },
        {
            title: 'Mixed Doubles Court Coverage',
            author: 'Zhang Nan & Zhao Yunlei',
            category: 'Mixed',
            comments: 27,
            likes: 178
        },
        {
            title: 'Counter-Attack Techniques',
            author: 'Viktor Axelsen',
            category: 'Attack',
            comments: 35,
            likes: 245
        }
    ];

    popularTopics = [
        { name: 'Court Positioning', count: 45 },
        { name: 'Serve Variations', count: 38 },
        { name: 'Mental Game', count: 32 },
        { name: 'Match Analysis', count: 28 }
    ];
}
