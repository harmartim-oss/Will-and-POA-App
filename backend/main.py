from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
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
from api.routes import documents, ai, compliance, blockchain
from database.connection import init_db
from models.schemas import (
    DocumentRequest, DocumentResponse, 
    AIAnalysisRequest, AIAnalysisResponse,
    ComplianceCheckRequest, ComplianceCheckResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Ontario Legal Document AI System",
    description="AI-powered legal document generation and analysis for Ontario jurisdiction",
    version="1.0.0",
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

# Initialize AI components
ai_engine = OntarioLegalAIEngine()
doc_generator = OntarioDocumentGenerator()
legal_knowledge = OntarioLegalKnowledgeBase()
compliance_checker = OntarioComplianceChecker()
risk_assessor = OntarioRiskAssessor()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting Ontario Legal Document AI System...")
    
    # Initialize database
    await init_db()
    
    # Load AI models
    await ai_engine.initialize()
    await legal_knowledge.initialize()
    
    logger.info("System initialized successfully")

@app.get("/")
async def root():
    return {
        "message": "Ontario Legal Document AI System",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "ai_engine": ai_engine.is_ready(),
        "components": {
            "legal_knowledge": legal_knowledge.is_ready(),
            "document_generator": doc_generator.is_ready(),
            "compliance_checker": compliance_checker.is_ready()
        }
    }

# Include API routes
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(compliance.router, prefix="/api/compliance", tags=["compliance"])
app.include_router(blockchain.router, prefix="/api/blockchain", tags=["blockchain"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )