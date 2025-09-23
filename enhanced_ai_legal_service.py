"""
Enhanced AI Legal Analysis Service
Integrates Ontario legal knowledge with AI-powered document analysis
"""

import re
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import os

from ontario_legal_kb import OntarioLegalKnowledgeBase, LegalRequirement, CaseLaw

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LegalAnalysisResult:
    """Comprehensive legal analysis result"""
    document_type: str
    compliance_score: float
    legal_issues: List[str]
    recommendations: List[str]
    missing_requirements: List[str]
    risk_factors: List[str]
    case_law_references: List[str]
    improvement_suggestions: List[str]
    confidence_score: float

@dataclass
class AIEnhancement:
    """AI-powered enhancement suggestion"""
    section: str
    original_text: str
    suggested_text: str
    reason: str
    legal_basis: str
    confidence: float
    priority: str  # "high", "medium", "low"

class EnhancedAILegalService:
    """
    Enhanced AI service combining legal knowledge base with intelligent analysis
    """
    
    def __init__(self):
        self.legal_kb = OntarioLegalKnowledgeBase()
        self.legal_patterns = self._load_legal_patterns()
        self.ai_prompts = self._load_ai_prompts()
        
    def _load_legal_patterns(self) -> Dict[str, List[str]]:
        """Load regex patterns for legal text analysis"""
        return {
            "names": [
                r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Basic name pattern
                r'\b[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+\b'  # Name with middle initial
            ],
            "addresses": [
                r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)',
                r'[A-Za-z\s]+,\s*Ontario'
            ],
            "legal_terms": [
                r'\b(?:executor|executrix|trustee|beneficiary|testator|testatrix|grantor|attorney)\b',
                r'\b(?:will|testament|codicil|power of attorney|POA)\b',
                r'\b(?:revoke|revokes|hereby|witnesseth|whereas)\b'
            ],
            "monetary_amounts": [
                r'\$[\d,]+\.?\d*',
                r'\b\d+\s+dollars?\b'
            ],
            "dates": [
                r'\b\d{1,2}(?:st|nd|rd|th)?\s+day\s+of\s+\w+,?\s+\d{4}\b',
                r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
            ]
        }
    
    def _load_ai_prompts(self) -> Dict[str, str]:
        """Load AI prompt templates for legal analysis"""
        return {
            "compliance_analysis": """
            As an Ontario estate law expert, analyze this {document_type} document for legal compliance.
            
            Document content: {content}
            
            Consider:
            1. Ontario Succession Law Reform Act requirements
            2. Substitute Decisions Act (for POA documents)
            3. Proper execution requirements
            4. Witness requirements
            5. Mental capacity considerations
            
            Provide compliance analysis with specific legal citations.
            """,
            
            "risk_assessment": """
            Analyze this {document_type} for potential legal risks and challenges:
            
            Document: {content}
            
            Consider:
            1. Will contest risks
            2. Family Law Act claims
            3. Dependant support claims
            4. Tax implications
            5. Estate administration challenges
            
            Provide risk assessment with mitigation strategies.
            """,
            
            "language_improvement": """
            Improve the legal language in this {document_type} section:
            
            Section: {section}
            Current text: {text}
            
            Provide:
            1. Clearer legal language
            2. Better structure
            3. More precise terminology
            4. Enhanced legal enforceability
            
            Maintain legal accuracy while improving readability.
            """,
            
            "completeness_check": """
            Analyze this {document_type} for completeness and missing elements:
            
            Document: {content}
            
            Check for:
            1. Required legal clauses
            2. Missing beneficiary information
            3. Incomplete executor/attorney details
            4. Missing execution requirements
            5. Additional protective clauses
            
            Suggest specific additions and improvements.
            """
        }
    
    def analyze_document(self, document_type: str, content: Dict[str, Any]) -> LegalAnalysisResult:
        """Comprehensive legal analysis of document"""
        logger.info(f"Starting legal analysis for {document_type}")
        
        # Get legal requirements
        requirements = self.legal_kb.get_requirements_for_document_type(document_type)
        
        # Perform compliance check
        compliance_results = self.legal_kb.validate_compliance(document_type, content)
        
        # Analyze document structure
        structure_analysis = self.legal_kb.analyze_document_structure(document_type, content)
        
        # Extract legal issues
        legal_issues = self._extract_legal_issues(document_type, content)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(document_type, content, compliance_results)
        
        # Assess risks
        risk_factors = self._assess_risk_factors(document_type, content)
        
        # Get relevant case law
        case_law_refs = self._get_case_law_references(document_type, legal_issues)
        
        # Generate improvement suggestions
        improvements = self._generate_improvements(document_type, content)
        
        # Calculate confidence score
        confidence = self._calculate_confidence_score(content, structure_analysis)
        
        return LegalAnalysisResult(
            document_type=document_type,
            compliance_score=1.0 - len(compliance_results.get("violations", [])) * 0.2,
            legal_issues=legal_issues,
            recommendations=recommendations,
            missing_requirements=compliance_results.get("violations", []),
            risk_factors=risk_factors,
            case_law_references=case_law_refs,
            improvement_suggestions=improvements,
            confidence_score=confidence
        )
    
    def _extract_legal_issues(self, document_type: str, content: Dict[str, Any]) -> List[str]:
        """Extract potential legal issues from document"""
        issues = []
        
        if document_type == "will":
            # Check for common will issues
            if not content.get("executor"):
                issues.append("No executor appointed")
            
            if not content.get("beneficiaries"):
                issues.append("No beneficiaries specified")
            
            if content.get("personal_info", {}).get("marital_status") == "married":
                if not any("spouse" in str(b).lower() for b in content.get("beneficiaries", [])):
                    issues.append("Married testator should consider spouse provisions")
            
            if content.get("personal_info", {}).get("has_children", False):
                if not content.get("guardian"):
                    issues.append("Should appoint guardian for minor children")
        
        elif document_type in ["poa_property", "poa_care"]:
            # Check for POA issues
            if not content.get("attorney"):
                issues.append("No attorney appointed")
            
            if not content.get("alternate_attorney"):
                issues.append("Should consider appointing alternate attorney")
            
            powers = content.get("powers", [])
            if document_type == "poa_property" and not powers:
                issues.append("No specific powers granted to attorney")
        
        return issues
    
    def _generate_recommendations(self, document_type: str, content: Dict[str, Any], 
                                compliance_results: Dict[str, Any]) -> List[str]:
        """Generate legal recommendations"""
        recommendations = []
        
        # Add compliance-based recommendations
        for violation in compliance_results.get("violations", []):
            recommendations.append(f"Legal compliance issue: {violation}")
        
        for warning in compliance_results.get("warnings", []):
            recommendations.append(f"Consider: {warning}")
        
        # Add document-specific recommendations
        if document_type == "will":
            recommendations.extend(self._get_will_recommendations(content))
        elif document_type in ["poa_property", "poa_care"]:
            recommendations.extend(self._get_poa_recommendations(document_type, content))
        
        return recommendations
    
    def _get_will_recommendations(self, content: Dict[str, Any]) -> List[str]:
        """Get will-specific recommendations"""
        recommendations = []
        
        # Executor recommendations
        if content.get("executor") and not content.get("alternate_executor"):
            recommendations.append("Consider appointing an alternate executor")
        
        # Beneficiary recommendations
        beneficiaries = content.get("beneficiaries", [])
        if len(beneficiaries) == 1:
            recommendations.append("Consider what happens if sole beneficiary predeceases you")
        
        # Guardian recommendations
        if content.get("personal_info", {}).get("has_children") and not content.get("guardian"):
            recommendations.append("Appoint a guardian for minor children")
        
        # Tax recommendations
        estate_value = content.get("estate_info", {}).get("estimated_value", 0)
        if estate_value > 1000000:
            recommendations.append("Consider tax planning strategies for large estate")
        
        return recommendations
    
    def _get_poa_recommendations(self, document_type: str, content: Dict[str, Any]) -> List[str]:
        """Get POA-specific recommendations"""
        recommendations = []
        
        if document_type == "poa_property":
            # Property POA recommendations
            if not content.get("powers"):
                recommendations.append("Specify detailed powers for property management")
            
            if not content.get("restrictions"):
                recommendations.append("Consider adding restrictions on attorney's powers")
            
            recommendations.append("Ensure attorney understands fiduciary duties")
        
        elif document_type == "poa_care":
            # Care POA recommendations
            if not content.get("care_instructions"):
                recommendations.append("Provide detailed personal care instructions")
            
            if not content.get("medical_preferences"):
                recommendations.append("Include medical treatment preferences")
            
            recommendations.append("Discuss wishes with appointed attorney")
        
        return recommendations
    
    def _assess_risk_factors(self, document_type: str, content: Dict[str, Any]) -> List[str]:
        """Assess potential risk factors"""
        risks = []
        
        if document_type == "will":
            # Will contest risks
            if content.get("personal_info", {}).get("marital_status") == "divorced":
                risks.append("Previous marriages may create family law claims")
            
            if not content.get("independent_legal_advice"):
                risks.append("Lack of independent legal advice may create challenges")
            
            beneficiaries = content.get("beneficiaries", [])
            if any("unequal" in str(b).lower() for b in beneficiaries):
                risks.append("Unequal distributions may lead to family disputes")
        
        elif document_type in ["poa_property", "poa_care"]:
            # POA risks
            if not content.get("attorney_relationship"):
                risks.append("Attorney relationship should be clearly documented")
            
            if content.get("attorney") == content.get("alternate_attorney"):
                risks.append("Attorney and alternate should be different people")
        
        return risks
    
    def _get_case_law_references(self, document_type: str, legal_issues: List[str]) -> List[str]:
        """Get relevant case law references"""
        references = []
        
        for issue in legal_issues:
            relevant_cases = self.legal_kb.get_relevant_case_law(issue, document_type)
            for case in relevant_cases[:2]:  # Top 2 most relevant
                references.append(f"{case.case_name}: {case.summary}")
        
        return references
    
    def _generate_improvements(self, document_type: str, content: Dict[str, Any]) -> List[str]:
        """Generate improvement suggestions"""
        improvements = []
        
        # Structural improvements
        if not content.get("date_created"):
            improvements.append("Add document creation date")
        
        if not content.get("jurisdiction"):
            improvements.append("Specify jurisdiction (Province of Ontario)")
        
        # Language improvements
        text_content = str(content)
        if "shall" not in text_content.lower():
            improvements.append("Consider using more formal legal language")
        
        if len(text_content) < 500:
            improvements.append("Document may be too brief for legal enforceability")
        
        return improvements
    
    def _calculate_confidence_score(self, content: Dict[str, Any], 
                                  structure_analysis: Dict[str, Any]) -> float:
        """Calculate confidence score for analysis"""
        score = 0.5  # Base score
        
        # Increase score based on content completeness
        score += structure_analysis.get("completeness_score", 0) * 0.3
        
        # Increase score if key fields are present
        if content.get("personal_info"):
            score += 0.1
        if content.get("execution"):
            score += 0.1
        
        return min(score, 1.0)
    
    def enhance_document_section(self, document_type: str, section: str, 
                               text: str) -> AIEnhancement:
        """Enhance a specific document section with AI"""
        logger.info(f"Enhancing {section} section for {document_type}")
        
        # Get legal template if available
        template = self.legal_kb.get_template(f"{document_type}_{section}")
        
        # Analyze current text
        issues = self._analyze_text_issues(text)
        
        # Generate suggestions
        suggested_text = self._improve_legal_text(document_type, section, text)
        
        # Determine legal basis
        legal_basis = self._get_legal_basis(document_type, section)
        
        # Calculate confidence
        confidence = self._calculate_enhancement_confidence(text, suggested_text)
        
        # Determine priority
        priority = self._determine_priority(issues)
        
        return AIEnhancement(
            section=section,
            original_text=text,
            suggested_text=suggested_text,
            reason=f"Enhanced for legal compliance and clarity in {section}",
            legal_basis=legal_basis,
            confidence=confidence,
            priority=priority
        )
    
    def _analyze_text_issues(self, text: str) -> List[str]:
        """Analyze issues in legal text"""
        issues = []
        
        if len(text) < 20:
            issues.append("Text too brief")
        
        if not re.search(r'[.!?]$', text.strip()):
            issues.append("Missing proper punctuation")
        
        if text.islower():
            issues.append("Should use proper capitalization")
        
        return issues
    
    def _improve_legal_text(self, document_type: str, section: str, text: str) -> str:
        """Improve legal text with AI-like enhancements"""
        # This is a simplified version - in production would use actual AI
        
        improved = text.strip()
        
        # Add formal legal language
        if section == "revocation_clause":
            improved = "I hereby revoke all former Wills and Codicils by me at any time heretofore made."
        elif section == "executor_appointment":
            if "appoint" not in improved.lower():
                improved = f"I appoint {improved} to be the Executor of this my Will."
        
        # Ensure proper capitalization
        if improved and improved[0].islower():
            improved = improved[0].upper() + improved[1:]
        
        # Ensure proper punctuation
        if not improved.endswith('.'):
            improved += '.'
        
        return improved
    
    def _get_legal_basis(self, document_type: str, section: str) -> str:
        """Get legal basis for enhancement"""
        if document_type == "will":
            if section in ["executor_appointment", "witness_requirements"]:
                return "Succession Law Reform Act, Section 4"
            elif section == "revocation_clause":
                return "Succession Law Reform Act, Section 15"
        elif document_type in ["poa_property", "poa_care"]:
            return "Substitute Decisions Act, Section 10"
        
        return "Ontario legal requirements"
    
    def _calculate_enhancement_confidence(self, original: str, enhanced: str) -> float:
        """Calculate confidence in enhancement"""
        if len(enhanced) > len(original):
            return 0.8
        elif original != enhanced:
            return 0.7
        else:
            return 0.5
    
    def _determine_priority(self, issues: List[str]) -> str:
        """Determine priority of enhancement"""
        if len(issues) > 2:
            return "high"
        elif len(issues) > 0:
            return "medium"
        else:
            return "low"
    
    def generate_document_insights(self, document_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive document insights"""
        analysis = self.analyze_document(document_type, content)
        
        insights = {
            "summary": {
                "compliance_score": analysis.compliance_score,
                "confidence_score": analysis.confidence_score,
                "total_issues": len(analysis.legal_issues),
                "total_recommendations": len(analysis.recommendations)
            },
            "compliance": {
                "score": analysis.compliance_score,
                "issues": analysis.legal_issues,
                "missing_requirements": analysis.missing_requirements
            },
            "recommendations": {
                "priority_recommendations": analysis.recommendations[:3],
                "all_recommendations": analysis.recommendations,
                "risk_factors": analysis.risk_factors
            },
            "legal_research": {
                "relevant_case_law": analysis.case_law_references,
                "legal_citations": self._get_legal_citations(document_type)
            },
            "improvements": {
                "suggestions": analysis.improvement_suggestions,
                "next_steps": self._get_next_steps(analysis)
            }
        }
        
        return insights
    
    def _get_legal_citations(self, document_type: str) -> List[str]:
        """Get relevant legal citations"""
        if document_type == "will":
            return [
                "Succession Law Reform Act, R.S.O. 1990, c. S.26",
                "Estates Act, R.S.O. 1990, c. E.21",
                "Family Law Act, R.S.O. 1990, c. F.3"
            ]
        elif document_type in ["poa_property", "poa_care"]:
            return [
                "Substitute Decisions Act, 1992, S.O. 1992, c. 30",
                "Health Care Consent Act, 1996, S.O. 1996, c. 2"
            ]
        
        return []
    
    def _get_next_steps(self, analysis: LegalAnalysisResult) -> List[str]:
        """Get recommended next steps"""
        steps = []
        
        if analysis.compliance_score < 0.8:
            steps.append("Address legal compliance issues before proceeding")
        
        if analysis.missing_requirements:
            steps.append("Complete all required document sections")
        
        if analysis.risk_factors:
            steps.append("Consider risk mitigation strategies")
        
        steps.append("Review document with legal professional")
        steps.append("Ensure proper execution with witnesses")
        
        return steps