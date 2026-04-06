# Walkthrough - Sports Networking App

## Prerequisites
-   **Python 3.8+**
-   **Node.js 18+**

## 1. Backend Setup (FastAPI)

1.  Navigate to the project root.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the server:
    ```bash

   
 .venv\Scripts\activate
    uvicorn backend.app.main:app --reload
    ```
4.  Verify API at: `http://127.0.0.1:8000/docs`

## 2. Frontend Setup (Angular)

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies (if not already done):
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm start
    ```
    *(Note: If `ng` is not found, use `npx ng serve`)*

4.  Open the app at: `http://localhost:4200`

## 3. Features Implemented
-   **Landing Page**: Premium landing page with links to authentication.
-   **Authentication**: Login/Signup page (Mock login redirects to app).
-   **App Shell**: Main application layout with Sidebar and Navbar.
-   **Feed**: Social feed with post creation and rich media posts.
-   **Profile**: Comprehensive athlete profile with stats, skills, and timeline.
-   **Jobs & Sponsorships**: Marketplace for finding funding and coaching opportunities.

## 4. Navigation Guide
1.  **Start**: Open `http://localhost:4200`.
2.  **Login**: Click "Get Started" or "Join Now" to go to the Login page.
3.  **Enter App**: Click "Sign In" (no credentials needed for mock) to enter the main app.
4.  **Explore**: Use the sidebar to navigate between Feed, Network, Jobs, and Profile.

## 5. GIT commands

1. After changing code add changed files to GIT

```
git add .
```

2. Commiting your changes to GIT (locally)

```
git commit -m "Add your comments here.."
```

3. Push your changes to GITHUB (Cloud) - develop branch

```
git push origin develop
```

4. Moving to branches

```
git checkout develop

# or 

git checkout master
```

5. Merge your changes from develop to master branch

```
git checkout master

git merge develop
```

## 6. Changelog

### Fix: Top-level Routing & Login Freeze (Working Smoothly)
-   **Issue**: The app used to freeze upon login failure without updating the error state properly in the UI. Also, navigating to `/feed` or `/profile` directly led to angular route match errors.
-   **Fix**: Added top-level redirects to `app.routes.ts` connecting main paths to `/app/*`. Used `finalize` rx operator and `ChangeDetectorRef.detectChanges()` within `auth.ts` to ensure UI properly displays login errors instead of spinning indefinitely.

### Fix: Profile Page Freeze
-   **Issue**: Profile page was freezing on "Loading profile..." because the loading state wasn't being reset if an error occurred during data processing.
-   **Fix**: Added `finalize` operator to the `getProfile` observable pipe to ensure `isLoading` is always set to `false`, and added error handling for data processing.
-   **Verification**:
    2.  Verify that the loading spinner disappears and the profile content (or an error message) is displayed.

### Feature: Diet Type Selection
-   **Description**: Added an option on the Diet & Nutrition Plan page to choose between Vegetarian and Non-Vegetarian diet plans.
-   **Changes**: 
    -   Updated the `DietPlan` model to store specific dietary details (`nutrition`, `strategy`, `prePostMatch`, etc.) underneath `veg` and `nonVeg` options.
    -   Added a toggle button group on the diet page to seamlessly switch between the chosen preferences.

### Feature: Digital Coach
-   **Description**: Added an interactive 'Digital Coach' drill timer accessible from the sidebar. 
-   **Changes**:
    -   Implemented a High-Contrast **Heads-Up Display (HUD)** for easy visibility from afar.
    -   Integrated an RxJS state-machine loop with the browser's native **Web Speech API** (`speechSynthesis.speak`) for verbal cues and mid-drill motivation ("Come on!").

### Feature: Gear Manager Tracking
-   **Description**: Embedded an equipment tracking manager beneath the user's Experience module.
-   **Changes**:
    -   Tracks stringing metrics (Racket Model, String Brand, Tension, Date).
    -   Auto-evaluates strings exceeding their 90-day duration logic to output a `Needs Restringing` alert badge.
    -   Added a robust **String Advisor** to quickly identify ideal strings for Power, Durability, and Tension metrics.