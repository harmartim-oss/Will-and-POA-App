# Complete Deployment Guide - Ontario Wills & Power of Attorney Creator v3.0

## 🚀 Overview

This guide provides comprehensive instructions for deploying the enhanced Ontario Wills & Power of Attorney Creator application across multiple platforms. Choose the deployment option that best fits your needs.

---

## 📋 Prerequisites

### Required Software
- **Node.js** 18+ and npm/pnpm
- **Python** 3.9+ with pip
- **Git** for version control
- **Docker** (optional, for containerized deployment)

### Required Accounts & API Keys
- **OpenAI API Key** (required for AI features)
- **Google AI Studio API Key** (optional, for enhanced AI)
- **CanLII API Key** (optional, for legal research)
- **Cloud Storage** (AWS S3, Google Drive, or Dropbox)

---

## 🌐 Deployment Options

### 1. GitHub Pages (Frontend Only) - FREE
**Best for**: Static demos, portfolio showcases
**Limitations**: No backend functionality, no AI features

#### Quick Setup (5 minutes)
```bash
# 1. Fork or clone the repository
git clone https://github.com/yourusername/ontario-wills-enhanced.git
cd ontario-wills-enhanced

# 2. Navigate to frontend
cd ontario-wills-frontend-enhanced

# 3. Install dependencies
npm install

# 4. Configure for GitHub Pages
# Edit package.json to set homepage
npm run build

# 5. Deploy to GitHub Pages
npm run deploy
```

#### Detailed GitHub Pages Setup
1. **Repository Setup**
   ```bash
   # Create new repository on GitHub
   # Clone locally
   git clone https://github.com/yourusername/ontario-wills.git
   cd ontario-wills
   
   # Copy enhanced frontend
   cp -r ontario-wills-frontend-enhanced/* .
   ```

2. **Configuration**
   ```bash
   # Install GitHub Pages deployment tool
   npm install --save-dev gh-pages
   
   # Update package.json
   {
     "homepage": "https://yourusername.github.io/ontario-wills",
     "scripts": {
       "predeploy": "npm run build",
       "deploy": "gh-pages -d dist"
     }
   }
   ```

3. **Environment Setup**
   ```bash
   # Create .env file
   VITE_API_BASE_URL=https://your-backend-url.com/api
   VITE_GITHUB_PAGES=true
   ```

4. **Deploy**
   ```bash
   npm run deploy
   ```

5. **GitHub Settings**
   - Go to repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: gh-pages
   - Your site will be available at: `https://yourusername.github.io/ontario-wills`

---

### 2. Render.com - RECOMMENDED
**Best for**: Full-stack applications, quick deployment
**Cost**: Free tier available, $7/month for production

#### Backend Deployment (10 minutes)
1. **Prepare Repository**
   ```bash
   # Push backend to GitHub
   cd ontario-wills-enhanced
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/ontario-wills-backend.git
   git push -u origin main
   ```

