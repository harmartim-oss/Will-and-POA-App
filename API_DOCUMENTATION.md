# API Documentation

## Base URLs

- **Development**: `http://localhost:8000`
- **Production**: Configure in `src/config/environment.js`

## Interactive Documentation

When backend is running:
- **Swagger UI**: `/api/docs`
- **ReDoc**: `/api/redoc`

## Authentication

Most endpoints require authentication via Bearer token:

```http
Authorization: Bearer <your_token_here>
```

## Endpoints

### Core System

#### Health Check
```http
GET /health
```

Returns comprehensive system health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-11T09:30:00.000Z",
  "components": {
    "ai_engine": {"status": "ready"},
    "database": true,
    "legal_knowledge": true,
    "document_generator": true
  }
}
```

### Document Management

#### Generate Document
```http
POST /api/documents/generate
Content-Type: application/json
Authorization: Bearer <token>

{
  "document_type": "will",
  "content": {
    "testator_name": "John Doe",
    "executor": "Jane Smith",
    "beneficiaries": [...]
  }
}
```

**Response:**
```json
{
  "document_id": "doc_20251011_093000",
  "content": "...",
  "pdf_content": "...",
  "docx_content": "...",
  "compliance_check": {...}
}
```

#### Get Document Template
```http
GET /api/documents/templates/{document_type}
```

#### Get Document Requirements
```http
GET /api/documents/requirements/{document_type}
```

### Document Storage

#### Store Document
```http
POST /api/storage/store
Content-Type: multipart/form-data

document: <file>
document_type: "will"
user_id: "user123"
```

**Response:**
```json
{
  "success": true,
  "document_id": "uuid-here",
  "filename": "will_20251011_093000_abc123.bin",
  "hash": "sha256-hash",
  "created_at": "2025-10-11T09:30:00.000Z"
}
```

#### Retrieve Document
```http
GET /api/storage/retrieve/{document_id}
```

#### List Documents
```http
GET /api/storage/list?user_id=user123&document_type=will&limit=100
```

**Response:**
```json
{
  "success": true,
  "count": 5,
  "documents": [
    {
      "document_id": "uuid",
      "document_type": "will",
      "user_id": "user123",
      "filename": "will_20251011.bin",
      "created_at": "2025-10-11T09:30:00.000Z",
      "status": "stored"
    }
  ]
}
```

#### Delete Document
```http
DELETE /api/storage/delete/{document_id}?user_id=user123
```

### Email Service

#### Send Document Email
```http
POST /api/email/send-document
Content-Type: multipart/form-data

to_email: "client@example.com"
subject: "Your Legal Document"
document_name: "will.pdf"
message_body: "Please find attached..."
document: <file>
```

**Response:**
```json
{
  "success": true,
  "message": "Email sent successfully",
  "simulation": false,
  "details": {
    "to": "client@example.com",
    "subject": "Your Legal Document",
    "attachment": "will.pdf"
  }
}
```

#### Send Notification
```http
POST /api/email/send-notification
Content-Type: application/json

{
  "to_email": "user@example.com",
  "subject": "Document Ready",
  "message_body": "<html>...</html>"
}
```

#### Email Service Status
```http
GET /api/email/status
```

**Response:**
```json
{
  "success": true,
  "configured": true,
  "simulation_mode": false,
  "from_email": "noreply@ontariowills.com",
  "from_name": "Ontario Wills & POA"
}
```

### Payment Processing

#### Create Payment Intent
```http
POST /api/payment/create-payment-intent
Content-Type: application/json

{
  "amount": 99.99,
  "user_id": "user123",
  "document_type": "premium_will",
  "metadata": {}
}
```

**Response:**
```json
{
  "success": true,
  "payment_intent_id": "pi_xyz",
  "client_secret": "pi_xyz_secret_abc",
  "amount": 99.99,
  "currency": "cad",
  "status": "requires_payment_method"
}
```

#### Create Checkout Session
```http
POST /api/payment/create-checkout-session
Content-Type: application/json

{
  "product_type": "basic_will",
  "user_id": "user123",
  "success_url": "https://yoursite.com/success",
  "cancel_url": "https://yoursite.com/cancel"
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "cs_xyz",
  "checkout_url": "https://checkout.stripe.com/...",
  "amount": 49.99,
  "product_type": "basic_will"
}
```

#### Confirm Payment
```http
POST /api/payment/confirm-payment/{payment_intent_id}
```

#### Process Refund
```http
POST /api/payment/refund
Content-Type: application/json

{
  "payment_intent_id": "pi_xyz",
  "amount": 49.99,
  "reason": "Customer request"
}
```

#### Get Pricing
```http
GET /api/payment/pricing
```

**Response:**
```json
{
  "success": true,
  "currency": "CAD",
  "pricing": {
    "basic_will": 49.99,
    "premium_will": 99.99,
    "poa_property": 39.99,
    "poa_personal_care": 39.99,
    "poa_combo": 69.99,
    "complete_package": 149.99,
    "lawyer_review": 299.99,
    "rush_processing": 49.99
  }
}
```

#### Payment Service Status
```http
GET /api/payment/status
```

### AI Analysis

#### Analyze Document
```http
POST /api/ai/analyze
Content-Type: application/json
Authorization: Bearer <token>

{
  "document_type": "will",
  "text": "I, John Doe, being of sound mind..."
}
```

**Response:**
```json
{
  "analysis": {
    "entities": [...],
    "sentiment": {...},
    "readability_score": 85.5,
    "legal_concepts": [...],
    "suggestions": [...],
    "risk_factors": [...],
    "compliance_issues": [...]
  }
}
```

#### Generate Recommendations
```http
POST /api/ai/generate-recommendations
Content-Type: application/json

