# Complete Deployment Guide - Ontario Wills & Power of Attorney Creator v3.0

## 🚀 **Comprehensive Deployment Options**

This guide provides detailed instructions for deploying the Ontario Wills & Power of Attorney Creator application across multiple platforms, including GitHub Pages, Render, and Google Cloud Run.

---

## 📋 **Table of Contents**

1. [Prerequisites](#prerequisites)
2. [GitHub Pages Deployment](#github-pages-deployment)
3. [Render Deployment](#render-deployment)
4. [Google Cloud Run Deployment](#google-cloud-run-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Domain Configuration](#domain-configuration)
7. [SSL/HTTPS Setup](#sslhttps-setup)
8. [Monitoring & Analytics](#monitoring--analytics)
9. [Troubleshooting](#troubleshooting)
10. [Performance Optimization](#performance-optimization)

---

## ✅ **Prerequisites**

### **Required Accounts**
- GitHub account (for all deployment options)
- Render account (for Render deployment)
- Google Cloud account (for Cloud Run deployment)
- Domain registrar account (optional, for custom domains)

### **Required Tools**
- Git (version control)
- Node.js 18+ and npm/pnpm (frontend)
- Python 3.11+ and pip (backend)
- Docker (for containerized deployments)
- Google Cloud CLI (for Cloud Run)

### **API Keys Required**
- OpenAI API key (for AI features)
- CanLII API key (optional, for legal research)
- Google AI Studio API key (optional, backup AI provider)

---

## 🌐 **GitHub Pages Deployment**

GitHub Pages is ideal for hosting the frontend as a static site, with the backend deployed separately.

### **Step 1: Repository Setup**

```bash
# Clone or fork the repository
git clone https://github.com/yourusername/ontario-wills-app.git
cd ontario-wills-app

# Create a new repository on GitHub (if not forked)
# Push your code to the repository
git remote add origin https://github.com/yourusername/ontario-wills-app.git
git push -u origin main
```

### **Step 2: Configure Frontend for GitHub Pages**

#### **Update vite.config.js**
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  base: process.env.NODE_ENV === 'production' ? '/ontario-wills-app/' : '/',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu']
        }
      }
    }
  }
})
```

#### **Update package.json**
```json
{
  "homepage": "https://yourusername.github.io/ontario-wills-app",
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d dist",
    "deploy:github": "npm run build && gh-pages -d dist"
  }
}
```

### **Step 3: Set Up GitHub Actions**

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    permissions:
      contents: read
      pages: write
      id-token: write
    
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    
    steps:
    - name: Checkout
      uses: actions/checkout@v4
      
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
        
    - name: Install dependencies
      run: |
        cd frontend
        npm ci
        
    - name: Build application
      run: |
        cd frontend
        npm run build
      env:
        NODE_ENV: production
        VITE_API_BASE_URL: ${{ vars.VITE_API_BASE_URL }}
        VITE_GITHUB_PAGES: true
        
    - name: Setup Pages
      uses: actions/configure-pages@v4
      
    - name: Upload artifact
      uses: actions/upload-pages-artifact@v3
      with:
        path: './frontend/dist'
        
    - name: Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v4
```

### **Step 4: Configure GitHub Repository**

1. Go to your repository settings
2. Navigate to "Pages" section
3. Select "GitHub Actions" as the source
4. Set environment variables in "Environments" → "github-pages":
   - `VITE_API_BASE_URL`: Your backend API URL

### **Step 5: Deploy Backend Separately**

Since GitHub Pages only hosts static sites, deploy your backend to Render or Google Cloud Run (see sections below).

### **Manual Deployment Alternative**

```bash
# Build and deploy manually
cd frontend
npm install
npm run build
npm run deploy
```

---

## 🎨 **Render Deployment**

Render provides easy deployment for both frontend and backend with automatic builds.

### **Option A: Monolithic Deployment (Recommended)**

Deploy frontend and backend as a single service.

#### **Step 1: Prepare Backend for Static Serving**

Update `backend/src/main.py`:

```python
from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')

# Serve React app
@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_react_routes(path):
    if path.startswith('api/'):
        # Handle API routes normally
        return handle_api_route(path)
    
    # Serve static files or React app
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
```

#### **Step 2: Create Build Script**

Create `build.sh` in the root directory:

```bash
#!/bin/bash
set -e

echo "Building frontend..."
cd frontend
npm ci
npm run build
cd ..

echo "Copying frontend build to backend..."
rm -rf backend/static
cp -r frontend/dist backend/static

echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt

echo "Build complete!"
```

#### **Step 3: Create render.yaml**

```yaml
services:
  - type: web
    name: ontario-wills-app
    env: python
    region: oregon
    plan: free
    buildCommand: ./build.sh
    startCommand: cd backend && gunicorn --bind 0.0.0.0:$PORT src.main:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: OPENAI_API_KEY
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: JWT_SECRET_KEY
        generateValue: true
```

### **Option B: Separate Services**

Deploy frontend and backend as separate services.

#### **Backend render.yaml**
```yaml
services:
  - type: web
    name: ontario-wills-backend
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT src.main:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: OPENAI_API_KEY
        sync: false
```

#### **Frontend render.yaml**
```yaml
services:
  - type: static
    name: ontario-wills-frontend
    buildCommand: npm run build
    staticPublishPath: ./dist
    envVars:
      - key: VITE_API_BASE_URL
        value: https://ontario-wills-backend.onrender.com
```

### **Step 4: Deploy to Render**

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Configure environment variables
4. Deploy automatically on git push

---

## ☁️ **Google Cloud Run Deployment**

Google Cloud Run provides serverless deployment with automatic scaling.

### **Step 1: Set Up Google Cloud**

```bash
# Install Google Cloud CLI
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set project
gcloud config set project your-project-id

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### **Step 2: Backend Deployment**

#### **Create Dockerfile for Backend**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Expose port
EXPOSE 8080

# Set environment variables
ENV FLASK_ENV=production
ENV PORT=8080

# Start command
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 src.main:app
```

#### **Deploy Backend**
```bash
cd backend

# Build and deploy
gcloud run deploy ontario-wills-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FLASK_ENV=production \
  --set-env-vars OPENAI_API_KEY=your-api-key
```

### **Step 3: Frontend Deployment**

#### **Create Dockerfile for Frontend**
```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci

# Copy source code and build
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built app
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port
EXPOSE 8080

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

#### **Create nginx.conf**
```nginx
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    server {
        listen 8080;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        # Handle client-side routing
        location / {
            try_files $uri $uri/ /index.html;
        }

        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

#### **Deploy Frontend**
```bash
cd frontend

# Build and deploy
gcloud run deploy ontario-wills-frontend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars VITE_API_BASE_URL=https://ontario-wills-backend-hash.a.run.app
```

### **Step 4: Set Up Cloud Build (Optional)**

Create `cloudbuild.yaml` for automated deployments:

```yaml
steps:
  # Build backend
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/ontario-wills-backend', './backend']
  
  # Deploy backend
  - name: 'gcr.io/cloud-builders/gcloud'
    args: [
      'run', 'deploy', 'ontario-wills-backend',
      '--image', 'gcr.io/$PROJECT_ID/ontario-wills-backend',
      '--region', 'us-central1',
      '--platform', 'managed',
      '--allow-unauthenticated'
    ]
  
  # Build frontend
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/ontario-wills-frontend', './frontend']
  
  # Deploy frontend
  - name: 'gcr.io/cloud-builders/gcloud'
    args: [
      'run', 'deploy', 'ontario-wills-frontend',
      '--image', 'gcr.io/$PROJECT_ID/ontario-wills-frontend',
      '--region', 'us-central1',
      '--platform', 'managed',
      '--allow-unauthenticated'
    ]

images:
  - 'gcr.io/$PROJECT_ID/ontario-wills-backend'
  - 'gcr.io/$PROJECT_ID/ontario-wills-frontend'
```

---

## ⚙️ **Environment Configuration**

### **Frontend Environment Variables**

#### **Development (.env.local)**
```env
VITE_API_BASE_URL=http://localhost:5000
VITE_GITHUB_PAGES=false
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=true
```

#### **Production (GitHub Pages)**
```env
VITE_API_BASE_URL=https://ontario-wills-backend.onrender.com
VITE_GITHUB_PAGES=true
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_DEBUG=false
```

#### **Production (Render/Cloud Run)**
```env
VITE_API_BASE_URL=https://your-backend-url.com
VITE_GITHUB_PAGES=false
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_DEBUG=false
```

### **Backend Environment Variables**

#### **Development (.env)**
```env
FLASK_ENV=development
SECRET_KEY=dev-secret-key
DATABASE_URL=sqlite:///ontario_wills.db
OPENAI_API_KEY=your-openai-api-key
CANLII_API_KEY=your-canlii-api-key
JWT_SECRET_KEY=jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

#### **Production**
```env
FLASK_ENV=production
SECRET_KEY=secure-production-secret
DATABASE_URL=postgresql://user:pass@host:port/dbname
OPENAI_API_KEY=your-openai-api-key
CANLII_API_KEY=your-canlii-api-key
JWT_SECRET_KEY=secure-jwt-secret
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000
CORS_ORIGINS=https://yourdomain.com,https://yourusername.github.io
```

---

## 🌍 **Domain Configuration**

### **Custom Domain for GitHub Pages**

1. **Add CNAME file** to your repository's root:
```
yourdomain.com
```

2. **Configure DNS** with your domain registrar:
```
Type: CNAME
Name: www
Value: yourusername.github.io

Type: A
Name: @
Value: 185.199.108.153
Value: 185.199.109.153
Value: 185.199.110.153
Value: 185.199.111.153
```

3. **Enable custom domain** in GitHub repository settings

### **Custom Domain for Render**

1. **Add custom domain** in Render dashboard
2. **Configure DNS**:
```
Type: CNAME
Name: www
Value: your-app-name.onrender.com

Type: A
Name: @
Value: [Render IP addresses provided in dashboard]
```

### **Custom Domain for Google Cloud Run**

1. **Map domain** using Cloud Run console
2. **Verify domain ownership**
3. **Configure DNS**:
```
Type: CNAME
Name: www
Value: ghs.googlehosted.com

Type: A
Name: @
Value: [Google Cloud IP addresses]
```

---

## 🔒 **SSL/HTTPS Setup**

### **GitHub Pages**
- Automatic SSL certificates provided
- Enable "Enforce HTTPS" in repository settings

### **Render**
- Automatic SSL certificates for all domains
- HTTPS enforced by default

### **Google Cloud Run**
- Automatic SSL certificates for custom domains
- HTTPS enforced by default

---

## 📊 **Monitoring & Analytics**

### **Application Monitoring**

#### **Google Analytics Setup**
```javascript
// Add to frontend/src/config/analytics.js
import { config } from './environment';

export const initAnalytics = () => {
  if (config.features.enableAnalytics && config.services.analytics.trackingId) {
    // Initialize Google Analytics
    gtag('config', config.services.analytics.trackingId);
  }
};
```

#### **Error Monitoring with Sentry**
```javascript
// Add to frontend/src/config/sentry.js
import * as Sentry from '@sentry/react';
import { config } from './environment';

if (config.services.errorReporting.enabled) {
  Sentry.init({
    dsn: config.services.errorReporting.dsn,
    environment: config.environment
  });
}
```

### **Performance Monitoring**

#### **Backend Monitoring**
```python
# Add to backend/src/utils/monitoring.py
import logging
import time
from functools import wraps

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logging.info(f"{func.__name__} executed in {end_time - start_time:.2f}s")
        return result
    return wrapper
```

#### **Frontend Performance**
```javascript
// Add to frontend/src/utils/performance.js
export const measurePerformance = (name, fn) => {
  const start = performance.now();
  const result = fn();
  const end = performance.now();
  
  console.log(`${name} took ${end - start} milliseconds`);
  return result;
};
```

---

## 🔧 **Troubleshooting**

### **Common Deployment Issues**

#### **GitHub Pages Issues**

**Problem**: 404 errors on page refresh
**Solution**: Ensure proper 404.html with SPA routing script

**Problem**: Assets not loading
**Solution**: Check base path configuration in vite.config.js

**Problem**: API calls failing
**Solution**: Verify CORS configuration and API endpoint URLs

#### **Render Issues**

**Problem**: Build failures
**Solution**: 
- Check build logs for specific errors
- Verify all dependencies are in requirements.txt/package.json
- Ensure build commands are correct

**Problem**: Application not starting
**Solution**:
- Verify start command syntax
- Check port binding (use $PORT environment variable)
- Review application logs

#### **Google Cloud Run Issues**

**Problem**: Container fails to start
**Solution**:
- Check Dockerfile syntax
- Verify port 8080 is exposed and used
- Review Cloud Run logs

**Problem**: Cold start latency
**Solution**:
- Implement proper health checks
- Consider using minimum instances
- Optimize container size

### **Performance Issues**

#### **Slow Loading Times**
- Enable gzip compression
- Implement proper caching headers
- Optimize images and assets
- Use CDN for static assets

#### **High Memory Usage**
- Implement proper garbage collection
- Optimize database queries
- Use connection pooling
- Monitor memory leaks

---

## ⚡ **Performance Optimization**

### **Frontend Optimization**

#### **Code Splitting**
```javascript
// Implement lazy loading
const DocumentWizard = lazy(() => import('./components/DocumentWizard'));
const LegalResearch = lazy(() => import('./components/LegalResearch'));

// Use Suspense for loading states
<Suspense fallback={<LoadingSpinner />}>
  <DocumentWizard />
</Suspense>
```

#### **Asset Optimization**
```javascript
// vite.config.js optimization
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-select'],
          utils: ['date-fns', 'clsx', 'tailwind-merge']
        }
      }
    },
    chunkSizeWarningLimit: 1000
  }
});
```

### **Backend Optimization**

#### **Database Optimization**
```python
# Implement connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

