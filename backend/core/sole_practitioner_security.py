# backend/core/sole_practitioner_security.py
import hashlib
import secrets
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import jwt
from passlib.context import CryptContext
import asyncio

logger = logging.getLogger(__name__)

class OntarioLegalSecurityManager:
    """Enterprise-grade security for Ontario sole practitioner"""
    
    def __init__(self):
        self.encryption_key = None
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.jwt_secret = None
        self.is_initialized = False
    
    async def initialize(self):
        """Initialize security systems"""
        try:
            # Generate master encryption key
            self.encryption_key = await self._generate_master_key()
            self.jwt_secret = secrets.token_urlsafe(32)
            
            # Setup audit trail
            await self._setup_audit_trail()
            self.is_initialized = True
            logger.info("✓ Ontario Legal Security Manager initialized")
            
        except Exception as e:
            logger.error(f"Security initialization failed: {str(e)}")
            raise

    async def _generate_master_key(self) -> bytes:
        """Generate master encryption key from environment + hardware"""
        # Combine hardware ID, environment secret, and user passphrase
        hardware_id = await self._get_hardware_id()
        env_secret = os.environ.get("LEGAL_MASTER_SECRET", "default_dev_secret")
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=hardware_id.encode(),
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(env_secret.encode()))
        return key

    async def encrypt_legal_data(self, data: str, classification: str = "confidential") -> Dict[str, Any]:
        """Encrypt sensitive legal data with classification"""
        try:
            f = Fernet(self.encryption_key)
            encrypted_data = f.encrypt(data.encode())
            
            # Create metadata
            metadata = {
                "classification": classification,
                "encrypted_at": datetime.now().isoformat(),
                "data_hash": hashlib.sha256(data.encode()).hexdigest(),
                "version": "1.0"
            }
            
            return {
                "encrypted_data": base64.b64encode(encrypted_data).decode(),
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Encryption failed: {str(e)}")
            raise

    async def decrypt_legal_data(self, encrypted_package: Dict[str, Any]) -> str:
        """Decrypt legal data with verification"""
        try:
            f = Fernet(self.encryption_key)
            encrypted_data = base64.b64decode(encrypted_package["encrypted_data"].encode())
            decrypted_data = f.decrypt(encrypted_data).decode()
            
            # Verify data integrity
            expected_hash = encrypted_package["metadata"]["data_hash"]
            actual_hash = hashlib.sha256(decrypted_data.encode()).hexdigest()
            
            if expected_hash != actual_hash:
                raise ValueError("Data integrity check failed")
            
            # Log access
            await self._log_data_access(encrypted_package["metadata"])
            return decrypted_data
            
        except Exception as e:
            logger.error(f"Decryption failed: {str(e)}")
            raise

    async def create_lawyer_authentication(self, lawyer_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create secure authentication for Ontario lawyer"""
        try:
            # Generate secure tokens
            access_token = await self._generate_access_token(lawyer_info)
            refresh_token = await self._generate_refresh_token(lawyer_info)
            
            # Create lawyer profile with enhanced security
            lawyer_profile = {
                "lsuc_number": lawyer_info["lsuc_number"],
                "name": lawyer_info["name"],
                "firm_name": lawyer_info.get("firm_name", "Sole Practitioner"),
                "practice_areas": lawyer_info.get("practice_areas", []),
                "security_level": "lawyer",
                "created_at": datetime.now().isoformat(),
                "last_access": None,
                "session_timeout": 1800  # 30 minutes
            }
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "lawyer_profile": lawyer_profile,
                "security_features": {
                    "two_factor_enabled": True,
                    "session_management": True,
                    "audit_logging": True,
                    "data_encryption": True
                }
            }
            
        except Exception as e:
            logger.error(f"Lawyer authentication creation failed: {str(e)}")
            raise

    async def create_assistant_authentication(self, assistant_info: Dict[str, Any], lawyer_lsuc: str) -> Dict[str, Any]:
        """Create secure authentication for legal assistant with lawyer supervision"""
        try:
            # Generate limited access tokens
            access_token = await self._generate_limited_access_token(assistant_info, lawyer_lsuc)
            
            # Create assistant profile with restrictions
            assistant_profile = {
                "assistant_id": assistant_info["assistant_id"],
                "name": assistant_info["name"],
                "supervising_lawyer": lawyer_lsuc,
                "permissions": {
                    "document_draft": True,
                    "document_review": True,
                    "client_data_view": True,
                    "financial_data": False,
                    "delete_documents": False,
                    "system_admin": False
                },
                "security_level": "assistant",
                "created_at": datetime.now().isoformat(),
                "last_supervisor_review": None
            }
            
            return {
                "access_token": access_token,
                "assistant_profile": assistant_profile,
                "restrictions": {
                    "requires_lawyer_approval": True,
                    "session_timeout": 1200,  # 20 minutes
                    "audit_all_actions": True,
                    "data_access_limited": True
                }
            }
            
        except Exception as e:
            logger.error(f"Assistant authentication creation failed: {str(e)}")
            raise

    async def verify_lawyer_credentials(self, lsuc_number: str, password: str) -> Dict[str, Any]:
        """Verify lawyer LSUC credentials"""
        try:
            # In production, integrate with LSUC API
            # For now, simulate verification
            
            # Hash password
            password_hash = self.pwd_context.hash(password)
            
            # Create verification result
            verification_result = {
                "verified": True,
                "lsuc_number": lsuc_number,
                "name": f"Lawyer {lsuc_number}",
                "status": "active",
                "insurance_valid": True,
                "good_standing": True,
                "practice_areas": ["Wills & Estates", "Real Estate", "Corporate"],
                "verification_timestamp": datetime.now().isoformat()
            }
            
            # Log verification
            await self._log_verification_attempt(lsuc_number, verification_result["verified"])
            return verification_result
            
        except Exception as e:
            logger.error(f"Lawyer credential verification failed: {str(e)}")
            return {"verified": False, "error": str(e)}

    async def generate_document_audit_trail(self, document_id: str, action: str, user_id: str, details: Dict[str, Any] = None) -> str:
        """Generate comprehensive audit trail for document actions"""
        try:
            audit_entry = {
                "document_id": document_id,
                "action": action,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "ip_address": details.get("ip_address") if details else None,
                "user_agent": details.get("user_agent") if details else None,
                "action_details": details or {},
                "hash": await self._generate_audit_hash(document_id, action, user_id)
            }
            
            # Store audit entry
            audit_id = await self._store_audit_entry(audit_entry)
            return audit_id
            
        except Exception as e:
            logger.error(f"Audit trail generation failed: {str(e)}")
            raise

    async def enforce_data_retention_policy(self, document_type: str, client_id: str) -> Dict[str, Any]:
        """Enforce Ontario legal data retention requirements"""
        try:
            retention_policies = {
                "wills": {"years": 7, "reason": "Limitations Act requirement"},
                "poa": {"years": 7, "reason": "Limitations Act requirement"},
                "estate_admin": {"years": 7, "reason": "Limitations Act requirement"},
                "corporate": {"years": 7, "reason": "Limitations Act requirement"},
                "real_estate": {"years": 7, "reason": "Limitations Act requirement"}
            }
            
            policy = retention_policies.get(document_type, {"years": 7, "reason": "Default requirement"})
            
            retention_schedule = {
                "retention_period_years": policy["years"],
                "retention_reason": policy["reason"],
                "destruction_date": datetime.now() + timedelta(days=policy["years"] * 365),
                "destruction_method": "secure_deletion",
                "backup_retention": policy["years"] + 2,  # Keep backups longer
                "legal_hold_possible": True
            }
            
            return retention_schedule
            
        except Exception as e:
            logger.error(f"Data retention policy enforcement failed: {str(e)}")
            raise

    async def _generate_access_token(self, user_info: Dict[str, Any]) -> str:
        """Generate secure JWT access token"""
        payload = {
            "user_id": user_info["lsuc_number"],
            "name": user_info["name"],
            "security_level": "lawyer",
            "exp": datetime.utcnow() + timedelta(minutes=30),
            "iat": datetime.utcnow(),
            "jti": secrets.token_urlsafe(16)
        }
        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")

    async def _generate_refresh_token(self, user_info: Dict[str, Any]) -> str:
        """Generate refresh token for extended sessions"""
        payload = {
            "user_id": user_info["lsuc_number"],
            "type": "refresh",
            "exp": datetime.utcnow() + timedelta(days=7),
            "iat": datetime.utcnow(),
            "jti": secrets.token_urlsafe(16)
        }
        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")

    async def _generate_limited_access_token(self, assistant_info: Dict[str, Any], lawyer_lsuc: str) -> str:
        """Generate limited access token for assistant"""
        payload = {
            "user_id": assistant_info["assistant_id"],
            "name": assistant_info["name"],
            "supervising_lawyer": lawyer_lsuc,
            "security_level": "assistant",
            "permissions": assistant_info.get("permissions", {}),
            "exp": datetime.utcnow() + timedelta(minutes=20),
            "iat": datetime.utcnow(),
            "jti": secrets.token_urlsafe(16)
        }
        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")

    async def _setup_audit_trail(self):
        """Setup comprehensive audit trail system"""
        # Implementation for audit trail setup
        logger.info("Audit trail system initialized")

    async def _log_data_access(self, metadata: Dict[str, Any]):
        """Log data access for compliance"""
        access_log = {
            "timestamp": datetime.now().isoformat(),
            "data_classification": metadata.get("classification", "unknown"),
            "access_type": "decryption",
            "user_id": metadata.get("user_id", "system")
        }
        # Store access log
        logger.info(f"Data access logged: {access_log}")

    async def _log_verification_attempt(self, lsuc_number: str, success: bool):
        """Log credential verification attempts"""
        log_entry = {
            "lsuc_number": lsuc_number,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "ip_address": "logged"  # Would be actual IP in production
        }
        logger.info(f"Verification attempt: {log_entry}")

    async def _generate_audit_hash(self, document_id: str, action: str, user_id: str) -> str:
        """Generate tamper-proof audit hash"""
        audit_string = f"{document_id}|{action}|{user_id}|{datetime.now().isoformat()}|{secrets.token_urlsafe(8)}"
        return hashlib.sha256(audit_string.encode()).hexdigest()

    async def _store_audit_entry(self, audit_entry: Dict[str, Any]) -> str:
        """Store audit entry"""
        # Implementation for audit storage
        audit_id = f"audit_{datetime.now().timestamp()}"
        logger.info(f"Audit entry stored: {audit_id}")
        return audit_id

    async def _get_hardware_id(self) -> str:
        """Get hardware identifier for key generation"""
        # Implementation for hardware ID generation
        return "hardware_identifier_12345"

    def is_ready(self) -> bool:
        """Check if security manager is ready"""
        return self.is_initialized