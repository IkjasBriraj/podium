# Podium Deployment Guide - Google Cloud Run

Complete guide for deploying the Podium application to Google Cloud Run with automated CI/CD using GitHub Actions.

## Architecture Overview

The Podium application is deployed as **two separate Cloud Run services**:

1. **Backend Service** (`podium-backend`): FastAPI application handling all API requests
2. **Frontend Service** (`podium-frontend`): Angular application served via nginx

```mermaid
graph LR
    A[User] --> B[Frontend<br/>Cloud Run]
    B --> C[Backend API<br/>Cloud Run]
    C --> D[MongoDB Atlas]
    C --> E[AWS S3]
```

## Prerequisites

### Required Accounts & Services

- ✅ Google Cloud account with billing enabled
- ✅ GitHub repository with your code
- ✅ MongoDB Atlas cluster (free tier available)
- ✅ AWS account with S3 bucket configured

### Required Tools (for initial setup)

- Google Cloud SDK (gcloud CLI)
- Git

---

## Step 1: Google Cloud Project Setup

### 1.1 Create/Select Project

```bash
# Create a new project (or use existing)
gcloud projects create podium-production --name="Podium Production"

# Set as active project
gcloud config set project podium-production
```

### 1.2 Enable Required APIs

```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Artifact Registry API (for Docker images)
gcloud services enable artifactregistry.googleapis.com

# Enable Cloud Build API (optional, for building images)
gcloud services enable cloudbuild.googleapis.com
```

### 1.3 Create Artifact Registry Repository

```bash
# Create repository for Docker images
gcloud artifacts repositories create podium \
  --repository-format=docker \
  --location=us-central1 \
  --description="Podium application images"
```

### 1.4 Create Service Account

```bash
# Create service account for GitHub Actions
gcloud iam service-accounts create github-actions \
  --display-name="GitHub Actions Deployment"

# Get your project ID
export PROJECT_ID=$(gcloud config get-value project)

# Grant necessary permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

# Create and download service account key
gcloud iam service-accounts keys create github-sa-key.json \
  --iam-account=github-actions@$PROJECT_ID.iam.gserviceaccount.com

# Display the key (you'll need this for GitHub Secrets)
cat github-sa-key.json
```

> [!IMPORTANT]
> Save the service account key JSON securely. You'll add it to GitHub Secrets in the next step.

---

## Step 2: MongoDB Atlas Setup

### 2.1 Create MongoDB Atlas Cluster

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster (or paid tier for production)
3. Create a database user with password
4. Whitelist IP address: `0.0.0.0/0` (allows connections from anywhere, including Cloud Run)

### 2.2 Get Connection String

