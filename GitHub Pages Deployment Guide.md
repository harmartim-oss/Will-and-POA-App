# GitHub Pages Deployment Guide
## Ontario Wills & Power of Attorney Creator

This guide will walk you through deploying the Ontario Wills & Power of Attorney Creator application to GitHub Pages for the frontend, with a separate backend deployment.

## 🎯 Overview

GitHub Pages is perfect for hosting the React frontend as a static site, while the Flask backend can be deployed to services like Render, Google Cloud Run, or Heroku. This setup provides:

- **Free frontend hosting** on GitHub Pages
- **Custom domain support** with automatic HTTPS
- **Automatic deployments** from GitHub repository
- **Global CDN** for fast loading times
- **Version control integration** with GitHub

## 📋 Prerequisites

- GitHub account
- Git installed locally
- Node.js and npm/pnpm installed
- Backend deployed to a cloud service (Render, Google Cloud Run, etc.)

## 🚀 Quick Deployment (10 Minutes)

### Step 1: Prepare Your Repository

1. **Create a new GitHub repository:**
   ```bash
   # Create repository on GitHub (public repository required for free GitHub Pages)
   # Repository name: ontario-wills-app
   ```

2. **Clone and setup locally:**
   ```bash
   git clone https://github.com/yourusername/ontario-wills-app.git
   cd ontario-wills-app
   
   # Copy the enhanced application files
   cp -r /path/to/ontario-wills-frontend-enhanced/* .
   ```

3. **Update configuration:**
   - Edit `package.json` and update the `homepage` field:
     ```json
     "homepage": "https://yourusername.github.io/ontario-wills-app"
     ```
   
   - Edit `src/config/environment.js` and update the production API URL:
     ```javascript
     const API_ENDPOINTS = {
       production: 'https://your-backend-url.com/api'  // Your deployed backend URL
     };
     ```

### Step 2: Install Dependencies and Build

```bash
# Install dependencies
npm install
# or
pnpm install

# Install gh-pages for deployment
npm install --save-dev gh-pages
# or
pnpm add -D gh-pages

# Build the application
npm run build
# or
pnpm run build
```

### Step 3: Deploy to GitHub Pages

```bash
# Add, commit, and push to GitHub
git add .
git commit -m "Initial commit: Ontario Wills App"
git push origin main

# Deploy to GitHub Pages
npm run deploy
# or
pnpm run deploy
```

### Step 4: Configure GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under **Source**, select **Deploy from a branch**
4. Select **gh-pages** branch and **/ (root)** folder
5. Click **Save**

Your app will be available at: `https://yourusername.github.io/ontario-wills-app`

## 🔧 Detailed Configuration

### Frontend Configuration

The application is pre-configured for GitHub Pages deployment with:

#### 1. Package.json Configuration
```json
{
  "homepage": "https://yourusername.github.io/ontario-wills-app",
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d dist"
  }
}
```

#### 2. Vite Configuration (vite.config.js)
```javascript
export default defineConfig({
  base: process.env.NODE_ENV === 'production' ? '/ontario-wills-app/' : '/',
  build: {
    outDir: 'dist',
    assetsDir: 'assets'
  }
})
```

#### 3. Router Configuration
```javascript
<Router basename={config.githubPages.basePath}>
```

#### 4. Environment Configuration
The app automatically detects GitHub Pages deployment and adjusts:
- API endpoints
- Feature availability (some features disabled for demo)
- Offline mode for demonstration

### SPA Routing Support

GitHub Pages doesn't natively support SPA routing. The application includes:

1. **404.html** - Redirects all routes to index.html
2. **Router configuration** - Handles GitHub Pages routing
3. **Base path handling** - Correctly handles subdirectory deployment

### Backend Integration

#### CORS Configuration
The Flask backend is configured to accept requests from GitHub Pages:

```python
CORS(app, origins=[
    'https://*.github.io',
    'https://*.githubpages.com',
    # ... other origins
])
```

#### API Endpoints
Update your backend URL in `src/config/environment.js`:

```javascript
const API_ENDPOINTS = {
  production: 'https://your-backend-domain.com/api'
};
```

## 🌐 Custom Domain Setup

