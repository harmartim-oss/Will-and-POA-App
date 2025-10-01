# tests/test_billing_features.py
"""
Tests for new billing features:
- Disbursements
- Invoice templates
- Bill of Costs
- Cover letters
- Document combining
"""

import pytest
import pytest_asyncio
import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.core.practice_management import OntarioPracticeManager
from backend.core.billing_documents import OntarioBillingDocumentGenerator, AIEnhancedCoverLetterGenerator
from backend.core.document_combiner import DocumentCombiner, BatchDocumentGenerator


@pytest_asyncio.fixture
async def practice_manager(tmp_path):
    """Create and initialize practice manager for testing"""
    db_file = tmp_path / "test.db"
    manager = OntarioPracticeManager(database_path=str(db_file))
    await manager.initialize()
    yield manager
    # Cleanup
    if db_file.exists():
        db_file.unlink()


@pytest.fixture
def billing_generator():
    """Create billing document generator"""
    return OntarioBillingDocumentGenerator()


@pytest.fixture
def cover_letter_generator():
    """Create cover letter generator"""
    return AIEnhancedCoverLetterGenerator()


class TestDisbursements:
    """Test disbursement tracking"""
    
    @pytest.mark.asyncio
    async def test_add_disbursement(self, practice_manager):
        """Test adding a disbursement entry"""
        # Create client and matter first
        client_data = {
            "name": "Test Client",
            "contact": {"email": "test@example.com", "phone": "555-1234"}
        }
        matter_data = {
            "type": "real_estate",
            "responsible_lawyer": "LSUC12345"
        }
        
        result = await practice_manager.create_client_matter(client_data, matter_data)
        matter_id = result["matter_id"]
        
        # Add disbursement
        disbursement_data = {
            "matter_id": matter_id,
            "description": "Title insurance policy",
            "category": "title_insurance",
            "amount": 500.00,
            "hst_applicable": True,
            "payee": "Title Insurance Company",
            "reference_number": "TI-12345"
        }
        
        result = await practice_manager.add_disbursement(disbursement_data)
        
        assert result["status"] == "recorded"
        assert result["amount"] == 500.00
        assert result["hst_amount"] == 65.00  # 13% HST
        assert result["total_amount"] == 565.00
        assert "disbursement_id" in result
    
    @pytest.mark.asyncio
    async def test_disbursement_without_hst(self, practice_manager):
        """Test disbursement without HST"""
        # Create client and matter first
        client_data = {
            "name": "Test Client",
            "contact": {"email": "test@example.com"}
        }
        matter_data = {
            "type": "litigation",
            "responsible_lawyer": "LSUC12345"
        }
        
        result = await practice_manager.create_client_matter(client_data, matter_data)
        matter_id = result["matter_id"]
        
        # Add disbursement without HST
        disbursement_data = {
            "matter_id": matter_id,
            "description": "Court filing fee",
            "category": "filing_fees",
            "amount": 100.00,
            "hst_applicable": False,
            "payee": "Ontario Superior Court"
        }
        
        result = await practice_manager.add_disbursement(disbursement_data)
        
        assert result["hst_amount"] == 0.00
        assert result["total_amount"] == 100.00


class TestInvoiceGeneration:
    """Test invoice generation with disbursements"""
    
    @pytest.mark.asyncio
    async def test_generate_bill_with_disbursements(self, practice_manager):
        """Test generating bill with time entries and disbursements"""
        # Create client and matter
        client_data = {
            "name": "Test Client",
            "contact": {"email": "test@example.com"}
        }
        matter_data = {
            "type": "real_estate",
            "responsible_lawyer": "LSUC12345"
        }
        
        result = await practice_manager.create_client_matter(client_data, matter_data)
        matter_id = result["matter_id"]
        
        # Add time entry
        time_data = {
            "matter_id": matter_id,
            "lawyer_id": "LSUC12345",
            "date": datetime.now().date().isoformat(),
            "duration_minutes": 120,
            "description": "Client consultation",
            "hourly_rate": 400.00,
            "billable": True
        }
        await practice_manager.track_time_entry(time_data)
        
        # Add disbursement
        disbursement_data = {
            "matter_id": matter_id,
            "description": "Title insurance",
            "amount": 500.00,
            "hst_applicable": True,
            "payee": "Title Co"
        }
        await practice_manager.add_disbursement(disbursement_data)
        
        # Generate bill
        bill_result = await practice_manager.generate_monthly_bill(
            matter_id,
            datetime.now().date().isoformat()
        )
        
        assert "bill_id" in bill_result
        assert bill_result["time_entry_count"] == 1
        assert bill_result["disbursement_count"] == 1
        assert bill_result["time_subtotal"] == 800.00  # 2 hours * $400
        assert bill_result["disbursement_subtotal"] == 500.00
        assert bill_result["subtotal"] == 1300.00
        # Total HST = 13% on time + HST on disbursement
        assert bill_result["taxes"] == (800.00 * 0.13 + 500.00 * 0.13)


