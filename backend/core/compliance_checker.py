import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)

class OntarioComplianceChecker:
    """Compliance checker for Ontario legal requirements"""
    
    def __init__(self):
        self.compliance_rules = {}
        self.is_initialized = False

    async def initialize(self):
        """Initialize the compliance checker"""
        try:
            logger.info("Initializing Ontario Compliance Checker...")
            
            # Load compliance rules
            self._load_compliance_rules()
            
            self.is_initialized = True
            logger.info("Compliance Checker initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Compliance Checker: {str(e)}")
            self.is_initialized = False

    def _load_compliance_rules(self):
        """Load Ontario compliance rules"""
        self.compliance_rules = {
            "will": {
                "age_requirement": {
                    "rule": "Testator must be 18 years or older",
                    "check": "age_check",
                    "severity": "critical"
                },
                "witness_requirement": {
                    "rule": "Two witnesses required, both present at signing",
                    "check": "witness_check", 
                    "severity": "critical"
                },
                "capacity_requirement": {
                    "rule": "Testator must have testamentary capacity",
                    "check": "capacity_check",
                    "severity": "critical"
                },
                "signature_requirement": {
                    "rule": "Testator must sign in presence of witnesses",
                    "check": "signature_check",
                    "severity": "critical"
                }
            },
            "poa_property": {
                "age_requirement": {
                    "rule": "Grantor must be 18 years or older",
                    "check": "age_check",
                    "severity": "critical"
                },
                "capacity_requirement": {
                    "rule": "Grantor must have capacity for property decisions",
                    "check": "capacity_check",
                    "severity": "critical"
                },
                "attorney_eligibility": {
                    "rule": "Attorney must be capable and willing to serve",
                    "check": "attorney_check",
                    "severity": "critical"
                },
                "witness_requirement": {
                    "rule": "Witness or notarization required",
                    "check": "witness_notary_check",
                    "severity": "high"
                }
            },
            "poa_personal_care": {
                "age_requirement": {
                    "rule": "Grantor must be 16 years or older",
                    "check": "age_check_16",
                    "severity": "critical"
                },
                "capacity_requirement": {
                    "rule": "Grantor must have capacity for personal care decisions",
                    "check": "personal_care_capacity_check",
                    "severity": "critical"
                },
                "attorney_eligibility": {
                    "rule": "Attorney must be capable and willing to serve",
                    "check": "attorney_check",
                    "severity": "critical"
                }
            }
        }

    def check_compliance(self, document_type: str, document_content: str, user_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Check document compliance with Ontario legal requirements"""
        if document_type not in self.compliance_rules:
            return {
                "status": "unknown",
                "score": 0,
                "issues": [{"type": "unknown_document_type", "message": "Unknown document type"}]
            }
        
        rules = self.compliance_rules[document_type]
        compliance_issues = []
        compliance_score = 100
        
        for rule_name, rule_data in rules.items():
            check_result = self._perform_check(rule_data["check"], document_content, user_info)
            
            if not check_result["passed"]:
                severity = rule_data["severity"]
                issue = {
                    "rule": rule_name,
                    "description": rule_data["rule"],
                    "severity": severity,
                    "message": check_result["message"],
                    "recommendation": check_result.get("recommendation", "")
                }
                compliance_issues.append(issue)
                
                # Deduct points based on severity
                if severity == "critical":
                    compliance_score -= 25
                elif severity == "high":
                    compliance_score -= 15
                elif severity == "medium":
                    compliance_score -= 10
                else:
                    compliance_score -= 5
        
        compliance_score = max(0, compliance_score)
        
        return {
            "status": "compliant" if compliance_score >= 80 else "non_compliant",
            "score": compliance_score,
            "issues": compliance_issues,
            "total_checks": len(rules),
            "passed_checks": len(rules) - len(compliance_issues),
            "document_type": document_type
        }

    def _perform_check(self, check_type: str, content: str, user_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Perform specific compliance check"""
        user_info = user_info or {}
        content_lower = content.lower()
        
        if check_type == "age_check":
            age = user_info.get("age")
            if age is None:
                return {
                    "passed": False,
                    "message": "Age information not provided",
                    "recommendation": "Verify testator is 18 years or older"
                }
            elif age < 18:
                return {
                    "passed": False,
                    "message": f"Testator age {age} is below required minimum of 18",
                    "recommendation": "Testator must be at least 18 years old"
                }
            else:
                return {"passed": True, "message": "Age requirement met"}
        
        elif check_type == "age_check_16":
            age = user_info.get("age")
            if age is None:
                return {
                    "passed": False,
                    "message": "Age information not provided",
                    "recommendation": "Verify grantor is 16 years or older"
                }
            elif age < 16:
                return {
                    "passed": False,
                    "message": f"Grantor age {age} is below required minimum of 16",
                    "recommendation": "Grantor must be at least 16 years old"
                }
            else:
                return {"passed": True, "message": "Age requirement met"}
        
        elif check_type == "witness_check":
            witness_count = content_lower.count("witness")
            if witness_count < 2:
                return {
                    "passed": False,
                    "message": f"Only {witness_count} witness reference(s) found, 2 required",
                    "recommendation": "Ensure two witnesses are present during signing"
                }
            else:
                return {"passed": True, "message": "Witness requirement appears to be met"}
        
        elif check_type == "witness_notary_check":
            has_witness = "witness" in content_lower
            has_notary = "notary" in content_lower or "notarized" in content_lower
            
            if not (has_witness or has_notary):
                return {
                    "passed": False,
                    "message": "No witness or notarization reference found",
                    "recommendation": "Document must be witnessed or notarized"
                }
            else:
                return {"passed": True, "message": "Witness or notary requirement appears to be met"}
        
        elif check_type == "capacity_check":
            capacity_indicators = ["capacity", "sound mind", "mentally capable"]
            has_capacity_clause = any(indicator in content_lower for indicator in capacity_indicators)
            
            if not has_capacity_clause:
                return {
                    "passed": False,
                    "message": "No testamentary capacity declaration found",
                    "recommendation": "Include statement of testamentary capacity"
                }
            else:
                return {"passed": True, "message": "Capacity declaration present"}
        
        elif check_type == "personal_care_capacity_check":
            capacity_indicators = ["capacity", "capable of", "understand"]
            has_capacity_clause = any(indicator in content_lower for indicator in capacity_indicators)
            
            if not has_capacity_clause:
                return {
                    "passed": False,
                    "message": "No personal care capacity declaration found",
                    "recommendation": "Include statement of capacity for personal care decisions"
                }
            else:
                return {"passed": True, "message": "Personal care capacity declaration present"}
        
        elif check_type == "attorney_check":
            has_attorney = "attorney" in content_lower
            
            if not has_attorney:
                return {
                    "passed": False,
                    "message": "No attorney appointment found",
                    "recommendation": "Must appoint an attorney for the power of attorney"
                }
            else:
                return {"passed": True, "message": "Attorney appointment present"}
        
        elif check_type == "signature_check":
            has_signature = "sign" in content_lower or "signature" in content_lower
            
            if not has_signature:
                return {
                    "passed": False,
                    "message": "No signature reference found",
                    "recommendation": "Document must include proper signature requirements"
                }
            else:
                return {"passed": True, "message": "Signature requirement present"}
        
        else:
            return {
                "passed": False,
                "message": f"Unknown check type: {check_type}",
                "recommendation": "Manual review required"
            }

    def get_compliance_requirements(self, document_type: str) -> Dict[str, Any]:
        """Get all compliance requirements for a document type"""
        if document_type not in self.compliance_rules:
            return {"error": "Unknown document type"}
        
        return {
            "document_type": document_type,
            "requirements": self.compliance_rules[document_type],
            "total_requirements": len(self.compliance_rules[document_type])
        }

    def is_ready(self) -> bool:
        """Check if compliance checker is ready"""
        return self.is_initialized