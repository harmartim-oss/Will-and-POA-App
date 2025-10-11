"""
Email API Routes
Endpoints for sending documents and notifications via email
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Optional
import logging
from pydantic import BaseModel, EmailStr

from services.email_service import get_email_service

logger = logging.getLogger(__name__)

router = APIRouter()

# Request Models
class SendDocumentEmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    document_name: str
    message_body: Optional[str] = None
    document_type: str = "application/pdf"

class SendNotificationRequest(BaseModel):
    to_email: EmailStr
    subject: str
    message_body: str
    template_id: Optional[str] = None

@router.post("/send-document")
async def send_document_email(
    request: SendDocumentEmailRequest,
    document: UploadFile = File(...)
):
    """Send a document via email"""
    try:
        email_service = get_email_service()
        
        # Read document content
        content = await document.read()
        
        # Send email
        result = email_service.send_document_email(
            to_email=request.to_email,
            subject=request.subject,
            document_content=content,
            document_name=request.document_name,
            message_body=request.message_body,
            document_type=request.document_type
        )
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result['error'])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending document email: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-notification")
async def send_notification(request: SendNotificationRequest):
    """Send a notification email"""
    try:
        email_service = get_email_service()
        
        result = email_service.send_notification_email(
            to_email=request.to_email,
            subject=request.subject,
            message_body=request.message_body,
            template_id=request.template_id
        )
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result['error'])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def email_status():
    """Get email service status"""
    email_service = get_email_service()
    
    return {
        'success': True,
        'configured': email_service.client is not None,
        'simulation_mode': email_service.client is None,
        'from_email': email_service.from_email,
        'from_name': email_service.from_name
    }
