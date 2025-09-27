from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from models.schemas import (
    DocumentRequest, DocumentResponse,
    ComplianceCheckRequest, ComplianceCheckResponse
)
# Remove problematic imports - services will be injected from main.py
# from backend.services.enhanced_document_manager import EnhancedDocumentManager
# from backend.services.enhanced_ai_legal_service import EnhancedAILegalService

logger = logging.getLogger(__name__)

router = APIRouter()

# Services will be injected from main.py
# document_manager = EnhancedDocumentManager()
# ai_legal_service = EnhancedAILegalService()
document_manager = None
ai_legal_service = None

@router.post("/generate", response_model=DocumentResponse)
async def generate_document(request: DocumentRequest):
    """Generate legal document using enhanced document manager"""
    try:
        logger.info(f"Generating {request.document_type} document")
        
        # Ensure document manager is initialized
        if not document_manager.is_ready():
            await document_manager.initialize()
        
        # Generate document content using enhanced manager
        content = await document_manager.generate_document(
            document_type=request.document_type,
            fields=request.content if isinstance(request.content, dict) else {"content": request.content}
        )
        
        # Apply Ontario formatting
        formatted_content = await document_manager._apply_ontario_formatting(
            content, request.document_type
        )
        
        # Generate document ID
        document_id = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Save document
        document_data = {
            "document_type": request.document_type,
            "client_id": request.content.get("client_id") if isinstance(request.content, dict) else None,
            "created_by": "api_user"
        }
        
        file_path = await document_manager._save_document(document_id, formatted_content, document_data)
        file_hash = await document_manager._calculate_file_hash(file_path)
        
        # Store metadata
        await document_manager._store_document_metadata(document_id, document_data, file_path, file_hash)
        
        return DocumentResponse(
            success=True,
            document_id=document_id,
            content=formatted_content,
            message="Document generated successfully with Ontario compliance"
        )
        
    except Exception as e:
        logger.error(f"Document generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@router.get("/templates/{document_type}")
async def get_document_template(document_type: str):
    """Get document template using enhanced document manager"""
    try:
        # Ensure document manager is initialized
        if not document_manager.is_ready():
            await document_manager.initialize()
        
        # Get template from enhanced document manager
        template = await document_manager._get_document_template(document_type)
        
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        return {
            "success": True,
            "document_type": document_type,
            "template": template,
            "ontario_compliant": template.get("ontario_compliant", True)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Template retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Template retrieval failed: {str(e)}")

@router.get("/requirements/{document_type}")
async def get_document_requirements(document_type: str):
    """Get legal requirements for document type"""
    try:
        # Placeholder requirements
        requirements = {
            "will": {
                "age_requirement": "18 years or older",
                "capacity_requirement": "Mental capacity to make a will",
                "witnesses": "Two witnesses required",
                "execution": "Signed in presence of witnesses",
                "statutory_compliance": "Ontario Succession Law Reform Act"
            },
            "poa_property": {
                "age_requirement": "18 years or older",
                "capacity_requirement": "Mental capacity for property decisions",
                "witnesses": "Witness or notarization required",
                "attorney_eligibility": "Attorney must be capable and willing",
                "statutory_compliance": "Ontario Substitute Decisions Act"
            }
        }
        
        requirement = requirements.get(document_type)
        if not requirement:
            raise HTTPException(status_code=404, detail="Requirements not found")
        
        return {
            "success": True,
            "document_type": document_type,
            "requirements": requirement
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Requirements retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Requirements retrieval failed: {str(e)}")

@router.post("/validate")
async def validate_document(request: Dict[str, Any]):
    """Validate document content using AI-enhanced analysis"""
    try:
        document_type = request.get("document_type")
        content = request.get("content", {})
        
        if not document_type:
            raise HTTPException(status_code=400, detail="Document type is required")
        
        # Use AI service for comprehensive document analysis
        analysis = await ai_legal_service.analyze_document(document_type, content)
        
        # Convert analysis to validation format
        validation_results = {
            "is_valid": analysis.compliance_score >= 0.7,
            "compliance_score": analysis.compliance_score,
            "legal_issues": analysis.legal_issues,
            "recommendations": analysis.recommendations,
            "risk_assessment": analysis.risk_assessment,
            "suggested_improvements": analysis.suggested_improvements
        }
        
        return {
            "success": True,
            "validation": validation_results,
            "ai_analysis": True
        }
        
    except Exception as e:
        logger.error(f"Document validation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

@router.get("/{document_id}/download")
async def download_document(document_id: str):
    """Download generated document"""
    try:
        # In production, this would retrieve the document from storage
        # and return it as a file download
        
        return {
            "success": True,
            "message": "Document download endpoint - implementation pending",
            "document_id": document_id
        }
        
    except Exception as e:
        logger.error(f"Document download failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload document for analysis"""
    try:
        # Read file content
        content = await file.read()
        
        # In production, this would:
        # 1. Validate file type
        # 2. Extract text content
        # 3. Store in database
        # 4. Return file ID for further processing
        
        return {
            "success": True,
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
            "message": "File uploaded successfully"
        }
        
    except Exception as e:
        logger.error(f"File upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# Enhanced Document Management Endpoints

@router.post("/search")
async def search_documents(search_criteria: Dict[str, Any]):
    """Search documents with advanced filtering"""
    try:
        if not document_manager.is_ready():
            await document_manager.initialize()
        
        documents = await document_manager.search_documents(search_criteria)
        
        return {
            "success": True,
            "documents": documents,
            "total_found": len(documents)
        }
        
    except Exception as e:
        logger.error(f"Document search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.get("/statistics")
async def get_document_statistics():
    """Get document management statistics"""
    try:
        if not document_manager.is_ready():
            await document_manager.initialize()
        
        stats = await document_manager.get_document_statistics()
        
        return {
            "success": True,
            "statistics": stats
        }
        
    except Exception as e:
        logger.error(f"Statistics retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Statistics failed: {str(e)}")

@router.get("/{document_id}/versions")
async def get_document_versions(document_id: str):
    """Get all versions of a document"""
    try:
        if not document_manager.is_ready():
            await document_manager.initialize()
        
        versions = await document_manager.get_document_versions(document_id)
        
        return {
            "success": True,
            "document_id": document_id,
            "versions": [
                {
                    "id": v.id,
                    "version_number": v.version_number,
                    "created_at": v.created_at.isoformat(),
                    "created_by": v.created_by,
                    "changes_summary": v.changes_summary
                }
                for v in versions
            ]
        }
        
    except Exception as e:
        logger.error(f"Version retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Version retrieval failed: {str(e)}")

@router.post("/court-forms/{form_number}")
async def create_court_form(form_number: str, data: Dict[str, Any]):
    """Create Ontario court form"""
    try:
        if not document_manager.is_ready():
            await document_manager.initialize()
        
        document_id = await document_manager.create_ontario_court_form(form_number, data)
        
        return {
            "success": True,
            "document_id": document_id,
            "form_number": form_number,
            "message": f"Court form {form_number} created successfully"
        }
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Court form creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Court form creation failed: {str(e)}")

# AI-Enhanced Legal Services Endpoints

@router.post("/legal-research")
async def conduct_legal_research(research_request: Dict[str, Any]):
    """Conduct AI-powered legal research"""
    try:
        query = research_request.get("query")
        document_type = research_request.get("document_type")
        
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        research_result = await ai_legal_service.conduct_legal_research(query, document_type)
        
        return {
            "success": True,
            "research_result": {
                "query": research_result.query,
                "relevant_cases": research_result.relevant_cases,
                "statutes": research_result.statutes,
                "analysis": research_result.analysis,
                "confidence": research_result.confidence,
                "recommendations": research_result.recommendations
            }
        }
        
    except Exception as e:
        logger.error(f"Legal research failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Legal research failed: {str(e)}")

@router.post("/case-prediction")
async def predict_case_outcome(prediction_request: Dict[str, Any]):
    """Predict case outcome based on Ontario precedents"""
    try:
        case_facts = prediction_request.get("case_facts", {})
        case_type = prediction_request.get("case_type", prediction_request.get("legal_issue"))
        
        if not case_facts:
            raise HTTPException(status_code=400, detail="Case facts are required")
        
        # Use the enhanced prediction method
        prediction = await ai_legal_service.predict_case_outcome(case_facts, case_type)
        
        return {
            "success": True,
            "prediction": prediction
        }
        
    except Exception as e:
        logger.error(f"Case prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Case prediction failed: {str(e)}")

@router.post("/ai-analysis")
async def perform_ai_analysis(analysis_request: Dict[str, Any]):
    """Perform comprehensive AI document analysis"""
    try:
        document_type = analysis_request.get("document_type")
        document_content = analysis_request.get("document_content", {})
        
        if not document_type:
            raise HTTPException(status_code=400, detail="Document type is required")
        
        analysis = await ai_legal_service.analyze_document(document_type, document_content)
        
        return {
            "success": True,
            "analysis": {
                "document_type": analysis.document_type,
                "compliance_score": analysis.compliance_score,
                "legal_issues": analysis.legal_issues,
                "recommendations": analysis.recommendations,
                "risk_assessment": analysis.risk_assessment,
                "suggested_improvements": analysis.suggested_improvements
            }
        }
        
    except Exception as e:
        logger.error(f"AI analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")

from datetime import datetime