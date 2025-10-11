# Quick Start Deployment Guide

## 🚀 Get Started in 5 Minutes

This guide will get your Ontario Wills & POA App running quickly.

## Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- Git

## Option 1: Local Development (Fastest)

### Frontend Only (Static Demo)

```bash
# Clone repository
git clone https://github.com/harmartim-oss/Will-and-POA-App.git
cd Will-and-POA-App

# Install dependencies
npm install --legacy-peer-deps

# Start development server
npm run dev

# Open http://localhost:5173
```

The app will run in demo mode without backend services.

### Full Stack (Frontend + Backend)

**Terminal 1 - Backend:**
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install core dependencies (without optional AI packages)
pip install fastapi uvicorn python-multipart pydantic sqlalchemy

# Start backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
# Install dependencies
npm install --legacy-peer-deps

# Start development server
npm run dev
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

## Option 2: Production Build

### Build Frontend

```bash
npm install --legacy-peer-deps
npm run build
```

Deploy the `dist/` folder to:
- **GitHub Pages**: Already configured, push to `main` branch
- **Netlify**: Drag and drop `dist/` folder
- **Vercel**: Connect repository and deploy

### Deploy Backend

Quick deploy options:

**Railway.app:**
1. Sign up at railway.app
2. New Project → Deploy from GitHub
3. Select repository
4. Railway auto-detects and deploys

**Render.com:**
1. Sign up at render.com
2. New Web Service → Connect repository
3. Build: `cd backend && pip install -r requirements.txt`
4. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Google Cloud Run:**
```bash
gcloud run deploy ontario-wills-api \
  --source ./backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Configuration

### Environment Variables (Optional)

Create `backend/.env` for production features:

```bash
# Email (optional - runs in simulation mode without)
SENDGRID_API_KEY=your_key_here

# Payment (optional - runs in simulation mode without)
STRIPE_SECRET_KEY=your_key_here

# AI Models (optional - uses fallback without)
OPENAI_API_KEY=your_key_here
```

### Frontend Configuration

Edit `src/config/environment.js`:

```javascript
const API_ENDPOINTS = {
  production: 'https://your-backend-url.com/api'
}
```

## Verify Installation

### Frontend
Open http://localhost:5173 and verify:
- ✅ Page loads within 45 seconds
- ✅ Navigation works
- ✅ Document creation forms display
- ✅ No console errors

### Backend
```bash
# Health check
curl http://localhost:8000/health

# Should return: {"status": "healthy", ...}
```

### Services Status
```bash
# Check email service
curl http://localhost:8000/api/email/status

# Check payment service  
curl http://localhost:8000/api/payment/status

# Check storage
curl http://localhost:8000/api/storage/list
```

## Common Issues

### Frontend won't build
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

### Backend import errors
```bash
# Install minimum dependencies
pip install fastapi uvicorn python-multipart pydantic

# Or install all
pip install -r requirements.txt
```

### Timeout on deployment
- Increase timeout in hosting platform settings
- Check network connectivity
- Verify assets are loading (F12 → Network tab)

### Services not working
All services have graceful fallback:
- **Email**: Logs to console instead of sending
- **Payment**: Simulates transactions
- **AI**: Uses basic text analysis

This is normal and expected without API keys configured.

## Development Tips

### Hot Reload
Both frontend and backend support hot reload:
- Frontend: Changes reload automatically
- Backend: Add `--reload` flag to uvicorn

### Debug Mode
Enable debug logging:
```bash
# Frontend: Check browser console (F12)
# Backend: Logs print to terminal
```

### API Testing
Use built-in Swagger UI:
- Open http://localhost:8000/api/docs
- Try endpoints interactively
- No authentication needed for testing

## Production Checklist

Before deploying to production:

- [ ] Set `NODE_ENV=production`
- [ ] Configure backend URL in frontend config
- [ ] Add SSL certificate (HTTPS)
- [ ] Set up environment variables
- [ ] Configure CORS for your domain
- [ ] Enable rate limiting
- [ ] Set up error monitoring
- [ ] Configure backups for documents
- [ ] Test all critical paths
- [ ] Set up health check monitoring

## Security Notes

⚠️ **Development Mode:**
- Runs without authentication
- Services in simulation mode
- Not suitable for production

✅ **Production Mode:**
- Configure authentication
- Use real API keys
- Enable HTTPS
- Set up proper CORS
- Use strong encryption keys

## Getting Help

**Documentation:**
- Full API docs: `API_DOCUMENTATION.md`
- Deployment guide: `DEPLOYMENT_CONFIGURATION.md`
- Interactive docs: `/api/docs` (when running)

**Troubleshooting:**
1. Check browser console (F12)
2. Check backend logs
3. Verify all dependencies installed
4. Check GitHub issues

**Support:**
- GitHub Issues: Report bugs and ask questions
- API Docs: http://localhost:8000/api/docs
- Code: Well-commented for self-service

## Next Steps

After basic deployment:

1. **Configure Services:**
   - Add SendGrid key for email
   - Add Stripe keys for payments
   - Download spaCy models for better AI

2. **Customize:**
   - Update branding in components
   - Modify templates in backend
   - Adjust pricing in payment service

3. **Monitor:**
   - Set up logging
   - Configure alerts
   - Track usage metrics

4. **Scale:**
   - Add database for persistence
   - Set up CDN for assets
   - Configure load balancing

## Success!

Your Ontario Wills & POA App should now be running!

- **Demo**: Works immediately without configuration
- **Development**: Full stack with local services
- **Production**: Deploy frontend to static host, backend to cloud

## Quick Commands Reference

```bash
# Development
npm run dev                          # Start frontend dev server
uvicorn main:app --reload            # Start backend dev server

# Production
npm run build                        # Build frontend
python -m uvicorn main:app          # Start backend production

# Testing
npm run test                         # Run frontend tests
pytest                               # Run backend tests

# Maintenance
npm update                           # Update frontend deps
pip install -r requirements.txt -U   # Update backend deps
```

---

**Ready to go!** The application is designed to work out of the box with sensible defaults and graceful degradation.
