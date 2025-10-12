"""
Payment Processing Service
Handles payment processing using Stripe
"""

import os
import logging
from typing import Dict, Optional, Any
from datetime import datetime
from decimal import Decimal

logger = logging.getLogger(__name__)

# Optional Stripe import with fallback
try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    logger.warning("Stripe not available - payment functionality will be simulated")

class PaymentService:
    """
    Service for processing payments via Stripe
    """
    
    # Pricing in CAD (Canadian dollars)
    PRICING = {
        'basic_will': 49.99,
        'premium_will': 99.99,
        'poa_property': 39.99,
        'poa_personal_care': 39.99,
        'poa_combo': 69.99,
        'complete_package': 149.99,
        'lawyer_review': 299.99,
        'rush_processing': 49.99
    }
    
    def __init__(self):
        """Initialize payment service"""
        self.api_key = os.getenv('STRIPE_SECRET_KEY')
        self.publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
        self.webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
        self.currency = 'cad'
        
        if STRIPE_AVAILABLE and self.api_key:
            stripe.api_key = self.api_key
            logger.info("Payment service initialized with Stripe")
        else:
            logger.warning("Payment service in simulation mode (no Stripe API key)")
    
    def create_payment_intent(
        self,
        amount: float,
        user_id: str,
        document_type: str,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create a payment intent for processing
        
        Args:
            amount: Payment amount in CAD
            user_id: User ID making the payment
            document_type: Type of document being purchased
            metadata: Additional metadata
            
        Returns:
            Payment intent details
        """
        try:
            if not STRIPE_AVAILABLE or not self.api_key:
                # Simulation mode
                payment_id = f"sim_pi_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                logger.info(f"[SIMULATION] Would create payment intent")
                logger.info(f"[SIMULATION] Amount: ${amount:.2f} CAD")
                logger.info(f"[SIMULATION] User: {user_id}")
                logger.info(f"[SIMULATION] Document: {document_type}")
                
                return {
                    'success': True,
                    'simulation': True,
                    'payment_intent_id': payment_id,
                    'client_secret': f"sim_secret_{payment_id}",
                    'amount': amount,
                    'currency': self.currency,
                    'status': 'simulated',
                    'message': 'Payment simulated (no Stripe configured)'
                }
            
            # Convert amount to cents
            amount_cents = int(amount * 100)
            
            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=self.currency,
                metadata={
                    'user_id': user_id,
                    'document_type': document_type,
                    'timestamp': datetime.now().isoformat(),
                    **(metadata or {})
                }
            )
            
            logger.info(f"Payment intent created: {intent.id}")
            
            return {
                'success': True,
                'payment_intent_id': intent.id,
                'client_secret': intent.client_secret,
                'amount': amount,
                'currency': self.currency,
                'status': intent.status
            }
            
        except Exception as e:
            logger.error(f"Error creating payment intent: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def confirm_payment(
        self,
        payment_intent_id: str
    ) -> Dict[str, Any]:
        """
        Confirm a payment intent
        
        Args:
            payment_intent_id: Payment intent ID
            
        Returns:
            Payment confirmation details
        """
        try:
            if not STRIPE_AVAILABLE or not self.api_key:
                # Simulation mode
                logger.info(f"[SIMULATION] Would confirm payment {payment_intent_id}")
                
                return {
                    'success': True,
                    'simulation': True,
                    'payment_intent_id': payment_intent_id,
                    'status': 'succeeded',
                    'message': 'Payment confirmed (simulated)'
                }
            
            # Retrieve payment intent
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            logger.info(f"Payment intent {payment_intent_id} status: {intent.status}")
            
            return {
                'success': True,
                'payment_intent_id': intent.id,
                'status': intent.status,
                'amount': intent.amount / 100,
                'currency': intent.currency
            }
            
        except Exception as e:
            logger.error(f"Error confirming payment {payment_intent_id}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_checkout_session(
        self,
        product_type: str,
        user_id: str,
        success_url: str,
        cancel_url: str,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create a Stripe Checkout session
        
        Args:
            product_type: Type of product being purchased
            user_id: User ID making the purchase
            success_url: URL to redirect on success
            cancel_url: URL to redirect on cancel
            metadata: Additional metadata
            
        Returns:
            Checkout session details
        """
        try:
            # Get price for product type
            price = self.PRICING.get(product_type)
            if not price:
                return {
                    'success': False,
                    'error': f'Invalid product type: {product_type}'
                }
            
            if not STRIPE_AVAILABLE or not self.api_key:
                # Simulation mode
                session_id = f"sim_cs_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                logger.info(f"[SIMULATION] Would create checkout session")
                logger.info(f"[SIMULATION] Product: {product_type} - ${price:.2f} CAD")
                
                return {
                    'success': True,
                    'simulation': True,
                    'session_id': session_id,
                    'checkout_url': f"{success_url}?session_id={session_id}",
                    'amount': price,
                    'product_type': product_type,
                    'message': 'Checkout simulated (no Stripe configured)'
                }
            
            # Create checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': self.currency,
                        'unit_amount': int(price * 100),
                        'product_data': {
                            'name': product_type.replace('_', ' ').title(),
                            'description': f'Ontario Legal Document - {product_type}'
                        }
                    },
                    'quantity': 1
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    'user_id': user_id,
                    'product_type': product_type,
                    'timestamp': datetime.now().isoformat(),
                    **(metadata or {})
                }
            )
            
            logger.info(f"Checkout session created: {session.id}")
            
            return {
                'success': True,
                'session_id': session.id,
                'checkout_url': session.url,
                'amount': price,
                'product_type': product_type
            }
            
        except Exception as e:
            logger.error(f"Error creating checkout session: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_refund(
        self,
        payment_intent_id: str,
        amount: Optional[float] = None,
        reason: str = None
    ) -> Dict[str, Any]:
        """
        Process a refund
        
        Args:
            payment_intent_id: Payment intent ID to refund
            amount: Optional partial refund amount
            reason: Refund reason
            
        Returns:
            Refund details
        """
        try:
            if not STRIPE_AVAILABLE or not self.api_key:
                # Simulation mode
                refund_id = f"sim_re_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                logger.info(f"[SIMULATION] Would process refund for {payment_intent_id}")
                logger.info(f"[SIMULATION] Reason: {reason}")
                
                return {
                    'success': True,
                    'simulation': True,
                    'refund_id': refund_id,
                    'status': 'succeeded',
                    'message': 'Refund simulated (no Stripe configured)'
                }
            
            # Create refund
            refund_params = {
                'payment_intent': payment_intent_id
            }
            
            if amount:
                refund_params['amount'] = int(amount * 100)
            
            if reason:
                refund_params['reason'] = reason
            
            refund = stripe.Refund.create(**refund_params)
            
            logger.info(f"Refund created: {refund.id}")
            
            return {
                'success': True,
                'refund_id': refund.id,
                'status': refund.status,
                'amount': refund.amount / 100 if refund.amount else None
            }
            
        except Exception as e:
            logger.error(f"Error processing refund: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_pricing(self) -> Dict[str, float]:
        """Get current pricing information"""
        return self.PRICING.copy()

# Global instance
_payment_service = None

def get_payment_service() -> PaymentService:
    """Get or create payment service instance"""
    global _payment_service
    if _payment_service is None:
        _payment_service = PaymentService()
    return _payment_service
