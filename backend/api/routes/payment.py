"""
Payment API Routes
Endpoints for payment processing via Stripe
"""

from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, Any
import logging
from pydantic import BaseModel

from services.payment_service import get_payment_service

logger = logging.getLogger(__name__)

router = APIRouter()

# Request Models
class CreatePaymentIntentRequest(BaseModel):
    amount: float
    user_id: str
    document_type: str
    metadata: Optional[Dict[str, Any]] = None

class CreateCheckoutSessionRequest(BaseModel):
    product_type: str
    user_id: str
    success_url: str
    cancel_url: str
    metadata: Optional[Dict[str, Any]] = None

class ProcessRefundRequest(BaseModel):
    payment_intent_id: str
    amount: Optional[float] = None
    reason: Optional[str] = None

@router.post("/create-payment-intent")
async def create_payment_intent(request: CreatePaymentIntentRequest):
    """Create a payment intent"""
    try:
        payment_service = get_payment_service()
        
        result = payment_service.create_payment_intent(
            amount=request.amount,
            user_id=request.user_id,
            document_type=request.document_type,
            metadata=request.metadata
        )
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result['error'])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating payment intent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create-checkout-session")
async def create_checkout_session(request: CreateCheckoutSessionRequest):
    """Create a Stripe Checkout session"""
    try:
        payment_service = get_payment_service()
        
        result = payment_service.create_checkout_session(
            product_type=request.product_type,
            user_id=request.user_id,
            success_url=request.success_url,
            cancel_url=request.cancel_url,
            metadata=request.metadata
        )
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result['error'])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating checkout session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/confirm-payment/{payment_intent_id}")
async def confirm_payment(payment_intent_id: str):
    """Confirm a payment"""
    try:
        payment_service = get_payment_service()
        
        result = payment_service.confirm_payment(payment_intent_id)
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result['error'])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error confirming payment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refund")
async def process_refund(request: ProcessRefundRequest):
    """Process a refund"""
    try:
        payment_service = get_payment_service()
        
        result = payment_service.process_refund(
            payment_intent_id=request.payment_intent_id,
            amount=request.amount,
            reason=request.reason
        )
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result['error'])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing refund: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pricing")
async def get_pricing():
    """Get pricing information"""
    try:
        payment_service = get_payment_service()
        pricing = payment_service.get_pricing()
        
        return {
            'success': True,
            'currency': 'CAD',
            'pricing': pricing
        }
        
    except Exception as e:
        logger.error(f"Error getting pricing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def payment_status():
    """Get payment service status"""
    payment_service = get_payment_service()
    
    return {
        'success': True,
        'configured': payment_service.api_key is not None,
        'simulation_mode': payment_service.api_key is None,
        'currency': payment_service.currency
    }
