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
