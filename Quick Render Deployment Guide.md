# Quick Render Deployment Guide

## 🚀 Deploy to Render in 5 Minutes

### Prerequisites
- GitHub account
- Render account (free at https://render.com)
- OpenAI API key

### Step 1: Push to GitHub
```bash
cd ontario-wills-complete
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/ontario-wills.git
git push -u origin main
```

### Step 2: Deploy Backend
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Select `ontario-wills-backend` folder
5. Configure:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT src.main:app`
6. Add environment variables:
   - `OPENAI_API_KEY`: your-api-key
   - `PYTHON_VERSION`: 3.11.0
7. Click "Create Web Service"

### Step 3: Deploy Frontend (Optional - for separate deployment)
1. Click "New +" → "Static Site"
2. Connect same GitHub repo
3. Select `ontario-wills-frontend` folder
4. Configure:
   - **Build Command:** `pnpm install && pnpm run build`
   - **Publish Directory:** `dist`
5. Add environment variable:
   - `VITE_API_BASE_URL`: your-backend-url/api
6. Click "Create Static Site"

### Step 4: Access Your App
Your application will be live at the provided Render URL!

## 🔄 Automatic Updates
Every time you push to GitHub, Render automatically rebuilds and deploys your app.

## 💡 Pro Tips
- Use the monolithic deployment (backend serves frontend) for simplicity
- Free tier includes 750 hours/month
- Custom domains available
- SSL certificates included automatically

For detailed instructions, see `DEPLOYMENT_GUIDE.md`.

