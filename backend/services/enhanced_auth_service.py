# backend/services/enhanced_auth_service.py
"""
Enhanced Authentication Service for Ontario Legal Practitioners
Integrates with the Ontario Legal Security Manager
"""

import jwt
import secrets
import asyncio
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, List, Any, Optional
from flask import request, jsonify, current_app

try:
    from backend.core.sole_practitioner_security import OntarioLegalSecurityManager
except ImportError:
    # Fallback if the import fails during development
    OntarioLegalSecurityManager = None

logger = logging.getLogger(__name__)

class EnhancedAuthService:
    """Enhanced authentication service for Ontario legal practitioners"""
    
    def __init__(self, app=None):
        self.app = app
        self.security_manager = None
        self._initialized = False
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the enhanced auth service with Flask app."""
        app.config.setdefault('JWT_SECRET_KEY', secrets.token_urlsafe(32))
        app.config.setdefault('JWT_EXPIRATION_HOURS', 24)
        app.config.setdefault('SESSION_EXPIRATION_HOURS', 168)  # 7 days
        app.config.setdefault('LEGAL_AUTH_ENABLED', True)
        
        # Initialize security manager if available
        if OntarioLegalSecurityManager:
            self.security_manager = OntarioLegalSecurityManager()
    
    async def initialize_async_components(self):
        """Initialize async components"""
        try:
            if self.security_manager and not self.security_manager.is_ready():
                await self.security_manager.initialize()
            self._initialized = True
            logger.info("✓ Enhanced Auth Service initialized with legal security")
        except Exception as e:
            logger.error(f"Failed to initialize enhanced auth service: {str(e)}")
            # Continue without enhanced security if it fails
            self._initialized = True
    
    async def register_lawyer(self, lawyer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new lawyer with LSUC verification"""
        try:
            # Validate required fields
            required_fields = ['lsuc_number', 'name', 'email', 'password']
            for field in required_fields:
                if field not in lawyer_data:
                    return {
                        'success': False,
                        'errors': [f'Missing required field: {field}']
                    }
            
            # Verify LSUC credentials if security manager is available
            if self.security_manager and self._initialized:
                verification_result = await self.security_manager.verify_lawyer_credentials(
                    lawyer_data['lsuc_number'], 
                    lawyer_data['password']
                )
                
                if not verification_result['verified']:
                    return {
                        'success': False,
                        'errors': ['LSUC credential verification failed']
                    }
            
            # Create lawyer authentication
            if self.security_manager and self._initialized:
                auth_result = await self.security_manager.create_lawyer_authentication(lawyer_data)
                
                return {
                    'success': True,
                    'access_token': auth_result['access_token'],
                    'refresh_token': auth_result['refresh_token'],
                    'lawyer_profile': auth_result['lawyer_profile'],
                    'security_features': auth_result['security_features']
                }
            else:
                # Fallback to basic JWT token
                payload = {
                    'user_id': lawyer_data['lsuc_number'],
                    'name': lawyer_data['name'],
                    'user_type': 'lawyer',
                    'exp': datetime.utcnow() + timedelta(hours=8),
                    'iat': datetime.utcnow()
                }
                
                token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
                
                return {
                    'success': True,
                    'access_token': token,
                    'lawyer_profile': {
                        'lsuc_number': lawyer_data['lsuc_number'],
                        'name': lawyer_data['name'],
                        'user_type': 'lawyer'
                    }
                }
                
        except Exception as e:
            logger.error(f"Lawyer registration failed: {str(e)}")
            return {
                'success': False,
                'errors': [f'Registration failed: {str(e)}']
            }
    
    async def register_assistant(self, assistant_data: Dict[str, Any], supervising_lawyer_lsuc: str) -> Dict[str, Any]:
        """Register a legal assistant under lawyer supervision"""
        try:
            # Validate required fields
            required_fields = ['assistant_id', 'name', 'email']
            for field in required_fields:
                if field not in assistant_data:
                    return {
                        'success': False,
                        'errors': [f'Missing required field: {field}']
                    }
            
            # Create assistant authentication
            if self.security_manager and self._initialized:
                auth_result = await self.security_manager.create_assistant_authentication(
                    assistant_data, 
                    supervising_lawyer_lsuc
                )
                
                return {
                    'success': True,
                    'access_token': auth_result['access_token'],
                    'assistant_profile': auth_result['assistant_profile'],
                    'restrictions': auth_result['restrictions']
                }
            else:
                # Fallback to basic JWT token
                payload = {
                    'user_id': assistant_data['assistant_id'],
                    'name': assistant_data['name'],
                    'user_type': 'assistant',
                    'supervising_lawyer': supervising_lawyer_lsuc,
                    'exp': datetime.utcnow() + timedelta(hours=4),
                    'iat': datetime.utcnow()
                }
                
                token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
                
                return {
                    'success': True,
                    'access_token': token,
                    'assistant_profile': {
                        'assistant_id': assistant_data['assistant_id'],
                        'name': assistant_data['name'],
                        'user_type': 'assistant',
                        'supervising_lawyer': supervising_lawyer_lsuc
                    }
                }
                
        except Exception as e:
            logger.error(f"Assistant registration failed: {str(e)}")
            return {
                'success': False,
                'errors': [f'Registration failed: {str(e)}']
            }
    
    async def authenticate_legal_user(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """Authenticate a legal user (lawyer or assistant)"""
        try:
            user_type = credentials.get('user_type', 'lawyer')
            
            if user_type == 'lawyer':
                return await self._authenticate_lawyer(credentials)
            elif user_type == 'assistant':
                return await self._authenticate_assistant(credentials)
            else:
                return {
                    'success': False,
                    'errors': ['Invalid user type']
                }
                
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return {
                'success': False,
                'errors': [f'Authentication failed: {str(e)}']
            }
    
    async def _authenticate_lawyer(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """Authenticate a lawyer"""
        lsuc_number = credentials.get('lsuc_number')
        password = credentials.get('password')
        
        if not lsuc_number or not password:
            return {
                'success': False,
                'errors': ['LSUC number and password required']
            }
        
        if self.security_manager and self._initialized:
            # Use enhanced security verification
            verification_result = await self.security_manager.verify_lawyer_credentials(
                lsuc_number, password
            )
            
            if verification_result['verified']:
                # Create authentication tokens
                auth_result = await self.security_manager.create_lawyer_authentication({
                    'lsuc_number': lsuc_number,
                    'name': verification_result['name'],
                    'practice_areas': verification_result['practice_areas']
                })
                
                return {
                    'success': True,
                    'access_token': auth_result['access_token'],
                    'refresh_token': auth_result['refresh_token'],
                    'user_profile': auth_result['lawyer_profile']
                }
            else:
                return {
                    'success': False,
                    'errors': ['Invalid LSUC credentials']
                }
        else:
            # Basic authentication fallback
            # In production, this would check against a user database
            payload = {
                'user_id': lsuc_number,
                'user_type': 'lawyer',
                'exp': datetime.utcnow() + timedelta(hours=8),
                'iat': datetime.utcnow()
            }
            
            token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
            
            return {
                'success': True,
                'access_token': token,
                'user_profile': {
                    'lsuc_number': lsuc_number,
                    'user_type': 'lawyer'
                }
            }
    
    async def _authenticate_assistant(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """Authenticate a legal assistant"""
        assistant_id = credentials.get('assistant_id')
        password = credentials.get('password')
        supervising_lawyer = credentials.get('supervising_lawyer')
        
        if not assistant_id or not password or not supervising_lawyer:
            return {
                'success': False,
                'errors': ['Assistant ID, password, and supervising lawyer required']
            }
        
        # Basic authentication for assistant
        # In production, this would verify against a database
        payload = {
            'user_id': assistant_id,
            'user_type': 'assistant',
            'supervising_lawyer': supervising_lawyer,
            'exp': datetime.utcnow() + timedelta(hours=4),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
        
        return {
            'success': True,
            'access_token': token,
            'user_profile': {
                'assistant_id': assistant_id,
                'user_type': 'assistant',
                'supervising_lawyer': supervising_lawyer
            }
        }
    
    async def generate_document_audit_trail(self, document_id: str, action: str, user_id: str, 
                                          details: Dict[str, Any] = None) -> Optional[str]:
        """Generate audit trail for document actions"""
        if self.security_manager and self._initialized:
            try:
                return await self.security_manager.generate_document_audit_trail(
                    document_id, action, user_id, details
                )
            except Exception as e:
                logger.error(f"Failed to generate audit trail: {str(e)}")
        return None
    
    async def encrypt_sensitive_data(self, data: str, classification: str = "confidential") -> Optional[Dict[str, Any]]:
        """Encrypt sensitive legal data"""
        if self.security_manager and self._initialized:
            try:
                return await self.security_manager.encrypt_legal_data(data, classification)
            except Exception as e:
                logger.error(f"Failed to encrypt data: {str(e)}")
        return None
    
    async def decrypt_sensitive_data(self, encrypted_package: Dict[str, Any]) -> Optional[str]:
        """Decrypt sensitive legal data"""
        if self.security_manager and self._initialized:
            try:
                return await self.security_manager.decrypt_legal_data(encrypted_package)
            except Exception as e:
                logger.error(f"Failed to decrypt data: {str(e)}")
        return None
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None
    
    def require_auth(self, allowed_user_types: List[str] = None):
        """Decorator to require authentication"""
        def decorator(f):
            @wraps(f)
            async def decorated_function(*args, **kwargs):
                token = None
                auth_header = request.headers.get('Authorization')
                
                if auth_header and auth_header.startswith('Bearer '):
                    token = auth_header[7:]  # Remove 'Bearer ' prefix
                
                if not token:
                    return jsonify({'error': 'Authentication token required'}), 401
                
                payload = self.verify_token(token)
                if not payload:
                    return jsonify({'error': 'Invalid or expired token'}), 401
                
                # Check user type if specified
                if allowed_user_types:
                    user_type = payload.get('user_type')
                    if user_type not in allowed_user_types:
                        return jsonify({'error': 'Insufficient permissions'}), 403
                
                # Add user info to request context
                request.current_user = payload
                
                return await f(*args, **kwargs)
            return decorated_function
        return decorator
    
    def is_initialized(self) -> bool:
        """Check if the service is properly initialized"""
        return self._initialized

# Global enhanced auth service instance
enhanced_auth_service = EnhancedAuthService()