# backend/api/routes/practice.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime, date
import logging
import sys
import os

# Add backend to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from core.practice_management import OntarioPracticeManager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/practice", tags=["practice-management"])

# Global practice manager instance (would be dependency injected in production)
practice_manager = None

def get_practice_manager() -> OntarioPracticeManager:
    """Dependency to get practice manager instance"""
    global practice_manager
    if not practice_manager:
        practice_manager = OntarioPracticeManager()
    if not practice_manager.is_ready():
        raise HTTPException(status_code=503, detail="Practice management system not initialized")
    return practice_manager

# Pydantic models for request/response
class ClientData(BaseModel):
    name: str = Field(..., description="Client full name")
    contact: Dict[str, Any] = Field(default_factory=dict, description="Contact information")

class MatterData(BaseModel):
    type: str = Field(..., description="Matter type (e.g., wills_estates, real_estate)")
    description: Optional[str] = Field(None, description="Matter description")
    responsible_lawyer: str = Field(..., description="LSUC number of responsible lawyer")
    supervising_lawyer: Optional[str] = Field(None, description="LSUC number of supervising lawyer")
    estimated_value: Optional[float] = Field(0.0, description="Estimated matter value")
    trust_account_required: Optional[bool] = Field(False, description="Whether trust account is required")
    conflict_checked: Optional[bool] = Field(False, description="Whether conflict check completed")

class ClientMatterRequest(BaseModel):
    client_data: ClientData
    matter_data: MatterData

class TimeEntryData(BaseModel):
    matter_id: str = Field(..., description="Matter ID")
    lawyer_id: str = Field(..., description="LSUC number")
    date: str = Field(..., description="Date worked (YYYY-MM-DD)")
    duration_minutes: int = Field(..., description="Duration in minutes")
    description: str = Field(..., description="Description of work performed")
    activity_type: Optional[str] = Field("legal_services", description="Type of activity")
    billable: Optional[bool] = Field(True, description="Whether time is billable")
    hourly_rate: Optional[float] = Field(400.0, description="Hourly rate")

class TrustTransactionData(BaseModel):
    matter_id: str = Field(..., description="Matter ID")
    client_id: str = Field(..., description="Client ID")
    date: str = Field(..., description="Transaction date (YYYY-MM-DD)")
    type: str = Field(..., description="Transaction type (receipt, disbursement, transfer)")
    amount: float = Field(..., description="Transaction amount")
    description: Optional[str] = Field("", description="Transaction description")
    reference: Optional[str] = Field("", description="Reference number")
    bank_account: Optional[str] = Field("main_trust", description="Bank account")

class DashboardResponse(BaseModel):
    active_matters: int
    monthly_billable_hours: float
    outstanding_bills: float
    trust_balance: float
    upcoming_deadlines: int
    lsuc_compliance_status: Dict[str, Any]
    generated_at: str

# API endpoints
@router.post("/client-matter", response_model=Dict[str, Any])
async def create_client_matter(
    request: ClientMatterRequest,
    practice_mgr: OntarioPracticeManager = Depends(get_practice_manager)
):
    """Create new client and matter with full setup"""
    try:
        logger.info(f"Creating client and matter: {request.client_data.name}")
        
        result = await practice_mgr.create_client_matter(
            client_data=request.client_data.dict(),
            matter_data=request.matter_data.dict()
        )
        
        return {
            "success": True,
            "data": result,
            "message": "Client and matter created successfully"
        }
        
    except Exception as e:
        logger.error(f"Client matter creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Client matter creation failed: {str(e)}")

@router.post("/time-entry", response_model=Dict[str, Any])
async def track_time_entry(
    time_data: TimeEntryData,
    practice_mgr: OntarioPracticeManager = Depends(get_practice_manager)
):
    """Track billable time with Ontario-specific requirements"""
    try:
        logger.info(f"Recording time entry for matter: {time_data.matter_id}")
        
        result = await practice_mgr.track_time_entry(time_data.dict())
        
        return {
            "success": True,
            "data": result,
            "message": "Time entry recorded successfully"
        }
        
    except Exception as e:
        logger.error(f"Time tracking failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Time tracking failed: {str(e)}")

