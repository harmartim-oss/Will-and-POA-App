"""
Ontario Legal Knowledge Base
Comprehensive knowledge base for Ontario estate and POA law compliance
"""

import json
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class LegalRequirement:
    """Represents a specific legal requirement"""
    id: str
    title: str
    description: str
    statute: str
    section: str
    mandatory: bool
    conditions: List[str]
    exceptions: List[str]

@dataclass
class CaseLaw:
    """Represents relevant case law"""
    case_name: str
    citation: str
    year: int
    court: str
    summary: str
    key_principles: List[str]
    relevance_score: float

class OntarioLegalKnowledgeBase:
    """
    Comprehensive Ontario legal knowledge base for estate planning and POA documents
    """
    
    def __init__(self):
        self.wills_act_requirements = self._load_wills_act_requirements()
        self.substitute_decisions_act = self._load_substitute_decisions_act()
        self.estates_act_requirements = self._load_estates_act_requirements()
        self.slra_requirements = self._load_slra_requirements()
        self.case_law_database = self._load_case_law_database()
        self.legal_templates = self._load_legal_templates()
        self.best_practices = self._load_best_practices()
        
    def _load_wills_act_requirements(self) -> Dict[str, LegalRequirement]:
        """Load Wills Act requirements"""
        return {
            "testator_capacity": LegalRequirement(
                id="wills_act_s3",
                title="Testamentary Capacity",
                description="The testator must be of sound mind and at least 18 years old",
                statute="Succession Law Reform Act",
                section="Section 1, 3",
                mandatory=True,
                conditions=[
                    "Must be 18 years or older at time of making will",
                    "Must understand nature and effect of making a will",
                    "Must understand extent of property being disposed of",
                    "Must understand claims of those who would normally expect to benefit"
                ],
                exceptions=["Military service exception for minors", "Married minors"]
            ),
            "will_execution": LegalRequirement(
                id="wills_act_s4",
                title="Proper Execution",
                description="Will must be properly signed and witnessed",
                statute="Succession Law Reform Act",
                section="Section 4",
                mandatory=True,
                conditions=[
                    "Will must be in writing",
                    "Signed by testator or by another in testator's presence",
                    "Signature must be at end of will",
                    "Two witnesses must sign in presence of testator",
                    "Witnesses must be competent (18+ and mentally capable)"
                ],
                exceptions=["Holograph wills (entirely handwritten and signed)"]
            ),
            "witness_requirements": LegalRequirement(
                id="wills_act_s12",
                title="Witness Competency",
                description="Witnesses must be competent and not beneficiaries",
                statute="Succession Law Reform Act",
                section="Section 12",
                mandatory=True,
                conditions=[
                    "Witnesses must be 18 years or older",
                    "Witnesses must be mentally competent",
                    "Witnesses cannot be beneficiaries or spouses of beneficiaries",
                    "Both witnesses must sign in presence of testator"
                ],
                exceptions=["Supernumerary witness rule if more than 2 witnesses"]
            ),
            "revocation_requirements": LegalRequirement(
                id="wills_act_s15",
                title="Revocation of Previous Wills",
                description="New will should explicitly revoke previous wills",
                statute="Succession Law Reform Act",
                section="Section 15",
                mandatory=False,
                conditions=[
                    "Express revocation clause recommended",
                    "Physical destruction revokes will",
                    "Marriage generally revokes will (with exceptions)"
                ],
                exceptions=["Wills made in contemplation of marriage"]
            )
        }
    
    def _load_substitute_decisions_act(self) -> Dict[str, LegalRequirement]:
        """Load Substitute Decisions Act requirements for POA"""
        return {
            "grantor_capacity": LegalRequirement(
                id="sda_s8",
                title="Grantor Mental Capacity",
                description="Grantor must be mentally capable when making POA",
                statute="Substitute Decisions Act",
                section="Section 8",
                mandatory=True,
                conditions=[
                    "Must be 18 years or older",
                    "Must understand what POA document means",
                    "Must understand what property/care decisions attorney will make",
                    "Must understand attorney can make decisions without consulting grantor"
                ],
                exceptions=[]
            ),
            "poa_execution": LegalRequirement(
                id="sda_s10",
                title="POA Execution Requirements",
                description="POA must be properly executed with witnesses",
                statute="Substitute Decisions Act",
                section="Section 10",
                mandatory=True,
                conditions=[
                    "Must be in writing and signed by grantor",
                    "Must be signed by two witnesses",
                    "Witnesses must sign in presence of grantor",
                    "Witnesses cannot be attorney or attorney's spouse/partner"
                ],
                exceptions=["POA made outside Ontario may have different requirements"]
            ),
            "attorney_duties": LegalRequirement(
                id="sda_s32",
                title="Attorney Fiduciary Duties",
                description="Attorney must act in grantor's best interests",
                statute="Substitute Decisions Act",
                section="Section 32",
                mandatory=True,
                conditions=[
                    "Must act honestly and in good faith",
                    "Must act in grantor's best interests",
                    "Must avoid conflicts of interest",
                    "Must keep accurate records"
                ],
                exceptions=[]
            )
        }
    
    def _load_estates_act_requirements(self) -> Dict[str, LegalRequirement]:
        """Load Estates Act requirements"""
        return {
            "executor_duties": LegalRequirement(
                id="estates_act_s2",
                title="Executor Appointment and Duties",
                description="Executor responsibilities and appointment requirements",
                statute="Estates Act",
                section="Section 2",
                mandatory=True,
                conditions=[
                    "Executor must be competent adult",
                    "Must obtain probate if required",
                    "Must administer estate according to will",
                    "Must file estate information return"
                ],
                exceptions=["Small estates may not require probate"]
            )
        }
    
    def _load_slra_requirements(self) -> Dict[str, LegalRequirement]:
        """Load Succession Law Reform Act additional requirements"""
        return {
            "family_provision": LegalRequirement(
                id="slra_s58",
                title="Family Support Claims",
                description="Dependants may claim support from estate",
                statute="Succession Law Reform Act",
                section="Section 58",
                mandatory=False,
                conditions=[
                    "Spouse and children may claim if inadequately provided for",
                    "Court may order provision from estate",
                    "Claims must be made within 6 months"
                ],
                exceptions=[]
            )
        }
    
    def _load_case_law_database(self) -> List[CaseLaw]:
        """Load relevant Ontario case law"""
        return [
            CaseLaw(
                case_name="Banks v. Goodfellow",
                citation="(1870) L.R. 5 Q.B. 549",
                year=1870,
                court="Court of Queen's Bench",
                summary="Established the test for testamentary capacity",
                key_principles=[
                    "Testator must understand nature and effect of making a will",
                    "Must understand extent of property being disposed of",
                    "Must understand claims of those who would normally expect to benefit",
                    "Must not be affected by disorder of mind that would poison judgments"
                ],
                relevance_score=0.95
            ),
            CaseLaw(
                case_name="Vout v. Hay",
                citation="[1995] 2 S.C.R. 876",
                year=1995,
                court="Supreme Court of Canada",
                summary="Modern approach to suspicious circumstances in will challenges",
                key_principles=[
                    "Suspicious circumstances shift burden to propounder",
                    "Court must be satisfied will represents true intentions",
                    "Independent legal advice is important factor"
                ],
                relevance_score=0.90
            ),
            CaseLaw(
                case_name="Calvert v. Calvert",
                citation="(1997) 32 O.R. (3d) 281 (C.A.)",
                year=1997,
                court="Ontario Court of Appeal",
                summary="POA interpretation and attorney duties",
                key_principles=[
                    "Attorney must act in grantor's best interests",
                    "Courts will scrutinize attorney's actions",
                    "Financial records must be maintained"
                ],
                relevance_score=0.85
            )
        ]
    
    def _load_legal_templates(self) -> Dict[str, str]:
        """Load Ontario-specific legal templates and clauses"""
        return {
            "will_opening": """
LAST WILL AND TESTAMENT

I, {full_name}, of {address}, in the Province of Ontario, being of sound mind and memory and not acting under duress, menace, fraud or undue influence of any person whomsoever, do make, publish and declare this to be my Last Will and Testament, hereby revoking all former Wills and Codicils by me at any time heretofore made.
            """.strip(),
            
            "executor_clause": """
APPOINTMENT OF EXECUTOR

I appoint {executor_name} of {executor_address} to be the Executor of this my Will. If {executor_name} is unable or unwilling to act as Executor, I appoint {alternate_executor} of {alternate_address} to be the Executor of this my Will.
            """.strip(),
            
            "guardian_clause": """
APPOINTMENT OF GUARDIAN

If at the time of my death any child of mine is a minor, I appoint {guardian_name} of {guardian_address} to be the Guardian of the person and property of such child. If {guardian_name} is unable or unwilling to act, I appoint {alternate_guardian} to be such Guardian.
            """.strip(),
            
            "poa_property_opening": """
CONTINUING POWER OF ATTORNEY FOR PROPERTY

I, {grantor_name}, of {grantor_address}, in the Province of Ontario, being mentally capable with respect to property, appoint {attorney_name} of {attorney_address} to be my Attorney for Property in accordance with the Substitute Decisions Act, 1992.
            """.strip(),
            
            "poa_care_opening": """
POWER OF ATTORNEY FOR PERSONAL CARE

I, {grantor_name}, of {grantor_address}, in the Province of Ontario, being mentally capable with respect to personal care, appoint {attorney_name} of {attorney_address} to be my Attorney for Personal Care in accordance with the Substitute Decisions Act, 1992.
            """.strip()
        }
    
    def get_requirements_for_document_type(self, document_type: str) -> List[LegalRequirement]:
        """Get all legal requirements for a specific document type"""
        requirements = []
        
        if document_type == "will":
            requirements.extend(self.wills_act_requirements.values())
            requirements.extend(self.estates_act_requirements.values())
            requirements.extend(self.slra_requirements.values())
        elif document_type in ["poa_property", "poa_care"]:
            requirements.extend(self.substitute_decisions_act.values())
            
        return requirements
    
    def validate_compliance(self, document_type: str, document_content: Dict[str, Any]) -> Dict[str, Any]:
        """Validate document compliance against Ontario law"""
        requirements = self.get_requirements_for_document_type(document_type)
        compliance_results = {
            "is_compliant": True,
            "violations": [],
            "warnings": [],
            "recommendations": []
        }
        
        for req in requirements:
            if req.mandatory:
                violation = self._check_requirement_compliance(req, document_content)
                if violation:
                    compliance_results["violations"].append(violation)
                    compliance_results["is_compliant"] = False
        
        return compliance_results
    
    def _check_requirement_compliance(self, requirement: LegalRequirement, content: Dict[str, Any]) -> Optional[str]:
        """Check if specific requirement is met"""
        # Implementation would check specific requirements against document content
        # This is a simplified version - full implementation would have detailed checks
        
        if requirement.id == "wills_act_s3" and "personal_info" in content:
            age = content.get("personal_info", {}).get("age")
            if age and int(age) < 18:
                return f"Testator must be 18 or older (current age: {age})"
        
        if requirement.id == "wills_act_s4":
            if not content.get("execution", {}).get("witness_count", 0) >= 2:
                return "Will must have at least 2 witnesses"
        
        return None
    
    def get_relevant_case_law(self, legal_issue: str, document_type: str) -> List[CaseLaw]:
        """Get relevant case law for specific legal issues"""
        relevant_cases = []
        
        # Simple keyword matching - in production would use NLP similarity
        issue_lower = legal_issue.lower()
        
        for case in self.case_law_database:
            relevance = 0.0
            
            # Check summary and principles for relevance
            if any(keyword in case.summary.lower() for keyword in issue_lower.split()):
                relevance += 0.3
            
            if any(keyword in " ".join(case.key_principles).lower() for keyword in issue_lower.split()):
                relevance += 0.4
            
            # Document type specific relevance
            if document_type == "will" and any(word in case.summary.lower() for word in ["will", "testament", "testator"]):
                relevance += 0.2
            elif document_type in ["poa_property", "poa_care"] and any(word in case.summary.lower() for word in ["power of attorney", "attorney", "substitute"]):
                relevance += 0.2
            
            if relevance > 0.3:
                case.relevance_score = relevance
                relevant_cases.append(case)
        
        return sorted(relevant_cases, key=lambda x: x.relevance_score, reverse=True)
    
    def get_template(self, template_name: str, **kwargs) -> str:
        """Get formatted legal template"""
        template = self.legal_templates.get(template_name, "")
        
        try:
            return template.format(**kwargs)
        except KeyError as e:
            return f"Template error: Missing parameter {e}"
    
    def analyze_document_structure(self, document_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze document structure for completeness"""
        analysis = {
            "completeness_score": 0.0,
            "missing_sections": [],
            "recommendations": [],
            "structure_issues": []
        }
        
        required_sections = self._get_required_sections(document_type)
        present_sections = []
        
        for section in required_sections:
            if self._has_section_content(section, content):
                present_sections.append(section)
            else:
                analysis["missing_sections"].append(section)
        
        analysis["completeness_score"] = len(present_sections) / len(required_sections)
        
        if analysis["completeness_score"] < 1.0:
            analysis["recommendations"].append("Document is missing required sections")
        
        return analysis
    
    def _get_required_sections(self, document_type: str) -> List[str]:
        """Get required sections for document type"""
        if document_type == "will":
            return [
                "personal_info",
                "revocation_clause", 
                "executor_appointment",
                "beneficiaries",
                "residuary_clause",
                "execution_clause"
            ]
        elif document_type == "poa_property":
            return [
                "grantor_info",
                "attorney_appointment", 
                "powers_granted",
                "execution_clause"
            ]
        elif document_type == "poa_care":
            return [
                "grantor_info",
                "attorney_appointment",
                "care_instructions",
                "execution_clause"
            ]
        
        return []
    
    def _has_section_content(self, section: str, content: Dict[str, Any]) -> bool:
        """Check if document has content for required section"""
        # Simplified check - would be more sophisticated in production
        return section in content and content[section]
    
    def _load_best_practices(self) -> Dict[str, List[str]]:
        """Load Ontario legal best practices for wills and POAs"""
        return {
            "will_preparation": [
                "Have will prepared by qualified legal professional or use comprehensive guided tool",
                "Ensure testator has full testamentary capacity at time of execution",
                "Use two independent witnesses who are not beneficiaries or spouses of beneficiaries",
                "Clearly identify all beneficiaries with full legal names and relationships",
                "Include specific bequests before residuary clause to avoid ambiguity",
                "Always include revocation clause to cancel previous wills and codicils",
                "Name alternate executors in case primary executor cannot serve",
                "Specify how debts, taxes, and funeral expenses should be paid",
                "Store original will in safe location and inform executor of location",
                "Review and update will after major life events (marriage, divorce, births, deaths)",
                "Consider including guardianship provisions for minor children",
                "Address digital assets and online accounts in will provisions",
                "Include funeral and burial instructions if desired",
                "Ensure executor has capacity and willingness to serve",
                "Consider potential for will challenges and document capacity clearly"
            ],
            "will_execution": [
                "Testator must sign at end of will in presence of both witnesses",
                "Both witnesses must be present simultaneously when testator signs",
                "Witnesses must sign in presence of testator and each other",
                "All parties should initial each page of multi-page wills",
                "Use attestation clause confirming proper execution procedure",
                "Do not make any marks, alterations or additions after signing",
                "Consider video recording execution ceremony for complex estates",
                "Witnesses should understand their role and responsibilities",
                "Ensure testator acts freely without undue influence or coercion",
                "Maintain original signed will - do not staple or attach items to it"
            ],
            "poa_property": [
                "Clearly specify when power of attorney takes effect (continuing vs. non-continuing)",
                "Name trusted individual with financial competency as attorney",
                "Include detailed instructions on financial management preferences",
                "Specify any limitations or restrictions on attorney's powers",
                "Name alternate attorney in case primary attorney cannot serve",
                "Require attorney to keep detailed records of all transactions",
                "Consider requiring attorney to provide periodic accountings",
                "Store original POA in safe location and provide copy to attorney",
                "Review and update POA regularly as circumstances change",
                "Ensure attorney understands their fiduciary duties and obligations",
                "Consider having attorney acknowledge appointment in writing",
                "Specify whether multiple attorneys must act jointly or can act separately",
                "Include provisions for attorney compensation if desired",
                "Address potential conflicts of interest",
                "Revoke previous powers of attorney explicitly"
            ],
            "poa_personal_care": [
                "Clearly specify healthcare preferences and treatment wishes",
                "Name someone who knows your values and will respect your wishes",
                "Include specific instructions on end-of-life care preferences",
                "Address preferences for medical procedures, life support, and organ donation",
                "Specify living arrangements preferences (home care vs. facility)",
                "Include dietary, religious, and cultural preferences",
                "Name alternate attorney for personal care decisions",
                "Discuss your wishes with appointed attorney before execution",
                "Provide copy to healthcare providers and family members",
                "Review and update regularly, especially after health changes",
                "Ensure attorney understands scope and limitations of authority",
                "Specify any activities or decisions attorney should avoid",
                "Consider including advance care planning directives",
                "Address mental health treatment preferences if applicable"
            ],
            "document_storage": [
                "Keep original documents in fireproof and waterproof safe or safety deposit box",
                "Inform executor/attorney of document location and access information",
                "Provide copies (not originals) to relevant parties",
                "Consider registering POA with Office of Public Guardian and Trustee",
                "Maintain list of all estate planning documents and their locations",
                "Update storage location information when documents are moved",
                "Ensure executor has access to safety deposit box after death",
                "Keep digital copies in secure encrypted storage as backup",
                "Document all updates and amendments with dates",
                "Maintain communication with appointed representatives about document locations"
            ],
            "professional_review": [
                "Have documents reviewed by Ontario-licensed lawyer before execution",
                "Obtain independent legal advice for complex estates or family situations",
                "Consider capacity assessment for elderly or vulnerable testators",
                "Seek tax planning advice for estates over certain thresholds",
                "Get professional advice for business succession planning",
                "Consult with financial advisor on estate planning implications",
                "Review documents with accountant for tax efficiency",
                "Consider mediation if anticipating family disputes",
                "Obtain appraisals for significant assets (real estate, collections)",
                "Work with estate planner for comprehensive wealth transfer strategies"
            ],
            "family_communication": [
                "Discuss general estate plans with family members to avoid surprises",
                "Explain reasoning for decisions that may be questioned",
                "Avoid surprising beneficiaries at will reading if possible",
                "Address potential conflicts or concerns proactively",
                "Inform family members of executor and attorney appointments",
                "Share information about asset locations and important contacts",
                "Discuss funeral and burial preferences with family",
                "Consider family meeting with lawyer to discuss estate plan",
                "Document reasons for unusual or unequal distributions",
                "Keep family informed of major changes to estate plans"
            ],
            "ontario_specific": [
                "Understand Ontario's Succession Law Reform Act requirements",
                "Be aware of spouse's entitlement to elect under Part II of SLRA",
                "Consider dependants' claims under Dependants' Relief legislation",
                "Understand probate fees (Estate Administration Tax) in Ontario",
                "Be aware of common law spouse rights in Ontario",
                "Know that marriage generally revokes prior wills in Ontario",
                "Understand that divorce does not automatically revoke gifts to ex-spouse",
                "Be aware of Ontario Human Rights Code considerations in estate planning",
                "Understand Family Law Act equalization rights impact on estate",
                "Know Office of Public Guardian and Trustee oversight role for POAs",
                "Be aware of capacity assessment procedures under Substitute Decisions Act",
                "Understand mandatory reporting requirements for attorneys under SDA",
                "Know requirements for court-ordered passing of accounts in Ontario",
                "Be aware of charitable gifts registration requirements in Ontario"
            ]
        }
    
    def get_best_practices_for_document(self, document_type: str) -> List[str]:
        """Get relevant best practices for specific document type"""
        practices = []
        
        if document_type == "will":
            practices.extend(self.best_practices.get("will_preparation", []))
            practices.extend(self.best_practices.get("will_execution", []))
        elif document_type == "poa_property":
            practices.extend(self.best_practices.get("poa_property", []))
        elif document_type == "poa_care":
            practices.extend(self.best_practices.get("poa_personal_care", []))
        
        # Add common practices for all documents
        practices.extend(self.best_practices.get("document_storage", []))
        practices.extend(self.best_practices.get("professional_review", []))
        practices.extend(self.best_practices.get("ontario_specific", []))
        
        return practices
    
    def get_all_best_practices(self) -> Dict[str, List[str]]:
        """Get all best practices organized by category"""
        return self.best_practices