class TestInvoiceTemplates:
    """Test custom invoice template management"""
    
    @pytest.mark.asyncio
    async def test_save_invoice_template(self, practice_manager):
        """Test saving a custom invoice template"""
        template_data = {
            "template_name": "Detailed Invoice Template",
            "template_type": "custom",
            "include_logo": True,
            "include_timesheet": True,
            "include_disbursements": True,
            "is_default": True
        }
        
        template_id = await practice_manager.save_invoice_template(template_data)
        
        assert template_id is not None
        
        # Retrieve template
        retrieved = await practice_manager.get_invoice_template(template_id)
        
        assert retrieved["template_name"] == "Detailed Invoice Template"
        assert retrieved["is_default"] == 1  # SQLite returns 1 for TRUE
    
    @pytest.mark.asyncio
    async def test_get_all_templates(self, practice_manager):
        """Test retrieving all invoice templates"""
        # Save multiple templates
        for i in range(3):
            template_data = {
                "template_name": f"Template {i}",
                "is_default": i == 0
            }
            await practice_manager.save_invoice_template(template_data)
        
        templates = await practice_manager.get_invoice_templates()
        
        assert len(templates) >= 3
        # Default template should be first
        assert templates[0]["is_default"] is True


class TestFirmSettings:
    """Test firm settings and logo management"""
    
    @pytest.mark.asyncio
    async def test_save_firm_logo(self, practice_manager):
        """Test saving firm logo"""
        import base64
        
        # Create dummy logo data
        dummy_image_data = b"fake_image_data"
        logo_base64 = base64.b64encode(dummy_image_data).decode('utf-8')
        
        await practice_manager.save_firm_setting(
            "firm_logo",
            logo_base64,
            "image",
            "Firm logo"
        )
        
        # Retrieve logo
        retrieved = await practice_manager.get_firm_setting("firm_logo")
        
        assert retrieved == logo_base64
    
    @pytest.mark.asyncio
    async def test_save_firm_info(self, practice_manager):
        """Test saving firm information"""
        await practice_manager.save_firm_setting("firm_name", "Smith & Associates", "text")
        await practice_manager.save_firm_setting("firm_address", "123 Main St", "text")
        await practice_manager.save_firm_setting("firm_phone", "555-1234", "text")
        
        firm_name = await practice_manager.get_firm_setting("firm_name")
        
        assert firm_name == "Smith & Associates"


class TestBillingDocuments:
    """Test billing document generation"""
    
    @pytest.mark.asyncio
    async def test_generate_invoice_pdf(self, billing_generator):
        """Test generating invoice in PDF format"""
        invoice_data = {
            "invoice_number": "INV-2024-001",
            "invoice_date": "2024-01-15",
            "matter_name": "Real Estate Transaction",
            "client_name": "John Doe",
            "time_subtotal": 800.00,
            "disbursement_subtotal": 500.00,
            "subtotal": 1300.00,
            "taxes": 169.00,
            "total": 1469.00
        }
        
        time_entries = [
            {
                "date": "2024-01-10",
                "description": "Client consultation",
                "duration_minutes": 120,
                "hourly_rate": 400.00,
                "total_amount": 800.00
            }
        ]
        
        disbursements = [
            {
                "date": "2024-01-12",
                "description": "Title insurance",
                "payee": "Title Co",
                "amount": 500.00,
                "hst_amount": 65.00,
                "total_amount": 565.00
            }
        ]
        
        template_config = {
            "include_logo": False,
            "include_timesheet": True,
            "include_disbursements": True
        }
        
        pdf_bytes = await billing_generator.generate_invoice(
            invoice_data,
            time_entries,
            disbursements,
            template_config,
            format="pdf"
        )
        
        assert pdf_bytes is not None
        assert len(pdf_bytes) > 0
        # Check PDF signature
        assert pdf_bytes[:4] == b'%PDF'
    
    @pytest.mark.asyncio
    async def test_generate_invoice_docx(self, billing_generator):
        """Test generating invoice in DOCX format"""
        invoice_data = {
            "invoice_number": "INV-2024-001",
            "invoice_date": "2024-01-15",
            "matter_name": "Real Estate Transaction",
            "client_name": "John Doe",
            "time_subtotal": 800.00,
            "disbursement_subtotal": 0.00,
            "subtotal": 800.00,
            "taxes": 104.00,
            "total": 904.00
        }
        
        time_entries = [
            {
                "date": "2024-01-10",
                "description": "Client consultation",
                "duration_minutes": 120,
                "hourly_rate": 400.00,
                "total_amount": 800.00
            }
        ]
        
        docx_bytes = await billing_generator.generate_invoice(
            invoice_data,
            time_entries,
            [],
            {},
            format="docx"
        )
        
        assert docx_bytes is not None
        assert len(docx_bytes) > 0
    
    @pytest.mark.asyncio
    async def test_generate_bill_of_costs(self, billing_generator):
        """Test generating Bill of Costs"""
        matter_data = {
            "matter_name": "Litigation Matter",
            "court_file_number": "CV-2024-001",
            "plaintiff": "John Smith",
            "defendant": "Jane Doe"
        }
        
        time_entries = [
            {
                "date": "2024-01-10",
                "description": "Document review",
                "duration_minutes": 180,
                "hourly_rate": 400.00,
                "total_amount": 1200.00
            }
        ]
        
        disbursements = [
            {
                "date": "2024-01-15",
                "description": "Filing fees",
                "payee": "Court",
                "total_amount": 200.00
            }
        ]
        
        docx_bytes = await billing_generator.generate_bill_of_costs(
            matter_data,
            time_entries,
            disbursements
        )
        
        assert docx_bytes is not None
        assert len(docx_bytes) > 0


