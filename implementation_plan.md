# Implementation Plan - Sports Networking App (Badminton Focus)

## Goal Description
Build a professional networking application for sports individuals, starting with Badminton. The app connects athletes, sponsors, and coaches, facilitating funding, mentorship, and knowledge sharing.

## User Review Required
> [!IMPORTANT]
> Please confirm if Next.js API Routes are acceptable for the "Mock APIs" requirement. This keeps the project contained in one repository and is easier to prototype.

## Proposed Features
1.  **Professional Athlete Identity (Profile)**:
    -   **Career Timeline**: Visual history of teams, tournaments, and achievements.
    -   **Skills & Endorsements**: Peers/Coaches endorse skills (e.g., "Jump Smash", "Agility").
    -   **Certifications**: Display coaching badges or training certifications.
    -   **Media Gallery**: High-quality photos and video highlights.
2.  **Professional Networking**:
    -   **Connections**: Connect with peers, coaches, and sponsors.
    -   **Messaging**: Direct messaging for mentorship or sponsorship discussions.
    -   **Groups**: Communities for specific interests (e.g., "Doubles Strategy", "Junior Development").
3.  **Opportunity Marketplace (Jobs/Sponsorships)**:
    -   **Sponsorship Open Calls**: Brands post funding opportunities; athletes apply.
    -   **Team Tryouts/Recruitment**: Clubs post openings.
    -   **Coaching Gigs**: Find or offer coaching services.
4.  **Knowledge & Experience Sharing (Feed)**:
    -   **Rich Media Posts**: Share video analysis, training drills, and match breakdowns.
    -   **Articles/Blogs**: Long-form content for sharing strategies or experiences.
    -   **Events Calendar**: Discover and register for tournaments or webinars.

## Architecture
-   **Frontend**: Angular (Latest) for a robust, scalable web app.
-   **Styling**: Tailwind CSS for premium, modern aesthetics (configured for Angular).
-   **Backend**: Python (FastAPI).
    -   FastAPI is chosen for its speed, automatic documentation (Swagger UI), and ease of creating mock endpoints.
-   **Data**: In-memory Python dictionaries or local JSON files to mock the database.

## Data Model (Mock)

### User (Profile)
```json
{
  "id": "u1",
  "name": "Lee Chong Wei",
  "role": "athlete",
  "sport": "Badminton",
  "headline": "3x Olympic Silver Medalist | Brand Ambassador",
  "location": "Kuala Lumpur, Malaysia",
  "skills": [
    {"name": "Smash", "endorsements": 45},
    {"name": "Footwork", "endorsements": 30}
  ],
  "experience": [
    {"role": "National Player", "org": "BAM", "years": "2000-2019"}
  ]
}
```

### Post (Feed)
```json
{
  "id": "p1",
  "author_id": "u1",
  "content": "Analyzing the backhand defense today. #Badminton #Training",
  "media_url": "video_s3_link",
  "type": "video",
  "likes": 500,
  "comments": 45
}
```

### Opportunity (Job/Sponsorship)
```json
{
  "id": "j1",
  "poster_id": "c1", // Company or Club ID
  "type": "sponsorship", // 'coaching_job', 'tryout'
  "title": "Yonex Brand Ambassador 2025",
  "description": "Looking for rising stars in SE Asia.",
  "requirements": ["Top 50 National Ranking"],
  "budget": "10000 USD/year"
}
```

## Mock APIs (FastAPI)
-   `GET /users/{id}/profile`: Get full profile with skills/experience.
-   `POST /users/{id}/endorse`: Endorse a skill.
-   `GET /feed`: Get personalized feed.
-   `GET /opportunities`: Search for sponsorships/jobs.
-   `POST /connections/request`: Connect with a user.

## Verification Plan
### Automated Tests
-   Verify API endpoints return correct mock data.
-   Check UI rendering for key pages.

### Manual Verification
-   Click through the "Sponsor an Athlete" flow.
-   Post a new "Technique" to the feed.

## Deployment Plan
### Cloud Run & CI/CD
-   **Infrastructure**: Google Cloud Run (Serverless Container)
-   **Database**: MongoDB Atlas (Cloud)
-   **Storage**: AWS S3 (Media)
-   **CI/CD**: GitHub Actions
    -   `deploy-backend.yml`: Builds and deploys backend on push to main.
    -   `deploy-frontend.yml`: Builds and deploys frontend on push to main.
-   **Manual Steps**:
    -   Set up Google Cloud Project and Service Account.
    -   Configure GitHub Secrets (`GCP_SA_KEY`, `MONGODB_URL`, etc.).
    -   Update `environment.production.ts` with backend URL after first deployment.
