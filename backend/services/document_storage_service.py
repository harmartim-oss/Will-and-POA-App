"""
Document Storage Service
Handles secure storage, retrieval, and management of generated legal documents
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import hashlib
import uuid
from pathlib import Path

logger = logging.getLogger(__name__)

class DocumentStorageService:
    """
    Service for storing and managing legal documents
    """
    
    def __init__(self, storage_path: str = None):
        """Initialize document storage service"""
        self.storage_path = storage_path or os.getenv(
            'DOCUMENT_STORAGE_PATH', 
            '/tmp/document_storage'
        )
        self.metadata_file = os.path.join(self.storage_path, 'metadata.json')
        self._ensure_storage_directory()
        self._load_metadata()
        logger.info(f"Document storage initialized at {self.storage_path}")
    
    def _ensure_storage_directory(self):
        """Ensure storage directory exists"""
        Path(self.storage_path).mkdir(parents=True, exist_ok=True)
        logger.info(f"Storage directory ensured at {self.storage_path}")
    
    def _load_metadata(self):
        """Load metadata from storage"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
                logger.info(f"Loaded {len(self.metadata)} document metadata entries")
            except Exception as e:
                logger.error(f"Error loading metadata: {e}")
                self.metadata = {}
        else:
            self.metadata = {}
    
    def _save_metadata(self):
        """Save metadata to storage"""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
            logger.info("Metadata saved successfully")
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
    
    def store_document(
        self,
        document_content: bytes,
        document_type: str,
        user_id: str,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Store a document with metadata
        
        Args:
            document_content: Document binary content
            document_type: Type of document (will, poa, etc.)
            user_id: User ID who created the document
            metadata: Additional metadata
            
        Returns:
            Dictionary with document ID and storage info
        """
        try:
            # Generate unique document ID
            document_id = str(uuid.uuid4())
            
            # Calculate document hash for integrity
            doc_hash = hashlib.sha256(document_content).hexdigest()
            
            # Create document filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{document_type}_{timestamp}_{document_id[:8]}.bin"
            filepath = os.path.join(self.storage_path, filename)
            
            # Store document
            with open(filepath, 'wb') as f:
                f.write(document_content)
            
            # Store metadata
            doc_metadata = {
                'document_id': document_id,
                'document_type': document_type,
                'user_id': user_id,
                'filename': filename,
                'filepath': filepath,
                'file_size': len(document_content),
                'hash': doc_hash,
                'created_at': datetime.now().isoformat(),
                'status': 'stored',
                'metadata': metadata or {}
            }
            
            self.metadata[document_id] = doc_metadata
            self._save_metadata()
            
            logger.info(f"Document {document_id} stored successfully")
            
            return {
                'success': True,
                'document_id': document_id,
                'filename': filename,
                'hash': doc_hash,
                'created_at': doc_metadata['created_at']
            }
            
        except Exception as e:
            logger.error(f"Error storing document: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def retrieve_document(self, document_id: str) -> Dict[str, Any]:
        """
        Retrieve a document by ID
        
        Args:
            document_id: Document ID
            
        Returns:
            Dictionary with document content and metadata
        """
        try:
            if document_id not in self.metadata:
                return {
                    'success': False,
                    'error': 'Document not found'
                }
            
            doc_meta = self.metadata[document_id]
            filepath = doc_meta['filepath']
            
            if not os.path.exists(filepath):
                return {
                    'success': False,
                    'error': 'Document file not found'
                }
            
            with open(filepath, 'rb') as f:
                content = f.read()
            
            # Verify hash
            current_hash = hashlib.sha256(content).hexdigest()
            if current_hash != doc_meta['hash']:
                logger.warning(f"Document {document_id} hash mismatch!")
            
            return {
                'success': True,
                'document_id': document_id,
                'content': content,
                'metadata': doc_meta
            }
            
        except Exception as e:
            logger.error(f"Error retrieving document {document_id}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_documents(
        self,
        user_id: Optional[str] = None,
        document_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List documents with optional filters
        
        Args:
            user_id: Filter by user ID
            document_type: Filter by document type
            limit: Maximum number of documents to return
            
        Returns:
            List of document metadata
        """
        try:
            documents = []
            
            for doc_id, doc_meta in self.metadata.items():
                # Apply filters
                if user_id and doc_meta['user_id'] != user_id:
                    continue
                if document_type and doc_meta['document_type'] != document_type:
                    continue
                
                # Remove sensitive file paths from response
                safe_meta = doc_meta.copy()
                safe_meta.pop('filepath', None)
                documents.append(safe_meta)
                
                if len(documents) >= limit:
                    break
            
            # Sort by creation date (newest first)
            documents.sort(
                key=lambda x: x.get('created_at', ''),
                reverse=True
            )
            
            return documents
            
        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            return []
    
    def delete_document(self, document_id: str, user_id: str = None) -> Dict[str, Any]:
        """
        Delete a document
        
        Args:
            document_id: Document ID
            user_id: Optional user ID for authorization
            
        Returns:
            Success status
        """
        try:
            if document_id not in self.metadata:
                return {
                    'success': False,
                    'error': 'Document not found'
                }
            
            doc_meta = self.metadata[document_id]
            
            # Check authorization if user_id provided
            if user_id and doc_meta['user_id'] != user_id:
                return {
                    'success': False,
                    'error': 'Unauthorized'
                }
            
            # Delete file
            filepath = doc_meta['filepath']
            if os.path.exists(filepath):
                os.remove(filepath)
            
            # Remove metadata
            del self.metadata[document_id]
            self._save_metadata()
            
            logger.info(f"Document {document_id} deleted successfully")
            
            return {
                'success': True,
                'message': 'Document deleted successfully'
            }
            
        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_document_status(
        self,
        document_id: str,
        status: str,
        metadata_update: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Update document status and metadata
        
        Args:
            document_id: Document ID
            status: New status
            metadata_update: Additional metadata to update
            
        Returns:
            Success status
        """
        try:
            if document_id not in self.metadata:
                return {
                    'success': False,
                    'error': 'Document not found'
                }
            
            self.metadata[document_id]['status'] = status
            self.metadata[document_id]['updated_at'] = datetime.now().isoformat()
            
            if metadata_update:
                self.metadata[document_id]['metadata'].update(metadata_update)
            
            self._save_metadata()
            
            logger.info(f"Document {document_id} status updated to {status}")
            
            return {
                'success': True,
                'message': 'Document updated successfully'
            }
            
        except Exception as e:
            logger.error(f"Error updating document {document_id}: {e}")
            return {
                'success': False,
                'error': str(e)
            }

# Global instance
_storage_service = None

def get_document_storage_service() -> DocumentStorageService:
    """Get or create document storage service instance"""
    global _storage_service
    if _storage_service is None:
        _storage_service = DocumentStorageService()
    return _storage_service
