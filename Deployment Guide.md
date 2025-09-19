# Deployment Guide
## Ontario Wills & Power of Attorney Creator - Enhanced Version

This comprehensive guide covers all deployment options for the enhanced Ontario Wills & Power of Attorney Creator application.

## 🎯 Deployment Options Overview

| Platform | Frontend | Backend | Cost | Complexity | Best For |
|----------|----------|---------|------|------------|----------|
| **GitHub Pages + Render** | GitHub Pages | Render | Free/Low | Easy | Demos, MVPs |
| **Google Cloud Run** | Cloud Run | Cloud Run | Pay-per-use | Medium | Production |
| **Render (Full-stack)** | Render | Render | $7+/month | Easy | Small business |
| **Heroku** | Heroku | Heroku | $5+/month | Easy | Rapid prototyping |
| **Netlify + Railway** | Netlify | Railway | Free/Low | Easy | Jamstack approach |

## 🌐 GitHub Pages Deployment (Recommended for Frontend)

Perfect for hosting the React frontend with a separate backend service.

### Quick Setup (10 Minutes)

1. **Create GitHub Repository:**
   ```bash
   # Create public repository on GitHub
   git clone https://github.com/yourusername/ontario-wills-app.git
   cd ontario-wills-app
   
   # Copy frontend files
   cp -r ontario-wills-frontend-enhanced/* .
   ```

2. **Configure Package.json:**
   ```json
   {
     "homepage": "https://yourusername.github.io/ontario-wills-app",
     "scripts": {
       "predeploy": "npm run build",
       "deploy": "gh-pages -d dist"
     }
   }
   ```

3. **Install and Deploy:**
   ```bash
   npm install
   npm install --save-dev gh-pages
   npm run build
   npm run deploy
   ```

4. **Enable GitHub Pages:**
   - Repository Settings → Pages
   - Source: Deploy from branch
   - Branch: gh-pages

### Features:
- ✅ **Free hosting** for static frontend
- ✅ **Custom domain** support with automatic SSL
- ✅ **Global CDN** for fast loading worldwide
- ✅ **Automatic deployments** from GitHub pushes
- ✅ **SPA routing** support included
- ✅ **Version control** integration

### Custom Domain Setup:
```bash
# Add CNAME file
echo "yourdomain.com" > public/CNAME

# DNS Configuration:
# CNAME: www → yourusername.github.io
# A records: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
```

## ☁️ Google Cloud Run Deployment

Enterprise-grade deployment with auto-scaling and pay-per-use pricing.

### Backend Deployment

1. **Setup Google Cloud:**
   ```bash
   # Install Google Cloud CLI
   gcloud auth login
   gcloud config set project your-project-id
   ```

2. **Deploy Backend:**
   ```bash
   cd ontario-wills-enhanced
   
   # Build and deploy
   gcloud run deploy ontario-wills-api \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

3. **Environment Variables:**
   ```bash
   gcloud run services update ontario-wills-api \
     --set-env-vars="SECRET_KEY=your-secret-key,OPENAI_API_KEY=your-openai-key"
   ```

### Frontend Deployment (Optional)

```bash
cd ontario-wills-frontend-enhanced

# Build for production
npm run build

# Deploy to Cloud Run
gcloud run deploy ontario-wills-frontend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Features:
- ✅ **Auto-scaling** from 0 to 1000+ instances
- ✅ **Pay-per-use** pricing model
- ✅ **Global load balancing**
- ✅ **Automatic SSL** certificates
- ✅ **Container-based** deployment
- ✅ **CI/CD integration** with Cloud Build

## 🚀 Render Deployment

Simple, developer-friendly platform with great free tier.

### Full-Stack Deployment

1. **Connect GitHub Repository:**
   - Go to render.com
   - Connect your GitHub account
   - Select ontario-wills repository

2. **Backend Service:**
   - Create new Web Service
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn src.main:app`
   - Environment: Python 3

3. **Frontend Service (Optional):**
   - Create new Static Site
   - Build Command: `npm run build`
   - Publish Directory: `dist`

### Environment Variables:
```
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
DATABASE_URL=postgresql://... (auto-provided)
```

### Features:
- ✅ **Free tier** with 750 hours/month
- ✅ **Automatic deployments** from GitHub
- ✅ **Built-in SSL** certificates
- ✅ **Database hosting** included
- ✅ **Easy scaling** options

## 🔧 Advanced Configuration

### Environment-Specific Settings

#### Development
```javascript
// src/config/environment.js
const config = {
  apiBaseUrl: 'http://localhost:5000/api',
  features: {
    enableAIAnalysis: true,
    enableESignature: true,
    enableLawyerReview: true
  }
};
```

#### Production (GitHub Pages)
```javascript
const config = {
  apiBaseUrl: 'https://your-backend.render.com/api',
  features: {
    enableAIAnalysis: true,
    enableESignature: false, // Disabled for demo
    enableLawyerReview: false // Disabled for demo
  }
};
```

### Database Configuration

#### SQLite (Development)
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
```

#### PostgreSQL (Production)
```python
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
```

### CORS Configuration

