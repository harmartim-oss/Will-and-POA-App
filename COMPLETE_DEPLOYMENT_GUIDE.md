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

