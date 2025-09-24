# Ontario Sole Practitioner Enhancement Package - Integration Guide

## Overview

The Ontario Sole Practitioner Enhancement Package provides enterprise-grade security, practice management, and compliance features specifically designed for Ontario legal practitioners. This guide shows how to integrate these features with your existing Will and POA application.

## Components

### 1. Ontario Legal Security Manager (`backend/core/sole_practitioner_security.py`)
- **Enterprise-grade encryption** for legal documents
- **LSUC credential verification** (with API integration placeholder)
- **Lawyer and assistant authentication** with role-based permissions
- **Comprehensive audit trails** for all document actions
- **Ontario legal data retention policies** (7-year requirements)

### 2. Practice Management System (`backend/core/practice_management.py`)
- **Client and matter management** with full relational database
- **Time tracking and billing** with hourly rates and flat fees
- **Document-matter associations** for organized case management
- **Legal deadline tracking** with automated reminders
- **Invoice generation** with HST calculation for Ontario

### 3. Enhanced Authentication Service (`backend/services/enhanced_auth_service.py`)
- **Seamless integration** with existing auth_service.py
- **Flask-compatible decorators** for route protection
- **JWT token management** with security manager integration
- **Role-based access control** for lawyers vs. assistants

## Integration with Existing Codebase

### Step 1: Enhance Document Generation with Security

```python
# In your document generation routes (e.g., src/routes/document.py)

from backend.services.enhanced_auth_service import enhanced_auth_service
from backend.core.practice_management import OntarioPracticeManager

@document_bp.route('/generate', methods=['POST'])
@enhanced_auth_service.require_auth(['lawyer', 'assistant'])
async def generate_document():
    user = request.current_user
    data = request.get_json()
    
    # Generate audit trail
    audit_id = await enhanced_auth_service.generate_document_audit_trail(
        document_id=data.get('document_id'),
        action='generation_started',
        user_id=user['user_id'],
        details={'ip_address': request.remote_addr}
    )
    
    # Your existing document generation logic here
    document_content = your_document_generator.generate(data)
    
    # Encrypt sensitive content
    encrypted_content = await enhanced_auth_service.encrypt_sensitive_data(
        document_content, 
        classification='confidential'
    )
    
    # Associate with matter if practice management is enabled
    if data.get('matter_id'):
        practice_manager = OntarioPracticeManager()
        await practice_manager.associate_document_with_matter(
            data['matter_id'], 
            data['document_id'],
            data['document_type'],
            data.get('filename', 'Generated Document'),
            user['user_id']
        )
    
    return jsonify({
        'success': True,
        'document_id': data['document_id'],
        'audit_id': audit_id,
        'encrypted': encrypted_content is not None
    })
```

### Step 2: Add Practice Management Routes

```python
# New routes file: src/routes/practice.py

from flask import Blueprint, request, jsonify
from backend.core.practice_management import OntarioPracticeManager
from backend.services.enhanced_auth_service import enhanced_auth_service

practice_bp = Blueprint('practice', __name__)
practice_manager = OntarioPracticeManager()

@practice_bp.route('/clients', methods=['POST'])
@enhanced_auth_service.require_auth(['lawyer'])
async def create_client():
    data = request.get_json()
    user = request.current_user
    
    data['created_by'] = user['user_id']
    client_id = await practice_manager.create_client(data)
    
    return jsonify({
        'success': True,
        'client_id': client_id
    })

@practice_bp.route('/matters', methods=['POST'])
@enhanced_auth_service.require_auth(['lawyer'])
async def create_matter():
    data = request.get_json()
    user = request.current_user
    
    data['responsible_lawyer'] = user['user_id']
    matter_id = await practice_manager.create_matter(data)
    
    return jsonify({
        'success': True,
        'matter_id': matter_id
    })

@practice_bp.route('/time-entries', methods=['POST'])
@enhanced_auth_service.require_auth(['lawyer', 'assistant'])
async def add_time_entry():
    data = request.get_json()
    user = request.current_user
    
    data['lawyer_id'] = user['user_id']
    entry_id = await practice_manager.add_time_entry(data)
    
    return jsonify({
        'success': True,
        'entry_id': entry_id
    })
```

### Step 3: Initialize Services in Main App

