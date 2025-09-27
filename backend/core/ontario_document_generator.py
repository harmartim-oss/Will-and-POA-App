# backend/core/ontario_document_generator.py
"""
Ontario Legal Document Generator with AI Enhancement
Generates legal documents with AI recommendations and validation
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class OntarioLegalDocumentGenerator:
    """Enhanced document generator for Ontario legal documents"""
    
    def __init__(self):
        self.document_templates = {}
        self.ai_recommendations_cache = {}
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize document generator"""
        try:
            logger.info("Initializing Ontario Legal Document Generator...")
            
            # Load document templates
            await self._load_document_templates()
            
            # Initialize AI enhancement capabilities
            await self._initialize_ai_enhancements()
            
            self.is_initialized = True
            logger.info("✓ Ontario Legal Document Generator initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Document Generator: {str(e)}")
            raise
    
    async def _load_document_templates(self):
        """Load Ontario legal document templates"""
        self.document_templates = {
            "will": {
                "template_id": "ontario_will_v2024",
                "title": "Last Will and Testament (Ontario)",
                "sections": {
                    "identification": {
                        "required": True,
                        "template": "I, {full_name}, of {address}, in the Province of Ontario, being of sound mind and memory, do hereby make, publish and declare this to be my Last Will and Testament."
                    },
                    "revocation": {
                        "required": True,
                        "template": "I hereby revoke all former Wills and testamentary dispositions by me at any time heretofore made."
                    },
                    "executor_appointment": {
                        "required": True,
                        "template": "I appoint {executor_name} of {executor_address} to be the Executor of this my Will."
                    },
                    "guardian_appointment": {
                        "required": False,
                        "template": "I appoint {guardian_name} to be the Guardian of my infant children."
                    },
                    "specific_bequests": {
                        "required": False,
                        "template": "I give, devise and bequeath the following specific gifts:"
                    },
                    "residuary_clause": {
                        "required": True,
                        "template": "I give, devise and bequeath all the rest, residue and remainder of my estate to {residuary_beneficiary}."
                    },
                    "execution": {
                        "required": True,
                        "template": "IN WITNESS WHEREOF I have hereunto set my hand this {day} day of {month}, {year}."
                    }
                },
                "witness_requirements": {
                    "minimum_witnesses": 2,
                    "witness_template": "SIGNED by the said Testator as and for their last Will and Testament in the presence of us both present at the same time who at their request in their presence and in the presence of each other have subscribed our names as witnesses."
                }
            },
            "poa_property": {
                "template_id": "ontario_poa_property_v2024",
                "title": "Continuing Power of Attorney for Property (Ontario)",
                "sections": {
                    "identification": {
                        "required": True,
                        "template": "I, {grantor_name}, of {grantor_address}, in the Province of Ontario, being mentally capable and at least eighteen years of age, APPOINT {attorney_name} of {attorney_address} to be my attorney for property."
                    },
                    "powers_granted": {
                        "required": True,
                        "template": "I GRANT to my attorney the power to do on my behalf anything in respect of property that I could do if capable of managing property, except make a will, subject to the law and to any conditions or restrictions contained in this document."
                    },
                    "continuing_authority": {
                        "required": True,
                        "template": "This power of attorney shall continue to be effective if I become mentally incapable."
                    },
                    "compensation": {
                        "required": False,
                        "template": "My attorney is entitled to reasonable compensation for services as my attorney."
                    },
                    "execution": {
                        "required": True,
                        "template": "DATED this {day} day of {month}, {year}."
                    }
                }
            },
            "poa_personal_care": {
                "template_id": "ontario_poa_personal_care_v2024",
                "title": "Power of Attorney for Personal Care (Ontario)",
                "sections": {
                    "identification": {
                        "required": True,
                        "template": "I, {grantor_name}, of {grantor_address}, in the Province of Ontario, being mentally capable and at least sixteen years of age, APPOINT {attorney_name} of {attorney_address} to be my attorney for personal care."
                    },
                    "authority_granted": {
                        "required": True,
                        "template": "I GRANT to my attorney the authority to make any personal care decision for me that I am mentally incapable of making for myself."
                    },
                    "healthcare_wishes": {
                        "required": False,
                        "template": "My wishes with respect to personal care are as follows:"
                    },
                    "treatment_instructions": {
                        "required": False,
                        "template": "My instructions with respect to treatment are:"
                    },
                    "execution": {
                        "required": True,
                        "template": "DATED this {day} day of {month}, {year}."
                    }
                }
            }
        }
        
        logger.info("✓ Document templates loaded")
    
    async def _initialize_ai_enhancements(self):
        """Initialize AI enhancement capabilities"""
        # Initialize AI recommendation system
        self.ai_recommendations_cache = {}
        logger.info("✓ AI enhancement capabilities initialized")
    
    async def generate_legal_documents(self, document_type: str, user_data: Dict[str, Any], 
                                     ai_recommendations: List[str] = None, 
                                     template_id: str = None) -> Dict[str, Any]:
        """Generate legal documents with AI assistance"""
        try:
            if document_type not in self.document_templates:
                raise ValueError(f"Unsupported document type: {document_type}")
            
            template = self.document_templates[document_type]
            
            # Generate document content
            document_content = await self._generate_document_content(template, user_data)
            
            # Apply AI recommendations if provided
            if ai_recommendations:
                document_content = await self._apply_ai_recommendations(
                    document_content, ai_recommendations, document_type
                )
            
            # Generate multiple formats
            documents = {
                "text_content": document_content,
                "pdf_content": await self._generate_pdf(document_content, template["title"]),
                "docx_content": await self._generate_docx(document_content, template["title"]),
                "metadata": {
                    "document_type": document_type,
                    "template_id": template.get("template_id", "unknown"),
                    "generated_at": datetime.now().isoformat(),
                    "user_data_hash": self._hash_user_data(user_data),
                    "ai_enhanced": bool(ai_recommendations)
                }
            }
            
            return documents
            
        except Exception as e:
            logger.error(f"Document generation failed: {str(e)}")
            raise
    
    async def _generate_document_content(self, template: Dict[str, Any], user_data: Dict[str, Any]) -> str:
        """Generate document content from template and user data"""
        content_parts = []
        
        # Add document title
        content_parts.append(f"{template['title']}\n")
        content_parts.append("=" * len(template['title']) + "\n\n")
        
        # Process each section
        for section_name, section_data in template["sections"].items():
            if section_data["required"] or self._should_include_section(section_name, user_data):
                section_content = await self._populate_section(section_data["template"], user_data)
                if section_content:
                    content_parts.append(f"{section_content}\n\n")
        
        # Add witness section for wills
        if template.get("witness_requirements"):
            witness_section = await self._generate_witness_section(template["witness_requirements"])
            content_parts.append(witness_section)
        
        return "".join(content_parts)
    
    async def _populate_section(self, template: str, user_data: Dict[str, Any]) -> str:
        """Populate section template with user data"""
        try:
            # Simple template substitution - in production would use more sophisticated templating
            populated = template
            
            # Replace common placeholders
            replacements = {
                "{full_name}": user_data.get("full_name", "[NAME TO BE INSERTED]"),
                "{address}": user_data.get("address", "[ADDRESS TO BE INSERTED]"),
                "{executor_name}": user_data.get("executor_name", "[EXECUTOR NAME TO BE INSERTED]"),
                "{executor_address}": user_data.get("executor_address", "[EXECUTOR ADDRESS TO BE INSERTED]"),
                "{guardian_name}": user_data.get("guardian_name", "[GUARDIAN NAME TO BE INSERTED]"),
                "{residuary_beneficiary}": user_data.get("residuary_beneficiary", "[BENEFICIARY TO BE INSERTED]"),
                "{grantor_name}": user_data.get("grantor_name", "[GRANTOR NAME TO BE INSERTED]"),
                "{grantor_address}": user_data.get("grantor_address", "[GRANTOR ADDRESS TO BE INSERTED]"),
                "{attorney_name}": user_data.get("attorney_name", "[ATTORNEY NAME TO BE INSERTED]"),
                "{attorney_address}": user_data.get("attorney_address", "[ATTORNEY ADDRESS TO BE INSERTED]"),
                "{day}": str(datetime.now().day),
                "{month}": datetime.now().strftime("%B"),
                "{year}": str(datetime.now().year)
            }
            
            for placeholder, value in replacements.items():
                populated = populated.replace(placeholder, value)
            
            return populated
            
        except Exception as e:
            logger.error(f"Section population failed: {str(e)}")
            return template
    
    async def _apply_ai_recommendations(self, content: str, recommendations: List[str], 
                                      document_type: str) -> str:
        """Apply AI recommendations to document content"""
        try:
            # Add AI recommendations as comments or suggestions
            ai_section = "\n\n--- AI RECOMMENDATIONS ---\n"
            for i, recommendation in enumerate(recommendations, 1):
                ai_section += f"{i}. {recommendation}\n"
            
            # For now, append recommendations as comments
            # In production, would integrate recommendations into the document
            enhanced_content = content + ai_section
            
            return enhanced_content
            
        except Exception as e:
            logger.error(f"Failed to apply AI recommendations: {str(e)}")
            return content
    
    async def _generate_pdf(self, content: str, title: str) -> str:
        """Generate PDF version of document"""
        try:
            # Placeholder for PDF generation
            # In production, would use ReportLab or similar
            pdf_content = f"PDF Version of {title}\n\n{content}"
            return pdf_content
            
        except Exception as e:
            logger.error(f"PDF generation failed: {str(e)}")
            return f"PDF generation failed: {str(e)}"
    
    async def _generate_docx(self, content: str, title: str) -> str:
        """Generate DOCX version of document"""
        try:
            # Placeholder for DOCX generation
            # In production, would use python-docx
            docx_content = f"DOCX Version of {title}\n\n{content}"
            return docx_content
            
        except Exception as e:
            logger.error(f"DOCX generation failed: {str(e)}")
            return f"DOCX generation failed: {str(e)}"
    
    async def _generate_witness_section(self, witness_requirements: Dict[str, Any]) -> str:
        """Generate witness section for documents"""
        witness_section = "\n\nWITNESS SECTION\n"
        witness_section += f"{witness_requirements['witness_template']}\n\n"
        
        for i in range(witness_requirements["minimum_witnesses"]):
            witness_section += f"Witness {i+1}:\n"
            witness_section += "Signature: _________________________\n"
            witness_section += "Print Name: _______________________\n"
            witness_section += "Address: __________________________\n"
            witness_section += "Date: _____________________________\n\n"
        
        return witness_section
    
    def _should_include_section(self, section_name: str, user_data: Dict[str, Any]) -> bool:
        """Determine if optional section should be included"""
        # Logic to determine section inclusion based on user data
        section_indicators = {
            "guardian_appointment": "has_minor_children",
            "specific_bequests": "has_specific_gifts",
            "compensation": "attorney_compensation",
            "healthcare_wishes": "has_healthcare_preferences",
            "treatment_instructions": "has_treatment_preferences"
        }
        
        indicator = section_indicators.get(section_name)
        return user_data.get(indicator, False) if indicator else False
    
    def _hash_user_data(self, user_data: Dict[str, Any]) -> str:
        """Generate hash of user data for tracking"""
        import hashlib
        data_string = json.dumps(user_data, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()[:16]
    
    async def validate_document_data(self, document_type: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user data for document generation"""
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": []
        }
        
        try:
            # Basic validation rules
            required_fields = {
                "will": ["full_name", "address", "executor_name"],
                "poa_property": ["grantor_name", "grantor_address", "attorney_name", "attorney_address"],
                "poa_personal_care": ["grantor_name", "grantor_address", "attorney_name", "attorney_address"]
            }
            
            if document_type in required_fields:
                for field in required_fields[document_type]:
                    if not user_data.get(field):
                        validation_result["errors"].append(f"Missing required field: {field}")
                        validation_result["is_valid"] = False
            
            # Additional validation rules
            if document_type == "will":
                if user_data.get("has_minor_children") and not user_data.get("guardian_name"):
                    validation_result["warnings"].append("Consider appointing a guardian for minor children")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Document validation failed: {str(e)}")
            return {
                "is_valid": False,
                "errors": [f"Validation error: {str(e)}"],
                "warnings": []
            }
    
    def is_ready(self) -> bool:
        """Check if document generator is ready"""
        return self.is_initialized