@router.post("/trust-transaction", response_model=Dict[str, Any])
async def manage_trust_account(
    transaction_data: TrustTransactionData,
    practice_mgr: OntarioPracticeManager = Depends(get_practice_manager)
):
    """Manage trust account with LSUC compliance"""
    try:
        logger.info(f"Processing trust transaction: {transaction_data.type} - ${transaction_data.amount}")
        
        result = await practice_mgr.manage_trust_account(transaction_data.dict())
        
        return {
            "success": True,
            "data": result,
            "message": "Trust transaction processed successfully"
        }
        
    except Exception as e:
        logger.error(f"Trust account management failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Trust account management failed: {str(e)}")

@router.post("/generate-bill/{matter_id}", response_model=Dict[str, Any])
async def generate_monthly_bill(
    matter_id: str,
    bill_date: Optional[str] = None,
    practice_mgr: OntarioPracticeManager = Depends(get_practice_manager)
):
    """Generate compliant monthly bill"""
    try:
        if not bill_date:
            bill_date = datetime.now().date().isoformat()
        
        logger.info(f"Generating monthly bill for matter: {matter_id}")
        
        result = await practice_mgr.generate_monthly_bill(matter_id, bill_date)
        
        return {
            "success": True,
            "data": result,
            "message": "Monthly bill generated successfully"
        }
        
    except Exception as e:
        logger.error(f"Monthly bill generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Monthly bill generation failed: {str(e)}")

@router.get("/dashboard/{lawyer_id}", response_model=Dict[str, Any])
async def get_dashboard_metrics(
    lawyer_id: str,
    practice_mgr: OntarioPracticeManager = Depends(get_practice_manager)
):
    """Get comprehensive practice dashboard metrics"""
    try:
        logger.info(f"Getting dashboard metrics for lawyer: {lawyer_id}")
        
        metrics = await practice_mgr.get_dashboard_metrics(lawyer_id)
        
        return {
            "success": True,
            "data": metrics,
            "message": "Dashboard metrics retrieved successfully"
        }
        
    except Exception as e:
        logger.error(f"Dashboard metrics retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Dashboard metrics retrieval failed: {str(e)}")

@router.get("/matters/client/{client_id}", response_model=Dict[str, Any])
async def get_client_matters(
    client_id: str,
    practice_mgr: OntarioPracticeManager = Depends(get_practice_manager)
):
    """Get all matters for a specific client"""
    try:
        logger.info(f"Getting matters for client: {client_id}")
        
        matters = await practice_mgr.get_client_matters(client_id)
        
        return {
            "success": True,
            "data": matters,
            "message": f"Retrieved {len(matters)} matters for client"
        }
        
    except Exception as e:
        logger.error(f"Client matters retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Client matters retrieval failed: {str(e)}")

@router.get("/time-summary/{matter_id}", response_model=Dict[str, Any])
async def get_time_summary(
    matter_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    practice_mgr: OntarioPracticeManager = Depends(get_practice_manager)
):
    """Get time summary for a matter"""
    try:
        logger.info(f"Getting time summary for matter: {matter_id}")
        
        summary = await practice_mgr.get_time_summary(matter_id, start_date, end_date)
        
        return {
            "success": True,
            "data": summary,
            "message": "Time summary retrieved successfully"
        }
        
    except Exception as e:
        logger.error(f"Time summary retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Time summary retrieval failed: {str(e)}")

@router.get("/deadlines/{lawyer_id}", response_model=Dict[str, Any])
async def get_upcoming_deadlines(
    lawyer_id: str,
    days_ahead: Optional[int] = 30,
    practice_mgr: OntarioPracticeManager = Depends(get_practice_manager)
):
    """Get upcoming deadlines for a lawyer"""
    try:
        logger.info(f"Getting upcoming deadlines for lawyer: {lawyer_id}")
        
        deadlines = await practice_mgr.get_upcoming_deadlines(lawyer_id, days_ahead)
        
        return {
            "success": True,
            "data": deadlines,
            "message": f"Retrieved {len(deadlines)} upcoming deadlines"
        }
        
    except Exception as e:
        logger.error(f"Deadlines retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Deadlines retrieval failed: {str(e)}")

@router.get("/health", response_model=Dict[str, Any])
async def health_check():
    """Health check endpoint for practice management system"""
    try:
        practice_mgr = get_practice_manager()
        return {
            "success": True,
            "status": "healthy",
            "initialized": practice_mgr.is_ready(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }