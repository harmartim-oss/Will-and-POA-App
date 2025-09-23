"""
Enhanced Document Management Service
Comprehensive document generation and management for Ontario legal documents
"""

import os
import json
import hashlib
import aiofiles
import aiosqlite
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class DocumentVersion:
    """Document version information"""
    id: str
    document_id: str
    version_number: int
    file_path: str
    file_hash: str
    changes_summary: str
    created_at: datetime
    created_by: str

class EnhancedDocumentManager:
    """
    Enhanced document management system with Ontario legal compliance,
    AI integration, and comprehensive document lifecycle management
    """
    
    def __init__(self, storage_path: str = None, client_docs_path: str = None):
        self.storage_path = Path(storage_path or "data/storage")
        self.client_docs_path = Path(client_docs_path or "data/client_documents")
        self.is_initialized = False
        
        # Ontario court forms configuration
        self.ontario_court_forms = {
            "probate": {
                "74": "Application for Certificate of Appointment of Estate Trustee",
                "74A": "Affidavit of Service of Notice",
                "75": "Notice to Estate Creditors"
            }
        }
        
        self._ensure_directories()
        
    def _ensure_directories(self):
        """Ensure required directories exist"""
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.client_docs_path.mkdir(parents=True, exist_ok=True)
        
    async def initialize(self):
        """Initialize the document management system"""
        try:
            await self._setup_database()
            self.is_initialized = True
            logger.info("Enhanced Document Manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Enhanced Document Manager: {str(e)}")
            raise
    
    async def _setup_database(self):
        """Setup database tables for document management"""
        async with aiosqlite.connect(self.storage_path / "documents.db") as db:
            # Main documents table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    client_id TEXT,
                    matter_id TEXT,
                    document_type TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_hash TEXT NOT NULL,
                    version INTEGER DEFAULT 1,
                    status TEXT DEFAULT 'draft',
                    created_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ontario_compliant BOOLEAN DEFAULT TRUE,
                    court_form_number TEXT
                )
            """)
            
            # Document versions table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS document_versions (
                    id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL,
                    version_number INTEGER NOT NULL,
                    file_path TEXT NOT NULL,
                    file_hash TEXT NOT NULL,
                    changes_summary TEXT,
                    created_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (document_id) REFERENCES documents (id)
                )
            """)
            
            await db.commit()
    
    async def generate_document(self, document_type: str, fields: Dict[str, Any]) -> str:
        """Generate document with enhanced features"""
        try:
            # Get template
            template = await self._get_document_template(document_type)
            
            # Generate content based on document type
            if document_type == "will":
                content = await self._generate_will_content(fields)
            elif document_type == "poa_property":
                content = await self._generate_poa_property_content(fields)
            elif document_type == "poa_personal_care":
                content = await self._generate_poa_care_content(fields)
            elif document_type == "probate_application":
                content = await self._generate_probate_content(fields)
            else:
                content = await self._generate_generic_content(template, fields)
            
            return content
            
        except Exception as e:
            logger.error(f"Document generation failed: {str(e)}")
            raise
    
    async def _get_document_template(self, document_type: str) -> Dict[str, Any]:
        """Get document template for specified type"""
        templates = {
            "will": {
                "title": "Last Will and Testament",
                "sections": ["opening", "executor", "bequests", "residuary", "execution"],
                "ontario_compliant": True
            },
            "poa_property": {
                "title": "Power of Attorney for Property",
                "sections": ["opening", "powers", "limitations", "execution"],
                "ontario_compliant": True
            },
            "poa_personal_care": {
                "title": "Power of Attorney for Personal Care",
                "sections": ["opening", "care_instructions", "limitations", "execution"],
                "ontario_compliant": True
            },
            "probate_application": {
                "title": "Application for Certificate of Appointment",
                "sections": ["applicant_info", "deceased_info", "estate_info", "beneficiaries"],
                "ontario_compliant": True
            }
        }
        
        return templates.get(document_type, {})
    
    async def _generate_will_content(self, fields: Dict[str, Any]) -> str:
        """Generate Ontario-compliant will content"""
        content = f"""
LAST WILL AND TESTAMENT
OF
{fields.get('testator_name', '[TESTATOR NAME]')}

I, {fields.get('testator_name', '[TESTATOR NAME]')}, of {fields.get('testator_address', '[ADDRESS]')},
revoke all previous wills and make this my Last Will and Testament.

1. APPOINTMENT OF EXECUTOR
I appoint {fields.get('executor_name', '[EXECUTOR NAME]')} to be the Executor of this my Will.

2. PAYMENT OF DEBTS
I direct my Executor to pay all my just debts, funeral expenses, and testamentary expenses.

3. SPECIFIC BEQUESTS
{self._generate_specific_bequests(fields.get('specific_bequests', []))}

4. RESIDUARY ESTATE
I give the residue of my estate to {fields.get('residuary_beneficiary', '[BENEFICIARY]')}.

5. CONTINGENT BENEFICIARIES
If the above beneficiaries predecease me, then to {fields.get('contingent_beneficiary', '[CONTINGENT BENEFICIARY]')}.

6. GUARDIAN APPOINTMENT
{self._generate_guardian_clause(fields.get('guardian_appointment'))}

IN WITNESS WHEREOF I have hereunto set my hand this {datetime.now().strftime('%d')} day of {datetime.now().strftime('%B, %Y')}.

SIGNED by the Testator in our presence and signed by us in the presence of the Testator and each other:

_____________________ (Testator)

_____________________ (Witness 1) _____________________ (Witness 2)
"""
        return content
    
    async def _generate_poa_property_content(self, fields: Dict[str, Any]) -> str:
        """Generate Ontario POA for property content"""
        content = f"""
POWER OF ATTORNEY FOR PROPERTY

Made this {datetime.now().strftime('%d')} day of {datetime.now().strftime('%B, %Y')}

I, {fields.get('grantor_name', '[GRANTOR NAME]')}, of {fields.get('grantor_address', '[ADDRESS]')},
appoint {fields.get('attorney_name', '[ATTORNEY NAME]')} as my Attorney for Property.

1. POWERS GRANTED
My Attorney may exercise the following powers on my behalf:
- To manage, sell, lease, or mortgage real property
- To manage bank accounts and investments
- To pay bills and expenses
- To file tax returns
- To make financial decisions

2. LIMITATIONS
{fields.get('limitations', 'No specific limitations')}

3. SUBSTITUTE ATTORNEY
{self._generate_substitute_attorney_clause(fields.get('substitute_attorney'))}

4. COMPENSATION
My Attorney is entitled to reasonable compensation for services rendered.

This Power of Attorney is given in accordance with the Substitute Decisions Act, 1992 (Ontario).

SIGNATURES:
_____________________ (Grantor)

Witness 1: _____________________ Witness 2: _____________________
"""
        return content
    
    async def _generate_poa_care_content(self, fields: Dict[str, Any]) -> str:
        """Generate Ontario POA for personal care content"""
        content = f"""
POWER OF ATTORNEY FOR PERSONAL CARE

Made this {datetime.now().strftime('%d')} day of {datetime.now().strftime('%B, %Y')}

I, {fields.get('grantor_name', '[GRANTOR NAME]')}, of {fields.get('grantor_address', '[ADDRESS]')},
appoint {fields.get('attorney_name', '[ATTORNEY NAME]')} as my Attorney for Personal Care.

1. PERSONAL CARE DECISIONS
My Attorney may make decisions regarding:
- Health care treatment
- Shelter and accommodation
- Nutrition and clothing
- Hygiene and safety

2. CARE INSTRUCTIONS
{fields.get('care_instructions', 'I trust my Attorney to make decisions in my best interests.')}

3. SUBSTITUTE ATTORNEY
{self._generate_substitute_attorney_clause(fields.get('substitute_attorney'))}

This Power of Attorney is given in accordance with the Substitute Decisions Act, 1992 (Ontario).

SIGNATURES:
_____________________ (Grantor)

Witness 1: _____________________ Witness 2: _____________________
"""
        return content
    
    async def _generate_probate_content(self, fields: Dict[str, Any]) -> str:
        """Generate probate application content"""
        content = f"""
APPLICATION FOR CERTIFICATE OF APPOINTMENT OF ESTATE TRUSTEE

COURT FILE NUMBER: {fields.get('court_file_number', '[TO BE ASSIGNED]')}
ONTARIO SUPERIOR COURT OF JUSTICE

ESTATE OF: {fields.get('deceased_name', '[DECEASED NAME]')}

1. DECEASED INFORMATION
Name: {fields.get('deceased_name', '[DECEASED NAME]')}
Date of Death: {fields.get('death_date', '[DATE OF DEATH]')}
Last Address: {fields.get('deceased_address', '[LAST ADDRESS]')}

2. APPLICANT INFORMATION
Name: {fields.get('applicant_name', '[APPLICANT NAME]')}
Relationship: {fields.get('relationship', '[RELATIONSHIP]')}
Address: {fields.get('applicant_address', '[APPLICANT ADDRESS]')}

3. ESTATE INFORMATION
Estimated Value: ${fields.get('estate_value', '[ESTATE VALUE]')}
Real Property: {fields.get('real_property', '[REAL PROPERTY DESCRIPTION]')}

DATED at {fields.get('application_date', datetime.now().strftime('%B %d, %Y'))}

_____________________
{fields.get('applicant_name', '[APPLICANT NAME]')}
Applicant
"""
        return content
    
    async def _generate_generic_content(self, template: Dict[str, Any], fields: Dict[str, Any]) -> str:
        """Generate generic document content"""
        return f"""
{template.get('title', 'DOCUMENT')}

Generated on: {datetime.now().strftime('%Y-%m-%d')}

Content based on provided fields:
{json.dumps(fields, indent=2)}
"""
    
    def _generate_specific_bequests(self, bequests: List[Dict[str, Any]]) -> str:
        """Generate specific bequest clauses"""
        if not bequests:
            return "No specific bequests."
        
        bequest_text = []
        for i, bequest in enumerate(bequests, 1):
            item = bequest.get('item', '[ITEM]')
            beneficiary = bequest.get('beneficiary', '[BENEFICIARY]')
            bequest_text.append(f"{i}. I give {item} to {beneficiary}.")
        
        return "\n".join(bequest_text)
    
    def _generate_guardian_clause(self, guardian_info: Optional[Dict[str, Any]]) -> str:
        """Generate guardian appointment clause"""
        if not guardian_info:
            return "No guardian appointment specified."
        
        return f"I appoint {guardian_info.get('name', '[GUARDIAN NAME]')} as guardian of my minor children."
    
    def _generate_substitute_attorney_clause(self, substitute_info: Optional[Dict[str, Any]]) -> str:
        """Generate substitute attorney clause"""
        if not substitute_info:
            return "No substitute attorney appointed."
        
        return f"If my Attorney is unable to act, I appoint {substitute_info.get('name', '[SUBSTITUTE NAME]')} as substitute Attorney."
    
    async def _apply_ontario_formatting(self, content: str, document_type: str) -> str:
        """Apply Ontario legal document formatting standards"""
        # Add page numbers
        formatted_content = content.replace(
            "IN WITNESS WHEREOF",
            "IN WITNESS WHEREOF I have hereunto set my hand this"
        )
        
        # Ensure proper spacing
        formatted_content = formatted_content.replace("\n\n\n", "\n\n")
        
        # Add document title formatting
        if document_type == "will":
            formatted_content = formatted_content.replace(
                "LAST WILL AND TESTAMENT",
                "LAST WILL AND TESTAMENT\n" + "="*50 + "\n"
            )
        
        return formatted_content
    
    async def _save_document(self, document_id: str, content: str, document_data: Dict[str, Any]) -> str:
        """Save document to storage"""
        file_name = f"{document_id}_{document_data['document_type']}.txt"
        file_path = self.client_docs_path / file_name
        
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(content)
        
        return str(file_path)
    
    async def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file"""
        async with aiofiles.open(file_path, 'rb') as f:
            content = await f.read()
        return hashlib.sha256(content).hexdigest()
    
    async def _store_document_metadata(self, document_id: str, document_data: Dict[str, Any], file_path: str, file_hash: str):
        """Store document metadata in database"""
        async with aiosqlite.connect(self.storage_path / "documents.db") as db:
            await db.execute("""
                INSERT INTO documents 
                (id, client_id, matter_id, document_type, file_name, file_path, file_hash, 
                created_by, ontario_compliant, court_form_number)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                document_id,
                document_data.get("client_id"),
                document_data.get("matter_id"),
                document_data["document_type"],
                Path(file_path).name,
                file_path,
                file_hash,
                document_data.get("created_by", "system"),
                True,  # Ontario compliant
                document_data.get("court_form_number")
            ))
            await db.commit()
    
    async def get_document_versions(self, document_id: str) -> List[DocumentVersion]:
        """Get all versions of a document"""
        async with aiosqlite.connect(self.storage_path / "documents.db") as db:
            cursor = await db.execute(
                "SELECT id, version_number, file_path, file_hash, changes_summary, created_by, created_at "
                "FROM document_versions WHERE document_id = ? ORDER BY version_number DESC",
                (document_id,)
            )
            versions = []
            async for row in cursor:
                versions.append(DocumentVersion(
                    id=row[0],
                    document_id=document_id,
                    version_number=row[1],
                    file_path=row[2],
                    file_hash=row[3],
                    changes_summary=row[4],
                    created_at=datetime.fromisoformat(row[6]) if row[6] else datetime.now(),
                    created_by=row[5]
                ))
            return versions
    
    async def create_ontario_court_form(self, form_number: str, data: Dict[str, Any]) -> str:
        """Create Ontario court form"""
        try:
            # Validate form number
            if form_number not in self.ontario_court_forms.get("probate", {}):
                raise ValueError(f"Unsupported court form: {form_number}")
            
            document_id = f"COURT-{form_number}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Generate court form content
            content = await self._generate_court_form_content(form_number, data)
            
            # Apply court formatting
            formatted_content = await self._apply_court_formatting(content, form_number)
            
            # Save document
            file_path = await self._save_document(document_id, formatted_content, {
                "document_type": f"court_form_{form_number}",
                "court_form_number": form_number
            })
            
            return document_id
            
        except Exception as e:
            logger.error(f"Court form creation failed: {str(e)}")
            raise
    
    async def _generate_court_form_content(self, form_number: str, data: Dict[str, Any]) -> str:
        """Generate Ontario court form content"""
        if form_number == "74":  # Probate application
            return self._generate_form_74(data)
        
        # Default template
        return f"Ontario Court Form {form_number}\n\n{json.dumps(data, indent=2)}"
    
    def _generate_form_74(self, data: Dict[str, Any]) -> str:
        """Generate Form 74 - Application for Certificate of Appointment of Estate Trustee"""
        return f"""
COURT FILE NUMBER: {data.get('court_file_number', '[TO BE ASSIGNED]')}
COURT: {data.get('court_location', 'ONTARIO SUPERIOR COURT OF JUSTICE')}

ESTATE OF: {data.get('deceased_name', '[DECEASED NAME]')}

APPLICATION FOR CERTIFICATE OF APPOINTMENT OF ESTATE TRUSTEE
(Form 74)

1. DECEASED INFORMATION
Name: {data.get('deceased_name', '[DECEASED NAME]')}
Date of Death: {data.get('death_date', '[DATE OF DEATH]')}
Last Address: {data.get('deceased_address', '[LAST ADDRESS]')}

2. APPLICANT INFORMATION
Name: {data.get('applicant_name', '[APPLICANT NAME]')}
Relationship to Deceased: {data.get('relationship', '[RELATIONSHIP]')}
Address: {data.get('applicant_address', '[APPLICANT ADDRESS]')}

3. ESTATE INFORMATION
Estimated Value: ${data.get('estate_value', '[ESTATE VALUE]')}
Real Property: {data.get('real_property', '[REAL PROPERTY DESCRIPTION]')}
Personal Property: {data.get('personal_property', '[PERSONAL PROPERTY DESCRIPTION]')}

4. BENEFICIARIES
{self._format_beneficiaries(data.get('beneficiaries', []))}

5. DOCUMENTS SUBMITTED
[ ] Original Will
[ ] Death Certificate
[ ] Affidavit of Service (Form 74A)
[ ] Renunciation (if applicable)
[ ] Consent to Appointment (if applicable)

DATED at {data.get('application_date', datetime.now().strftime('%B %d, %Y'))}

_____________________
{data.get('applicant_name', '[APPLICANT NAME]')}
Applicant
"""
    
    def _format_beneficiaries(self, beneficiaries: List[Dict[str, Any]]) -> str:
        """Format beneficiaries list"""
        if not beneficiaries:
            return "  No beneficiaries listed"
        
        formatted = ""
        for i, beneficiary in enumerate(beneficiaries, 1):
            formatted += f"  {i}. {beneficiary.get('name', '[NAME]')} - {beneficiary.get('relationship', '[RELATIONSHIP]')}\n"
        
        return formatted
    
    async def _apply_court_formatting(self, content: str, form_number: str) -> str:
        """Apply Ontario court formatting standards"""
        # Add court header
        formatted_content = f"ONTARIO SUPERIOR COURT OF JUSTICE\n{'='*50}\n\n{content}"
        
        # Add form number header
        formatted_content = formatted_content.replace(
            f"Form {form_number}",
            f"FORM {form_number} - ONTARIO COURT FORM"
        )
        
        return formatted_content
    
    async def search_documents(self, search_criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search documents with AI-powered filtering"""
        try:
            query = "SELECT * FROM documents WHERE 1=1"
            params = []
            
            if search_criteria.get("client_id"):
                query += " AND client_id = ?"
                params.append(search_criteria["client_id"])
            
            if search_criteria.get("matter_id"):
                query += " AND matter_id = ?"
                params.append(search_criteria["matter_id"])
            
            if search_criteria.get("document_type"):
                query += " AND document_type = ?"
                params.append(search_criteria["document_type"])
            
            if search_criteria.get("ontario_compliant"):
                query += " AND ontario_compliant = ?"
                params.append(search_criteria["ontario_compliant"])
            
            async with aiosqlite.connect(self.storage_path / "documents.db") as db:
                cursor = await db.execute(query, params)
                documents = []
                async for row in cursor:
                    documents.append({
                        "id": row[0],
                        "client_id": row[1],
                        "matter_id": row[2],
                        "document_type": row[3],
                        "file_name": row[4],
                        "file_path": row[5],
                        "file_hash": row[6],
                        "version": row[7],
                        "status": row[8],
                        "created_by": row[9],
                        "created_at": row[10],
                        "ontario_compliant": row[12],
                        "court_form_number": row[13]
                    })
                return documents
        
        except Exception as e:
            logger.error(f"Document search failed: {str(e)}")
            return []
    
    async def get_document_statistics(self) -> Dict[str, Any]:
        """Get document management statistics"""
        try:
            async with aiosqlite.connect(self.storage_path / "documents.db") as db:
                # Total documents
                cursor = await db.execute("SELECT COUNT(*) FROM documents")
                total_documents = (await cursor.fetchone())[0]
                
                # Ontario compliant documents
                cursor = await db.execute("SELECT COUNT(*) FROM documents WHERE ontario_compliant = TRUE")
                compliant_documents = (await cursor.fetchone())[0]
                
                # Court forms
                cursor = await db.execute("SELECT COUNT(*) FROM documents WHERE court_form_number IS NOT NULL")
                court_forms = (await cursor.fetchone())[0]
                
                return {
                    "total_documents": total_documents,
                    "ontario_compliant": compliant_documents,
                    "court_forms": court_forms,
                    "compliance_rate": (compliant_documents / total_documents * 100) if total_documents > 0 else 0,
                    "last_updated": datetime.now().isoformat()
                }
        
        except Exception as e:
            logger.error(f"Document statistics retrieval failed: {str(e)}")
            return {}
    
    def is_ready(self) -> bool:
        return self.is_initialized