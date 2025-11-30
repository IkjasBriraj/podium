// Environment configuration for production (Cloud Run)
// IMPORTANT: Update this with your actual backend Cloud Run URL after deployment
export const environment = {
    production: true,
    apiUrl: 'https://podium-backend-4kngvq4raa-el.a.run.app'
};

// To get your backend URL after deployment, run:
// gcloud run services describe podium-backend --region us-central1 --format 'value(status.url)'