#### **Caching Implementation**
```python
# Add Redis caching
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'redis://localhost:6379')
})

@cache.memoize(timeout=300)
def get_legal_research_results(query):
    # Expensive legal research operation
    return research_results
```

### **CDN Configuration**

#### **Cloudflare Setup**
1. Add your domain to Cloudflare
2. Configure DNS settings
3. Enable caching and optimization features
4. Set up SSL/TLS encryption

#### **AWS CloudFront Setup**
```yaml
# CloudFormation template for CloudFront
Resources:
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Origins:
          - DomainName: your-app.onrender.com
            Id: render-origin
            CustomOriginConfig:
              HTTPPort: 443
              OriginProtocolPolicy: https-only
        DefaultCacheBehavior:
          TargetOriginId: render-origin
          ViewerProtocolPolicy: redirect-to-https
          CachePolicyId: 4135ea2d-6df8-44a3-9df3-4b5a84be39ad
```

---

## 📈 **Scaling Considerations**

### **Horizontal Scaling**

#### **Load Balancing**
- Use platform-provided load balancing (Render, Cloud Run)
- Implement session affinity if needed
- Configure health checks

#### **Database Scaling**
- Implement read replicas for read-heavy workloads
- Use connection pooling
- Consider database sharding for large datasets

### **Vertical Scaling**

#### **Resource Allocation**
```yaml
# Google Cloud Run scaling configuration
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  annotations:
    run.googleapis.com/cpu-throttling: "false"
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "100"
    spec:
      containerConcurrency: 80
      containers:
      - image: gcr.io/project/ontario-wills-backend
        resources:
          limits:
            cpu: "2"
            memory: "2Gi"
```

---

## 📞 **Support & Resources**

### **Platform Documentation**
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Render Documentation](https://render.com/docs)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)

### **Community Resources**
- GitHub Issues for bug reports and feature requests
- Stack Overflow for technical questions
- Platform-specific community forums

### **Professional Support**
- Enterprise deployment consultation available
- Custom domain and SSL setup assistance
- Performance optimization services
- 24/7 monitoring and support packages

---

**© 2024 Ontario Legal Tech Solutions. All rights reserved.**

*This deployment guide is current as of Version 3.0. For the most up-to-date information, please refer to the official repository and platform documentation.*

