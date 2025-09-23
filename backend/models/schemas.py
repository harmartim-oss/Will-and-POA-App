from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class DocumentRequest(BaseModel):
    document_type: str = Field(..., description="Type of legal document")
    content: Dict[str, Any] = Field(..., description="Document content")
    user_info: Optional[Dict[str, Any]] = Field(None, description="User information")

class DocumentResponse(BaseModel):
    success: bool
    document_id: Optional[str] = None
    content: Optional[str] = None
    message: Optional[str] = None

class AIAnalysisRequest(BaseModel):
    document_type: str = Field(..., description="Type of document to analyze")
    content: str = Field(..., description="Document content to analyze")
    analysis_type: Optional[str] = Field("full", description="Type of analysis to perform")

class AIAnalysisResponse(BaseModel):
    success: bool
    analysis: Optional[Dict[str, Any]] = None
    recommendations: Optional[List[str]] = None
    confidence_score: Optional[float] = None
    processing_time: Optional[float] = None

class ComplianceCheckRequest(BaseModel):
    document_type: str = Field(..., description="Type of document to check")
    content: str = Field(..., description="Document content")
    user_info: Optional[Dict[str, Any]] = Field(None, description="User information for checks")

class ComplianceCheckResponse(BaseModel):
    success: bool
    compliance_status: Optional[str] = None
    score: Optional[int] = None
    issues: Optional[List[Dict[str, Any]]] = None
    recommendations: Optional[List[str]] = None

class RiskAssessmentRequest(BaseModel):
    document_type: str = Field(..., description="Type of document to assess")
    content: str = Field(..., description="Document content")
    user_info: Optional[Dict[str, Any]] = Field(None, description="User information")

class RiskAssessmentResponse(BaseModel):
    success: bool
    risk_level: Optional[str] = None
    risk_score: Optional[float] = None
    risk_factors: Optional[List[Dict[str, Any]]] = None
    mitigation_strategies: Optional[List[Dict[str, Any]]] = None

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: str
    components: Dict[str, bool]
    ai_engine_ready: bool