{
  "document_type": "will",
  "user_data": {...}
}
```

#### Legal Knowledge Query
```http
GET /api/ai/legal-knowledge/{query}
```

### Compliance Checking

#### Check Compliance
```http
POST /api/compliance/check
Content-Type: application/json

{
  "document_type": "will",
  "content": "...",
  "jurisdiction": "ontario"
}
```

**Response:**
```json
{
  "is_compliant": true,
  "issues": [],
  "warnings": [],
  "requirements_met": ["requirement1", "requirement2"],
  "requirements_missing": [],
  "compliance_score": 95.5
}
```

#### Get Requirements
```http
GET /api/compliance/requirements/{document_type}
```

#### Validate Execution
```http
POST /api/compliance/validate-execution
Content-Type: application/json

{
  "document_type": "will",
  "execution_details": {
    "witnesses": 2,
    "notarized": false,
    "signed_date": "2025-10-11"
  }
}
```

### Practice Management

#### Create Client
```http
POST /api/practice/clients
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "416-555-1234",
  "address": "..."
}
```

#### Time Tracking
```http
POST /api/practice/time-entries
Content-Type: application/json

{
  "client_id": "client123",
  "description": "Document review",
  "hours": 2.5,
  "rate": 250.00
}
```

#### Generate Invoice
```http
POST /api/practice/invoices
Content-Type: application/json

{
  "client_id": "client123",
  "time_entries": ["entry1", "entry2"],
  "due_date": "2025-11-11"
}
```

## Error Responses

All endpoints return consistent error responses:

```json
{
  "detail": "Error message here"
}
```

**Common Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid parameters)
- `401` - Unauthorized (missing/invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `500` - Internal Server Error

## Rate Limiting

API endpoints are rate-limited to prevent abuse:
- **General**: 100 requests per minute
- **Document Generation**: 10 requests per minute
- **AI Analysis**: 20 requests per minute

## Pagination

List endpoints support pagination:

```http
GET /api/storage/list?limit=50&offset=0
```

## WebSocket Support

Real-time updates for:
- Document generation progress
- AI analysis status
- Payment confirmations

Connect to: `ws://localhost:8000/ws`

## SDK Examples

### JavaScript/TypeScript

```javascript
// Initialize API client
const apiClient = {
  baseURL: 'http://localhost:8000',
  token: 'your_token_here'
};

// Generate document
async function generateDocument(data) {
  const response = await fetch(`${apiClient.baseURL}/api/documents/generate`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiClient.token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });
  return await response.json();
}

// Store document
async function storeDocument(file, metadata) {
  const formData = new FormData();
  formData.append('document', file);
  formData.append('document_type', metadata.type);
  formData.append('user_id', metadata.userId);
  
  const response = await fetch(`${apiClient.baseURL}/api/storage/store`, {
    method: 'POST',
    body: formData
  });
  return await response.json();
}

// Send email
async function sendDocumentEmail(emailData, file) {
  const formData = new FormData();
  formData.append('document', file);
  Object.keys(emailData).forEach(key => {
    formData.append(key, emailData[key]);
  });
  
  const response = await fetch(`${apiClient.baseURL}/api/email/send-document`, {
    method: 'POST',
    body: formData
  });
  return await response.json();
}

// Create payment
async function createPayment(paymentData) {
  const response = await fetch(`${apiClient.baseURL}/api/payment/create-payment-intent`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(paymentData)
  });
  return await response.json();
}
```

### Python

```python
import requests

class OntarioWillsAPI:
    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.token = token
    
    def generate_document(self, data):
        headers = {}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        
        response = requests.post(
            f'{self.base_url}/api/documents/generate',
            json=data,
            headers=headers
        )
        return response.json()
    
    def store_document(self, file_path, document_type, user_id):
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {
                'document_type': document_type,
                'user_id': user_id
            }
            response = requests.post(
                f'{self.base_url}/api/storage/store',
                files=files,
                data=data
            )
        return response.json()
    
    def send_email(self, email_data, file_path):
        with open(file_path, 'rb') as f:
            files = {'document': f}
            response = requests.post(
                f'{self.base_url}/api/email/send-document',
                files=files,
                data=email_data
            )
        return response.json()
    
    def create_payment(self, payment_data):
        response = requests.post(
            f'{self.base_url}/api/payment/create-payment-intent',
            json=payment_data
        )
        return response.json()

# Usage
api = OntarioWillsAPI('http://localhost:8000', token='your_token')

# Generate document
result = api.generate_document({
    'document_type': 'will',
    'content': {...}
})

# Store document
storage_result = api.store_document(
    '/path/to/document.pdf',
    'will',
    'user123'
)

# Send email
email_result = api.send_email(
    {
        'to_email': 'client@example.com',
        'subject': 'Your Legal Document',
        'document_name': 'will.pdf'
    },
    '/path/to/document.pdf'
)

# Create payment
payment_result = api.create_payment({
    'amount': 99.99,
    'user_id': 'user123',
    'document_type': 'premium_will'
})
```

## Testing

Use the provided test scripts or API client to test endpoints:

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test email status
curl http://localhost:8000/api/email/status

# Test payment status
curl http://localhost:8000/api/payment/status

# Test pricing
curl http://localhost:8000/api/payment/pricing
```

## Support

For API support:
1. Check interactive documentation at `/api/docs`
2. Review logs for detailed error messages
3. Open GitHub issue with API endpoint, request, and response

---

**Note**: All services support graceful degradation and will function in simulation mode if external services (SendGrid, Stripe) are not configured.
