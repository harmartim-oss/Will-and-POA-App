# Quick Google Cloud Run Deployment Guide

## 🚀 Deploy to Google Cloud Run in 10 Minutes

### Prerequisites
- Google Cloud account with billing enabled
- gcloud CLI installed
- OpenAI API key

### Step 1: Setup Google Cloud
```bash
# Install gcloud CLI (if not installed)
curl https://sdk.cloud.google.com | bash

# Login and set project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com containerregistry.googleapis.com
```

### Step 2: Prepare Application
```bash
# Build frontend and copy to backend (for monolithic deployment)
cd ontario-wills-frontend
npm install && npm run build
cp -r dist/* ../ontario-wills-backend/src/static/

cd ../ontario-wills-backend
```

### Step 3: Deploy to Cloud Run
```bash
# Deploy directly from source (easiest method)
gcloud run deploy ontario-wills-app \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY="your-api-key-here" \
  --set-env-vars FLASK_ENV=production
```

### Step 4: Access Your App
After deployment, you'll receive a URL like:
```
https://ontario-wills-app-xxxxxxxxx-uc.a.run.app
```

## 🔄 Automatic Updates via Cloud Build

### Setup CI/CD Pipeline
```bash
# Connect GitHub repository for automatic deployments
gcloud alpha builds triggers create github \
  --repo-name=ontario-wills \
  --repo-owner=yourusername \
  --branch-pattern="^main$" \
  --build-config=ontario-wills-backend/cloudbuild.yaml
```

Now every push to main branch automatically deploys!

## 💡 Pro Tips
- **Free Tier:** 2 million requests/month included
- **Auto-scaling:** Scales to zero when not in use
- **Custom Domains:** Easy setup with automatic SSL
- **Monitoring:** Built-in logging and metrics

## 🔧 Advanced Configuration

### Separate Frontend/Backend Services
```bash
# Deploy backend
cd ontario-wills-backend
gcloud run deploy ontario-wills-backend --source . --region us-central1

# Deploy frontend
cd ../ontario-wills-frontend
gcloud run deploy ontario-wills-frontend --source . --region us-central1
```

### Using Cloud SQL Database
```bash
# Create Cloud SQL instance
gcloud sql instances create ontario-wills-db \
  --database-version=POSTGRES_13 \
  --tier=db-f1-micro \
  --region=us-central1

# Connect to Cloud Run
gcloud run services update ontario-wills-app \
  --add-cloudsql-instances YOUR_PROJECT_ID:us-central1:ontario-wills-db
```

### Custom Domain
```bash
# Map custom domain
gcloud run domain-mappings create \
  --service ontario-wills-app \
  --domain your-domain.com \
  --region us-central1
```

For detailed instructions, see `DEPLOYMENT_GUIDE.md`.

