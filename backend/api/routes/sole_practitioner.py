# backend/api/routes/sole_practitioner.py
"""
API routes for Ontario sole practitioner functionality
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime, timedelta
from pydantic import BaseModel

# Import the new systems
from core.sole_practitioner_management import OntarioSolePractitionerManager
from core.enhanced_ontario_document_generator import OntarioLegalDocumentGenerator
from core.ontario_legal_knowledge import OntarioLegalKnowledgeBase

logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/sole-practitioner", tags=["sole-practitioner"])

# Pydantic models for requests/responses
class ClientRequest(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    referral_source: Optional[str] = None

class MatterRequest(BaseModel):
    client_id: str
    client_name: str
    matter_type: str
    estimated_value: Optional[float] = 0.0
    billing_method: Optional[str] = "hourly"
    priority: Optional[str] = "medium"

class TimeEntryRequest(BaseModel):
    matter_id: str
    duration_minutes: int
    description: str
    hourly_rate: float
    billable: Optional[bool] = True
    activity_type: Optional[str] = "legal_work"
    date: Optional[datetime] = None

class DocumentGenerationRequest(BaseModel):
    document_type: str
    user_data: Dict[str, Any]
    ai_recommendations: Optional[List[str]] = None
    template_id: Optional[str] = None

class CaseLawSearchRequest(BaseModel):
    query: str
    category: Optional[str] = None
    document_type: Optional[str] = None

class ComplianceCheckRequest(BaseModel):
    document_type: str
    content: Dict[str, Any]

# Global instances (will be injected by main.py)
practice_manager: OntarioSolePractitionerManager = None
document_generator: OntarioLegalDocumentGenerator = None 
legal_knowledge: OntarioLegalKnowledgeBase = None

@router.get("/dashboard")
async def get_practice_dashboard():
    """Get practice management dashboard"""
    try:
        if not practice_manager or not practice_manager.is_ready():
            raise HTTPException(status_code=503, detail="Practice manager not ready")
        
        dashboard_data = await practice_manager.get_practice_dashboard()
        return {
            "success": True,
            "data": dashboard_data
        }
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clients")
async def create_client(client_data: ClientRequest):
    """Create new client"""
    try:
        if not practice_manager or not practice_manager.is_ready():
            raise HTTPException(status_code=503, detail="Practice manager not ready")
        
        client_id = await practice_manager.create_new_client(client_data.dict())
        return {
            "success": True,
            "client_id": client_id,
            "message": "Client created successfully"
        }
    except Exception as e:
        logger.error(f"Client creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/matters")
async def create_matter(matter_data: MatterRequest):
    """Create new matter"""
    try:
        if not practice_manager or not practice_manager.is_ready():
            raise HTTPException(status_code=503, detail="Practice manager not ready")
        
        matter_id = await practice_manager.create_new_matter(matter_data.dict())
        return {
            "success": True,
            "matter_id": matter_id,
            "message": "Matter created successfully"
        }
    except Exception as e:
        logger.error(f"Matter creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/time-entries")
async def add_time_entry(time_data: TimeEntryRequest):
    """Add time entry for billing"""
    try:
        if not practice_manager or not practice_manager.is_ready():
            raise HTTPException(status_code=503, detail="Practice manager not ready")
        
        # Set current time if not provided
        if not time_data.date:
            time_data.date = datetime.now()
        
        entry_id = await practice_manager.add_time_entry(time_data.dict())
        return {
            "success": True,
            "entry_id": entry_id,
            "message": "Time entry added successfully"
        }
    except Exception as e:
        logger.error(f"Time entry error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clients/{client_id}/matters")
async def get_client_matters(client_id: str):
    """Get all matters for a client"""
    try:
        if not practice_manager or not practice_manager.is_ready():
            raise HTTPException(status_code=503, detail="Practice manager not ready")
        
        matters = await practice_manager.get_client_matters(client_id)
        return {
            "success": True,
            "matters": matters
        }
    except Exception as e:
        logger.error(f"Client matters error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/matters/{matter_id}/tasks")
async def get_matter_tasks(matter_id: str):
    """Get all tasks for a matter"""
    try:
        if not practice_manager or not practice_manager.is_ready():
            raise HTTPException(status_code=503, detail="Practice manager not ready")
        
        tasks = await practice_manager.get_matter_tasks(matter_id)
        return {
            "success": True,
            "tasks": tasks
        }
    except Exception as e:
        logger.error(f"Matter tasks error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/matters/{matter_id}/bill")
async def generate_bill(matter_id: str, start_date: datetime, end_date: datetime):
    """Generate bill for matter"""
    try:
        if not practice_manager or not practice_manager.is_ready():
            raise HTTPException(status_code=503, detail="Practice manager not ready")
        
        billing_period = {
            "start_date": start_date,
            "end_date": end_date
        }
        
        bill_data = await practice_manager.generate_bill(matter_id, billing_period)
        return {
            "success": True,
            "bill": bill_data
        }
    except Exception as e:
        logger.error(f"Bill generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/billing/summary")
async def get_billing_summary(period: str = "month"):
    """Get billing summary"""
    try:
        if not practice_manager or not practice_manager.is_ready():
            raise HTTPException(status_code=503, detail="Practice manager not ready")
        
        summary = await practice_manager.get_billing_summary(period)
        return {
            "success": True,
            "summary": summary
        }
    except Exception as e:
        logger.error(f"Billing summary error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/generate")
async def generate_legal_document(request: DocumentGenerationRequest):
    """Generate professional legal document"""
    try:
        if not document_generator or not document_generator.is_ready():
            raise HTTPException(status_code=503, detail="Document generator not ready")
        
        document_package = await document_generator.generate_legal_documents(
            request.document_type,
            request.user_data,
            request.ai_recommendations,
            request.template_id
        )
        
        return {
            "success": True,
            "document_package": document_package,
            "message": "Document generated successfully"
        }
    except Exception as e:
        logger.error(f"Document generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/legal/case-law/search")
async def search_case_law(request: CaseLawSearchRequest):
    """Search Ontario case law database"""
    try:
        if not legal_knowledge or not legal_knowledge.is_ready():
            raise HTTPException(status_code=503, detail="Legal knowledge base not ready")
        
        # Search case law
        case_results = legal_knowledge.search_case_law(request.query, request.category)
        
        # Get relevant case law if document type specified
        relevant_cases = []
        if request.document_type:
            relevant_cases = legal_knowledge.get_relevant_case_law(request.query, request.document_type)
        
        return {
            "success": True,
            "query": request.query,
            "category": request.category,
            "case_results": [
                {
                    "case_name": case.case_name,
                    "year": case.year,
                    "court": case.court,
                    "citation": case.citation,
                    "key_principles": case.key_principles,
                    "legal_test": case.legal_test,
                    "outcome": case.outcome
                } for case in case_results
            ],
            "relevant_cases": [
                {
                    "case_name": case.case_name,
                    "year": case.year,
                    "court": case.court,
                    "citation": case.citation,
                    "key_principles": case.key_principles,
                    "legal_test": case.legal_test,
                    "outcome": case.outcome
                } for case in relevant_cases
            ],
            "total_results": len(case_results)
        }
    except Exception as e:
        logger.error(f"Case law search error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/legal/compliance/check")
async def check_document_compliance(request: ComplianceCheckRequest):
    """Check document compliance against Ontario law"""
    try:
        if not legal_knowledge or not legal_knowledge.is_ready():
            raise HTTPException(status_code=503, detail="Legal knowledge base not ready")
        
        compliance_issues = legal_knowledge.check_compliance(
            request.document_type,
            request.content
        )
        
        # Get statutory requirements
        statutory_requirements = legal_knowledge.get_statutory_requirements(request.document_type)
        
        # Calculate compliance score
        total_checks = len(statutory_requirements) if statutory_requirements else 10
        critical_issues = len([issue for issue in compliance_issues if issue.get('severity') == 'critical'])
        major_issues = len([issue for issue in compliance_issues if issue.get('severity') == 'major'])
        
        compliance_score = max(0, (total_checks - critical_issues * 3 - major_issues * 1) / total_checks)
        
        return {
            "success": True,
            "document_type": request.document_type,
            "compliance_score": round(compliance_score, 2),
            "compliance_issues": compliance_issues,
            "statutory_requirements": statutory_requirements,
            "summary": {
                "total_issues": len(compliance_issues),
                "critical_issues": critical_issues,
                "major_issues": major_issues,
                "is_compliant": len(compliance_issues) == 0
            }
        }
    except Exception as e:
        logger.error(f"Compliance check error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/legal/definitions/{term}")
async def get_legal_definition(term: str):
    """Get legal definition for term"""
    try:
        if not legal_knowledge or not legal_knowledge.is_ready():
            raise HTTPException(status_code=503, detail="Legal knowledge base not ready")
        
        definition = legal_knowledge.get_legal_definition(term)
        
        if not definition:
            raise HTTPException(status_code=404, detail=f"No definition found for '{term}'")
        
        return {
            "success": True,
            "term": term,
            "definition": definition
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Legal definition error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/legal/statistics")
async def get_legal_knowledge_statistics():
    """Get legal knowledge base statistics"""
    try:
        if not legal_knowledge or not legal_knowledge.is_ready():
            raise HTTPException(status_code=503, detail="Legal knowledge base not ready")
        
        stats = legal_knowledge.get_statistics()
        return {
            "success": True,
            "statistics": stats
        }
    except Exception as e:
        logger.error(f"Statistics error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check for sole practitioner services"""
    try:
        return {
            "success": True,
            "services": {
                "practice_manager": practice_manager.is_ready() if practice_manager else False,
                "document_generator": document_generator.is_ready() if document_generator else False,
                "legal_knowledge": legal_knowledge.is_ready() if legal_knowledge else False
            },
            "message": "Sole practitioner services operational"
        }
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))