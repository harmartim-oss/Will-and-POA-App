# Quick Start Guide - Ontario Wills & Power of Attorney Creator v3.0

## 🚀 **Get Your Legal Document Platform Running in Minutes**

This guide will get you up and running with the Ontario Wills & Power of Attorney Creator in the fastest way possible.

---

## ⚡ **5-Minute GitHub Pages Deployment**

### **Step 1: Fork the Repository**
1. Go to the GitHub repository
2. Click "Fork" to create your own copy
3. Clone your fork locally:
```bash
git clone https://github.com/YOUR-USERNAME/ontario-wills-app.git
cd ontario-wills-app
```

### **Step 2: Configure for GitHub Pages**
1. Edit `frontend/vite.config.js` - update the base path:
```javascript
base: process.env.NODE_ENV === 'production' ? '/ontario-wills-app/' : '/',
```

2. Edit `frontend/package.json` - update homepage:
```json
"homepage": "https://YOUR-USERNAME.github.io/ontario-wills-app",
```

### **Step 3: Enable GitHub Pages**
1. Go to your repository settings on GitHub
2. Navigate to "Pages" section
3. Select "GitHub Actions" as the source
4. The deployment will start automatically

### **Step 4: Configure Environment Variables**
1. Go to repository Settings → Environments → github-pages
2. Add environment variables:
   - `VITE_API_BASE_URL`: `https://ontario-wills-backend.onrender.com`
   - `VITE_GITHUB_PAGES`: `true`

**🎉 Your frontend is now live at: `https://YOUR-USERNAME.github.io/ontario-wills-app`**

---

## 🎨 **10-Minute Render Deployment (Full Stack)**

### **Step 1: Connect to Render**
1. Go to [render.com](https://render.com) and sign up
2. Connect your GitHub account
3. Select your forked repository

### **Step 2: Deploy Backend**
1. Create a new "Web Service"
2. Select your repository
3. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT src.main:app`
   - **Environment**: `Python 3`

### **Step 3: Set Environment Variables**
Add these environment variables in Render:
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
JWT_SECRET_KEY=your-jwt-secret
```

### **Step 4: Deploy Frontend**
1. Create a new "Static Site"
2. Configure:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Publish Directory**: `dist`

### **Step 5: Connect Frontend to Backend**
Add environment variable to frontend service:
```
VITE_API_BASE_URL=https://your-backend-service.onrender.com
```

**🎉 Your full application is now live with both frontend and backend!**

---

## ☁️ **15-Minute Google Cloud Run Deployment**

### **Step 1: Set Up Google Cloud**
```bash
# Install Google Cloud CLI
# https://cloud.google.com/sdk/docs/install

# Authenticate and set project
gcloud auth login
gcloud config set project YOUR-PROJECT-ID

# Enable required APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
```

### **Step 2: Deploy Backend**
```bash
cd backend

# Deploy to Cloud Run
gcloud run deploy ontario-wills-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FLASK_ENV=production,OPENAI_API_KEY=your-key
```

### **Step 3: Deploy Frontend**
```bash
cd ../frontend

# Update environment configuration
echo "VITE_API_BASE_URL=https://ontario-wills-backend-HASH.a.run.app" > .env.production

# Deploy to Cloud Run
gcloud run deploy ontario-wills-frontend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**🎉 Your enterprise-grade application is now running on Google Cloud!**

---

## 💻 **Local Development Setup**

### **Prerequisites**
- Node.js 18+ and npm/pnpm
- Python 3.11+ and pip
- Git

### **Backend Setup (5 minutes)**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run development server
python src/main.py
```

### **Frontend Setup (3 minutes)**
```bash
cd frontend

# Install dependencies
npm install  # or pnpm install

# Set up environment
cp .env.example .env.local
# Edit .env.local with backend URL

# Start development server
npm run dev
```

**🎉 Your local development environment is ready!**

---

## 🔑 **Required API Keys**

### **Essential (Required)**
- **OpenAI API Key**: Get from [platform.openai.com](https://platform.openai.com/api-keys)
  - Used for AI-powered document analysis and suggestions
  - Free tier available, pay-per-use pricing

### **Optional (Enhanced Features)**
- **CanLII API Key**: Get from [canlii.org](https://www.canlii.org/en/info/api/)
  - Used for legal research and case law access
  - Free for non-commercial use

- **Google AI Studio Key**: Get from [aistudio.google.com](https://aistudio.google.com/)
  - Used as backup AI provider
  - Free tier available

---

## 🎯 **Configuration Examples**

### **Frontend Environment (.env.local)**
```env
# Development
VITE_API_BASE_URL=http://localhost:5000
VITE_GITHUB_PAGES=false
VITE_ENABLE_DEBUG=true

# Production (GitHub Pages)
VITE_API_BASE_URL=https://ontario-wills-backend.onrender.com
VITE_GITHUB_PAGES=true
VITE_ENABLE_DEBUG=false
```

### **Backend Environment (.env)**
```env
# Development
FLASK_ENV=development
SECRET_KEY=dev-secret-key
DATABASE_URL=sqlite:///ontario_wills.db
OPENAI_API_KEY=sk-your-openai-key-here
JWT_SECRET_KEY=jwt-secret-key
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Production
FLASK_ENV=production
SECRET_KEY=secure-production-secret
DATABASE_URL=postgresql://user:pass@host:port/dbname
OPENAI_API_KEY=sk-your-openai-key-here
JWT_SECRET_KEY=secure-jwt-secret
CORS_ORIGINS=https://yourdomain.com
```

---

## 🔧 **Troubleshooting Common Issues**

### **GitHub Pages Issues**

**Problem**: 404 errors on page refresh
**Solution**: The 404.html file handles SPA routing automatically

**Problem**: API calls failing
**Solution**: Check CORS configuration and ensure backend is deployed

### **Render Issues**

**Problem**: Build failures
**Solution**: Check build logs and verify all dependencies are listed

**Problem**: Environment variables not working
**Solution**: Ensure variables are set in Render dashboard, not in code

### **Local Development Issues**

**Problem**: Backend won't start
**Solution**: 
```bash
# Check Python version
python --version  # Should be 3.11+

# Activate virtual environment
source venv/bin/activate

# Install dependencies again
pip install -r requirements.txt
```

**Problem**: Frontend won't start
**Solution**:
```bash
# Check Node version
node --version  # Should be 18+

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## 📊 **Testing Your Deployment**

### **Frontend Tests**
1. Visit your deployed URL
2. Check that the landing page loads with animations
3. Try creating a new document
4. Verify responsive design on mobile

### **Backend Tests**
1. Check API health: `GET /api/health`
2. Test authentication: `POST /api/auth/register`
3. Verify CORS: Check browser console for errors
4. Test AI integration: Create a document and check for suggestions

### **Full Integration Tests**
1. Create a user account
2. Start document creation wizard
3. Complete all steps with AI suggestions
4. Generate and download a document
5. Verify document formatting and content

---

## 🎉 **You're Ready to Go!**

Your Ontario Wills & Power of Attorney Creator is now deployed and ready to help users create professional legal documents with AI assistance.

### **Next Steps**
1. **Customize branding**: Update colors, logos, and content
2. **Add custom domain**: Configure your own domain name
3. **Enable analytics**: Set up Google Analytics for usage tracking
4. **Monitor performance**: Set up error tracking and monitoring

### **Need Help?**
- Check the complete documentation in `docs/`
- Review troubleshooting guides
- Open GitHub issues for bugs or questions
- Contact support for professional assistance

**🚀 Start creating professional legal documents with AI today!**