### Option 1: GitHub Pages Custom Domain

1. **Purchase a domain** (GoDaddy, Namecheap, etc.)

2. **Configure DNS:**
   - **CNAME record**: `www` → `yourusername.github.io`
   - **A records** for apex domain:
     ```
     185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153
     ```

3. **Configure in GitHub:**
   - Go to repository **Settings** → **Pages**
   - Enter your custom domain in **Custom domain**
   - Enable **Enforce HTTPS**

4. **Add CNAME file:**
   ```bash
   echo "yourdomain.com" > public/CNAME
   ```

### Option 2: Subdomain Setup

For a subdomain like `app.yourdomain.com`:

1. **DNS Configuration:**
   - **CNAME record**: `app` → `yourusername.github.io`

2. **GitHub Configuration:**
   - Custom domain: `app.yourdomain.com`

## 🔄 Automated Deployment

### GitHub Actions Workflow

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
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
      
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
        
    - name: Install dependencies
      run: npm ci
      
    - name: Build
      run: npm run build
      
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      if: github.ref == 'refs/heads/main'
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./dist
```

This automatically deploys when you push to the main branch.

## 🛠️ Development Workflow

### Local Development
```bash
# Start development server
npm run dev
# or
pnpm run dev

# Access at http://localhost:3000
```

### Testing Before Deployment
```bash
# Build and preview
npm run build
npm run preview
# or
pnpm run build
pnpm run preview
```

### Deploy Updates
```bash
# Make changes, then:
git add .
git commit -m "Update: description of changes"
git push origin main

# Deploy to GitHub Pages
npm run deploy
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Blank Page After Deployment
- **Cause**: Incorrect base path configuration
- **Solution**: Check `vite.config.js` base path and `package.json` homepage

#### 2. 404 Errors on Refresh
- **Cause**: Missing SPA routing support
- **Solution**: Ensure `404.html` is in the `public` folder

#### 3. API Calls Failing
- **Cause**: CORS issues or incorrect API URL
- **Solution**: 
  - Check backend CORS configuration
  - Verify API URL in `src/config/environment.js`
  - Ensure backend is deployed and accessible

#### 4. Assets Not Loading
- **Cause**: Incorrect asset paths
- **Solution**: Check Vite configuration and ensure assets are in the correct directory

### Debug Steps

1. **Check GitHub Pages Status:**
   - Repository Settings → Pages
   - Look for deployment status and errors

2. **Check Browser Console:**
   - Look for JavaScript errors
   - Check network tab for failed requests

3. **Verify Configuration:**
   - Confirm all URLs and paths are correct
   - Test API endpoints directly

## 📊 Performance Optimization

### Build Optimization
The Vite configuration includes:
- **Code splitting** for better loading
- **Asset optimization** for smaller files
- **Tree shaking** to remove unused code

### CDN Benefits
GitHub Pages provides:
- **Global CDN** for fast loading
- **Automatic compression** (gzip)
- **HTTP/2 support**
- **Free SSL certificates**

## 🔒 Security Considerations

### GitHub Pages Limitations
- **Static hosting only** - no server-side processing
- **Public repositories** required for free tier
- **No environment variables** - use build-time configuration

### Best Practices
- **Separate sensitive data** - keep API keys in backend
- **Use HTTPS** - always enable SSL
- **Validate inputs** - client-side validation only for UX

## 📈 Monitoring and Analytics

### GitHub Pages Analytics
- Built-in traffic analytics in repository insights
- Integration with Google Analytics possible

### Performance Monitoring
- Use browser dev tools
- Consider tools like Lighthouse for performance audits

## 🎯 Next Steps

After successful deployment:

1. **Test all functionality** on the live site
2. **Set up monitoring** for uptime and performance
3. **Configure analytics** if needed
4. **Set up automated backups** of your repository
5. **Document your deployment process** for team members

## 📞 Support

If you encounter issues:

1. **Check GitHub Pages documentation**
2. **Review repository settings**
3. **Test locally first**
4. **Check browser console for errors**
5. **Verify backend connectivity**

Your Ontario Wills & Power of Attorney Creator is now ready for professional use on GitHub Pages! 🎉