```python
CORS(app, origins=[
    'http://localhost:3000',
    'https://*.github.io',
    'https://*.render.com',
    'https://*.run.app',
    'https://yourdomain.com'
])
```

## 🔄 CI/CD Pipeline

### GitHub Actions for Automated Deployment

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Application

on:
  push:
    branches: [ main ]

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-node@v3
      with:
        node-version: '18'
    - run: npm ci
    - run: npm run build
    - uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./dist

  deploy-backend:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to Render
      run: |
        curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
```

## 🛡️ Security Best Practices

### Environment Variables
```bash
# Never commit these to version control
SECRET_KEY=your-super-secret-key
JWT_SECRET_KEY=your-jwt-secret
OPENAI_API_KEY=your-openai-api-key
DATABASE_URL=your-database-url
```

### HTTPS Configuration
- Always use HTTPS in production
- Enable HSTS headers
- Use secure cookie settings

### API Security
```python
# Rate limiting
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

## 📊 Monitoring and Analytics

### Application Monitoring
- **Render**: Built-in metrics and logs
- **Google Cloud**: Cloud Monitoring and Logging
- **GitHub Pages**: Repository insights

### Error Tracking
```javascript
// Frontend error tracking
window.addEventListener('error', (event) => {
  console.error('Application error:', event.error);
  // Send to monitoring service
});
```

### Performance Monitoring
```python
# Backend performance monitoring
import time
from flask import request

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time
    print(f"Request to {request.path} took {duration:.2f}s")
    return response
```

## 🔍 Troubleshooting

### Common Issues

#### 1. CORS Errors
```python
# Fix: Update CORS configuration
CORS(app, origins=['https://yourdomain.github.io'])
```

#### 2. Build Failures
```bash
# Fix: Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### 3. Database Connection Issues
```python
# Fix: Check DATABASE_URL format
# PostgreSQL: postgresql://user:pass@host:port/db
# SQLite: sqlite:///path/to/db.sqlite
```

#### 4. API Endpoint Not Found
```javascript
// Fix: Check API base URL configuration
const apiBaseUrl = 'https://your-backend.render.com/api';
```

### Debug Commands

```bash
# Check deployment status
curl -I https://yourdomain.github.io/ontario-wills-app

# Test API endpoints
curl https://your-backend.render.com/api/health

# Check build logs
npm run build --verbose

# Test locally
npm run dev
```

## 📈 Scaling Considerations

### Frontend Scaling
- **GitHub Pages**: Automatic global CDN
- **Render Static Sites**: Global CDN included
- **Google Cloud Run**: Auto-scaling frontend

### Backend Scaling
- **Render**: Easy vertical and horizontal scaling
- **Google Cloud Run**: Automatic scaling 0-1000+ instances
- **Database**: Consider managed database services

### Performance Optimization
```javascript
// Code splitting
const LazyComponent = React.lazy(() => import('./Component'));

// Image optimization
<img src="image.webp" alt="Description" loading="lazy" />

// Bundle analysis
npm run build -- --analyze
```

## 💰 Cost Estimation

### GitHub Pages + Render
- **Frontend**: Free (GitHub Pages)
- **Backend**: $0-7/month (Render free tier + paid)
- **Database**: Included with Render
- **Total**: $0-7/month

### Google Cloud Run
- **Frontend**: $0-5/month (depending on traffic)
- **Backend**: $0-20/month (pay-per-use)
- **Database**: $10-50/month (Cloud SQL)
- **Total**: $10-75/month

### Full Render
- **Full-stack**: $7-25/month
- **Database**: Included
- **SSL**: Included
- **Total**: $7-25/month

## 🎯 Deployment Checklist

### Pre-Deployment
- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] CORS settings updated
- [ ] API endpoints tested
- [ ] Build process verified

### Post-Deployment
- [ ] Health check endpoints working
- [ ] Frontend loads correctly
- [ ] API calls successful
- [ ] Authentication working
- [ ] Document generation functional
- [ ] SSL certificate active
- [ ] Custom domain configured (if applicable)

### Testing
- [ ] Create test user account
- [ ] Generate sample documents
- [ ] Test AI analysis features
- [ ] Verify export functionality
- [ ] Check mobile responsiveness
- [ ] Test error handling

## 📞 Support and Resources

### Documentation
- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [Render Documentation](https://render.com/docs)
- [Google Cloud Run Docs](https://cloud.google.com/run/docs)

### Community
- GitHub Issues for bug reports
- Stack Overflow for technical questions
- Platform-specific support channels

### Professional Support
- Consider managed hosting for enterprise needs
- Professional deployment services available
- Custom domain and SSL setup assistance

## 🎉 Conclusion

Your enhanced Ontario Wills & Power of Attorney Creator is now ready for professional deployment! Choose the deployment option that best fits your needs:

- **GitHub Pages + Render**: Best for demos and small projects
- **Google Cloud Run**: Best for enterprise and high-traffic applications
- **Render Full-stack**: Best for simplicity and rapid deployment

All deployment options include the enhanced features:
- Advanced AI analysis and suggestions
- Professional document generation
- User authentication and document versioning
- External service integrations
- Modern, responsive UI/UX

Happy deploying! 🚀

