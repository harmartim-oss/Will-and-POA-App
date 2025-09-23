import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)

class OntarioDocumentGenerator:
    """Document generator for Ontario legal documents"""
    
    def __init__(self):
        self.templates = {}
        self.is_initialized = False

    async def initialize(self):
        """Initialize the document generator"""
        try:
            logger.info("Initializing Ontario Document Generator...")
            
            # Load document templates
            self._load_templates()
            
            self.is_initialized = True
            logger.info("Document Generator initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Document Generator: {str(e)}")
            self.is_initialized = False

    def _load_templates(self):
        """Load document templates"""
        self.templates = {
            "will": {
                "title": "Last Will and Testament",
                "structure": [
                    "declaration",
                    "revocation",
                    "executor_appointment", 
                    "bequests",
                    "residuary_clause",
                    "execution_clause"
                ]
            },
            "poa_property": {
                "title": "Power of Attorney for Property",
                "structure": [
                    "appointment",
                    "powers_granted",
                    "capacity_clause",
                    "successor_provision",
                    "execution_clause"
                ]
            },
            "poa_personal_care": {
                "title": "Power of Attorney for Personal Care",
                "structure": [
                    "appointment",
                    "healthcare_decisions",
                    "personal_care_instructions",
                    "end_of_life_wishes",
                    "execution_clause"
                ]
            }
        }

    def get_document_insights(self, document_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive document insights and recommendations"""
        insights = {
            "document_type": document_type,
            "analysis_timestamp": datetime.now().isoformat(),
            "structure_analysis": self._analyze_structure(document_type, content),
            "completeness_check": self._check_completeness(document_type, content),
            "recommendations": self._generate_recommendations(document_type, content),
            "potential_issues": self._identify_issues(document_type, content)
        }
        
        return insights

    def _analyze_structure(self, document_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze document structure"""
        template = self.templates.get(document_type, {})
        required_sections = template.get("structure", [])
        
        present_sections = []
        missing_sections = []
        
        for section in required_sections:
            if section in content or any(section in str(v).lower() for v in content.values()):
                present_sections.append(section)
            else:
                missing_sections.append(section)
        
        return {
            "required_sections": required_sections,
            "present_sections": present_sections,
            "missing_sections": missing_sections,
            "completion_percentage": len(present_sections) / len(required_sections) * 100 if required_sections else 0
        }

    def _check_completeness(self, document_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Check document completeness"""
        completeness_score = 100
        issues = []
        
        if document_type == "will":
            # Check for executor
            if not any("executor" in str(v).lower() for v in content.values()):
                issues.append("Missing executor appointment")
                completeness_score -= 20
            
            # Check for beneficiaries
            if not any("beneficiary" in str(v).lower() or "inherit" in str(v).lower() for v in content.values()):
                issues.append("Missing beneficiary information")
                completeness_score -= 15
        
        elif document_type.startswith("poa"):
            # Check for attorney appointment
            if not any("attorney" in str(v).lower() for v in content.values()):
                issues.append("Missing attorney appointment")
                completeness_score -= 25
        
        return {
            "score": max(0, completeness_score),
            "issues": issues,
            "status": "complete" if completeness_score >= 90 else "incomplete"
        }

    def _generate_recommendations(self, document_type: str, content: Dict[str, Any]) -> List[str]:
        """Generate document-specific recommendations"""
        recommendations = []
        
        if document_type == "will":
            recommendations.extend([
                "Consider adding a residuary clause to handle remaining assets",
                "Ensure executor is willing and able to serve",
                "Review beneficiary designations for completeness",
                "Consider naming an alternate executor"
            ])
        
        elif document_type == "poa_property":
            recommendations.extend([
                "Clearly define the scope of financial powers",
                "Consider succession provisions for the attorney",
                "Include specific instructions for investment decisions",
                "Review capacity determination procedures"
            ])
        
        elif document_type == "poa_personal_care":
            recommendations.extend([
                "Specify healthcare preferences clearly",
                "Include end-of-life care instructions",
                "Consider naming an alternate attorney",
                "Ensure compliance with healthcare legislation"
            ])
        
        return recommendations

    def _identify_issues(self, document_type: str, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify potential issues in the document"""
        issues = []
        
        # Check for common issues
        content_str = str(content).lower()
        
        if "conflict" in content_str:
            issues.append({
                "type": "potential_conflict",
                "severity": "medium",
                "description": "Potential conflict of interest detected"
            })
        
        if "unclear" in content_str or "ambiguous" in content_str:
            issues.append({
                "type": "ambiguity",
                "severity": "high", 
                "description": "Ambiguous language detected - consider clarification"
            })
        
        # Document-specific issues
        if document_type == "will" and "minor" in content_str and "guardian" not in content_str:
            issues.append({
                "type": "missing_guardian",
                "severity": "high",
                "description": "Minor beneficiaries identified but no guardian appointed"
            })
        
        return issues

    def is_ready(self) -> bool:
        """Check if document generator is ready"""
        return self.is_initialized