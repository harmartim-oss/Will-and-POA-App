# backend/api/routes/lsuc_compliance.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import sys
import os

# Add backend to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from core.lsuc_compliance import LSUCComplianceManager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/compliance", tags=["lsuc-compliance"])

# Global compliance manager instance (would be dependency injected in production)
compliance_manager = None

def get_compliance_manager() -> LSUCComplianceManager:
    """Dependency to get compliance manager instance"""
    global compliance_manager
    if not compliance_manager:
        compliance_manager = LSUCComplianceManager()
    if not compliance_manager.is_ready():
        raise HTTPException(status_code=503, detail="LSUC compliance system not initialized")
    return compliance_manager

# Pydantic models for request/response
class ActivityLogRequest(BaseModel):
    activity_type: str = Field(..., description="Type of activity (e.g., client_consultation, document_creation)")
    user_id: str = Field(..., description="LSUC number or user ID")
    matter_id: Optional[str] = Field(None, description="Associated matter ID")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional activity details")
    ip_address: Optional[str] = Field(None, description="IP address of user")

class TrustTransactionValidation(BaseModel):
    matter_id: str = Field(..., description="Matter ID")
    client_id: str = Field(..., description="Client ID")
    amount: float = Field(..., description="Transaction amount")
    type: str = Field(..., description="Transaction type (receipt, disbursement, transfer)")
    date: str = Field(..., description="Transaction date (YYYY-MM-DD)")
    description: Optional[str] = Field("", description="Transaction description")
    reference: Optional[str] = Field("", description="Reference number")

class ConflictCheckRequest(BaseModel):
    matter_id: str = Field(..., description="Matter ID")
    client_name: str = Field(..., description="Client name")
    performed_by: str = Field(..., description="LSUC number of person performing check")
    additional_parties: Optional[List[str]] = Field(None, description="Additional parties to check")

class ComplianceReportRequest(BaseModel):
    start_date: str = Field(..., description="Report start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="Report end date (YYYY-MM-DD)")
    lawyer_id: Optional[str] = Field(None, description="Filter by specific lawyer LSUC number")

# API endpoints
@router.post("/log-activity", response_model=Dict[str, Any])
async def log_professional_activity(
    request: ActivityLogRequest,
    compliance_mgr: LSUCComplianceManager = Depends(get_compliance_manager)
):
    """Log professional activity for compliance tracking"""
    try:
        logger.info(f"Logging activity: {request.activity_type} for user {request.user_id}")
        
        log_id = await compliance_mgr.log_activity(
            activity_type=request.activity_type,
            user_id=request.user_id,
            matter_id=request.matter_id,
            details=request.details,
            ip_address=request.ip_address
        )
        
        return {
            "success": True,
            "data": {"log_id": log_id},
            "message": "Activity logged successfully"
        }
        
    except Exception as e:
        logger.error(f"Activity logging failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Activity logging failed: {str(e)}")

@router.post("/validate-trust-transaction", response_model=Dict[str, Any])
async def validate_trust_transaction(
    request: TrustTransactionValidation,
    compliance_mgr: LSUCComplianceManager = Depends(get_compliance_manager)
):
    """Validate trust account transaction for LSUC compliance"""
    try:
        logger.info(f"Validating trust transaction: {request.type} - ${request.amount}")
        
        validation_result = await compliance_mgr.validate_trust_transaction(request.dict())
        
        return {
            "success": True,
            "data": validation_result,
            "message": "Trust transaction validation completed"
        }
        
    except Exception as e:
        logger.error(f"Trust transaction validation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Trust transaction validation failed: {str(e)}")

@router.post("/conflict-check", response_model=Dict[str, Any])
async def perform_conflict_check(
    request: ConflictCheckRequest,
    compliance_mgr: LSUCComplianceManager = Depends(get_compliance_manager)
):
    """Perform conflict of interest check"""
    try:
        logger.info(f"Performing conflict check for matter: {request.matter_id}")
        
        result = await compliance_mgr.perform_conflict_check(
            matter_id=request.matter_id,
            client_name=request.client_name,
            performed_by=request.performed_by,
            additional_parties=request.additional_parties
        )
        
        return {
            "success": True,
            "data": result,
            "message": "Conflict check completed successfully"
        }
        
    except Exception as e:
        logger.error(f"Conflict check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Conflict check failed: {str(e)}")

@router.post("/compliance-report", response_model=Dict[str, Any])
async def generate_compliance_report(
    request: ComplianceReportRequest,
    compliance_mgr: LSUCComplianceManager = Depends(get_compliance_manager)
):
    """Generate compliance report for specified period"""
    try:
        logger.info(f"Generating compliance report: {request.start_date} to {request.end_date}")
        
        report = await compliance_mgr.get_compliance_report(
            start_date=request.start_date,
            end_date=request.end_date,
            lawyer_id=request.lawyer_id
        )
        
        return {
            "success": True,
            "data": report,
            "message": "Compliance report generated successfully"
        }
        
    except Exception as e:
        logger.error(f"Compliance report generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Compliance report generation failed: {str(e)}")

@router.get("/health", response_model=Dict[str, Any])
async def health_check():
    """Health check endpoint for LSUC compliance system"""
    try:
        compliance_mgr = get_compliance_manager()
        return {
            "success": True,
            "status": "healthy",
            "initialized": compliance_mgr.is_ready(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }