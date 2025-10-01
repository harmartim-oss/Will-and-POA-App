# Billing and Invoice Management Features

This document describes the enhanced billing and invoice management features for the Ontario legal practice management system.

## Overview

The system now supports comprehensive billing and invoice management with the following features:

1. **Disbursement Tracking** - Track out-of-pocket expenses to be billed to clients
2. **Custom Invoice Templates** - Create and save custom invoice templates
3. **Bill of Costs** - Generate compliant Bill of Costs per Ontario Rules of Civil Procedure
4. **AI-Powered Cover Letters** - Generate professional cover letters
5. **Firm Logo Management** - Upload and display firm logo on documents
6. **Batch Document Generation** - Generate multiple documents at once
7. **Document Combining** - Combine multiple documents with page numbering

## Features in Detail

### 1. Disbursement Tracking

Track out-of-pocket expenses like title insurance, filing fees, courier services, etc.

#### API Endpoint
```http
POST /api/practice/disbursement
```

#### Request Body
```json
{
  "matter_id": "matter_abc123",
  "date": "2024-01-15",
  "description": "Title insurance policy for 123 Main St",
  "category": "title_insurance",
  "amount": 500.00,
  "hst_applicable": true,
  "payee": "First Canadian Title",
  "reference_number": "TI-2024-001",
  "billable": true,
  "notes": "Policy for client's new home"
}
```

#### Response
```json
{
  "success": true,
  "data": {
    "disbursement_id": "disb_xyz789",
    "amount": 500.00,
    "hst_amount": 65.00,
    "total_amount": 565.00,
    "status": "recorded"
  },
  "message": "Disbursement recorded successfully"
}
```

#### Features
- Automatic HST calculation (13% for Ontario)
- Optional HST exemption for certain items
- Category tracking (title_insurance, filing_fees, courier, etc.)
- Payee and reference number tracking
- Billable/non-billable flag

### 2. Enhanced Invoice Generation

Invoices now include both time entries and disbursements.

#### API Endpoint
```http
POST /api/billing/generate-invoice
```

#### Request Body
```json
{
  "matter_id": "matter_abc123",
  "bill_date": "2024-01-31",
  "template_id": "template_custom_001",
  "format": "pdf"
}
```

#### Invoice Includes
- Legal services (time entries) with detailed breakdown
- Disbursements with payee and description
- Subtotals for services and disbursements
- HST calculations (separate for services and disbursements)
- Firm logo and letterhead
- Professional formatting

### 3. Custom Invoice Templates

Create and manage custom invoice templates with different layouts and options.

#### Save Template
```http
POST /api/practice/invoice-template
```

```json
{
  "template_name": "Detailed Real Estate Invoice",
  "template_type": "custom",
  "include_logo": true,
  "include_timesheet": true,
  "include_disbursements": true,
  "is_default": false,
  "layout_config": {
    "show_hourly_rate": true,
    "group_by_date": true,
    "show_activity_type": true
  }
}
```

#### Get All Templates
```http
GET /api/practice/invoice-templates
```

#### Get Specific Template
```http
GET /api/practice/invoice-template/{template_id}
```

### 4. Bill of Costs

Generate Ontario-compliant Bill of Costs for court proceedings.

#### API Endpoint
```http
POST /api/billing/generate-bill-of-costs
```

#### Request Body
```json
{
  "matter_id": "matter_abc123",
  "court_file_number": "CV-2024-00123",
  "plaintiff": "John Smith",
  "defendant": "Jane Doe"
}
```

#### Bill of Costs Includes
- **Part I - Legal Fees**: Detailed breakdown of legal services
- **Part II - Disbursements**: Itemized out-of-pocket expenses
- **Summary**: Total fees and disbursements
- Court-compliant formatting per Ontario Rules of Civil Procedure
- Assessment officer certification section

### 5. AI-Powered Cover Letter Generator

Generate professional cover letters using AI-enhanced templates.

#### API Endpoint
```http
POST /api/billing/generate-cover-letter
```

#### Request Body
```json
{
  "client_id": "client_xyz789",
  "matter_id": "matter_abc123",
  "documents_included": [
    "Invoice #INV-2024-001",
    "Detailed Timesheet",
    "Disbursement Summary"
  ],
  "invoice_number": "INV-2024-001",
  "additional_notes": "Please note the revised closing date.",
  "format": "pdf"
}
```

#### Cover Letter Features
- Professional letterhead with firm logo
- Personalized client greeting
- Matter reference
- Invoice details and payment instructions
- List of enclosed documents
- Professional closing
- Available in PDF or DOCX format

### 6. Firm Logo and Settings

Upload and manage firm branding.

#### Upload Logo
```http
POST /api/billing/upload-logo
```

```json
{
  "logo_data": "base64_encoded_image_data"
}
```

#### Save Firm Settings
```http
POST /api/practice/firm-setting
```

```json
{
  "setting_key": "firm_name",
  "setting_value": "Smith & Associates",
  "setting_type": "text",
  "description": "Firm name for documents"
}
```

#### Common Firm Settings
- `firm_name`: Law firm name
- `firm_address`: Physical address
- `firm_phone`: Contact phone number
- `firm_email`: Contact email
- `lawyer_name`: Principal lawyer name
- `firm_logo`: Base64 encoded logo image

### 7. Batch Document Download

Generate multiple documents at once and download as ZIP or combined PDF.

#### API Endpoint
```http
POST /api/billing/batch-download
```

#### Request Body
```json
{
  "matter_id": "matter_abc123",
  "document_types": [
    "invoice",
    "timesheet",
    "bill_of_costs",
    "cover_letter"
  ],
  "combine": true,
  "format": "pdf"
}
```

#### Options
- `combine: false` - Creates a ZIP file with separate documents
- `combine: true` - Merges all documents into single PDF/DOCX with:
  - Each document on separate pages
  - Page numbers starting on second page (top right)
  - Professional page breaks between documents

## Code Examples

### Python - Add Disbursement
```python
from backend.core.practice_management import OntarioPracticeManager

manager = OntarioPracticeManager()
await manager.initialize()

disbursement_data = {
    "matter_id": "matter_abc123",
    "description": "Title insurance policy",
    "category": "title_insurance",
    "amount": 500.00,
    "hst_applicable": True,
    "payee": "Title Company"
}

result = await manager.add_disbursement(disbursement_data)
print(f"Disbursement recorded: {result['disbursement_id']}")
print(f"Total amount: ${result['total_amount']:.2f}")
```

### Python - Generate Invoice
```python
from backend.core.billing_documents import OntarioBillingDocumentGenerator

generator = OntarioBillingDocumentGenerator()

# Set firm info
generator.set_firm_info({
    "firm_name": "Smith & Associates",
    "address": "123 Main St, Toronto, ON",
    "phone": "416-555-1234",
    "email": "info@smithlaw.ca"
})

# Set logo
generator.set_firm_logo(logo_base64_data)

# Generate invoice
invoice_bytes = await generator.generate_invoice(
    invoice_data,
    time_entries,
    disbursements,
    template_config,
    format="pdf"
)

# Save to file
with open("invoice.pdf", "wb") as f:
    f.write(invoice_bytes)
```

### Python - Generate Bill of Costs
```python
from backend.core.billing_documents import OntarioBillingDocumentGenerator

generator = OntarioBillingDocumentGenerator()

matter_data = {
    "matter_name": "Smith v. Jones",
    "court_file_number": "CV-2024-00123",
    "plaintiff": "John Smith",
    "defendant": "Jane Jones"
}

bill_bytes = await generator.generate_bill_of_costs(
    matter_data,
    time_entries,
    disbursements
)

with open("bill_of_costs.docx", "wb") as f:
    f.write(bill_bytes)
```

### Python - Generate Cover Letter
```python
from backend.core.billing_documents import AIEnhancedCoverLetterGenerator

generator = AIEnhancedCoverLetterGenerator()

# Set firm info
generator.set_firm_info({
    "firm_name": "Smith & Associates",
    "lawyer_name": "Jane Smith",
    "address": "123 Main St, Toronto, ON",
    "phone": "416-555-1234",
    "email": "jane@smithlaw.ca"
})

# Generate cover letter
letter_bytes = await generator.generate_cover_letter(
    client_info={
        "name": "John Doe",
        "address": "456 Oak Ave, Toronto, ON",
        "matter_name": "Real Estate Purchase"
    },
    documents_included=[
        "Invoice #INV-2024-001",
        "Detailed Timesheet",
        "Disbursement Summary"
    ],
    invoice_data={
        "invoice_number": "INV-2024-001",
        "total": 2500.00,
        "payment_terms": "Payment due within 30 days"
    },
    format="pdf"
)
```

### Python - Combine Documents
```python
from backend.core.document_combiner import DocumentCombiner

documents = [
    {"content": cover_letter_bytes, "name": "cover_letter.pdf", "type": "pdf"},
    {"content": invoice_bytes, "name": "invoice.pdf", "type": "pdf"},
    {"content": timesheet_bytes, "name": "timesheet.pdf", "type": "pdf"}
]

# Combine with page numbering (starting on page 2)
combined_pdf = await DocumentCombiner.combine_pdfs(
    documents,
    add_page_numbers=True,
    start_numbering_page=2
)

with open("combined_documents.pdf", "wb") as f:
    f.write(combined_pdf)
```

## Database Schema

### Disbursements Table
```sql
CREATE TABLE disbursements (
    disbursement_id TEXT PRIMARY KEY,
    matter_id TEXT NOT NULL,
    date DATE NOT NULL,
    description TEXT NOT NULL,
    category TEXT,
    amount REAL NOT NULL,
    hst_applicable BOOLEAN DEFAULT TRUE,
    hst_amount REAL DEFAULT 0.0,
    total_amount REAL NOT NULL,
    payee TEXT,
    reference_number TEXT,
    billable BOOLEAN DEFAULT TRUE,
    billed BOOLEAN DEFAULT FALSE,
    billed_date TIMESTAMP,
    status TEXT DEFAULT 'draft',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    FOREIGN KEY (matter_id) REFERENCES matters (matter_id)
);
```

### Invoice Templates Table
```sql
CREATE TABLE invoice_templates (
    template_id TEXT PRIMARY KEY,
    template_name TEXT NOT NULL UNIQUE,
    template_type TEXT DEFAULT 'standard',
    layout_config TEXT,
    header_template TEXT,
    footer_template TEXT,
    line_item_template TEXT,
    include_logo BOOLEAN DEFAULT TRUE,
    include_timesheet BOOLEAN DEFAULT TRUE,
    include_disbursements BOOLEAN DEFAULT TRUE,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Firm Settings Table
```sql
CREATE TABLE firm_settings (
    setting_id TEXT PRIMARY KEY,
    setting_key TEXT NOT NULL UNIQUE,
    setting_value TEXT,
    setting_type TEXT DEFAULT 'text',
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by TEXT
);
```

## Testing

All features have been tested with 14 comprehensive test cases:

```bash
# Run all billing feature tests
pytest tests/test_billing_features.py -v

# Test results:
# ✓ Disbursement tracking (2 tests)
# ✓ Invoice generation with disbursements (1 test)
# ✓ Invoice template management (2 tests)
# ✓ Firm settings and logo (2 tests)
# ✓ Document generation (PDF/DOCX) (3 tests)
# ✓ Cover letter generation (2 tests)
# ✓ Document combining (2 tests)
```

## Dependencies

The following Python packages are required:

```
python-docx==1.1.0
reportlab==4.1.0
PyPDF2==3.0.1
aiosqlite==0.20.0
Pillow>=9.0.0
```

## Ontario Compliance

All billing features comply with:

- **Law Society of Ontario (LSO)** requirements for client billing
- **Ontario Rules of Civil Procedure** for Bill of Costs formatting
- **HST regulations** for Ontario (13% HST)
- **Professional standards** for legal invoicing and communication

## Best Practices

1. **Always include detailed descriptions** for time entries and disbursements
2. **Save custom templates** for different matter types
3. **Use professional cover letters** for all client communications
4. **Keep firm logo and settings up to date**
5. **Generate Bill of Costs** for all litigated matters
6. **Provide combined documents** for client convenience
7. **Review invoices before sending** to ensure accuracy

## Support and Documentation

For more information:
- See `ONTARIO_ENHANCEMENT_INTEGRATION_GUIDE.md` for practice management features
- See `backend/api/routes/billing.py` for complete API documentation
- See `tests/test_billing_features.py` for usage examples

## Future Enhancements

Planned features:
- Payment processing integration
- Automatic invoice reminders
- Client portal for invoice viewing
- Multi-currency support
- Batch invoice generation
- Advanced reporting and analytics
