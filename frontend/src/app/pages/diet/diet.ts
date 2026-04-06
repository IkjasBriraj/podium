import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

type DietType = 'veg' | 'non-veg';

interface DietaryDetails {
    nutrition: string;
    strategy: string;
    bestSnacks?: string;
    prePostMatch?: { pre: string, post: string };
}

interface DietPlan {
    id: string;
    ageGroup: string;
    focus: string;
    hydration: string;
    veg: DietaryDetails;
    nonVeg: DietaryDetails;
}

@Component({
    selector: 'app-diet',
    imports: [CommonModule, RouterModule],
    templateUrl: './diet.html',
    styleUrl: './diet.css',
})
export class DietComponent {
    selectedAgeId: string = '8-9';
    dietType: DietType = 'veg';

    dietPlans: DietPlan[] = [
        {
            id: '8-9',
            ageGroup: 'Ages 8–9 (Foundational Years)',
            focus: 'Establishing healthy habits and hydration.',
            hydration: 'Teach them to drink water before they feel thirsty.',
            veg: {
                nutrition: 'They are growing rapidly. Do not restrict calories. Focus on "food first." Incorporate plenty of legumes and dairy.',
                strategy: 'Provide 3 main meals + 2 snacks.',
                bestSnacks: 'Yogurt with berries, apple slices with peanut butter, string cheese.'
            },
            nonVeg: {
                nutrition: 'They are growing rapidly. Do not restrict calories. Focus on "food first." Include lean meats and dairy.',
                strategy: 'Provide 3 main meals + 2 snacks.',
                bestSnacks: 'Yogurt with berries, apple slices with peanut butter, string cheese.'
            }
        },
        {
            id: '10-11',
            ageGroup: 'Ages 10–11 (Developing Coordination)',
            focus: 'Energy availability for increased training hours.',
            hydration: 'Introduce the "check your pee" method (should be pale yellow).',
            veg: {
                nutrition: 'Badminton requires quick reflexes. Focus on brain-boosting foods like Omega-3s (walnuts, chia seeds, flaxseeds) which help with focus and cognitive speed.',
                strategy: 'Ensure they eat a snack 60–90 minutes before practice.',
                bestSnacks: 'Whole-grain crackers with hummus, banana, trail mix (no candy).'
            },
            nonVeg: {
                nutrition: 'Badminton requires quick reflexes. Focus on brain-boosting foods like Omega-3s (salmon, walnuts, chia seeds) which help with focus and cognitive speed.',
                strategy: 'Ensure they eat a snack 60–90 minutes before practice.',
                bestSnacks: 'Whole-grain crackers with hummus, banana, trail mix (no candy).'
            }
        },
        {
            id: '12-13',
            ageGroup: 'Ages 12–13 (The Growth Spurt)',
            focus: 'Bone health and muscle repair. This is usually when puberty hits, and they need extra Calcium and Vitamin D for bone density (crucial for the impact of jumping in badminton).',
            hydration: 'Start monitoring fluid loss during tournaments.',
            veg: {
                nutrition: 'Increase protein intake to support muscle development during growth spurts. Good sources include paneer, tofu, and Greek yogurt.',
                strategy: 'Iron is critical, especially for girls, to prevent fatigue. Include spinach, lentils, or fortified cereals.',
                bestSnacks: 'Hard-boiled eggs, Greek yogurt, protein-rich smoothies.'
            },
            nonVeg: {
                nutrition: 'Increase protein intake to support muscle development during growth spurts.',
                strategy: 'Iron is critical, especially for girls, to prevent fatigue. Include lean red meat, spinach, or lentils.',
                bestSnacks: 'Hard-boiled eggs, Greek yogurt, protein-rich smoothies.'
            }
        },
        {
            id: '14-15',
            ageGroup: 'Ages 14–15 (Performance & Intensity)',
            focus: 'Nutrient timing. They are now training longer and playing more competitive matches.',
            hydration: 'Electrolytes become more important if they are sweating heavily.',
            veg: {
                nutrition: 'This is the age to master the "Pre-match/Post-match" window.',
                prePostMatch: {
                    pre: 'High carb, moderate protein, low fat (e.g., oatmeal with fruit).',
                    post: 'Protein + Carbs to replenish glycogen (e.g., chocolate milk, paneer/tofu sandwich).'
                },
                strategy: 'Avoid sugary sports drinks unless they are playing for more than 90 minutes straight.'
            },
            nonVeg: {
                nutrition: 'This is the age to master the "Pre-match/Post-match" window.',
                prePostMatch: {
                    pre: 'High carb, moderate protein, low fat (e.g., oatmeal with fruit).',
                    post: 'Protein + Carbs to replenish glycogen (e.g., chocolate milk, turkey or chicken sandwich).'
                },
                strategy: 'Avoid sugary sports drinks unless they are playing for more than 90 minutes straight.'
            }
        },
        {
            id: '16-17',
            ageGroup: 'Ages 16–17 (Elite/High School Prep)',
            focus: 'Fine-tuning and recovery optimization.',
            hydration: 'Athletes should know exactly how much they sweat by weighing themselves before and after a practice session.',
            veg: {
                nutrition: 'They should be eating for body composition (lean muscle vs. body fat). Supplements like creatine or plant-based protein powders can be introduced here, but only if they are training at a high level and their diet is already perfect.',
                strategy: 'Focus on "Anti-inflammatory" foods for recovery—cherries, turmeric, ginger, and high-quality fats (avocados, olive oil).'
            },
            nonVeg: {
                nutrition: 'They should be eating for body composition (lean muscle vs. body fat). Supplements like creatine or whey protein powders can be introduced here, but only if they are training at a high level and their diet is already perfect.',
                strategy: 'Focus on "Anti-inflammatory" foods for recovery—cherries, turmeric, ginger, and high-quality fats (avocados, olive oil, fatty fish).'
            }
        }
    ];

    get selectedPlan() {
        return this.dietPlans.find(p => p.id === this.selectedAgeId);
    }

    get dietDetails() {
        const plan = this.selectedPlan;
        if (!plan) return null;
        return this.dietType === 'veg' ? plan.veg : plan.nonVeg;
    }

    selectAge(id: string) {
        this.selectedAgeId = id;
    }

    setDietType(type: DietType) {
        this.dietType = type;
    }
}
