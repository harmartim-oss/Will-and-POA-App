"""
Storage API Routes
Endpoints for document storage and retrieval
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from typing import List, Optional
import logging

from services.document_storage_service import get_document_storage_service
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter()

# Request/Response Models
class StoreDocumentRequest(BaseModel):
    document_type: str
    user_id: str
    metadata: dict = {}

class DocumentResponse(BaseModel):
    success: bool
    document_id: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None

@router.post("/store", response_model=DocumentResponse)
async def store_document(
    document: UploadFile = File(...),
    document_type: str = "general",
    user_id: str = "anonymous"
):
    """Store a document"""
    try:
        storage = get_document_storage_service()
        
        # Read document content
        content = await document.read()
        
        # Store document
        result = storage.store_document(
            document_content=content,
            document_type=document_type,
            user_id=user_id,
            metadata={
                'original_filename': document.filename,
                'content_type': document.content_type
            }
        )
        
        return DocumentResponse(**result)
        
    except Exception as e:
        logger.error(f"Error storing document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/retrieve/{document_id}")
async def retrieve_document(document_id: str):
    """Retrieve a document by ID"""
    try:
        storage = get_document_storage_service()
        
        result = storage.retrieve_document(document_id)
        
        if not result['success']:
            raise HTTPException(status_code=404, detail=result['error'])
        
        # Return document metadata (not content for security)
        return {
            'success': True,
            'document_id': document_id,
            'metadata': result['metadata']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_documents(
    user_id: Optional[str] = None,
    document_type: Optional[str] = None,
    limit: int = 100
):
    """List documents with optional filters"""
    try:
        storage = get_document_storage_service()
        
        documents = storage.list_documents(
            user_id=user_id,
            document_type=document_type,
            limit=limit
        )
        
        return {
            'success': True,
            'count': len(documents),
            'documents': documents
        }
        
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{document_id}")
async def delete_document(
    document_id: str,
    user_id: Optional[str] = None
):
    """Delete a document"""
    try:
        storage = get_document_storage_service()
        
        result = storage.delete_document(document_id, user_id)
        
        if not result['success']:
            raise HTTPException(
                status_code=404 if 'not found' in result.get('error', '').lower() else 403,
                detail=result['error']
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))
