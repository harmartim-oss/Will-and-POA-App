# Deployment Guide - Ontario Wills & Power of Attorney Creator

## 🚀 Production Deployment Options

### Option 1: Simple VPS/Server Deployment

#### Requirements:
- Ubuntu 20.04+ or similar Linux distribution
- Python 3.11+
- Node.js 18+
- Nginx (recommended)
- SSL certificate (Let's Encrypt recommended)

#### Step-by-Step Deployment:

1. **Server Setup:**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python 3.11
   sudo apt install python3.11 python3.11-venv python3-pip -y
   
   # Install Node.js 18
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   
   # Install pnpm
   npm install -g pnpm
   
   # Install Nginx
   sudo apt install nginx -y
   ```

2. **Upload Application:**
   ```bash
   # Upload the ontario-wills-complete folder to /var/www/
   sudo mkdir -p /var/www/ontario-wills
   # Copy your files here
   sudo chown -R www-data:www-data /var/www/ontario-wills
   ```

3. **Backend Setup:**
   ```bash
   cd /var/www/ontario-wills/ontario-wills-backend
   
   # Create virtual environment
   python3.11 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install gunicorn
   
   # Set environment variables
   sudo nano /etc/environment
   # Add: OPENAI_API_KEY="your-key-here"
   ```

4. **Frontend Build:**
   ```bash
   cd /var/www/ontario-wills/ontario-wills-frontend
   
   # Install dependencies and build
   pnpm install
   pnpm run build
   
   # Copy to backend static folder
   cp -r dist/* ../ontario-wills-backend/src/static/
   ```

5. **Create Systemd Service:**
   ```bash
   sudo nano /etc/systemd/system/ontario-wills.service
   ```
   
   Add this content:
   ```ini
   [Unit]
   Description=Ontario Wills Application
   After=network.target
   
   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/ontario-wills/ontario-wills-backend
   Environment=PATH=/var/www/ontario-wills/ontario-wills-backend/venv/bin
   Environment=OPENAI_API_KEY=your-key-here
   ExecStart=/var/www/ontario-wills/ontario-wills-backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 src.main:app
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

6. **Configure Nginx:**
   ```bash
   sudo nano /etc/nginx/sites-available/ontario-wills
   ```
   
   Add this configuration:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
       
       location /static/ {
           alias /var/www/ontario-wills/ontario-wills-backend/src/static/;
           expires 1y;
           add_header Cache-Control "public, immutable";
       }
   }
   ```

7. **Enable and Start Services:**
   ```bash
   # Enable Nginx site
   sudo ln -s /etc/nginx/sites-available/ontario-wills /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   
   # Start application service
   sudo systemctl enable ontario-wills
   sudo systemctl start ontario-wills
   sudo systemctl status ontario-wills
   ```

8. **SSL Certificate (Let's Encrypt):**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d your-domain.com
   ```

### Option 2: Docker Deployment

#### Create Dockerfile for Backend:
```dockerfile
# ontario-wills-backend/Dockerfile
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
COPY src/ ./src/

# Create database directory
RUN mkdir -p src/database

EXPOSE 5000

CMD ["python", "src/main.py"]
```

#### Create Docker Compose:
```yaml
# docker-compose.yml
version: '3.8'

services:
  ontario-wills:
    build: ./ontario-wills-backend
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - FLASK_ENV=production
    volumes:
      - ./data:/app/src/database
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - ontario-wills
    restart: unless-stopped
```

#### Deploy with Docker:
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Update application
docker-compose pull
docker-compose up -d --build
```

### Option 3: Cloud Platform Deployment

#### Heroku Deployment:

1. **Prepare for Heroku:**
   ```bash
   # In ontario-wills-backend directory
   echo "web: gunicorn src.main:app" > Procfile
   echo "python-3.11.0" > runtime.txt
   ```

2. **Deploy to Heroku:**
   ```bash
   # Install Heroku CLI and login
   heroku login
   
   # Create app
   heroku create ontario-wills-app
   
   # Set environment variables
   heroku config:set OPENAI_API_KEY=your-key-here
   
   # Deploy
   git init
   git add .
   git commit -m "Initial commit"
   heroku git:remote -a ontario-wills-app
   git push heroku main
   ```

#### AWS Elastic Beanstalk:

1. **Install EB CLI:**
   ```bash
   pip install awsebcli
   ```

2. **Initialize and Deploy:**
   ```bash
   cd ontario-wills-backend
   eb init
   eb create ontario-wills-env
   eb deploy
   ```

#### Google Cloud Platform:

1. **Create app.yaml:**
   ```yaml
   runtime: python311
   
   env_variables:
     OPENAI_API_KEY: "your-key-here"
   
   handlers:
   - url: /static
     static_dir: src/static
   
   - url: /.*
     script: auto
   ```

2. **Deploy:**
   ```bash
   gcloud app deploy
   ```

### Option 4: Serverless Deployment

#### Vercel (Frontend + API):

1. **Configure vercel.json:**
   ```json
   {
     "builds": [
       {
         "src": "ontario-wills-backend/src/main.py",
         "use": "@vercel/python"
       },
       {
         "src": "ontario-wills-frontend/package.json",
         "use": "@vercel/static-build"
       }
     ],
     "routes": [
       { "src": "/api/(.*)", "dest": "ontario-wills-backend/src/main.py" },
       { "src": "/(.*)", "dest": "ontario-wills-frontend/dist/$1" }
     ]
   }
   ```

2. **Deploy:**
   ```bash
   npm install -g vercel
   vercel --prod
   ```

## 🔧 Production Configuration

### Environment Variables:
```bash
# Required
OPENAI_API_KEY=your-openai-api-key
OPENAI_API_BASE=https://api.openai.com/v1

# Optional
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://localhost:6379/0
```

### Database Configuration:

#### PostgreSQL (Recommended for Production):
```python
# In src/main.py, replace SQLite config with:
import os
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/ontario_wills')
```

#### MySQL:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql://user:pass@localhost/ontario_wills')
```

### Security Hardening:

1. **SSL/TLS Configuration:**
   ```nginx
   # In Nginx config
   ssl_protocols TLSv1.2 TLSv1.3;
   ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
   ssl_prefer_server_ciphers off;
   add_header Strict-Transport-Security "max-age=63072000" always;
   ```

2. **Rate Limiting:**
   ```python
   # Install flask-limiter
   pip install Flask-Limiter
   
   # In src/main.py
   from flask_limiter import Limiter
   from flask_limiter.util import get_remote_address
   
   limiter = Limiter(
       app,
       key_func=get_remote_address,
       default_limits=["200 per day", "50 per hour"]
   )
   ```

3. **Input Validation:**
   ```python
   # Install flask-wtf for CSRF protection
   pip install Flask-WTF
   
   # Configure CSRF protection
   from flask_wtf.csrf import CSRFProtect
   csrf = CSRFProtect(app)
   ```

## 📊 Monitoring and Maintenance

### Application Monitoring:

1. **Health Check Endpoint:**
   ```python
   # Add to src/routes/
   @app.route('/health')
   def health_check():
       return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
   ```

2. **Logging Configuration:**
   ```python
   import logging
   from logging.handlers import RotatingFileHandler
   
   if not app.debug:
       file_handler = RotatingFileHandler('logs/ontario_wills.log', maxBytes=10240, backupCount=10)
       file_handler.setFormatter(logging.Formatter(
           '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
       ))
       file_handler.setLevel(logging.INFO)
       app.logger.addHandler(file_handler)
   ```

3. **Performance Monitoring:**
   ```bash
   # Install monitoring tools
   pip install prometheus-flask-exporter
   
   # Add to application
   from prometheus_flask_exporter import PrometheusMetrics
   metrics = PrometheusMetrics(app)
   ```

### Backup Strategy:

1. **Database Backups:**
   ```bash
   # PostgreSQL backup script
   #!/bin/bash
   pg_dump ontario_wills > backup_$(date +%Y%m%d_%H%M%S).sql
   
   # Schedule with cron
   0 2 * * * /path/to/backup_script.sh
   ```

2. **File Backups:**
   ```bash
   # Backup generated documents
   rsync -av /var/www/ontario-wills/documents/ /backup/documents/
   ```

### Updates and Maintenance:

1. **Application Updates:**
   ```bash
   # Pull latest code
   git pull origin main
   
   # Update dependencies
   pip install -r requirements.txt
   
   # Restart service
   sudo systemctl restart ontario-wills
   ```

2. **Security Updates:**
   ```bash
   # System updates
   sudo apt update && sudo apt upgrade -y
   
   # Python package updates
   pip list --outdated
   pip install --upgrade package-name
   ```

## 🚨 Troubleshooting

### Common Production Issues:

1. **Application Won't Start:**
   ```bash
   # Check service status
   sudo systemctl status ontario-wills
   
   # View logs
   sudo journalctl -u ontario-wills -f
   
   # Check permissions
   sudo chown -R www-data:www-data /var/www/ontario-wills
   ```

2. **Database Connection Issues:**
   ```bash
   # Test database connection
   python -c "from src.models.user import db; print('DB connection OK')"
   
   # Check database permissions
   sudo -u postgres psql -c "\l"
   ```

3. **SSL Certificate Issues:**
   ```bash
   # Renew Let's Encrypt certificate
   sudo certbot renew
   
   # Test SSL configuration
   sudo nginx -t
   ```

4. **Performance Issues:**
   ```bash
   # Monitor system resources
   htop
   
   # Check application metrics
   curl http://localhost:8000/metrics
   
   # Analyze logs
   tail -f /var/log/nginx/access.log
   ```

## 📋 Pre-Deployment Checklist

- [ ] Environment variables configured
- [ ] Database setup and migrated
- [ ] SSL certificate installed
- [ ] Backup strategy implemented
- [ ] Monitoring configured
- [ ] Security hardening applied
- [ ] Performance testing completed
- [ ] Legal disclaimers reviewed
- [ ] Terms of service and privacy policy added
- [ ] Professional liability insurance considered

## 🔒 Legal and Compliance

### Required Legal Pages:

1. **Terms of Service**
2. **Privacy Policy**
3. **Legal Disclaimers**
4. **Professional Liability Notice**

### Compliance Considerations:

- **PIPEDA** (Personal Information Protection and Electronic Documents Act)
- **Ontario Law Society** regulations
- **Professional liability** insurance
- **Data retention** policies
- **Cross-border data** transfer restrictions

---

**Remember: This application deals with sensitive legal documents. Ensure proper security, backup, and legal compliance measures are in place before production deployment.**



## 🌟 Render.com Deployment (Recommended)

Render is a modern cloud platform that makes it easy to deploy web applications with automatic builds from GitHub. This is the recommended deployment method for the Ontario Wills application.

### Prerequisites for Render Deployment

1. **GitHub Account** - Your code must be in a GitHub repository
2. **Render Account** - Sign up at https://render.com (free tier available)
3. **OpenAI API Key** - For AI-powered features

### Option A: Full-Stack Deployment (Backend + Frontend Together)

This approach deploys both the Flask backend and React frontend as a single web service.

#### Step 1: Prepare Your Repository

1. **Push to GitHub:**
   ```bash
   cd ontario-wills-complete
   git init
   git add .
   git commit -m "Initial commit for Render deployment"
   git branch -M main
   git remote add origin https://github.com/yourusername/ontario-wills.git
   git push -u origin main
   ```

2. **Ensure files are in place:**
   - `ontario-wills-backend/build.sh` (build script)
   - `ontario-wills-backend/render.yaml` (Render configuration)
   - `ontario-wills-backend/requirements.txt` (with gunicorn)

#### Step 2: Deploy Backend on Render

1. **Create New Web Service:**
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `ontario-wills-backend` directory

2. **Configure Service Settings:**
   ```
   Name: ontario-wills-backend
   Environment: Python 3
   Build Command: ./build.sh
   Start Command: gunicorn --bind 0.0.0.0:$PORT src.main:app
   ```

3. **Set Environment Variables:**
   ```
   OPENAI_API_KEY=your-openai-api-key-here
   OPENAI_API_BASE=https://api.openai.com/v1
   FLASK_ENV=production
   PYTHON_VERSION=3.11.0
   ```

4. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Note your backend URL (e.g., `https://ontario-wills-backend.onrender.com`)

#### Step 3: Deploy Frontend on Render

1. **Create Static Site:**
   - Click "New +" → "Static Site"
   - Connect the same GitHub repository
   - Select the `ontario-wills-frontend` directory

2. **Configure Static Site Settings:**
   ```
   Name: ontario-wills-frontend
   Build Command: pnpm install && pnpm run build
   Publish Directory: dist
   ```

3. **Set Environment Variables:**
   ```
   NODE_VERSION=18
   VITE_API_BASE_URL=https://ontario-wills-backend.onrender.com/api
   ```

4. **Deploy:**
   - Click "Create Static Site"
   - Wait for deployment to complete
   - Your frontend will be available at the provided URL

### Option B: Monolithic Deployment (Recommended for Simplicity)

Deploy the entire application as a single web service with the frontend served by Flask.

#### Step 1: Prepare Monolithic Structure

1. **Build frontend and copy to backend:**
   ```bash
   cd ontario-wills-frontend
   pnpm install && pnpm run build
   cp -r dist/* ../ontario-wills-backend/src/static/
   ```

2. **Commit changes:**
   ```bash
   git add .
   git commit -m "Add built frontend to backend static folder"
   git push
   ```

#### Step 2: Deploy on Render

1. **Create Web Service:**
   - Go to Render dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `ontario-wills-backend` directory as root

2. **Configure Service:**
   ```
   Name: ontario-wills-app
   Environment: Python 3
   Build Command: ./build.sh
   Start Command: gunicorn --bind 0.0.0.0:$PORT src.main:app
   ```

3. **Environment Variables:**
   ```
   OPENAI_API_KEY=your-openai-api-key-here
   OPENAI_API_BASE=https://api.openai.com/v1
   FLASK_ENV=production
   PYTHON_VERSION=3.11.0
   ```

4. **Deploy:**
   - Click "Create Web Service"
   - Your complete application will be available at the provided URL

### Render Configuration Files

The following files have been added to support Render deployment:

#### Backend Configuration (`ontario-wills-backend/render.yaml`):
```yaml
services:
  - type: web
    name: ontario-wills-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT src.main:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: OPENAI_API_KEY
        sync: false
      - key: FLASK_ENV
        value: production
```

#### Frontend Configuration (`ontario-wills-frontend/render.yaml`):
```yaml
services:
  - type: static_site
    name: ontario-wills-frontend
    buildCommand: pnpm install && pnpm run build
    staticPublishPath: ./dist
    envVars:
      - key: NODE_VERSION
        value: 18
```

#### Build Script (`ontario-wills-backend/build.sh`):
```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
mkdir -p src/database
```

### Automatic Deployments

Render automatically deploys your application when you push changes to your GitHub repository:

1. **Push changes:**
   ```bash
   git add .
   git commit -m "Update application"
   git push
   ```

2. **Automatic deployment:**
   - Render detects the push
   - Automatically rebuilds and deploys
   - No manual intervention required

### Custom Domain Setup

1. **Add Custom Domain:**
   - Go to your service settings in Render
   - Click "Custom Domains"
   - Add your domain (e.g., `ontariowills.com`)

2. **Configure DNS:**
   - Add CNAME record pointing to your Render URL
   - Or use Render's nameservers for full DNS management

3. **SSL Certificate:**
   - Render automatically provides SSL certificates
   - HTTPS is enabled by default

### Environment Management

#### Development vs Production

1. **Development Environment:**
   ```bash
   # Local development
   export OPENAI_API_KEY="your-dev-key"
   export FLASK_ENV="development"
   python src/main.py
   ```

2. **Production Environment:**
   - Set environment variables in Render dashboard
   - Use production OpenAI API key
   - Enable production optimizations

#### Environment Variables Best Practices

1. **Never commit API keys to Git**
2. **Use Render's environment variable management**
3. **Set different keys for development and production**
4. **Use Render's secret management for sensitive data**

### Monitoring and Logs

#### Viewing Logs

1. **Real-time logs:**
   - Go to your service in Render dashboard
   - Click "Logs" tab
   - View real-time application logs

2. **Download logs:**
   - Export logs for analysis
   - Set up log retention policies

#### Health Monitoring

1. **Health checks:**
   - Render automatically monitors your service
   - Restarts if the service becomes unhealthy
   - Sends notifications on failures

2. **Metrics:**
   - View CPU and memory usage
   - Monitor response times
   - Track deployment history

### Scaling and Performance

#### Automatic Scaling

1. **Free Tier Limitations:**
   - Services sleep after 15 minutes of inactivity
   - Cold start time when waking up
   - 750 hours per month limit

2. **Paid Plans:**
   - Always-on services
   - Faster performance
   - More resources
   - Custom scaling options

#### Performance Optimization

1. **Database optimization:**
   - Use PostgreSQL for production
   - Enable connection pooling
   - Optimize queries

2. **Static asset optimization:**
   - Enable CDN for static files
   - Compress images and assets
   - Use browser caching

### Troubleshooting Render Deployment

#### Common Issues

1. **Build Failures:**
   ```bash
   # Check build logs in Render dashboard
   # Verify all dependencies are in requirements.txt
   # Ensure build.sh is executable
   ```

2. **Environment Variable Issues:**
   ```bash
   # Verify all required environment variables are set
   # Check variable names match exactly
   # Ensure sensitive variables are marked as secret
   ```

3. **Database Connection Issues:**
   ```bash
   # Verify database directory is created in build script
   # Check file permissions
   # Ensure SQLite database path is correct
   ```

4. **Static File Issues:**
   ```bash
   # Verify frontend build is copied to backend static folder
   # Check static file serving in Flask app
   # Ensure correct file paths
   ```

#### Debug Steps

1. **Check Render logs:**
   - Build logs for build issues
   - Runtime logs for application errors
   - Event logs for service events

2. **Test locally:**
   - Reproduce the issue locally
   - Check environment variable configuration
   - Verify all dependencies are installed

3. **Verify configuration:**
   - Check render.yaml syntax
   - Verify build and start commands
   - Ensure all files are committed to Git

### Render Deployment Checklist

- [ ] Code pushed to GitHub repository
- [ ] `build.sh` script is executable
- [ ] `requirements.txt` includes gunicorn
- [ ] Environment variables configured in Render
- [ ] OpenAI API key set and valid
- [ ] Frontend built and copied to backend static folder
- [ ] Database directory creation in build script
- [ ] Flask app configured for production
- [ ] CORS enabled for cross-origin requests
- [ ] Custom domain configured (optional)
- [ ] SSL certificate verified
- [ ] Health checks passing
- [ ] Logs reviewed for errors

### Cost Considerations

#### Free Tier
- **Web Services:** 750 hours/month
- **Static Sites:** Unlimited
- **Bandwidth:** 100GB/month
- **Build Minutes:** 500/month

#### Paid Plans
- **Starter:** $7/month per service
- **Standard:** $25/month per service
- **Pro:** $85/month per service

#### Cost Optimization Tips
1. Use static site for frontend (free)
2. Combine frontend and backend in single service
3. Optimize build times to reduce build minutes usage
4. Use efficient database queries to reduce CPU usage

---

**Render deployment provides a modern, hassle-free way to deploy your Ontario Wills application with automatic builds, SSL certificates, and monitoring built-in.**


## ☁️ Google Cloud Run Deployment

Google Cloud Run is a fully managed serverless platform that automatically scales your containerized applications. This section provides comprehensive instructions for deploying the Ontario Wills application to Google Cloud Run.

### Prerequisites for Google Cloud Run

1. **Google Cloud Account** - Sign up at https://cloud.google.com
2. **Google Cloud SDK** - Install gcloud CLI
3. **Docker** - For local testing (optional)
4. **Project Setup** - Create a Google Cloud project
5. **Billing Enabled** - Required for Cloud Run
6. **APIs Enabled** - Cloud Run API, Cloud Build API, Container Registry API

### Initial Setup

#### Step 1: Install Google Cloud SDK

**macOS:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

**Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

**Windows:**
Download and run the installer from https://cloud.google.com/sdk/docs/install

#### Step 2: Initialize gcloud

```bash
# Login to Google Cloud
gcloud auth login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

#### Step 3: Configure Authentication

```bash
# Configure Docker to use gcloud as a credential helper
gcloud auth configure-docker
```

### Deployment Options

### Option A: Monolithic Deployment (Recommended)

Deploy both frontend and backend as a single Cloud Run service.

#### Step 1: Prepare Monolithic Structure

```bash
# Build frontend and copy to backend
cd ontario-wills-frontend
npm install && npm run build
cp -r dist/* ../ontario-wills-backend/src/static/

cd ../ontario-wills-backend
```

#### Step 2: Deploy to Cloud Run

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

#### Step 3: Access Your Application

After deployment, you'll receive a URL like:
```
https://ontario-wills-app-xxxxxxxxx-uc.a.run.app
```

### Option B: Separate Services Deployment

Deploy frontend and backend as separate Cloud Run services.

#### Backend Deployment

```bash
cd ontario-wills-backend

# Deploy backend service
gcloud run deploy ontario-wills-backend \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY="your-api-key-here" \
  --set-env-vars FLASK_ENV=production \
  --port 8080
```

#### Frontend Deployment

```bash
cd ontario-wills-frontend

# Set backend URL environment variable
export VITE_API_BASE_URL="https://ontario-wills-backend-xxxxxxxxx-uc.a.run.app/api"

# Deploy frontend service
gcloud run deploy ontario-wills-frontend \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8080
```

### Option C: Using Cloud Build (CI/CD Pipeline)

Set up automated deployments using Cloud Build.

#### Step 1: Setup Cloud Build Triggers

```bash
# Connect your GitHub repository
gcloud alpha builds triggers create github \
  --repo-name=ontario-wills \
  --repo-owner=yourusername \
  --branch-pattern="^main$" \
  --build-config=ontario-wills-backend/cloudbuild.yaml
```

#### Step 2: Push to GitHub

```bash
git add .
git commit -m "Add Cloud Run deployment configuration"
git push origin main
```

Cloud Build will automatically build and deploy your application.

### Docker-based Deployment

For more control over the deployment process, use Docker.

#### Backend Docker Deployment

```bash
cd ontario-wills-backend

# Build Docker image
docker build -t gcr.io/YOUR_PROJECT_ID/ontario-wills-backend .

# Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/ontario-wills-backend

# Deploy to Cloud Run
gcloud run deploy ontario-wills-backend \
  --image gcr.io/YOUR_PROJECT_ID/ontario-wills-backend \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY="your-api-key-here"
```

#### Frontend Docker Deployment

```bash
cd ontario-wills-frontend

# Build Docker image
docker build -t gcr.io/YOUR_PROJECT_ID/ontario-wills-frontend .

# Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/ontario-wills-frontend

# Deploy to Cloud Run
gcloud run deploy ontario-wills-frontend \
  --image gcr.io/YOUR_PROJECT_ID/ontario-wills-frontend \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated
```

### Environment Variables Configuration

#### Setting Environment Variables

```bash
# Set environment variables during deployment
gcloud run deploy ontario-wills-app \
  --source . \
  --set-env-vars OPENAI_API_KEY="your-api-key" \
  --set-env-vars OPENAI_API_BASE="https://api.openai.com/v1" \
  --set-env-vars FLASK_ENV="production" \
  --region us-central1
```

#### Update Environment Variables

```bash
# Update existing service environment variables
gcloud run services update ontario-wills-app \
  --update-env-vars OPENAI_API_KEY="new-api-key" \
  --region us-central1
```

#### Using Secret Manager (Recommended for Production)

```bash
# Create secret
echo "your-openai-api-key" | gcloud secrets create openai-api-key --data-file=-

# Grant Cloud Run access to secret
gcloud secrets add-iam-policy-binding openai-api-key \
  --member="serviceAccount:YOUR_PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Deploy with secret
gcloud run deploy ontario-wills-app \
  --source . \
  --set-secrets OPENAI_API_KEY=openai-api-key:latest \
  --region us-central1
```

### Custom Domain Setup

#### Step 1: Verify Domain Ownership

```bash
# Add domain mapping
gcloud run domain-mappings create \
  --service ontario-wills-app \
  --domain your-domain.com \
  --region us-central1
```

#### Step 2: Configure DNS

Add the following DNS records:
- **Type:** CNAME
- **Name:** your-domain.com
- **Value:** ghs.googlehosted.com

#### Step 3: SSL Certificate

Cloud Run automatically provisions SSL certificates for custom domains.

### Scaling and Performance Configuration

#### Configure Scaling

```bash
# Set minimum and maximum instances
gcloud run services update ontario-wills-app \
  --min-instances 0 \
  --max-instances 10 \
  --region us-central1
```

#### Configure Resources

```bash
# Set CPU and memory limits
gcloud run services update ontario-wills-app \
  --cpu 1 \
  --memory 512Mi \
  --region us-central1
```

#### Configure Concurrency

```bash
# Set maximum concurrent requests per instance
gcloud run services update ontario-wills-app \
  --concurrency 80 \
  --region us-central1
```

### Monitoring and Logging

#### View Logs

```bash
# View service logs
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=ontario-wills-app" \
  --limit 50 \
  --format "table(timestamp,textPayload)"
```

#### Set up Monitoring

```bash
# Enable monitoring
gcloud services enable monitoring.googleapis.com

# Create uptime check
gcloud alpha monitoring uptime create \
  --display-name="Ontario Wills App" \
  --http-check-path="/" \
  --hostname="your-app-url.run.app"
```

### Database Configuration

#### Using Cloud SQL (Recommended for Production)

```bash
# Create Cloud SQL instance
gcloud sql instances create ontario-wills-db \
  --database-version=POSTGRES_13 \
  --tier=db-f1-micro \
  --region=us-central1

# Create database
gcloud sql databases create ontario_wills \
  --instance=ontario-wills-db

# Create user
gcloud sql users create appuser \
  --instance=ontario-wills-db \
  --password=secure-password

# Connect Cloud Run to Cloud SQL
gcloud run services update ontario-wills-app \
  --add-cloudsql-instances YOUR_PROJECT_ID:us-central1:ontario-wills-db \
  --set-env-vars DATABASE_URL="postgresql://appuser:secure-password@/ontario_wills?host=/cloudsql/YOUR_PROJECT_ID:us-central1:ontario-wills-db" \
  --region us-central1
```

### Security Best Practices

#### IAM Configuration

```bash
# Create service account for Cloud Run
gcloud iam service-accounts create ontario-wills-sa \
  --display-name="Ontario Wills Service Account"

# Grant minimal permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:ontario-wills-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"

# Deploy with service account
gcloud run deploy ontario-wills-app \
  --source . \
  --service-account ontario-wills-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com \
  --region us-central1
```

#### VPC Configuration (Optional)

```bash
# Create VPC connector
gcloud compute networks vpc-access connectors create ontario-wills-connector \
  --region us-central1 \
  --subnet default \
  --subnet-project YOUR_PROJECT_ID \
  --min-instances 2 \
  --max-instances 3

# Deploy with VPC connector
gcloud run deploy ontario-wills-app \
  --source . \
  --vpc-connector ontario-wills-connector \
  --region us-central1
```

### Cost Optimization

#### Pricing Model

Cloud Run pricing is based on:
- **CPU allocation time**
- **Memory allocation time**
- **Requests**
- **Networking**

#### Cost Optimization Tips

1. **Set appropriate resource limits:**
   ```bash
   gcloud run services update ontario-wills-app \
     --cpu 0.5 \
     --memory 256Mi \
     --region us-central1
   ```

2. **Configure minimum instances for warm starts:**
   ```bash
   gcloud run services update ontario-wills-app \
     --min-instances 1 \
     --region us-central1
   ```

3. **Use request-based scaling:**
   ```bash
   gcloud run services update ontario-wills-app \
     --concurrency 100 \
     --region us-central1
   ```

### Troubleshooting Cloud Run Deployment

#### Common Issues

1. **Build Failures:**
   ```bash
   # Check build logs
   gcloud builds log BUILD_ID
   
   # Verify Dockerfile syntax
   docker build -t test-image .
   ```

2. **Service Not Starting:**
   ```bash
   # Check service logs
   gcloud logs read "resource.type=cloud_run_revision" --limit 50
   
   # Verify port configuration
   gcloud run services describe ontario-wills-app --region us-central1
   ```

3. **Environment Variable Issues:**
   ```bash
   # List current environment variables
   gcloud run services describe ontario-wills-app \
     --region us-central1 \
     --format="value(spec.template.spec.template.spec.containers[0].env[].name,spec.template.spec.template.spec.containers[0].env[].value)"
   ```

4. **Permission Issues:**
   ```bash
   # Check IAM permissions
   gcloud projects get-iam-policy YOUR_PROJECT_ID
   
   # Verify service account permissions
   gcloud iam service-accounts get-iam-policy ontario-wills-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com
   ```

#### Debug Steps

1. **Local Testing:**
   ```bash
   # Test Docker image locally
   docker build -t ontario-wills-local .
   docker run -p 8080:8080 -e OPENAI_API_KEY="your-key" ontario-wills-local
   ```

2. **Cloud Build Testing:**
   ```bash
   # Submit build manually
   gcloud builds submit --config cloudbuild.yaml .
   ```

3. **Service Health Check:**
   ```bash
   # Check service status
   gcloud run services describe ontario-wills-app --region us-central1
   ```

### Cloud Run Configuration Files

The following files have been added for Google Cloud Run support:

#### Backend Dockerfile
```dockerfile
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
# ... (see full file in project)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 src.main:app
```

#### Frontend Dockerfile
```dockerfile
FROM node:18-alpine as build
# ... build stage
FROM nginx:alpine
# ... production stage with nginx
EXPOSE 8080
```

#### Cloud Build Configuration
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/ontario-wills-backend:$COMMIT_SHA', '.']
  # ... (see full file in project)
```

### Deployment Checklist for Google Cloud Run

- [ ] Google Cloud project created and billing enabled
- [ ] Required APIs enabled (Cloud Run, Cloud Build, Container Registry)
- [ ] gcloud CLI installed and authenticated
- [ ] Environment variables configured (OPENAI_API_KEY)
- [ ] Dockerfile and .dockerignore files created
- [ ] Application configured for port 8080
- [ ] Database configuration updated (if using Cloud SQL)
- [ ] Custom domain configured (optional)
- [ ] Monitoring and logging set up
- [ ] Security best practices implemented
- [ ] Cost optimization settings applied

### Cost Estimates

#### Free Tier
- **2 million requests per month**
- **400,000 GB-seconds of memory**
- **200,000 vCPU-seconds**

#### Typical Monthly Costs (after free tier)
- **Small application:** $5-15/month
- **Medium application:** $15-50/month
- **Large application:** $50-200/month

---

**Google Cloud Run provides enterprise-grade scalability and reliability for your Ontario Wills application with pay-per-use pricing and automatic scaling.**

