"""
Enhanced AI API Routes
Advanced AI capabilities for legal research, case prediction, and analysis
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Request/Response Models
class LegalResearchRequest(BaseModel):
    query: str = Field(..., description="Legal research query")
    jurisdiction: str = Field(default="Ontario", description="Legal jurisdiction")
    max_results: int = Field(default=10, ge=1, le=50, description="Maximum number of results")

class CasePredictionRequest(BaseModel):
    case_data: Dict[str, Any] = Field(..., description="Case facts and details")

class LegalArgumentRequest(BaseModel):
    topic: str = Field(..., description="Legal argument topic")
    position: str = Field(..., description="Legal position to argue")
    supporting_facts: List[str] = Field(..., description="Supporting facts")

class RiskAnalysisRequest(BaseModel):
    document_content: str = Field(..., description="Document content to analyze")
    document_type: str = Field(..., description="Type of document")
    client_situation: Dict[str, Any] = Field(..., description="Client situation details")

class CaseStrategyRequest(BaseModel):
    case_facts: Dict[str, Any] = Field(..., description="Case facts")
    legal_issues: List[str] = Field(..., description="Legal issues involved")
    desired_outcome: str = Field(..., description="Desired case outcome")

# Dependency to get Enhanced Legal AI instance
async def get_enhanced_ai():
    """Get Enhanced Legal AI instance from main app"""
    # Import here to avoid circular imports
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    
    try:
        from main import enhanced_legal_ai
        if not enhanced_legal_ai.is_initialized:
            raise HTTPException(status_code=503, detail="Enhanced Legal AI not initialized")
        return enhanced_legal_ai
    except ImportError:
        raise HTTPException(status_code=503, detail="Enhanced Legal AI not available")

@router.post("/research", summary="Perform Legal Research")
async def perform_legal_research(
    request: LegalResearchRequest,
    ai: Any = Depends(get_enhanced_ai)
):
    """
    Perform comprehensive legal research using advanced AI capabilities
    """
    try:
        logger.info(f"Legal research requested: {request.query}")
        
        result = await ai.perform_legal_research(
            query=request.query,
            jurisdiction=request.jurisdiction,
            max_results=request.max_results
        )
        
        return {
            "success": True,
            "data": {
                "query": result.query,
                "relevant_cases": result.relevant_cases,
                "statutes": result.statutes,
                "analysis": result.analysis,
                "confidence": result.confidence,
                "recommendations": result.recommendations
            }
        }
        
    except Exception as e:
        logger.error(f"Legal research failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Legal research failed: {str(e)}")

@router.post("/predict-case", summary="Predict Case Outcome")
async def predict_case_outcome(
    request: CasePredictionRequest,
    ai: Any = Depends(get_enhanced_ai)
):
    """
    Predict case outcome using machine learning and case analysis
    """
    try:
        logger.info("Case outcome prediction requested")
        
        prediction = await ai.predict_case_outcome(request.case_data)
        
        return {
            "success": True,
            "data": {
                "predicted_outcome": prediction.predicted_outcome,
                "probability": prediction.probability,
                "key_factors": prediction.key_factors,
                "similar_cases": prediction.similar_cases,
                "confidence_level": prediction.confidence_level,
                "success_probability": prediction.success_probability
            }
        }
        
    except Exception as e:
        logger.error(f"Case prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Case prediction failed: {str(e)}")

@router.post("/generate-argument", summary="Generate Legal Argument")
async def generate_legal_argument(
    request: LegalArgumentRequest,
    ai: Any = Depends(get_enhanced_ai)
):
    """
    Generate comprehensive legal argument with supporting authorities
    """
    try:
        logger.info(f"Legal argument generation requested: {request.topic}")
        
        argument = await ai.generate_legal_argument(
            topic=request.topic,
            position=request.position,
            supporting_facts=request.supporting_facts
        )
        
        return {
            "success": True,
            "data": argument
        }
        
    except Exception as e:
        logger.error(f"Legal argument generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Legal argument generation failed: {str(e)}")

@router.post("/analyze-risk", summary="Analyze Legal Risk")
async def analyze_legal_risk(
    request: RiskAnalysisRequest,
    ai: Any = Depends(get_enhanced_ai)
):
    """
    Analyze legal risks in documents and client situations
    """
    try:
        logger.info("Legal risk analysis requested")
        
        risk_analysis = await ai.analyze_legal_risk(
            document_content=request.document_content,
            document_type=request.document_type,
            client_situation=request.client_situation
        )
        
        return {
            "success": True,
            "data": risk_analysis
        }
        
    except Exception as e:
        logger.error(f"Risk analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Risk analysis failed: {str(e)}")

@router.post("/suggest-strategy", summary="Suggest Case Strategy")
async def suggest_case_strategy(
    request: CaseStrategyRequest,
    ai: Any = Depends(get_enhanced_ai)
):
    """
    Suggest case strategy based on AI analysis and precedents
    """
    try:
        logger.info("Case strategy suggestion requested")
        
        strategy = await ai.suggest_case_strategy(
            case_facts=request.case_facts,
            legal_issues=request.legal_issues,
            desired_outcome=request.desired_outcome
        )
        
        return {
            "success": True,
            "data": strategy
        }
        
    except Exception as e:
        logger.error(f"Case strategy suggestion failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Case strategy suggestion failed: {str(e)}")

@router.get("/status", summary="Enhanced AI Status")
async def get_enhanced_ai_status(ai: Any = Depends(get_enhanced_ai)):
    """
    Get status and capabilities of Enhanced Legal AI system
    """
    try:
        return {
            "success": True,
            "data": {
                "initialized": ai.is_initialized,
                "ml_models": {
                    name: model.is_initialized for name, model in ai.ml_models.items()
                },
                "prediction_engine": ai.prediction_engine.is_initialized if ai.prediction_engine else False,
                "capabilities": [
                    "legal_research",
                    "case_prediction", 
                    "argument_generation",
                    "risk_analysis",
                    "strategy_suggestion"
                ]
            }
        }
        
    except Exception as e:
        logger.error(f"Status check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")