#!/usr/bin/env python3
"""
Example Integration: Ontario Sole Practitioner Enhancement Package
Shows how to integrate the enhancement package with the existing Flask application
"""

from flask import Flask, request, jsonify, Blueprint
import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

# Import the enhancement package components
from backend.services.enhanced_auth_service import EnhancedAuthService
from backend.core.practice_management import OntarioPracticeManager
from backend.core.sole_practitioner_security import OntarioLegalSecurityManager

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-here'

# Initialize enhancement services
enhanced_auth = EnhancedAuthService(app)
practice_manager = OntarioPracticeManager()
security_manager = OntarioLegalSecurityManager()

# Create a blueprint for Ontario legal features
ontario_bp = Blueprint('ontario', __name__, url_prefix='/api/ontario')

@ontario_bp.route('/register/lawyer', methods=['POST'])
async def register_lawyer():
    """Register a new lawyer with LSUC verification"""
    try:
        data = request.get_json()
        result = await enhanced_auth.register_lawyer(data)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Lawyer registered successfully',
                'access_token': result['access_token'],
                'lawyer_profile': result['lawyer_profile']
            }), 201
        else:
            return jsonify({
                'success': False,
                'errors': result['errors']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Registration failed: {str(e)}'
        }), 500

@ontario_bp.route('/auth/login', methods=['POST'])
async def login():
    """Authenticate lawyer or assistant"""
    try:
        credentials = request.get_json()
        result = await enhanced_auth.authenticate_legal_user(credentials)
        
        if result['success']:
            return jsonify({
                'success': True,
                'access_token': result['access_token'],
                'user_profile': result['user_profile']
            }), 200
        else:
            return jsonify({
                'success': False,
                'errors': result['errors']
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Authentication failed: {str(e)}'
        }), 500

@ontario_bp.route('/clients', methods=['POST'])
async def create_client():
    """Create a new client (lawyer only)"""
    # This would use the @enhanced_auth.require_auth(['lawyer']) decorator
    # For this example, we'll do a simple check
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authentication required'}), 401
    
    token = auth_header[7:]
    user = enhanced_auth.verify_token(token)
    if not user:
        return jsonify({'error': 'Invalid token'}), 401
    
    try:
        data = request.get_json()
        data['created_by'] = user['user_id']
        
        client_id = await practice_manager.create_client(data)
        
        return jsonify({
            'success': True,
            'client_id': client_id,
            'message': 'Client created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Client creation failed: {str(e)}'
        }), 500

@ontario_bp.route('/matters', methods=['POST'])
async def create_matter():
    """Create a new legal matter"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authentication required'}), 401
    
    token = auth_header[7:]
    user = enhanced_auth.verify_token(token)
    if not user or user.get('user_type') != 'lawyer':
        return jsonify({'error': 'Lawyer access required'}), 403
    
    try:
        data = request.get_json()
        data['responsible_lawyer'] = user['user_id']
        
        matter_id = await practice_manager.create_matter(data)
        
        return jsonify({
            'success': True,
            'matter_id': matter_id,
            'message': 'Matter created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Matter creation failed: {str(e)}'
        }), 500

@ontario_bp.route('/documents/generate', methods=['POST'])
async def generate_secure_document():
    """Generate a document with enhanced security and audit trails"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authentication required'}), 401
    
    token = auth_header[7:]
    user = enhanced_auth.verify_token(token)
    if not user:
        return jsonify({'error': 'Invalid token'}), 401
    
    try:
        data = request.get_json()
        document_id = f"doc_{hash(str(data))}"
        
        # Generate audit trail
        audit_id = await enhanced_auth.generate_document_audit_trail(
            document_id=document_id,
            action='generation_started',
            user_id=user['user_id'],
            details={
                'ip_address': request.remote_addr,
                'user_agent': request.headers.get('User-Agent'),
                'document_type': data.get('document_type')
            }
        )
        
        # Your existing document generation logic would go here
        document_content = f"Generated {data.get('document_type', 'document')} for client"
        
        # Encrypt the document content
        encrypted_content = await enhanced_auth.encrypt_sensitive_data(
            document_content,
            classification='confidential'
        )
        
        # Associate with matter if provided
        if data.get('matter_id'):
            await practice_manager.associate_document_with_matter(
                data['matter_id'],
                document_id,
                data.get('document_type', 'unknown'),
                f"{data.get('document_type', 'Document')}.docx",
                user['user_id']
            )
        
        return jsonify({
            'success': True,
            'document_id': document_id,
            'audit_id': audit_id,
            'encrypted': encrypted_content is not None,
            'message': 'Document generated with enhanced security'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Document generation failed: {str(e)}'
        }), 500

@ontario_bp.route('/time-entries', methods=['POST'])
async def add_time_entry():
    """Add a time entry for billing"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authentication required'}), 401
    
    token = auth_header[7:]
    user = enhanced_auth.verify_token(token)
    if not user:
        return jsonify({'error': 'Invalid token'}), 401
    
    try:
        data = request.get_json()
        data['lawyer_id'] = user['user_id']
        
        entry_id = await practice_manager.add_time_entry(data)
        
        return jsonify({
            'success': True,
            'entry_id': entry_id,
            'message': 'Time entry added successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Time entry failed: {str(e)}'
        }), 500

@ontario_bp.route('/matters/<matter_id>/summary', methods=['GET'])
async def get_matter_summary(matter_id):
    """Get time and billing summary for a matter"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authentication required'}), 401
    
    token = auth_header[7:]
    user = enhanced_auth.verify_token(token)
    if not user:
        return jsonify({'error': 'Invalid token'}), 401
    
    try:
        # Get time summary
        time_summary = await practice_manager.get_time_summary(matter_id)
        
        # Get client matters to verify access
        # In production, you'd verify the user has access to this matter
        
        return jsonify({
            'success': True,
            'matter_id': matter_id,
            'time_summary': time_summary
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Summary retrieval failed: {str(e)}'
        }), 500

# Register the blueprint
app.register_blueprint(ontario_bp)

@app.before_first_request
def initialize_services():
    """Initialize the Ontario enhancement services"""
    async def init_async():
        try:
            await enhanced_auth.initialize_async_components()
            await practice_manager.initialize()
            await security_manager.initialize()
            print("✓ Ontario Legal Services initialized successfully")
        except Exception as e:
            print(f"❌ Service initialization failed: {str(e)}")
    
    asyncio.run(init_async())

@app.route('/')
def index():
    """API documentation endpoint"""
    return jsonify({
        'message': 'Ontario Will & POA App - Enhanced for Legal Practitioners',
        'version': '1.0.0',
        'ontario_features': {
            'security': 'Enterprise-grade encryption and audit trails',
            'practice_management': 'Client, matter, and time tracking',
            'compliance': 'Ontario legal requirements and LSUC integration',
            'authentication': 'Lawyer and assistant role-based access'
        },
        'endpoints': {
            'POST /api/ontario/register/lawyer': 'Register a new lawyer',
            'POST /api/ontario/auth/login': 'Authenticate user',
            'POST /api/ontario/clients': 'Create client',
            'POST /api/ontario/matters': 'Create matter',
            'POST /api/ontario/documents/generate': 'Generate secure document',
            'POST /api/ontario/time-entries': 'Add time entry',
            'GET /api/ontario/matters/<id>/summary': 'Get matter summary'
        }
    })

if __name__ == '__main__':
    print("🚀 Starting Ontario Enhanced Will & POA Application")
    print("📋 Features: Security, Practice Management, Compliance")
    print("🔗 Access: http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)