```python
# In your main.py or app initialization

import asyncio
from backend.services.enhanced_auth_service import enhanced_auth_service
from backend.core.practice_management import OntarioPracticeManager

app = Flask(__name__)

# Initialize enhanced services
practice_manager = OntarioPracticeManager()

@app.before_first_request
def initialize_services():
    asyncio.run(init_async_services())

async def init_async_services():
    # Initialize enhanced auth service
    enhanced_auth_service.init_app(app)
    await enhanced_auth_service.initialize_async_components()
    
    # Initialize practice manager
    await practice_manager.initialize()
    
    print("✓ Ontario Legal Services initialized")

# Register new blueprints
from src.routes.practice import practice_bp
app.register_blueprint(practice_bp, url_prefix='/api/practice')
```

## Configuration

### Environment Variables

```bash
# Required for production
LEGAL_MASTER_SECRET=your-master-encryption-secret
JWT_SECRET_KEY=your-jwt-secret

# Optional - for LSUC integration (future)
LSUC_API_URL=https://api.lsuc.on.ca
LSUC_API_KEY=your-lsuc-api-key

# Database paths
PRACTICE_DB_PATH=data/practice_management.db
```

### Database Initialization

The practice management system will automatically create its database tables on first initialization. For production, consider using PostgreSQL:

```python
# For PostgreSQL instead of SQLite
practice_manager = OntarioPracticeManager(
    database_path="postgresql://user:pass@localhost/practice_db"
)
```

## Security Features

### Document Encryption
All sensitive legal documents can be encrypted at rest using the Fernet symmetric encryption:

```python
# Encrypt sensitive data
encrypted_package = await security_manager.encrypt_legal_data(
    document_content, 
    classification="confidential"
)

# Decrypt when needed
decrypted_content = await security_manager.decrypt_legal_data(encrypted_package)
```

### Audit Trails
Every document action is logged with tamper-proof audit trails:

```python
audit_id = await security_manager.generate_document_audit_trail(
    document_id="doc_123",
    action="accessed", 
    user_id="LSUC12345",
    details={
        "ip_address": "192.168.1.100",
        "user_agent": "Mozilla/5.0...",
        "reason": "client_review"
    }
)
```

### Data Retention
Ontario legal requirements are automatically enforced:

```python
retention_policy = await security_manager.enforce_data_retention_policy(
    document_type="wills", 
    client_id="client_123"
)
# Returns 7-year retention schedule as per Ontario Limitations Act
```

## Practice Management Features

### Client and Matter Management
Full CRM-style client and matter tracking:

```python
# Create client
client_id = await practice_manager.create_client({
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "416-555-0123"
})

# Create matter
matter_id = await practice_manager.create_matter({
    "client_id": client_id,
    "matter_name": "Estate Planning Package",
    "matter_type": "wills_estates",
    "responsible_lawyer": "LSUC12345",
    "estimated_value": 2500.00
})
```

### Time Tracking and Billing
Professional time tracking with automatic billing calculations:

```python
# Add time entry
entry_id = await practice_manager.add_time_entry({
    "matter_id": matter_id,
    "lawyer_id": "LSUC12345",
    "date_worked": "2024-01-15",
    "duration_minutes": 120,
    "description": "Will preparation and client consultation",
    "activity_type": "legal_work",
    "billable": True,
    "hourly_rate": 400.00
})

# Generate invoice
invoice_id = await practice_manager.generate_invoice({
    "matter_id": matter_id,
    "client_id": client_id,
    "total_amount": 800.00  # 2 hours x $400
})
```

## Testing

Run the comprehensive test suite:

```bash
python test_ontario_enhancements.py
```

This tests all components:
- Security manager (encryption, authentication, audit trails)
- Practice manager (clients, matters, time tracking, billing)
- Enhanced auth service (lawyer/assistant registration and authentication)

## Production Deployment

1. **Set environment variables** for encryption keys and database paths
2. **Use PostgreSQL** instead of SQLite for production database
3. **Enable HTTPS** for all legal document transmissions
4. **Configure backup retention** according to Ontario legal requirements
5. **Set up monitoring** for audit trail integrity
6. **Implement LSUC API integration** for real credential verification

## Ontario Legal Compliance

This enhancement package specifically addresses:

- ✅ **Law Society of Ontario (LSO) requirements** for client data protection
- ✅ **Limitations Act** 7-year document retention requirements
- ✅ **Personal Information Protection Act (PIPA)** data security
- ✅ **Professional conduct requirements** for lawyer supervision of staff
- ✅ **Audit trail requirements** for legal document management
- ✅ **HST calculation** for Ontario legal services (13%)

## Support

For issues or questions about the Ontario Sole Practitioner Enhancement Package:

1. Check the test suite output for specific component failures
2. Review audit logs for security-related issues
3. Ensure all environment variables are properly configured
4. Verify database permissions and connectivity

The package is designed to enhance existing functionality without breaking changes, providing a smooth upgrade path for Ontario legal practitioners.