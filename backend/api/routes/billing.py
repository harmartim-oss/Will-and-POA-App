# backend/api/routes/billing.py
"""
Billing and Invoice Document Generation Routes
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.responses import Response
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import sys
import os
import base64

# Add backend to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from core.practice_management import OntarioPracticeManager
from core.billing_documents import OntarioBillingDocumentGenerator, AIEnhancedCoverLetterGenerator
from core.document_combiner import DocumentCombiner, BatchDocumentGenerator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/billing", tags=["billing-documents"])

# Global instances
practice_manager = None
billing_generator = None
cover_letter_generator = None

def get_practice_manager() -> OntarioPracticeManager:
    """Dependency to get practice manager instance"""
    global practice_manager
    if not practice_manager:
        practice_manager = OntarioPracticeManager()
    if not practice_manager.is_ready():
        raise HTTPException(status_code=503, detail="Practice management system not initialized")
    return practice_manager

def get_billing_generator() -> OntarioBillingDocumentGenerator:
    """Get billing document generator"""
    global billing_generator
    if not billing_generator:
        billing_generator = OntarioBillingDocumentGenerator()
    return billing_generator

def get_cover_letter_generator() -> AIEnhancedCoverLetterGenerator:
    """Get cover letter generator"""
    global cover_letter_generator
    if not cover_letter_generator:
        cover_letter_generator = AIEnhancedCoverLetterGenerator()
    return cover_letter_generator


# Pydantic models
class GenerateInvoiceRequest(BaseModel):
    matter_id: str = Field(..., description="Matter ID")
    bill_date: Optional[str] = Field(None, description="Bill date (YYYY-MM-DD)")
    template_id: Optional[str] = Field(None, description="Invoice template ID")
    format: Optional[str] = Field("pdf", description="Output format (pdf or docx)")

class GenerateBillOfCostsRequest(BaseModel):
    matter_id: str = Field(..., description="Matter ID")
    court_file_number: Optional[str] = Field(None, description="Court file number")
    plaintiff: Optional[str] = Field(None, description="Plaintiff/Applicant name")
    defendant: Optional[str] = Field(None, description="Defendant/Respondent name")

class GenerateCoverLetterRequest(BaseModel):
    client_id: str = Field(..., description="Client ID")
    matter_id: str = Field(..., description="Matter ID")
    documents_included: List[str] = Field(..., description="List of documents included")
    invoice_number: Optional[str] = Field(None, description="Invoice number if applicable")
    additional_notes: Optional[str] = Field(None, description="Additional notes")
    format: Optional[str] = Field("pdf", description="Output format (pdf or docx)")

class BatchDownloadRequest(BaseModel):
    matter_id: str = Field(..., description="Matter ID")
    document_types: List[str] = Field(..., description="Document types to include (invoice, timesheet, bill_of_costs, cover_letter)")
    combine: Optional[bool] = Field(False, description="Combine into single document or ZIP")
    format: Optional[str] = Field("pdf", description="Document format (pdf or docx)")

class UploadLogoRequest(BaseModel):
    logo_data: str = Field(..., description="Base64 encoded logo image")


# API Endpoints

@router.post("/generate-invoice", response_model=Dict[str, Any])
async def generate_invoice(
    request: GenerateInvoiceRequest,
    practice_mgr: OntarioPracticeManager = Depends(get_practice_manager),
    billing_gen: OntarioBillingDocumentGenerator = Depends(get_billing_generator)
):
    """Generate professional invoice with time entries and disbursements"""
    try:
        logger.info(f"Generating invoice for matter: {request.matter_id}")
        
        # Get bill data with time entries and disbursements
        bill_date = request.bill_date or datetime.now().date().isoformat()
        bill_result = await practice_mgr.generate_monthly_bill(request.matter_id, bill_date)
        
        if bill_result.get("status") == "error":
            raise HTTPException(status_code=404, detail=bill_result.get("message"))
        
        if bill_result.get("status") == "no_entries":
            raise HTTPException(status_code=404, detail="No billable entries or disbursements found")
        
        # Get matter and client details
        async with practice_mgr.db_path as db_path:
            import aiosqlite
            async with aiosqlite.connect(db_path) as db:
                # Get matter details
                cursor = await db.execute('''
                    SELECT m.matter_name, m.client_id, c.full_name, c.client_name, c.address
                    FROM matters m
                    JOIN clients c ON m.client_id = c.client_id
                    WHERE m.matter_id = ?
                ''', (request.matter_id,))
                matter_row = await cursor.fetchone()
                
                if not matter_row:
                    raise HTTPException(status_code=404, detail="Matter not found")
                
                matter_name, client_id, client_full_name, client_name, client_address = matter_row
                
                # Get time entries
                cursor = await db.execute('''
                    SELECT date, description, duration_minutes, hourly_rate, total_amount
                    FROM time_entries
                    WHERE matter_id = ? AND billed = TRUE
                    ORDER BY date
                ''', (request.matter_id,))
                time_rows = await cursor.fetchall()
                
                time_entries = []
                for row in time_rows:
                    time_entries.append({
                        "date": row[0],
                        "description": row[1],
                        "duration_minutes": row[2],
                        "hourly_rate": row[3],
                        "total_amount": row[4]
                    })
                
                # Get disbursements
                cursor = await db.execute('''
                    SELECT date, description, payee, amount, hst_amount, total_amount
                    FROM disbursements
                    WHERE matter_id = ? AND billed = TRUE
                    ORDER BY date
                ''', (request.matter_id,))
                disb_rows = await cursor.fetchall()
                
                disbursements = []
                for row in disb_rows:
                    disbursements.append({
                        "date": row[0],
                        "description": row[1],
                        "payee": row[2],
                        "amount": row[3],
                        "hst_amount": row[4],
                        "total_amount": row[5]
                    })
        
        # Get template config
        template_config = {}
        if request.template_id:
            template_config = await practice_mgr.get_invoice_template(request.template_id)
        else:
            # Use default settings
            template_config = {
                "include_logo": True,
                "include_timesheet": True,
                "include_disbursements": True
            }
        
        # Get firm logo and settings
        logo_data = await practice_mgr.get_firm_setting("firm_logo")
        if logo_data:
            billing_gen.set_firm_logo(logo_data)
        
        firm_info = {
            "firm_name": await practice_mgr.get_firm_setting("firm_name") or "Law Firm",
            "address": await practice_mgr.get_firm_setting("firm_address") or "",
            "phone": await practice_mgr.get_firm_setting("firm_phone") or "",
            "email": await practice_mgr.get_firm_setting("firm_email") or ""
        }
        billing_gen.set_firm_info(firm_info)
        
        # Prepare invoice data
        invoice_data = {
            "invoice_number": bill_result["bill_number"],
            "invoice_date": bill_date,
            "matter_name": matter_name,
            "client_name": client_name or client_full_name,
            "time_subtotal": bill_result["time_subtotal"],
            "disbursement_subtotal": bill_result["disbursement_subtotal"],
            "subtotal": bill_result["subtotal"],
            "taxes": bill_result["taxes"],
            "total": bill_result["total"],
            "payment_terms": "Payment due within 30 days"
        }
        
        # Generate invoice document
        invoice_bytes = await billing_gen.generate_invoice(
            invoice_data,
            time_entries,
            disbursements,
            template_config,
            format=request.format
        )
        
        # Return as file response
        media_type = "application/pdf" if request.format == "pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        filename = f"invoice_{bill_result['bill_number']}.{request.format}"
        
        return Response(
            content=invoice_bytes,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Invoice generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Invoice generation failed: {str(e)}")


@router.post("/generate-bill-of-costs", response_model=Dict[str, Any])
async def generate_bill_of_costs(
    request: GenerateBillOfCostsRequest,
    practice_mgr: OntarioPracticeManager = Depends(get_practice_manager),
    billing_gen: OntarioBillingDocumentGenerator = Depends(get_billing_generator)
):
    """Generate Bill of Costs compliant with Ontario Rules of Civil Procedure"""
    try:
        logger.info(f"Generating Bill of Costs for matter: {request.matter_id}")
        
        # Get matter details
        async with practice_mgr.db_path as db_path:
            import aiosqlite
            async with aiosqlite.connect(db_path) as db:
                cursor = await db.execute('''
                    SELECT m.matter_name, m.court_file_number, c.client_name, c.full_name
                    FROM matters m
                    JOIN clients c ON m.client_id = c.client_id
                    WHERE m.matter_id = ?
                ''', (request.matter_id,))
                matter_row = await cursor.fetchone()
                
                if not matter_row:
                    raise HTTPException(status_code=404, detail="Matter not found")
                
                matter_name, db_court_file, client_name, client_full_name = matter_row
                
                # Get billed time entries
                cursor = await db.execute('''
                    SELECT date, description, duration_minutes, hourly_rate, total_amount
                    FROM time_entries
                    WHERE matter_id = ? AND billed = TRUE
                    ORDER BY date
                ''', (request.matter_id,))
                time_rows = await cursor.fetchall()
                
                time_entries = []
                for row in time_rows:
                    time_entries.append({
                        "date": row[0],
                        "description": row[1],
                        "duration_minutes": row[2],
                        "hourly_rate": row[3],
                        "total_amount": row[4]
                    })
                
                # Get billed disbursements
                cursor = await db.execute('''
                    SELECT date, description, payee, total_amount
                    FROM disbursements
                    WHERE matter_id = ? AND billed = TRUE
                    ORDER BY date
                ''', (request.matter_id,))
                disb_rows = await cursor.fetchall()
                
                disbursements = []
                for row in disb_rows:
                    disbursements.append({
                        "date": row[0],
                        "description": row[1],
                        "payee": row[2],
                        "total_amount": row[3]
                    })
        
        # Prepare matter data
        matter_data = {
            "matter_name": matter_name,
            "court_file_number": request.court_file_number or db_court_file or "N/A",
            "plaintiff": request.plaintiff or client_name or client_full_name,
            "defendant": request.defendant or "N/A"
        }
        
        # Generate Bill of Costs
        bill_of_costs_bytes = await billing_gen.generate_bill_of_costs(
            matter_data,
            time_entries,
            disbursements
        )
        
        # Return as file response
        filename = f"bill_of_costs_{request.matter_id}.docx"
        
        return Response(
            content=bill_of_costs_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Bill of Costs generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Bill of Costs generation failed: {str(e)}")


@router.post("/generate-cover-letter", response_model=Dict[str, Any])
async def generate_cover_letter(
    request: GenerateCoverLetterRequest,
    practice_mgr: OntarioPracticeManager = Depends(get_practice_manager),
    letter_gen: AIEnhancedCoverLetterGenerator = Depends(get_cover_letter_generator)
):
    """Generate AI-enhanced professional cover letter"""
    try:
        logger.info(f"Generating cover letter for client: {request.client_id}")
        
        # Get client and matter details
        async with practice_mgr.db_path as db_path:
            import aiosqlite
            async with aiosqlite.connect(db_path) as db:
                cursor = await db.execute('''
                    SELECT c.client_name, c.full_name, c.address, m.matter_name
                    FROM clients c
                    JOIN matters m ON m.client_id = c.client_id
                    WHERE c.client_id = ? AND m.matter_id = ?
                ''', (request.client_id, request.matter_id))
                row = await cursor.fetchone()
                
                if not row:
                    raise HTTPException(status_code=404, detail="Client or matter not found")
                
                client_name, full_name, address, matter_name = row
        
        # Get firm logo and settings
        logo_data = await practice_mgr.get_firm_setting("firm_logo")
        if logo_data:
            letter_gen.set_firm_logo(logo_data)
        
        firm_info = {
            "firm_name": await practice_mgr.get_firm_setting("firm_name") or "Law Firm",
            "address": await practice_mgr.get_firm_setting("firm_address") or "",
            "phone": await practice_mgr.get_firm_setting("firm_phone") or "",
            "email": await practice_mgr.get_firm_setting("firm_email") or "",
            "lawyer_name": await practice_mgr.get_firm_setting("lawyer_name") or ""
        }
        letter_gen.set_firm_info(firm_info)
        
        # Prepare client info
        client_info = {
            "name": client_name or full_name,
            "address": address,
            "matter_name": matter_name
        }
        
        # Prepare invoice data if applicable
        invoice_data = None
        if request.invoice_number:
            # Get invoice details
            async with practice_mgr.db_path as db_path:
                async with aiosqlite.connect(db_path) as db:
                    cursor = await db.execute('''
                        SELECT total_amount, payment_terms
                        FROM invoices
                        WHERE invoice_number = ?
                    ''', (request.invoice_number,))
                    inv_row = await cursor.fetchone()
                    
                    if inv_row:
                        invoice_data = {
                            "invoice_number": request.invoice_number,
                            "total": inv_row[0],
                            "payment_terms": inv_row[1] or "Payment is due within 30 days"
                        }
        
        # Generate cover letter
        letter_bytes = await letter_gen.generate_cover_letter(
            client_info,
            request.documents_included,
            invoice_data,
            request.additional_notes,
            format=request.format
        )
        
        # Return as file response
        media_type = "application/pdf" if request.format == "pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        filename = f"cover_letter_{request.client_id}.{request.format}"
        
        return Response(
            content=letter_bytes,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Cover letter generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Cover letter generation failed: {str(e)}")


@router.post("/batch-download", response_model=Dict[str, Any])
async def batch_download(
    request: BatchDownloadRequest,
    practice_mgr: OntarioPracticeManager = Depends(get_practice_manager),
    billing_gen: OntarioBillingDocumentGenerator = Depends(get_billing_generator),
    letter_gen: AIEnhancedCoverLetterGenerator = Depends(get_cover_letter_generator)
):
    """Generate and download multiple documents as batch (ZIP or combined)"""
    try:
        logger.info(f"Generating batch download for matter: {request.matter_id}")
        
        documents = []
        
        # Generate requested documents
        for doc_type in request.document_types:
            if doc_type == "invoice":
                # Generate invoice (reuse logic from generate_invoice)
                # This is simplified - in production would refactor common logic
                pass  # Would call invoice generation
            
            elif doc_type == "timesheet":
                # Generate detailed timesheet
                pass  # Would generate timesheet
            
            elif doc_type == "bill_of_costs":
                # Generate Bill of Costs (reuse logic)
                pass  # Would call bill of costs generation
            
            elif doc_type == "cover_letter":
                # Generate cover letter (reuse logic)
                pass  # Would call cover letter generation
        
        # Combine or package documents
        if request.combine:
            # Combine into single document with page numbering
            result_bytes = await DocumentCombiner.combine_pdfs(documents, add_page_numbers=True)
            media_type = "application/pdf" if request.format == "pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            filename = f"combined_documents_{request.matter_id}.{request.format}"
        else:
            # Create ZIP package
            result_bytes = await BatchDocumentGenerator.create_batch_download(documents, format="zip")
            media_type = "application/zip"
            filename = f"documents_{request.matter_id}.zip"
        
        return Response(
            content=result_bytes,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        logger.error(f"Batch download failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch download failed: {str(e)}")


@router.post("/upload-logo", response_model=Dict[str, Any])
async def upload_firm_logo(
    request: UploadLogoRequest,
    practice_mgr: OntarioPracticeManager = Depends(get_practice_manager)
):
    """Upload and store firm logo"""
    try:
        logger.info("Uploading firm logo")
        
        # Validate base64 data
        try:
            logo_bytes = base64.b64decode(request.logo_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid base64 logo data")
        
        # Save logo to firm settings
        await practice_mgr.save_firm_setting(
            "firm_logo",
            request.logo_data,
            "image",
            "Firm logo for documents"
        )
        
        return {
            "success": True,
            "message": "Firm logo uploaded successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Logo upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Logo upload failed: {str(e)}")


@router.get("/health", response_model=Dict[str, Any])
async def health_check():
    """Health check endpoint"""
    return {
        "success": True,
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