2. **Render Setup**
   - Go to [render.com](https://render.com)
   - Connect GitHub account
   - Create new Web Service
   - Select your repository
   - Configure:
     ```
     Name: ontario-wills-backend
     Environment: Python 3
     Build Command: pip install -r requirements.txt
     Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT src.main:app
     ```

3. **Environment Variables**
   ```
   OPENAI_API_KEY=your_openai_key
   GOOGLE_AI_API_KEY=your_google_ai_key
   FLASK_ENV=production
   DATABASE_URL=postgresql://...
   JWT_SECRET_KEY=your_secret_key
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Note your backend URL: `https://ontario-wills-backend.onrender.com`

#### Frontend Deployment
1. **Static Site Setup**
   ```bash
   # Prepare frontend repository
   cd ontario-wills-frontend-enhanced
   git init
   git add .
   git commit -m "Frontend initial commit"
   git remote add origin https://github.com/yourusername/ontario-wills-frontend.git
   git push -u origin main
   ```

2. **Render Configuration**
   - Create new Static Site
   - Connect repository
   - Configure:
     ```
     Build Command: npm install && npm run build
     Publish Directory: dist
     ```

3. **Environment Variables**
   ```
   VITE_API_BASE_URL=https://ontario-wills-backend.onrender.com/api
   ```

---

### 3. Google Cloud Run - ENTERPRISE
**Best for**: Production applications, enterprise use
**Cost**: Pay-per-use, typically $10-50/month

#### Prerequisites
```bash
# Install Google Cloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
gcloud auth configure-docker
```

#### Backend Deployment
1. **Prepare Application**
   ```bash
   cd ontario-wills-enhanced
   
   # Build Docker image
   docker build -t gcr.io/YOUR_PROJECT_ID/ontario-wills-backend .
   
   # Push to Google Container Registry
   docker push gcr.io/YOUR_PROJECT_ID/ontario-wills-backend
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy ontario-wills-backend \
     --image gcr.io/YOUR_PROJECT_ID/ontario-wills-backend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars OPENAI_API_KEY=your_key,FLASK_ENV=production
   ```

3. **Configure Custom Domain** (Optional)
   ```bash
   gcloud run domain-mappings create \
     --service ontario-wills-backend \
     --domain api.yourwillsapp.com
   ```

#### Frontend Deployment
1. **Build and Deploy**
   ```bash
   cd ontario-wills-frontend-enhanced
   
   # Build for production
   npm run build
   
   # Deploy to Google Cloud Storage + CDN
   gsutil -m cp -r dist/* gs://your-bucket-name/
   
   # Set up Cloud CDN (optional)
   gcloud compute backend-buckets create ontario-wills-frontend \
     --gcs-bucket-name=your-bucket-name
   ```

---

### 4. AWS (Advanced) - ENTERPRISE
**Best for**: Large-scale production, enterprise requirements
**Cost**: Variable, typically $20-100/month

#### Backend (Elastic Beanstalk)
1. **Prepare Application**
   ```bash
   # Install EB CLI
   pip install awsebcli
   
   cd ontario-wills-enhanced
   eb init ontario-wills-backend
   eb create production
   ```

2. **Environment Configuration**
   ```bash
   eb setenv OPENAI_API_KEY=your_key FLASK_ENV=production
   eb deploy
   ```

#### Frontend (S3 + CloudFront)
1. **S3 Setup**
   ```bash
   # Create S3 bucket
   aws s3 mb s3://ontario-wills-frontend
   
   # Build and upload
   cd ontario-wills-frontend-enhanced
   npm run build
   aws s3 sync dist/ s3://ontario-wills-frontend
   ```

2. **CloudFront Distribution**
   ```bash
   # Create CloudFront distribution (via AWS Console)
   # Point to S3 bucket
   # Configure custom domain
   ```

---

### 5. Docker Compose (Local/VPS)
**Best for**: Self-hosting, development, VPS deployment

#### Setup
1. **Create docker-compose.yml**
   ```yaml
   version: '3.8'
   services:
     backend:
       build: ./ontario-wills-enhanced
       ports:
         - "5000:5000"
       environment:
         - OPENAI_API_KEY=${OPENAI_API_KEY}
         - DATABASE_URL=postgresql://postgres:password@db:5432/ontario_wills
       depends_on:
         - db
     
     frontend:
       build: ./ontario-wills-frontend-enhanced
       ports:
         - "3000:80"
       environment:
         - VITE_API_BASE_URL=http://localhost:5000/api
     
     db:
       image: postgres:15
       environment:
         - POSTGRES_DB=ontario_wills
         - POSTGRES_USER=postgres
         - POSTGRES_PASSWORD=password
       volumes:
         - postgres_data:/var/lib/postgresql/data
   
   volumes:
     postgres_data:
   ```

2. **Deploy**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_key" > .env
   
   # Start services
   docker-compose up -d
   ```

---

## 🔧 Configuration Guide

### Environment Variables Reference

#### Backend (.env)
```bash
# Required
OPENAI_API_KEY=sk-...
FLASK_ENV=production
JWT_SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:pass@host:port/dbname
SQLITE_DB_PATH=/app/data/ontario_wills.db

# Optional AI Services
GOOGLE_AI_API_KEY=your-google-ai-key
SPACY_MODEL=en_core_web_lg

# Cloud Storage (choose one)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
S3_BUCKET_NAME=your-bucket

# Legal Research
CANLII_API_KEY=your-canlii-key

# Security
DOCUMENT_ENCRYPTION_KEY=your-encryption-key
SESSION_TIMEOUT=3600

# Application
DEBUG=false
LOG_LEVEL=INFO
MAX_UPLOAD_SIZE=52428800
```

#### Frontend (.env)
```bash
# API Configuration
VITE_API_BASE_URL=https://your-backend-url.com/api
VITE_ENVIRONMENT=production

# Features
VITE_ENABLE_AI_FEATURES=true
VITE_ENABLE_LEGAL_RESEARCH=true
VITE_ENABLE_CLOUD_STORAGE=true

# Analytics (optional)
VITE_GOOGLE_ANALYTICS_ID=GA-...
VITE_SENTRY_DSN=https://...
```

---

## 🔒 Security Configuration

### SSL/TLS Setup
1. **Automatic SSL** (Render, Vercel, Netlify)
   - SSL certificates are automatically provided
   - No additional configuration needed

2. **Custom SSL** (VPS, self-hosted)
   ```bash
   # Using Let's Encrypt with Certbot
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourwillsapp.com
   ```

### Security Headers
```nginx
# Nginx configuration
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
```

---

## 📊 Monitoring & Analytics

### Application Monitoring
1. **Health Checks**
   ```bash
   # Backend health endpoint
   curl https://your-backend-url.com/api/health
   
   # Expected response
   {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}
   ```

2. **Error Tracking**
   ```python
   # Sentry integration (optional)
   import sentry_sdk
   sentry_sdk.init(dsn="your-sentry-dsn")
   ```

### Performance Monitoring
1. **Google Analytics** (Frontend)
   ```javascript
   // Add to index.html
   gtag('config', 'GA-MEASUREMENT-ID');
   ```

2. **Application Insights** (Backend)
   ```python
   # Azure Application Insights
   from applicationinsights import TelemetryClient
   tc = TelemetryClient('your-instrumentation-key')
   ```

---

## 🚨 Troubleshooting

### Common Issues

#### 1. CORS Errors
```python
# Backend: Ensure CORS is properly configured
from flask_cors import CORS
CORS(app, origins=["https://your-frontend-domain.com"])
```

#### 2. Environment Variables Not Loading
```bash
# Check environment variables
printenv | grep OPENAI
echo $VITE_API_BASE_URL
```

#### 3. Database Connection Issues
```python
# Test database connection
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL)
connection = engine.connect()
```

#### 4. Build Failures
```bash
# Clear cache and rebuild
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Performance Optimization

