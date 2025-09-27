from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
from typing import List, Optional, Dict, Any
import asyncio
from datetime import datetime
import logging

from core.ai_engine import OntarioLegalAIEngine
from core.document_generator import OntarioDocumentGenerator
from core.legal_knowledge import OntarioLegalKnowledgeBase
from core.compliance_checker import OntarioComplianceChecker
from core.risk_assessor import OntarioRiskAssessor
from core.practice_management import OntarioPracticeManager
from core.lsuc_compliance import LSUCComplianceManager
from core.case_law_analyzer import OntarioCaseLawAnalyzer
from services.enhanced_legal_ai import EnhancedLegalAI
from services.enhanced_ai_legal_service import EnhancedAILegalService

# Import new AI system components
from core.database_manager import DatabaseManager
from core.blockchain_authenticator import BlockchainAuthenticator
from core.ontario_legal_knowledge import OntarioLegalKnowledgeBase as EnhancedLegalKnowledge
from core.ontario_document_generator import OntarioLegalDocumentGenerator
from core.sole_practitioner_security import OntarioLegalSecurityManager

from api.routes import documents, ai, compliance, blockchain, enhanced_ai
# Import new practice management routes individually to avoid circular imports
from api.routes.practice import router as practice_router
from api.routes.lsuc_compliance import router as lsuc_router
from database.connection import init_db
from models.schemas import (
    DocumentRequest, DocumentResponse, 
    AIAnalysisRequest, AIAnalysisResponse,
    ComplianceCheckRequest, ComplianceCheckResponse,
    DocumentAnalysisRequest, DocumentAnalysisResponse,
    DocumentGenerationRequest, DocumentGenerationResponse,
    LegalQueryRequest, LegalQueryResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Ontario Legal Document AI System with Practice Management",
    description="AI-powered legal document generation, analysis, and comprehensive practice management for Ontario sole practitioners",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize AI components and practice management
ai_engine = OntarioLegalAIEngine()
doc_generator = OntarioDocumentGenerator()
legal_knowledge = OntarioLegalKnowledgeBase()
compliance_checker = OntarioComplianceChecker()
risk_assessor = OntarioRiskAssessor()
enhanced_legal_ai = EnhancedLegalAI()
enhanced_ai_legal_service = EnhancedAILegalService()
case_law_analyzer = OntarioCaseLawAnalyzer()

# Initialize practice management components
practice_manager = OntarioPracticeManager()
lsuc_compliance_manager = LSUCComplianceManager()

# Initialize enhanced AI system components
database = DatabaseManager()
blockchain_auth = BlockchainAuthenticator()
enhanced_legal_knowledge = EnhancedLegalKnowledge()
enhanced_doc_generator = OntarioLegalDocumentGenerator()
security_manager = OntarioLegalSecurityManager()

@app.on_event("startup")
async def startup_event():
    """Initialize AI systems on startup"""
    logger.info("Initializing Ontario Legal AI System...")
    
    try:
        # Initialize database
        await database.initialize()
        logger.info("✓ Database initialized")
        
        # Initialize legacy database
        await init_db()
        
        # Initialize AI components
        await ai_engine.initialize()
        await legal_knowledge.initialize()
        await enhanced_legal_knowledge.initialize()
        
        # Initialize case law analyzer
        await case_law_analyzer.initialize()
        
        # Initialize document generator
        await enhanced_doc_generator.initialize()
        
        # Initialize security manager
        await security_manager.initialize()
        
        # Initialize blockchain authenticator
        await blockchain_auth.initialize()
        
        # Initialize Enhanced Legal AI
        await enhanced_legal_ai.initialize()
        
        # Initialize practice management system
        logger.info("Initializing Practice Management System...")
        await practice_manager.initialize()
        
        # Make services available to API routes
        import api.routes.practice as practice_module
        import api.routes.lsuc_compliance as compliance_module
        import api.routes.documents as documents_module
        
        practice_module.practice_manager = practice_manager
        compliance_module.compliance_manager = lsuc_compliance_manager
        documents_module.ai_legal_service = enhanced_ai_legal_service
        documents_module.case_law_analyzer = case_law_analyzer
        
        logger.info("✓ All systems initialized successfully")
        logger.info("✓ Enhanced AI Legal Service ready for case predictions")
        logger.info("✓ Case Law Analyzer loaded with Ontario legal precedents")
        logger.info("✓ Blockchain authentication system ready")
        logger.info("✓ Security manager initialized with encryption")
        
    except Exception as e:
        logger.error(f"✗ Failed to initialize systems: {str(e)}")
        raise

@app.get("/")
async def root():
    return {
        "message": "Ontario Legal Document AI System with Practice Management",
        "version": "2.0.0",
        "status": "operational",
        "features": [
            "AI-powered document generation",
            "Legal compliance checking",
            "Comprehensive practice management",
            "LSUC compliance tracking",
            "Trust account management",
            "Time tracking and billing"
        ]
    }

@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    try:
        ai_health = await ai_engine.health_check() if hasattr(ai_engine, 'health_check') else {"status": "ready" if ai_engine.is_ready() else "not_ready"}
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "ai_engine": ai_health,
            "database": database.is_connected() if database else False,
            "security": security_manager.is_ready() if security_manager else False,
            "blockchain": blockchain_auth.is_ready() if blockchain_auth else False,
            "components": {
                "legal_knowledge": legal_knowledge.is_ready(),
                "enhanced_legal_knowledge": enhanced_legal_knowledge.is_ready(),
                "document_generator": doc_generator.is_ready(),
                "enhanced_document_generator": enhanced_doc_generator.is_ready(),
                "compliance_checker": compliance_checker.is_ready(),
                "enhanced_legal_ai": enhanced_legal_ai.is_initialized,
                "enhanced_ai_legal_service": enhanced_ai_legal_service.is_ready(),
                "case_law_analyzer": case_law_analyzer.is_ready(),
                "practice_manager": practice_manager.is_ready(),
                "lsuc_compliance": lsuc_compliance_manager.is_ready()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")

# Include API routes
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(compliance.router, prefix="/api/compliance", tags=["compliance"])
app.include_router(blockchain.router, prefix="/api/blockchain", tags=["blockchain"])  
app.include_router(enhanced_ai.router, prefix="/api/enhanced-ai", tags=["enhanced-ai"])

# Include new practice management routes
app.include_router(practice_router, prefix="/api/practice", tags=["practice-management"])
app.include_router(lsuc_router, prefix="/api/lsuc", tags=["lsuc-compliance"])

# New enhanced AI endpoints
@app.post("/api/analyze-document", response_model=DocumentAnalysisResponse)
async def analyze_document(
    request: DocumentAnalysisRequest,
    background_tasks: BackgroundTasks,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Analyze legal document using AI"""
    try:
        # Verify authentication (simplified for demo)
        user_id = "demo_user"  # In production: await security_manager.verify_token(credentials.credentials)
        
        # Log the analysis request
        background_tasks.add_task(
            database.log_analysis_request,
            user_id=user_id,
            document_type=request.document_type,
            text_length=len(request.text)
        )
        
        # Perform AI analysis
        start_time = datetime.now()
        analysis_result = await ai_engine.analyze_document(
            text=request.text,
            document_type=request.document_type,
            case_context=request.case_context
        )
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Store analysis results
        document_id = await database.store_analysis(
            user_id=user_id,
            analysis_result=analysis_result,
            processing_time=processing_time
        )
        
        return DocumentAnalysisResponse(
            document_id=document_id,
            document_type=analysis_result.get("document_type", request.document_type),
            confidence=analysis_result.get("confidence", 0.5),
            entities=analysis_result.get("entities", []),
            requirements=analysis_result.get("requirements", []),
            compliance_issues=analysis_result.get("compliance_issues", []),
            recommendations=analysis_result.get("recommendations", ["Consider legal review"]),
            sentiment=analysis_result.get("sentiment", {"label": "NEUTRAL", "score": 0.5}),
            processing_time=processing_time,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Document analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/generate-document", response_model=DocumentGenerationResponse)
async def generate_document(
    request: DocumentGenerationRequest,
    background_tasks: BackgroundTasks,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Generate legal document with AI assistance"""
    try:
        # Verify authentication (simplified for demo)
        user_id = "demo_user"  # In production: await security_manager.verify_token(credentials.credentials)
        
        # Validate user data
        validation_result = await enhanced_doc_generator.validate_document_data(
            document_type=request.document_type,
            user_data=request.user_data
        )
        
        if not validation_result["is_valid"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid data: {validation_result['errors']}"
            )
        
        # Generate AI recommendations if requested
        ai_recommendations = []
        if request.include_ai_recommendations:
            ai_recommendations = await ai_engine.generate_document_recommendations(
                document_type=request.document_type,
                user_data=request.user_data
            )
        
        # Generate documents
        documents = await enhanced_doc_generator.generate_legal_documents(
            document_type=request.document_type,
            user_data=request.user_data,
            ai_recommendations=ai_recommendations,
            template_id=request.template_id
        )
        
        # Store document records
        document_id = await database.store_document(
            user_id=user_id,
            document_type=request.document_type,
            documents=documents,
            ai_recommendations=ai_recommendations
        )
        
        # Blockchain authentication (optional)
        blockchain_hash = None
        if blockchain_auth:
            blockchain_hash = await blockchain_auth.store_document_hash(
                document_id=document_id,
                document_content=documents["text_content"]
            )
        
        # Generate authentication token (simplified)
        auth_token = f"token_{document_id}_{datetime.now().timestamp()}"
        
        # Schedule background tasks
        background_tasks.add_task(
            database.log_document_generation,
            user_id=user_id,
            document_type=request.document_type,
            document_id=document_id
        )
        
        return DocumentGenerationResponse(
            document_id=document_id,
            download_url=f"/api/documents/{document_id}/download",
            docx_url=f"/api/documents/{document_id}/download/docx",
            pdf_url=f"/api/documents/{document_id}/download/pdf",
            blockchain_hash=blockchain_hash,
            authentication_token=auth_token
        )
        
    except Exception as e:
        logger.error(f"Document generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/api/query-legal", response_model=LegalQueryResponse)
async def query_legal(
    request: LegalQueryRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Query legal knowledge base with AI"""
    try:
        # Verify authentication (simplified for demo)
        user_id = "demo_user"  # In production: await security_manager.verify_token(credentials.credentials)
        
        # Search case law
        relevant_cases = await case_law_analyzer.find_relevant_cases(
            query=request.query,
            document_context=request.document_context,
            document_type=request.document_type
        )
        
        # Get AI answer
        ai_answer = await ai_engine.answer_legal_question(
            question=request.query,
            context=request.document_context or "",
            document_type=request.document_type
        )
        
        # Generate recommendations
        recommendations = await ai_engine.generate_query_recommendations(
            query=request.query,
            relevant_cases=relevant_cases,
            ai_answer=ai_answer
        )
        
        return LegalQueryResponse(
            answer=ai_answer.get("answer", "Analysis complete. Please consult with a qualified lawyer."),
            confidence=ai_answer.get("confidence", 0.5),
            relevant_cases=relevant_cases[:5],  # Top 5 cases
            legal_sources=[case.get("citation", "Unknown") for case in relevant_cases[:5]],
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Legal query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@app.get("/api/documents/{document_id}/download/{format}")
async def download_document(
    document_id: str,
    format: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Download generated document"""
    try:
        # Verify authentication (simplified for demo)
        user_id = "demo_user"  # In production: await security_manager.verify_token(credentials.credentials)
        
        # Verify document access
        if not await database.verify_document_access(user_id, document_id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get document
        document = await database.get_document(document_id, format)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Return file response
        return {
            "filename": document["filename"],
            "content_type": document["content_type"],
            "content": document["content"]
        }
        
    except Exception as e:
        logger.error(f"Document download failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@app.post("/api/research")
async def real_time_research(
    query: str,
    jurisdiction: str = "ontario",
    max_results: int = 10,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Perform real-time legal research"""
    try:
        # Verify authentication (simplified for demo)
        user_id = "demo_user"  # In production: await security_manager.verify_token(credentials.credentials)
        
        # Perform research using case law analyzer
        research_results = await case_law_analyzer.perform_research(
            query=query,
            jurisdiction=jurisdiction,
            max_results=max_results
        )
        
        return {
            "query": query,
            "jurisdiction": jurisdiction,
            "results": research_results,
            "timestamp": datetime.now().isoformat(),
            "total_results": len(research_results)
        }
        
    except Exception as e:
        logger.error(f"Legal research failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Research failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )