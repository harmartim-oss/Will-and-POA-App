# Deployment Configuration Guide

## Overview
This guide covers configuration for the Ontario Wills & Power of Attorney App with all integrated services.

## Environment Variables

### Backend Configuration

Create a `.env` file in the backend directory with the following variables:

```bash
# Document Storage
DOCUMENT_STORAGE_PATH=/var/lib/ontario-wills/documents

# Email Service (SendGrid)
SENDGRID_API_KEY=your_sendgrid_api_key_here
FROM_EMAIL=noreply@yourdomain.com
FROM_NAME=Ontario Wills & POA

# Payment Processing (Stripe)
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Digital Signatures (DocuSign)
DOCUSIGN_CLIENT_ID=your_docusign_client_id
DOCUSIGN_CLIENT_SECRET=your_docusign_client_secret
DOCUSIGN_ACCOUNT_ID=your_account_id
DOCUSIGN_BASE_URL=https://demo.docusign.net/restapi

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/ontario_wills

# AI Services (Optional)
OPENAI_API_KEY=your_openai_api_key  # For enhanced AI features
HUGGINGFACE_TOKEN=your_huggingface_token  # For NLP models

# Security
JWT_SECRET_KEY=your_jwt_secret_key_here
ENCRYPTION_KEY=your_32_byte_encryption_key
```

## Frontend Configuration

The frontend automatically detects GitHub Pages deployment. For custom deployments:

1. Edit `src/config/environment.js`
2. Update `API_ENDPOINTS.production` with your backend URL
3. Configure feature flags as needed

## Installation Steps

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model (optional, will use fallback if not available)
python -m spacy download en_core_web_sm

# Run backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Install dependencies
npm install --legacy-peer-deps

# Development
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

## Service Configuration

### SendGrid Email Service

1. Sign up at [SendGrid](https://sendgrid.com/)
2. Create an API key with "Mail Send" permissions
3. Add API key to `.env` file
4. Verify sender email address in SendGrid dashboard

**Without configuration:** Email service will run in simulation mode and log emails to console.

### Stripe Payment Processing

1. Sign up at [Stripe](https://stripe.com/)
2. Get API keys from Dashboard > Developers > API keys
3. Add keys to `.env` file
4. Set up webhook endpoint at `/api/payment/webhook`

**Without configuration:** Payment service will run in simulation mode.

### DocuSign Digital Signatures

1. Sign up at [DocuSign Developer](https://developers.docusign.com/)
2. Create an integration key
3. Configure OAuth settings
4. Add credentials to `.env` file

**Without configuration:** Signature features will not be available.

## Graceful Degradation

All services are designed with graceful degradation:

- **Email Service**: Falls back to simulation mode, logs to console
- **Payment Service**: Falls back to simulation mode, allows testing
- **NLP/AI Services**: Uses fallback text analysis if spaCy not available
- **Storage**: Uses local filesystem by default

## Production Deployment

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Manual Deployment

1. Build frontend: `npm run build`
2. Deploy `dist/` folder to static hosting (GitHub Pages, Netlify, Vercel)
3. Deploy backend to cloud service (Railway, Render, Google Cloud Run)
4. Configure CORS in backend to allow your frontend domain
5. Set all environment variables in hosting platform

## Testing Configuration

```bash
# Test backend
cd backend
pytest

# Test frontend
npm run test

# Test email service
curl -X GET http://localhost:8000/api/email/status

# Test payment service
curl -X GET http://localhost:8000/api/payment/status

# Test storage service
curl -X GET http://localhost:8000/api/storage/list
```

## Monitoring

### Health Checks

- Backend: `GET /health`
- Email Service: `GET /api/email/status`
- Payment Service: `GET /api/payment/status`

### Logs

Backend logs to stdout. Configure log aggregation service for production.

## Security Considerations

1. **Never commit** `.env` files to version control
2. Use **strong encryption keys** (32+ bytes)
3. Enable **HTTPS** in production
4. Configure **rate limiting** on API endpoints
5. Set up **API key rotation** policies
6. Use **environment variables** for all secrets
7. Enable **CORS** only for trusted domains

## Troubleshooting

### Timeout Issues
- **Symptom**: App shows timeout after 45 seconds
- **Solution**: Check network speed, CDN availability, and chunk loading
- **Action**: Hard refresh (Ctrl+Shift+R) or clear browser cache

### Email Not Sending
- **Check**: SendGrid API key configured
- **Check**: Sender email verified in SendGrid
- **Check**: API key has Mail Send permissions
- **Fallback**: Service runs in simulation mode

### Payment Not Processing
- **Check**: Stripe API keys configured
- **Check**: Webhook endpoint configured
- **Check**: Using correct API keys (test vs live)
- **Fallback**: Service runs in simulation mode

### NLP/AI Features Not Working
- **Check**: spaCy installed: `pip install spacy`
- **Check**: Model downloaded: `python -m spacy download en_core_web_sm`
- **Fallback**: Uses basic text analysis

## Support

For issues or questions:
- Check logs: Backend logs to stdout
- Check browser console: Frontend logs to console
- Review API documentation: `/api/docs` when backend running
- Open GitHub issue with logs and error messages

## Updates

To update dependencies:

```bash
# Frontend
npm update

# Backend
pip install -r requirements.txt --upgrade
```

## Backup and Recovery

### Document Storage
- Default location: `/tmp/document_storage` (development)
- Production: Set `DOCUMENT_STORAGE_PATH` to persistent storage
- Backup: Regular backups of storage directory
- Metadata: Stored in `metadata.json` file

### Database
- If using PostgreSQL, set up automated backups
- Export data regularly: `pg_dump`
- Test recovery procedures

---

**Note**: All services are designed to work with or without external dependencies. The application will function in demo mode if external services are not configured.
