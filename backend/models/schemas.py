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

# New schemas for enhanced AI system
class DocumentAnalysisRequest(BaseModel):
    text: str = Field(..., description="Document text to analyze")
    document_type: str = Field(..., description="Type of document")
    case_context: Optional[str] = Field(None, description="Additional case context")

class DocumentAnalysisResponse(BaseModel):
    document_id: str
    document_type: str
    confidence: float
    entities: List[Dict[str, Any]]
    requirements: List[Dict[str, Any]]
    compliance_issues: List[Dict[str, Any]]
    recommendations: List[str]
    sentiment: Dict[str, Any]
    processing_time: float
    timestamp: str

class DocumentGenerationRequest(BaseModel):
    document_type: str = Field(..., description="Type of document to generate")
    user_data: Dict[str, Any] = Field(..., description="User data for document generation")
    include_ai_recommendations: Optional[bool] = Field(True, description="Include AI recommendations")
    template_id: Optional[str] = Field(None, description="Specific template ID to use")

class DocumentGenerationResponse(BaseModel):
    document_id: str
    download_url: str
    docx_url: str
    pdf_url: str
    blockchain_hash: Optional[str]
    authentication_token: str

class LegalQueryRequest(BaseModel):
    query: str = Field(..., description="Legal query")
    document_context: Optional[str] = Field(None, description="Document context")
    document_type: Optional[str] = Field(None, description="Document type for context")

class LegalQueryResponse(BaseModel):
    answer: str
    confidence: float
    relevant_cases: List[Dict[str, Any]]
    legal_sources: List[str]
    recommendations: List[str]