Your connection string will look like:
```
mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

> [!WARNING]
> Keep this connection string secure. Never commit it to your repository.

---

## Step 3: GitHub Repository Secrets

Navigate to your GitHub repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add the following secrets:

| Secret Name | Value | Example |
|------------|-------|---------|
| `GCP_PROJECT_ID` | Your Google Cloud project ID | `podium-production` |
| `GCP_SA_KEY` | Service account JSON key (entire content) | `{\"type\":\"service_account\",...}` |
| `MONGODB_URL` | MongoDB Atlas connection string | `mongodb+srv://user:pass@cluster...` |
| `DB_NAME` | Database name | `podium_db` |
| `AWS_ACCESS_KEY_ID` | AWS access key for S3 | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | `wJalrXUtnFEMI/K7MDENG/...` |
| `AWS_REGION` | AWS region for S3 bucket | `us-east-1` |
| `S3_BUCKET_NAME` | S3 bucket name | `podium-media` |

> [!TIP]
> To add the GCP service account key:
> 1. Copy the entire content of `github-sa-key.json`
> 2. Paste it as is (don't encode or modify)
> 3. GitHub will automatically handle it correctly

---

## Step 4: Update Frontend Configuration

The frontend needs to know the backend API URL. After your first deployment, you'll need to update the Angular application.

### 4.1 Create Environment File

Create `frontend/src/environments/environment.production.ts`:

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://podium-backend-XXXXXXXXXX-uc.a.run.app'
};
```

Replace `XXXXXXXXXX` with your actual backend Cloud Run URL.

### 4.2 Update API Service

Ensure your services use the environment configuration:

```typescript
import { environment } from '../../environments/environment.production';

// Use environment.apiUrl for all API calls
```

---

## Step 5: Initial Deployment

### 5.1 Deploy Backend First

```bash
# From project root
cd d:/learning/code/podium

# Build backend Docker image
docker build -f Dockerfile.backend -t podium-backend .

# Tag for Artifact Registry
docker tag podium-backend us-central1-docker.pkg.dev/$PROJECT_ID/podium/backend:latest

# Configure Docker authentication
gcloud auth configure-docker us-central1-docker.pkg.dev

# Push to Artifact Registry
docker push us-central1-docker.pkg.dev/$PROJECT_ID/podium/backend:latest

# Deploy to Cloud Run
gcloud run deploy podium-backend \
  --image us-central1-docker.pkg.dev/$PROJECT_ID/podium/backend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "MONGODB_URL=YOUR_MONGODB_URL" \
  --set-env-vars "DB_NAME=podium_db" \
  --set-env-vars "AWS_ACCESS_KEY_ID=YOUR_AWS_KEY" \
  --set-env-vars "AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET" \
  --set-env-vars "AWS_REGION=us-east-1" \
  --set-env-vars "S3_BUCKET_NAME=podium-media" \
  --min-instances 0 \
  --max-instances 10 \
  --memory 512Mi
```

> [!NOTE]
> Replace `YOUR_MONGODB_URL`, `YOUR_AWS_KEY`, etc. with your actual values.

### 5.2 Get Backend URL

```bash
gcloud run services describe podium-backend \
  --region us-central1 \
  --format 'value(status.url)'
```

Save this URL - you'll need it for the frontend configuration.

### 5.3 Update Frontend Environment

Update `frontend/src/environments/environment.production.ts` with the backend URL from step 5.2.

### 5.4 Deploy Frontend

```bash
# Build frontend Docker image
docker build -f Dockerfile.frontend -t podium-frontend .

# Tag for Artifact Registry
docker tag podium-frontend us-central1-docker.pkg.dev/$PROJECT_ID/podium/frontend:latest

# Push to Artifact Registry
docker push us-central1-docker.pkg.dev/$PROJECT_ID/podium/frontend:latest

# Deploy to Cloud Run
gcloud run deploy podium-frontend \
  --image us-central1-docker.pkg.dev/$PROJECT_ID/podium/frontend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --min-instances 0 \
  --max-instances 10 \
  --memory 256Mi
```

### 5.5 Get Frontend URL

```bash
gcloud run services describe podium-frontend \
  --region us-central1 \
  --format 'value(status.url)'
```

Open this URL in your browser to access your deployed application! 🎉

---

## Step 6: Update Backend CORS

Update `backend/app/main.py` to allow requests from your frontend URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://podium-frontend-XXXXXXXXXX-uc.a.run.app",  # Your frontend URL
        "http://localhost:4200"  # For local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push this change - GitHub Actions will automatically redeploy!

---

## Step 7: Automated CI/CD Usage

After the initial setup, deployments are automatic:

### Backend Deployment Triggers

The backend will automatically deploy when you push changes to:
- `backend/**` files
- `requirements.txt`
- `Dockerfile.backend`
- `.github/workflows/deploy-backend.yml`

### Frontend Deployment Triggers

The frontend will automatically deploy when you push changes to:
- `frontend/**` files
- `nginx.conf`
- `Dockerfile.frontend`
- `.github/workflows/deploy-frontend.yml`

### Deployment Process

1. Make your code changes
2. Commit and push to `main` or `master` branch:
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```
3. GitHub Actions automatically:
   - Builds Docker image
   - Pushes to Artifact Registry
   - Deploys to Cloud Run
4. Check deployment status in GitHub Actions tab

---

## Monitoring & Logs

### View Logs

```bash
# Backend logs
gcloud run services logs read podium-backend --region us-central1

# Frontend logs
gcloud run services logs read podium-frontend --region us-central1

# Live tail
gcloud run services logs tail podium-backend --region us-central1
```

### Cloud Console

Visit [Google Cloud Run Console](https://console.cloud.google.com/run) to:
- View service metrics
- Monitor requests and errors
- Adjust scaling settings
- View detailed logs

---

## Troubleshooting

### Backend Connection Issues

**Problem**: "Can't connect to MongoDB"

**Solution**:
1. Check MongoDB Atlas network access (whitelist `0.0.0.0/0`)
2. Verify connection string in GitHub Secrets
3. Check service logs: `gcloud run services logs read podium-backend`

### Frontend Can't Reach Backend

**Problem**: API calls failing with CORS errors

**Solution**:
1. Update backend CORS settings with frontend URL
2. Verify frontend environment.production.ts has correct backend URL
3. Redeploy backend after CORS changes

### Deployment Fails

**Problem**: GitHub Actions deployment failing

**Solution**:
1. Check GitHub Actions logs for specific error
2. Verify all GitHub Secrets are correctly set
3. Ensure service account has required permissions
4. Check Artifact Registry repository exists

### High Costs

**Problem**: Unexpected Cloud Run charges

**Solution**:
1. Check if services have minimum instances > 0
2. Review request patterns in Cloud Console
3. Consider setting `--max-instances` to limit scaling
4. Use `--min-instances 0` for development

---

## Cost Optimization

### Free Tier

Cloud Run free tier includes:
- 2 million requests per month
- 360,000 GB-seconds of memory
- 180,000 vCPU-seconds of compute time

### Recommended Settings for Low-Traffic Apps

```bash
--min-instances 0        # Scale to zero when unused
--max-instances 3        # Limit maximum scaling
--memory 256Mi           # Frontend
--memory 512Mi           # Backend
--cpu 1                  # Single CPU core
```

### Monitoring Costs

Visit [Google Cloud Billing](https://console.cloud.google.com/billing) to monitor your costs.

---

## Updating Your Application

### Code Changes

1. Make changes locally
2. Test locally: `docker-compose up`
3. Commit and push to main branch
4. GitHub Actions deploys automatically

### Environment Variables

Update via Cloud Console or gcloud:

```bash
gcloud run services update podium-backend \
  --region us-central1 \
  --update-env-vars "NEW_VAR=value"
```

### Scaling Configuration

```bash
gcloud run services update podium-backend \
  --region us-central1 \
  --min-instances 1 \
  --max-instances 20
```

---

## Security Best Practices

> [!IMPORTANT]
> - ✅ Never commit secrets to Git
> - ✅ Use GitHub Secrets for all sensitive data
> - ✅ Regularly rotate service account keys
> - ✅ Use MongoDB Atlas IP whitelist
> - ✅ Enable S3 bucket encryption
> - ✅ Review Cloud Run IAM permissions regularly

---

## Support & Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Angular Documentation](https://angular.io/docs)

---

## Quick Reference

### Service URLs

After deployment, save these for reference:

```
Backend:  https://podium-backend-XXXXXXXXXX-uc.a.run.app
Frontend: https://podium-frontend-XXXXXXXXXX-uc.a.run.app
```

### Useful Commands

```bash
# View all services
gcloud run services list

# Describe service
gcloud run services describe SERVICE_NAME --region us-central1

# Delete service
gcloud run services delete SERVICE_NAME --region us-central1

# View logs
gcloud run services logs read SERVICE_NAME --region us-central1
```

---

**Deployment Complete!** Your Podium application is now running on Google Cloud Run with automated CI/CD. 🚀