#### Frontend
```bash
# Bundle analysis
npm run build -- --analyze

# Optimize images
npm install --save-dev imagemin-webpack-plugin
```

#### Backend
```python
# Database query optimization
# Use database indexes
# Implement caching with Redis
# Use connection pooling
```

---

## 📞 Support & Maintenance

### Backup Strategy
1. **Database Backups**
   ```bash
   # PostgreSQL backup
   pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
   
   # Automated backups (cron)
   0 2 * * * pg_dump $DATABASE_URL > /backups/backup_$(date +\%Y\%m\%d).sql
   ```

2. **File Storage Backups**
   ```bash
   # S3 backup
   aws s3 sync s3://your-bucket s3://your-backup-bucket
   ```

### Update Procedures
1. **Backend Updates**
   ```bash
   git pull origin main
   pip install -r requirements.txt
   flask db upgrade  # If using migrations
   sudo systemctl restart your-app
   ```

2. **Frontend Updates**
   ```bash
   git pull origin main
   npm install
   npm run build
   # Deploy new build
   ```

### Monitoring Checklist
- [ ] Application health checks
- [ ] Database performance
- [ ] SSL certificate expiry
- [ ] Backup verification
- [ ] Security updates
- [ ] Log analysis
- [ ] User feedback review

---

## 🎯 Production Checklist

### Pre-Deployment
- [ ] Environment variables configured
- [ ] SSL certificates installed
- [ ] Database migrations applied
- [ ] Security headers configured
- [ ] Monitoring tools setup
- [ ] Backup strategy implemented
- [ ] Load testing completed
- [ ] Security audit performed

### Post-Deployment
- [ ] Health checks passing
- [ ] All features functional
- [ ] Performance metrics acceptable
- [ ] Error rates within limits
- [ ] User acceptance testing
- [ ] Documentation updated
- [ ] Team training completed
- [ ] Support procedures documented

---

This comprehensive deployment guide ensures your Ontario Wills & Power of Attorney Creator application is properly deployed, secured, and maintained across any platform you choose.