class TestCoverLetterGeneration:
    """Test AI-enhanced cover letter generation"""
    
    @pytest.mark.asyncio
    async def test_generate_cover_letter_pdf(self, cover_letter_generator):
        """Test generating cover letter in PDF format"""
        client_info = {
            "name": "John Doe",
            "matter_name": "Real Estate Transaction",
            "address": "123 Main St\nToronto, ON M1A 1A1"
        }
        
        documents_included = [
            "Invoice #INV-2024-001",
            "Detailed Timesheet",
            "Disbursement Summary"
        ]
        
        invoice_data = {
            "invoice_number": "INV-2024-001",
            "total": 1469.00,
            "payment_terms": "Payment due within 30 days"
        }
        
        pdf_bytes = await cover_letter_generator.generate_cover_letter(
            client_info,
            documents_included,
            invoice_data,
            "Thank you for your business.",
            format="pdf"
        )
        
        assert pdf_bytes is not None
        assert len(pdf_bytes) > 0
        assert pdf_bytes[:4] == b'%PDF'
    
    @pytest.mark.asyncio
    async def test_generate_cover_letter_docx(self, cover_letter_generator):
        """Test generating cover letter in DOCX format"""
        client_info = {
            "name": "Jane Smith",
            "matter_name": "Estate Planning"
        }
        
        documents_included = ["Will", "Power of Attorney"]
        
        docx_bytes = await cover_letter_generator.generate_cover_letter(
            client_info,
            documents_included,
            None,
            None,
            format="docx"
        )
        
        assert docx_bytes is not None
        assert len(docx_bytes) > 0


class TestDocumentCombining:
    """Test document combining and batch generation"""
    
    @pytest.mark.asyncio
    async def test_combine_pdfs(self):
        """Test combining multiple PDFs"""
        # Create dummy PDF documents
        from reportlab.pdfgen import canvas
        from io import BytesIO
        
        doc1 = BytesIO()
        can1 = canvas.Canvas(doc1)
        can1.drawString(100, 750, "Document 1")
        can1.showPage()
        can1.save()
        
        doc2 = BytesIO()
        can2 = canvas.Canvas(doc2)
        can2.drawString(100, 750, "Document 2")
        can2.showPage()
        can2.save()
        
        documents = [
            {"content": doc1.getvalue(), "name": "doc1.pdf", "type": "pdf"},
            {"content": doc2.getvalue(), "name": "doc2.pdf", "type": "pdf"}
        ]
        
        combined = await DocumentCombiner.combine_pdfs(documents, add_page_numbers=True)
        
        assert combined is not None
        assert len(combined) > 0
        assert combined[:4] == b'%PDF'
    
    @pytest.mark.asyncio
    async def test_batch_download_zip(self):
        """Test creating ZIP package of documents"""
        from reportlab.pdfgen import canvas
        from io import BytesIO
        
        doc1 = BytesIO()
        can1 = canvas.Canvas(doc1)
        can1.drawString(100, 750, "Invoice")
        can1.showPage()
        can1.save()
        
        doc2 = BytesIO()
        can2 = canvas.Canvas(doc2)
        can2.drawString(100, 750, "Timesheet")
        can2.showPage()
        can2.save()
        
        documents = [
            {"content": doc1.getvalue(), "name": "invoice.pdf", "type": "pdf"},
            {"content": doc2.getvalue(), "name": "timesheet.pdf", "type": "pdf"}
        ]
        
        zip_bytes = await BatchDocumentGenerator.create_batch_download(documents, format="zip")
        
        assert zip_bytes is not None
        assert len(zip_bytes) > 0
        # Check ZIP signature
        assert zip_bytes[:2] == b'PK'


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
