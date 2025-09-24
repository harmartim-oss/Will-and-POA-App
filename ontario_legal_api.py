"""
Enhanced FastAPI Service for Ontario Legal Document AI System
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import asdict

# FastAPI imports (would be available after pip install)
try:
    from fastapi import FastAPI, HTTPException, UploadFile, File
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import FileResponse, JSONResponse
    from pydantic import BaseModel, Field
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    # Fallback classes for development
    class BaseModel:
        pass
    class Field:
        def __init__(self, *args, **kwargs):
            pass

from backend.core.ai_enhanced_document_generator import AIEnhancedDocumentGenerator
from backend.core.enhanced_ai_legal_service import EnhancedAILegalService
from backend.core.legal_knowledge import OntarioLegalKnowledgeBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for API
class PersonalInfo(BaseModel):
    full_name: str = Field(..., description="Full legal name")
    address: str = Field(..., description="Complete address")
    age: Optional[int] = Field(None, description="Age of person")
    marital_status: Optional[str] = Field(None, description="Marital status")
    has_children: Optional[bool] = Field(False, description="Has minor children")

class ExecutorInfo(BaseModel):
    name: str = Field(..., description="Executor full name")
    address: str = Field(..., description="Executor address")
    relationship: Optional[str] = Field(None, description="Relationship to testator")
    phone: Optional[str] = Field(None, description="Contact phone")

class BequestInfo(BaseModel):
    item: str = Field(..., description="Item being bequeathed")
    beneficiary: str = Field(..., description="Beneficiary name")
    value: Optional[str] = Field(None, description="Estimated value")

class WillCreateRequest(BaseModel):
    personal_info: PersonalInfo
    executor: ExecutorInfo
    alternate_executor: Optional[ExecutorInfo] = None
    guardian: Optional[ExecutorInfo] = None
    bequests: Optional[List[BequestInfo]] = []
    residuary: Dict[str, Any] = Field(default_factory=dict)
    enable_ai_enhancements: bool = Field(True, description="Enable AI enhancements")

class POACreateRequest(BaseModel):
    poa_type: str = Field(..., description="POA type: poa_property or poa_care")
    grantor_info: PersonalInfo
    attorney: ExecutorInfo
    alternate_attorney: Optional[ExecutorInfo] = None
    powers: Optional[List[str]] = []
    care_instructions: Optional[Dict[str, Any]] = Field(default_factory=dict)
    conditions: Optional[List[str]] = []
    enable_ai_enhancements: bool = Field(True, description="Enable AI enhancements")

class DocumentAnalysisRequest(BaseModel):
    document_type: str = Field(..., description="Document type")
    content: Dict[str, Any] = Field(..., description="Document content")

class AIEnhancementRequest(BaseModel):
    document_type: str = Field(..., description="Document type")
    section: str = Field(..., description="Document section")
    text: str = Field(..., description="Text to enhance")

# Initialize services
document_generator = AIEnhancedDocumentGenerator()
ai_service = EnhancedAILegalService()
legal_kb = OntarioLegalKnowledgeBase()

if FASTAPI_AVAILABLE:
    # Create FastAPI app
    app = FastAPI(
        title="Ontario Legal Document AI System",
        description="AI-powered Ontario legal document generation with compliance checking",
        version="1.0.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        """API health check"""
        return {
            "message": "Ontario Legal Document AI System",
            "version": "1.0.0",
            "status": "operational",
            "features": [
                "AI-powered document analysis",
                "Ontario legal compliance checking",
                "Professional document generation",
                "Case law integration",
                "Real-time legal guidance"
            ]
        }

    @app.post("/api/documents/will/create")
    async def create_will(request: WillCreateRequest):
        """Create Ontario-compliant will with AI enhancements"""
        try:
            logger.info("Creating will document with AI enhancements")
            
            # Convert request to dict
            form_data = {
                "personal_info": request.personal_info.dict(),
                "executor": request.executor.dict(),
                "alternate_executor": request.alternate_executor.dict() if request.alternate_executor else None,
                "guardian": request.guardian.dict() if request.guardian else None,
                "bequests": [b.dict() for b in request.bequests] if request.bequests else [],
                "residuary": request.residuary
            }
            
            # Generate document
            result = document_generator.generate_ontario_will(
                form_data, 
                enable_ai_enhancements=request.enable_ai_enhancements
            )
            
            return JSONResponse(content={
                "success": True,
                "document_id": os.path.basename(result["document_path"]),
                "document_path": result["document_path"],
                "format": result["format"],
                "ai_analysis": result.get("ai_analysis"),
                "compliance_score": result.get("compliance_score"),
                "generation_time": result["generation_time"]
            })
            
        except Exception as e:
            logger.error(f"Error creating will: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error creating will: {str(e)}")

    @app.post("/api/documents/poa/create")
    async def create_poa(request: POACreateRequest):
        """Create Ontario-compliant Power of Attorney with AI enhancements"""
        try:
            logger.info(f"Creating {request.poa_type} document with AI enhancements")
            
            # Convert request to dict
            form_data = {
                "grantor_info": request.grantor_info.dict(),
                "attorney": request.attorney.dict(),
                "alternate_attorney": request.alternate_attorney.dict() if request.alternate_attorney else None,
                "powers": request.powers,
                "care_instructions": request.care_instructions,
                "conditions": request.conditions
            }
            
            # Generate document
            result = document_generator.generate_ontario_poa(
                request.poa_type,
                form_data,
                enable_ai_enhancements=request.enable_ai_enhancements
            )
            
            return JSONResponse(content={
                "success": True,
                "document_id": os.path.basename(result["document_path"]),
                "document_path": result["document_path"],
                "format": result["format"],
                "ai_analysis": result.get("ai_analysis"),
                "compliance_score": result.get("compliance_score"),
                "generation_time": result["generation_time"]
            })
            
        except Exception as e:
            logger.error(f"Error creating POA: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error creating POA: {str(e)}")

    @app.post("/api/ai/analyze")
    async def analyze_document(request: DocumentAnalysisRequest):
        """Analyze document for legal compliance and improvements"""
        try:
            logger.info(f"Analyzing {request.document_type} document")
            
            # Perform AI analysis
            analysis = ai_service.analyze_document(request.document_type, request.content)
            
            return JSONResponse(content={
                "success": True,
                "analysis": asdict(analysis),
                "insights": ai_service.generate_document_insights(request.document_type, request.content)
            })
            
        except Exception as e:
            logger.error(f"Error analyzing document: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error analyzing document: {str(e)}")

    @app.post("/api/ai/enhance")
    async def enhance_text(request: AIEnhancementRequest):
        """Enhance specific document section with AI"""
        try:
            logger.info(f"Enhancing {request.section} section for {request.document_type}")
            
            enhancement = ai_service.enhance_document_section(
                request.document_type,
                request.section,
                request.text
            )
            
            return JSONResponse(content={
                "success": True,
                "enhancement": asdict(enhancement)
            })
            
        except Exception as e:
            logger.error(f"Error enhancing text: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error enhancing text: {str(e)}")

    @app.get("/api/legal/requirements/{document_type}")
    async def get_legal_requirements(document_type: str):
        """Get legal requirements for document type"""
        try:
            requirements = legal_kb.get_requirements_for_document_type(document_type)
            
            return JSONResponse(content={
                "success": True,
                "document_type": document_type,
                "requirements": [asdict(req) for req in requirements]
            })
            
        except Exception as e:
            logger.error(f"Error getting requirements: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error getting requirements: {str(e)}")

    @app.get("/api/legal/caselaw/{document_type}")
    async def get_case_law(document_type: str, issue: Optional[str] = None):
        """Get relevant case law for document type and legal issue"""
        try:
            if issue:
                cases = legal_kb.get_relevant_case_law(issue, document_type)
            else:
                cases = legal_kb.case_law_database
            
            return JSONResponse(content={
                "success": True,
                "document_type": document_type,
                "issue": issue,
                "cases": [asdict(case) for case in cases[:10]]  # Limit to top 10
            })
            
        except Exception as e:
            logger.error(f"Error getting case law: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error getting case law: {str(e)}")

    @app.post("/api/documents/{document_id}/pdf")
    async def convert_to_pdf(document_id: str):
        """Convert document to PDF format"""
        try:
            # Find document file
            document_path = f"/tmp/{document_id}"  # Simplified path logic
            
            if not os.path.exists(document_path):
                raise HTTPException(status_code=404, detail="Document not found")
            
            # Convert to PDF
            pdf_path = document_generator.generate_pdf_version(document_path)
            
            return JSONResponse(content={
                "success": True,
                "pdf_path": pdf_path,
                "document_id": document_id
            })
            
        except Exception as e:
            logger.error(f"Error converting to PDF: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error converting to PDF: {str(e)}")

    @app.get("/api/documents/{document_id}/download")
    async def download_document(document_id: str):
        """Download generated document"""
        try:
            # Find document file (simplified logic)
            for ext in ['.docx', '.txt', '.pdf']:
                document_path = f"/tmp/{document_id}{ext}"
                if os.path.exists(document_path):
                    return FileResponse(
                        path=document_path,
                        filename=f"{document_id}{ext}",
                        media_type='application/octet-stream'
                    )
            
            raise HTTPException(status_code=404, detail="Document not found")
            
        except Exception as e:
            logger.error(f"Error downloading document: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error downloading document: {str(e)}")

    @app.get("/api/templates/{template_name}")
    async def get_template(template_name: str):
        """Get legal document template"""
        try:
            template = legal_kb.legal_templates.get(template_name)
            
            if not template:
                raise HTTPException(status_code=404, detail="Template not found")
            
            return JSONResponse(content={
                "success": True,
                "template_name": template_name,
                "template": template
            })
            
        except Exception as e:
            logger.error(f"Error getting template: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error getting template: {str(e)}")

    @app.post("/api/validate")
    async def validate_document(request: DocumentAnalysisRequest):
        """Validate document against Ontario legal requirements"""
        try:
            validation_result = legal_kb.validate_compliance(
                request.document_type,
                request.content
            )
            
            return JSONResponse(content={
                "success": True,
                "validation": validation_result
            })
            
        except Exception as e:
            logger.error(f"Error validating document: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error validating document: {str(e)}")

    @app.get("/api/insights/{document_type}")
    async def get_document_insights(document_type: str, content: Dict[str, Any]):
        """Get comprehensive document insights and recommendations"""
        try:
            insights = document_generator.get_document_insights(document_type, content)
            
            return JSONResponse(content={
                "success": True,
                "insights": insights
            })
            
        except Exception as e:
            logger.error(f"Error getting insights: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error getting insights: {str(e)}")

    @app.post("/api/ai/enhanced-analysis")
    async def enhanced_ai_analysis(request: DocumentAnalysisRequest):
        """Enhanced AI document analysis with advanced features"""
        try:
            logger.info(f"Performing enhanced AI analysis for {request.document_type}")
            
            # Use the enhanced AI service
            analysis = ai_service.analyze_document(request.document_type, request.content)
            insights = ai_service.generate_document_insights(request.document_type, request.content)
            
            return JSONResponse(content={
                "success": True,
                "analysis": asdict(analysis),
                "insights": insights,
                "capabilities": {
                    "compliance_checking": True,
                    "risk_assessment": True,
                    "case_law_analysis": True,
                    "ai_recommendations": True
                }
            })
            
        except Exception as e:
            logger.error(f"Enhanced AI analysis failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Enhanced AI analysis failed: {str(e)}")

    @app.post("/api/documents/generate-enhanced")
    async def generate_enhanced_document(request: Dict[str, Any]):
        """Generate document using enhanced AI document generator"""
        try:
            document_type = request.get("document_type", "will")
            user_data = request.get("user_data", {})
            ai_enhancements = request.get("ai_enhancements", True)
            
            logger.info(f"Generating enhanced {document_type} document")
            
            if document_type == "will":
                result = await document_generator.generate_ontario_will(user_data, ai_enhancements)
            elif document_type in ["poa_property", "poa_personal_care"]:
                result = await document_generator.generate_ontario_poa(user_data, document_type, ai_enhancements)
            else:
                raise HTTPException(status_code=400, detail="Unsupported document type")
            
            return JSONResponse(content=result)
            
        except Exception as e:
            logger.error(f"Enhanced document generation failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Enhanced document generation failed: {str(e)}")

    @app.get("/api/ai/capabilities")
    async def get_ai_capabilities():
        """Get AI system capabilities and status"""
        try:
            health_check = await ai_service.health_check()
            generator_status = await document_generator.health_check()
            
            return JSONResponse(content={
                "success": True,
                "ai_service": health_check,
                "document_generator": generator_status,
                "features": {
                    "advanced_nlp": True,
                    "case_law_analysis": True,
                    "compliance_checking": True,
                    "risk_assessment": True,
                    "document_optimization": True,
                    "semantic_analysis": True,
                    "real_time_guidance": True
                }
            })
            
        except Exception as e:
            logger.error(f"Error getting AI capabilities: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error getting AI capabilities: {str(e)}")

    @app.post("/api/documents/preview")
    async def generate_document_preview(request: Dict[str, Any]):
        """Generate document preview without full processing"""
        try:
            document_type = request.get("document_type", "will")
            user_data = request.get("user_data", {})
            
            preview = document_generator.get_document_preview(document_type, user_data)
            
            return JSONResponse(content={
                "success": True,
                "preview": preview
            })
            
        except Exception as e:
            logger.error(f"Preview generation failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Preview generation failed: {str(e)}")

    @app.post("/api/documents/validate-data")
    async def validate_document_data(request: Dict[str, Any]):
        """Validate document data completeness and correctness"""
        try:
            document_type = request.get("document_type", "will")
            user_data = request.get("user_data", {})
            
            validation = document_generator.validate_document_data(document_type, user_data)
            
            return JSONResponse(content={
                "success": True,
                "validation": validation
            })
            
        except Exception as e:
            logger.error(f"Data validation failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Data validation failed: {str(e)}")

    @app.get("/api/templates/fields/{document_type}")
    async def get_template_fields(document_type: str):
        """Get required and optional fields for document type"""
        try:
            fields = document_generator.get_template_fields(document_type)
            
            return JSONResponse(content={
                "success": True,
                "document_type": document_type,
                "fields": fields
            })
            
        except Exception as e:
            logger.error(f"Error getting template fields: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error getting template fields: {str(e)}")

    @app.get("/api/system/health")
    async def system_health_check():
        """Comprehensive system health check"""
        try:
            health_status = {
                "timestamp": datetime.now().isoformat(),
                "status": "healthy",
                "components": {
                    "ai_service": await ai_service.health_check() if ai_service.is_ready() else {"status": "not_ready"},
                    "document_generator": await document_generator.health_check() if document_generator.is_ready() else {"status": "not_ready"},
                    "legal_kb": {
                        "status": "ready" if legal_kb.is_ready() else "not_ready",
                        "stats": legal_kb.get_knowledge_base_stats()
                    }
                },
                "features": {
                    "fastapi_available": FASTAPI_AVAILABLE,
                    "ai_enhancements": ai_service.is_ready(),
                    "document_generation": document_generator.is_ready(),
                    "legal_knowledge": legal_kb.is_ready()
                }
            }
            
            # Determine overall health
            component_health = [
                comp.get("status") == "ready" or comp.get("service_status") == "ready" 
                for comp in health_status["components"].values()
            ]
            
            if not all(component_health):
                health_status["status"] = "degraded"
            
            return JSONResponse(content=health_status)
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return JSONResponse(
                content={
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                },
                status_code=500
            )

else:
    # Fallback Flask implementation for when FastAPI is not available
    from flask import Flask, request, jsonify, send_file
    from flask_cors import CORS
    
    app = Flask(__name__)
    CORS(app)
    
    @app.route('/')
    def root():
        return jsonify({
            "message": "Ontario Legal Document AI System (Flask Fallback)",
            "version": "1.0.0",
            "status": "operational"
        })
    
    @app.route('/api/documents/will/create', methods=['POST'])
    def create_will_flask():
        try:
            data = request.get_json()
            result = document_generator.generate_ontario_will(
                data,
                enable_ai_enhancements=data.get('enable_ai_enhancements', True)
            )
            return jsonify({
                "success": True,
                "document_path": result["document_path"],
                "format": result["format"]
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/ai/analyze', methods=['POST'])
    def analyze_document_flask():
        try:
            data = request.get_json()
            analysis = ai_service.analyze_document(
                data['document_type'],
                data['content']
            )
            return jsonify({
                "success": True,
                "analysis": asdict(analysis)
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Utility functions for both FastAPI and Flask
def create_app():
    """Factory function to create the appropriate app"""
    return app

def run_server(host: str = "0.0.0.0", port: int = 8000, debug: bool = True):
    """Run the API server"""
    if FASTAPI_AVAILABLE:
        import uvicorn
        uvicorn.run(app, host=host, port=port, log_level="info")
    else:
        app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    run_server()