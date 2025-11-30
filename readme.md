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
    uvicorn backend.main:app --reload
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
    uvicorn backend.main:app --reload
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

---

## 7. Production Deployment

### Google Cloud Run Deployment

The application is configured for production deployment on Google Cloud Run with automated CI/CD using GitHub Actions.

**Architecture:**
- **Frontend Service**: Angular app served via nginx
- **Backend Service**: FastAPI REST API
- **Database**: MongoDB Atlas
- **Storage**: AWS S3

**Quick Deploy:**
1. See [DEPLOYMENT.md](./DEPLOYMENT.md) for complete setup instructions
2. Configure GitHub Secrets (project ID, service account, MongoDB URI, AWS credentials)
3. Push to `main` branch - automatic deployment via GitHub Actions

**Deployment Features:**
- ✅ Automated CI/CD with GitHub Actions
- ✅ Separate frontend and backend services
- ✅ Health check endpoints
- ✅ Auto-scaling with Cloud Run
- ✅ Production-optimized Docker images
- ✅ Environment-based configuration

For detailed deployment instructions, see **[DEPLOYMENT.md](./DEPLOYMENT.md)**.

---

## 8. Docker Support

See [DOCKER.md](./DOCKER.md) for local Docker development setup.

## 6. Changelog

### Fix: Profile Page Freeze
-   **Issue**: Profile page was freezing on "Loading profile..." because the loading state wasn't being reset if an error occurred during data processing.
-   **Fix**: Added `finalize` operator to the `getProfile` observable pipe to ensure `isLoading` is always set to `false`, and added error handling for data processing.
-   **Verification**:
    1.  Open the Profile page.
    2.  Verify that the loading spinner disappears and the profile content (or an error message) is displayed.