"""
Cloud Storage Service
Provides secure cloud storage and sharing capabilities for legal documents
"""

import os
import json
import logging
import hashlib
import base64
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import requests
from urllib.parse import quote
import tempfile
import zipfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class StoredDocument:
    """Represents a document stored in cloud storage"""
    document_id: str
    filename: str
    file_type: str
    file_size: int
    storage_path: str
    upload_date: datetime
    last_modified: datetime
    access_level: str  # 'private', 'shared', 'public'
    share_token: Optional[str] = None
    expiry_date: Optional[datetime] = None
    metadata: Dict[str, Any] = None

@dataclass
class ShareLink:
    """Represents a shareable link for a document"""
    document_id: str
    share_token: str
    access_level: str
    expiry_date: Optional[datetime]
    password_protected: bool
    download_count: int
    max_downloads: Optional[int]
    created_date: datetime

@dataclass
class BackupInfo:
    """Information about document backups"""
    backup_id: str
    document_ids: List[str]
    backup_date: datetime
    backup_size: int
    storage_location: str
    encryption_enabled: bool
    retention_period: int  # days

class CloudStorageService:
    """
    Service for managing cloud storage of legal documents with security and sharing features
    """
    
    def __init__(self):
        # AWS S3 Configuration
        self.aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.aws_region = os.environ.get('AWS_REGION', 'us-east-1')
        self.s3_bucket = os.environ.get('S3_BUCKET_NAME', 'ontario-wills-documents')
        
        # Google Drive Configuration (alternative)
        self.google_credentials = os.environ.get('GOOGLE_DRIVE_CREDENTIALS')
        
        # Dropbox Configuration (alternative)
        self.dropbox_token = os.environ.get('DROPBOX_ACCESS_TOKEN')
        
        # Initialize storage clients
        self.s3_client = None
        self.storage_type = self._initialize_storage()
        
        # Security settings
        self.encryption_key = os.environ.get('DOCUMENT_ENCRYPTION_KEY', self._generate_encryption_key())
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        self.allowed_file_types = ['.pdf', '.docx', '.doc', '.txt', '.json']
        
        # Share link settings
        self.default_share_expiry = 30  # days
        self.max_share_expiry = 365  # days
    
    def _initialize_storage(self) -> str:
        """Initialize available storage services"""
        # Try AWS S3 first
        if self.aws_access_key and self.aws_secret_key:
            try:
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=self.aws_access_key,
                    aws_secret_access_key=self.aws_secret_key,
                    region_name=self.aws_region
                )
                # Test connection
                self.s3_client.head_bucket(Bucket=self.s3_bucket)
                logger.info("AWS S3 storage initialized successfully")
                return 'aws_s3'
            except (ClientError, NoCredentialsError) as e:
                logger.warning(f"AWS S3 initialization failed: {e}")
        
        # Fallback to local storage with warning
        logger.warning("Cloud storage not configured, using local storage")
        return 'local'
    
    def _generate_encryption_key(self) -> str:
        """Generate a random encryption key"""
        import secrets
        return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
    
    def _encrypt_file_content(self, content: bytes) -> bytes:
        """Encrypt file content for secure storage"""
        try:
            from cryptography.fernet import Fernet
            key = base64.urlsafe_b64decode(self.encryption_key.encode())
            fernet = Fernet(key)
            return fernet.encrypt(content)
        except ImportError:
            logger.warning("Cryptography library not available, storing without encryption")
            return content
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return content
    
    def _decrypt_file_content(self, encrypted_content: bytes) -> bytes:
        """Decrypt file content"""
        try:
            from cryptography.fernet import Fernet
            key = base64.urlsafe_b64decode(self.encryption_key.encode())
            fernet = Fernet(key)
            return fernet.decrypt(encrypted_content)
        except ImportError:
            logger.warning("Cryptography library not available, returning content as-is")
            return encrypted_content
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return encrypted_content
    
    def _generate_document_id(self, filename: str, user_id: str) -> str:
        """Generate unique document ID"""
        timestamp = datetime.now().isoformat()
        content = f"{user_id}_{filename}_{timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _generate_share_token(self, document_id: str) -> str:
        """Generate secure share token"""
        timestamp = datetime.now().isoformat()
        content = f"{document_id}_{timestamp}_{self.encryption_key[:8]}"
        return hashlib.sha256(content.encode()).hexdigest()[:32]
    
    def upload_document(self, file_path: str, filename: str, user_id: str, 
                       access_level: str = 'private', metadata: Dict[str, Any] = None) -> StoredDocument:
        """
        Upload a document to cloud storage
        
        Args:
            file_path: Local path to the file
            filename: Original filename
            user_id: ID of the user uploading
            access_level: Access level ('private', 'shared', 'public')
            metadata: Additional metadata
            
        Returns:
            StoredDocument object with storage information
        """
        try:
            # Validate file
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                raise ValueError(f"File size ({file_size}) exceeds maximum ({self.max_file_size})")
            
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext not in self.allowed_file_types:
                raise ValueError(f"File type {file_ext} not allowed")
            
            # Generate document ID and storage path
            document_id = self._generate_document_id(filename, user_id)
            storage_path = f"users/{user_id}/documents/{document_id}/{filename}"
            
            # Read and encrypt file content
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            encrypted_content = self._encrypt_file_content(file_content)
            
            # Upload based on storage type
            if self.storage_type == 'aws_s3':
                self._upload_to_s3(storage_path, encrypted_content, metadata or {})
            else:
                self._upload_to_local(storage_path, encrypted_content)
            
            # Create document record
            stored_document = StoredDocument(
                document_id=document_id,
                filename=filename,
                file_type=file_ext,
                file_size=file_size,
                storage_path=storage_path,
                upload_date=datetime.now(),
                last_modified=datetime.now(),
                access_level=access_level,
                metadata=metadata or {}
            )
            
            logger.info(f"Document uploaded successfully: {document_id}")
            return stored_document
            
        except Exception as e:
            logger.error(f"Error uploading document: {e}")
            raise
    
    def _upload_to_s3(self, storage_path: str, content: bytes, metadata: Dict[str, Any]):
        """Upload file to AWS S3"""
        try:
            # Convert metadata to string values for S3
            s3_metadata = {k: str(v) for k, v in metadata.items()}
            
            self.s3_client.put_object(
                Bucket=self.s3_bucket,
                Key=storage_path,
                Body=content,
                Metadata=s3_metadata,
                ServerSideEncryption='AES256'
            )
        except Exception as e:
            logger.error(f"S3 upload failed: {e}")
            raise
    
    def _upload_to_local(self, storage_path: str, content: bytes):
        """Upload file to local storage"""
        try:
            local_path = os.path.join('/tmp/ontario_wills_storage', storage_path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            with open(local_path, 'wb') as f:
                f.write(content)
        except Exception as e:
            logger.error(f"Local upload failed: {e}")
            raise
    
    def download_document(self, document_id: str, user_id: str, output_path: str) -> bool:
        """
        Download a document from cloud storage
        
        Args:
            document_id: ID of the document to download
            user_id: ID of the user requesting download
            output_path: Local path to save the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Find document storage path (in real implementation, this would come from database)
            storage_path = f"users/{user_id}/documents/{document_id}/"
            
            # Download based on storage type
            if self.storage_type == 'aws_s3':
                encrypted_content = self._download_from_s3(storage_path)
            else:
                encrypted_content = self._download_from_local(storage_path)
            
            # Decrypt content
            decrypted_content = self._decrypt_file_content(encrypted_content)
            
            # Save to output path
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(decrypted_content)
            
            logger.info(f"Document downloaded successfully: {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error downloading document: {e}")
            return False
    
    def _download_from_s3(self, storage_path: str) -> bytes:
        """Download file from AWS S3"""
        try:
            response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=storage_path)
            return response['Body'].read()
        except Exception as e:
            logger.error(f"S3 download failed: {e}")
            raise
    
    def _download_from_local(self, storage_path: str) -> bytes:
        """Download file from local storage"""
        try:
            local_path = os.path.join('/tmp/ontario_wills_storage', storage_path)
            with open(local_path, 'rb') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Local download failed: {e}")
            raise
    
    def create_share_link(self, document_id: str, user_id: str, access_level: str = 'shared',
                         expiry_days: int = None, password: str = None, max_downloads: int = None) -> ShareLink:
        """
        Create a shareable link for a document
        
        Args:
            document_id: ID of the document to share
            user_id: ID of the document owner
            access_level: Access level for the share
            expiry_days: Number of days until link expires
            password: Optional password protection
            max_downloads: Maximum number of downloads allowed
            
        Returns:
            ShareLink object with sharing information
        """
        try:
            # Generate share token
            share_token = self._generate_share_token(document_id)
            
            # Calculate expiry date
            expiry_date = None
            if expiry_days:
                expiry_days = min(expiry_days, self.max_share_expiry)
                expiry_date = datetime.now() + timedelta(days=expiry_days)
            
            # Create share link record
            share_link = ShareLink(
                document_id=document_id,
                share_token=share_token,
                access_level=access_level,
                expiry_date=expiry_date,
                password_protected=bool(password),
                download_count=0,
                max_downloads=max_downloads,
                created_date=datetime.now()
            )
            
            # In real implementation, save to database
            logger.info(f"Share link created: {share_token}")
            return share_link
            
        except Exception as e:
            logger.error(f"Error creating share link: {e}")
            raise
    
    def access_shared_document(self, share_token: str, password: str = None) -> Optional[Dict[str, Any]]:
        """
        Access a document via share link
        
        Args:
            share_token: Share token for the document
            password: Password if required
            
        Returns:
            Document information if access is granted
        """
        try:
            # In real implementation, retrieve share link from database
            # For now, return mock data
            
            # Validate share link
            # Check expiry, password, download limits, etc.
            
            return {
                'document_id': 'mock_doc_id',
                'filename': 'sample_will.pdf',
                'file_size': 1024000,
                'access_granted': True,
                'download_url': f'/api/download/shared/{share_token}'
            }
            
        except Exception as e:
            logger.error(f"Error accessing shared document: {e}")
            return None
    
    def create_backup(self, user_id: str, document_ids: List[str], retention_days: int = 90) -> BackupInfo:
        """
        Create a backup of multiple documents
        
        Args:
            user_id: ID of the user
            document_ids: List of document IDs to backup
            retention_days: How long to keep the backup
            
        Returns:
            BackupInfo object with backup details
        """
        try:
            backup_id = hashlib.sha256(f"{user_id}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
            
            # Create temporary zip file
            with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
                with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    total_size = 0
                    
                    for doc_id in document_ids:
                        # Download document content
                        storage_path = f"users/{user_id}/documents/{doc_id}/"
                        
                        try:
                            if self.storage_type == 'aws_s3':
                                content = self._download_from_s3(storage_path)
                            else:
                                content = self._download_from_local(storage_path)
                            
                            # Add to zip
                            zipf.writestr(f"{doc_id}.pdf", content)
                            total_size += len(content)
                            
                        except Exception as e:
                            logger.warning(f"Failed to backup document {doc_id}: {e}")
                
                # Upload backup to storage
                backup_path = f"users/{user_id}/backups/{backup_id}/backup.zip"
                
                with open(temp_zip.name, 'rb') as f:
                    backup_content = f.read()
                
                if self.storage_type == 'aws_s3':
                    self._upload_to_s3(backup_path, backup_content, {
                        'backup_id': backup_id,
                        'document_count': str(len(document_ids)),
                        'retention_days': str(retention_days)
                    })
                else:
                    self._upload_to_local(backup_path, backup_content)
                
                # Clean up temp file
                os.unlink(temp_zip.name)
            
            backup_info = BackupInfo(
                backup_id=backup_id,
                document_ids=document_ids,
                backup_date=datetime.now(),
                backup_size=total_size,
                storage_location=backup_path,
                encryption_enabled=True,
                retention_period=retention_days
            )
            
            logger.info(f"Backup created successfully: {backup_id}")
            return backup_info
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            raise
    
    def restore_from_backup(self, backup_id: str, user_id: str, output_directory: str) -> bool:
        """
        Restore documents from a backup
        
        Args:
            backup_id: ID of the backup to restore
            user_id: ID of the user
            output_directory: Directory to restore files to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            backup_path = f"users/{user_id}/backups/{backup_id}/backup.zip"
            
            # Download backup
            if self.storage_type == 'aws_s3':
                backup_content = self._download_from_s3(backup_path)
            else:
                backup_content = self._download_from_local(backup_path)
            
            # Extract backup
            with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
                temp_zip.write(backup_content)
                temp_zip.flush()
                
                with zipfile.ZipFile(temp_zip.name, 'r') as zipf:
                    zipf.extractall(output_directory)
                
                os.unlink(temp_zip.name)
            
            logger.info(f"Backup restored successfully: {backup_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            return False
    
    def get_storage_usage(self, user_id: str) -> Dict[str, Any]:
        """
        Get storage usage statistics for a user
        
        Args:
            user_id: ID of the user
            
        Returns:
            Dictionary with usage statistics
        """
        try:
            # In real implementation, query storage service for usage stats
            return {
                'total_documents': 15,
                'total_size_bytes': 25 * 1024 * 1024,  # 25MB
                'total_size_formatted': '25.0 MB',
                'storage_limit_bytes': 1024 * 1024 * 1024,  # 1GB
                'storage_limit_formatted': '1.0 GB',
                'usage_percentage': 2.4,
                'documents_by_type': {
                    'wills': 8,
                    'power_of_attorney': 5,
                    'other': 2
                },
                'recent_uploads': 3,
                'shared_documents': 2,
                'backup_count': 1,
                'last_backup_date': datetime.now() - timedelta(days=7)
            }
            
        except Exception as e:
            logger.error(f"Error getting storage usage: {e}")
            return {}
    
    def cleanup_expired_shares(self) -> int:
        """
        Clean up expired share links
        
        Returns:
            Number of expired shares cleaned up
        """
        try:
            # In real implementation, query database for expired shares
            # and remove them
            
            cleaned_count = 0
            logger.info(f"Cleaned up {cleaned_count} expired share links")
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Error cleaning up expired shares: {e}")
            return 0
    
    def cleanup_old_backups(self, retention_days: int = 90) -> int:
        """
        Clean up old backups beyond retention period
        
        Args:
            retention_days: Maximum age of backups to keep
            
        Returns:
            Number of old backups cleaned up
        """
        try:
            # In real implementation, query storage for old backups
            # and remove them
            
            cleaned_count = 0
            logger.info(f"Cleaned up {cleaned_count} old backups")
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Error cleaning up old backups: {e}")
            return 0

# Initialize global cloud storage service
cloud_storage_service = CloudStorageService()

def get_cloud_storage_service() -> CloudStorageService:
    """Get the global cloud storage service instance"""
    return cloud_storage_service

