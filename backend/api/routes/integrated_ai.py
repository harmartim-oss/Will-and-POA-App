"""
Integrated AI API Routes
Provides unified endpoints for comprehensive AI-powered legal document analysis
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import logging

from services.integrated_ai_service import get_integrated_ai_service, IntegratedAIService

logger = logging.getLogger(__name__)

router = APIRouter()

class IntegratedAnalysisRequest(BaseModel):
    """Request model for comprehensive document analysis"""
    document_text: str = Field(..., description="The legal document text to analyze")
    document_type: str = Field(..., description="Type of document (will, power_of_attorney, etc.)")
    user_context: Optional[Dict[str, Any]] = Field(None, description="Additional user context")
    include_research: bool = Field(True, description="Whether to include legal research")
    include_citations: bool = Field(True, description="Whether to include legal citations")

class IntegratedAnalysisResponse(BaseModel):
    """Response model for comprehensive document analysis"""
    success: bool
    analysis: Dict[str, Any]
    confidence_score: float
    compliance_score: float
    suggestions: List[str]
    improvements: List[str]
    risk_assessment: Dict[str, Any]
    legal_citations: List[Dict[str, Any]]
    processing_time_ms: int

class ServiceStatusResponse(BaseModel):
    """Response model for service status"""
    status: str
    services: Dict[str, Any]
    initialized: bool
    timestamp: str

@router.post("/analyze-comprehensive", response_model=IntegratedAnalysisResponse)
async def analyze_document_comprehensive(
    request: IntegratedAnalysisRequest,
    ai_service: IntegratedAIService = Depends(get_integrated_ai_service)
):
    """
    Perform comprehensive document analysis using all available AI services
    """
    try:
        import time
        start_time = time.time()
        
        logger.info(f"Starting comprehensive analysis for document type: {request.document_type}")
        
        # Perform the comprehensive analysis
        result = await ai_service.analyze_document_comprehensive(
            document_text=request.document_text,
            document_type=request.document_type,
            user_context=request.user_context
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return IntegratedAnalysisResponse(
            success=True,
            analysis={
                "nlp_analysis": result.nlp_analysis,
                "legal_research": result.legal_research if request.include_research else {},
            },
            confidence_score=result.confidence_score,
            compliance_score=result.compliance_score,
            suggestions=result.ai_suggestions,
            improvements=result.document_improvements,
            risk_assessment=result.risk_assessment,
            legal_citations=result.legal_citations if request.include_citations else [],
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"Comprehensive analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )

@router.get("/status", response_model=ServiceStatusResponse)
async def get_service_status(
    ai_service: IntegratedAIService = Depends(get_integrated_ai_service)
):
    """
    Get the status of all integrated AI services
    """
    try:
        status_info = ai_service.get_service_status()
        
        return ServiceStatusResponse(
            status="operational" if status_info["initialized"] else "initializing",
            services=status_info,
            initialized=status_info["initialized"],
            timestamp=status_info["timestamp"]
        )
        
    except Exception as e:
        logger.error(f"Status check failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Status check failed: {str(e)}"
        )

@router.post("/initialize")
async def initialize_services(
    ai_service: IntegratedAIService = Depends(get_integrated_ai_service)
):
    """
    Initialize all AI services (useful for warming up the system)
    """
    try:
        logger.info("Initializing integrated AI services...")
        await ai_service.initialize()
        
        return {
            "success": True,
            "message": "All AI services initialized successfully",
            "status": ai_service.get_service_status()
        }
        
    except Exception as e:
        logger.error(f"Service initialization failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Initialization failed: {str(e)}"
        )

@router.post("/analyze-nlp-only")
async def analyze_nlp_only(
    request: IntegratedAnalysisRequest,
    ai_service: IntegratedAIService = Depends(get_integrated_ai_service)
):
    """
    Perform NLP-only analysis (faster, no external API calls)
    """
    try:
        import time
        start_time = time.time()
        
        logger.info("Starting NLP-only analysis")
        
        # Just use the NLP service directly
        nlp_result = await ai_service._analyze_nlp(
            request.document_text, 
            request.document_type
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return {
            "success": True,
            "nlp_analysis": nlp_result,
            "processing_time_ms": processing_time,
            "analysis_type": "nlp_only"
        }
        
    except Exception as e:
        logger.error(f"NLP analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"NLP analysis failed: {str(e)}"
        )

# Add health check endpoint
@router.get("/health")
async def health_check():
    """Simple health check for the integrated AI services"""
    return {
        "status": "healthy",
        "service": "integrated_ai",
        "timestamp": "2024-01-01T00:00:00Z"  # This would be current time in production
    }