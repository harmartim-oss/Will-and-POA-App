from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import logging

from models.schemas import ComplianceCheckRequest, ComplianceCheckResponse

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/check", response_model=ComplianceCheckResponse)
async def check_compliance(request: ComplianceCheckRequest):
    """Check document compliance with Ontario legal requirements"""
    try:
        logger.info(f"Checking compliance for {request.document_type}")
        
        # Placeholder compliance check
        compliance_issues = []
        compliance_score = 85
        
        # Basic compliance checks
        content_lower = request.content.lower()
        
        if request.document_type == "will":
            if "witness" not in content_lower:
                compliance_issues.append({
                    "type": "witness_requirement",
                    "severity": "critical",
                    "message": "No witness references found",
                    "recommendation": "Ensure two witnesses are present during signing"
                })
                compliance_score -= 20
            
            if "executor" not in content_lower:
                compliance_issues.append({
                    "type": "executor_appointment", 
                    "severity": "high",
                    "message": "No executor appointment found",
                    "recommendation": "Appoint an executor to manage the estate"
                })
                compliance_score -= 15
        
        elif request.document_type.startswith("poa"):
            if "attorney" not in content_lower:
                compliance_issues.append({
                    "type": "attorney_appointment",
                    "severity": "critical", 
                    "message": "No attorney appointment found",
                    "recommendation": "Must appoint an attorney for the power of attorney"
                })
                compliance_score -= 25
                
            if "capacity" not in content_lower:
                compliance_issues.append({
                    "type": "capacity_declaration",
                    "severity": "high",
                    "message": "No capacity declaration found", 
                    "recommendation": "Include statement of mental capacity"
                })
                compliance_score -= 15
        
        status = "compliant" if compliance_score >= 80 else "non_compliant"
        
        recommendations = [issue["recommendation"] for issue in compliance_issues]
        if not recommendations:
            recommendations = ["Document appears to meet basic compliance requirements"]
        
        return ComplianceCheckResponse(
            success=True,
            compliance_status=status,
            score=max(0, compliance_score),
            issues=compliance_issues,
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Compliance check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Compliance check failed: {str(e)}")

@router.get("/requirements/{document_type}")
async def get_compliance_requirements(document_type: str):
    """Get compliance requirements for document type"""
    try:
        # Placeholder requirements
        requirements = {
            "will": {
                "critical_requirements": [
                    "Testator must be 18 years or older",
                    "Two witnesses required",
                    "Testamentary capacity required",
                    "Proper execution procedure"
                ],
                "recommended_requirements": [
                    "Clear appointment of executor",
                    "Residuary clause included",
                    "Revocation of previous wills"
                ]
            },
            "poa_property": {
                "critical_requirements": [
                    "Grantor must be 18 years or older",
                    "Mental capacity for property decisions",
                    "Clear appointment of attorney",
                    "Witness or notarization required"
                ],
                "recommended_requirements": [
                    "Scope of powers clearly defined",
                    "Successor provisions included",
                    "Capacity determination procedures"
                ]
            },
            "poa_personal_care": {
                "critical_requirements": [
                    "Grantor must be 16 years or older",
                    "Mental capacity for personal care decisions",
                    "Clear appointment of attorney",
                    "Witness or notarization required"
                ],
                "recommended_requirements": [
                    "Healthcare preferences specified",
                    "End-of-life instructions included",
                    "Successor attorney provisions"
                ]
            }
        }
        
        requirement = requirements.get(document_type)
        if not requirement:
            raise HTTPException(status_code=404, detail="Requirements not found for document type")
        
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

@router.post("/validate-execution")
async def validate_execution_requirements(request: Dict[str, Any]):
    """Validate document execution requirements"""
    try:
        document_type = request.get("document_type")
        execution_details = request.get("execution_details", {})
        
        validation_results = {
            "is_valid": True,
            "issues": [],
            "requirements_met": [],
            "score": 100
        }
        
        # Check age requirement
        age = execution_details.get("age")
        if document_type == "poa_personal_care":
            min_age = 16
        else:
            min_age = 18
            
        if not age or age < min_age:
            validation_results["issues"].append({
                "type": "age_requirement",
                "message": f"Signatory must be at least {min_age} years old"
            })
            validation_results["score"] -= 25
            validation_results["is_valid"] = False
        else:
            validation_results["requirements_met"].append("Age requirement satisfied")
        
        # Check witness requirements
        witness_count = execution_details.get("witnesses", 0)
        if document_type == "will" and witness_count < 2:
            validation_results["issues"].append({
                "type": "witness_requirement",
                "message": "Two witnesses required for will execution"
            })
            validation_results["score"] -= 30
            validation_results["is_valid"] = False
        elif witness_count >= 1 or execution_details.get("notarized", False):
            validation_results["requirements_met"].append("Witness/notary requirement satisfied")
        else:
            validation_results["issues"].append({
                "type": "witness_requirement",
                "message": "Document must be witnessed or notarized"
            })
            validation_results["score"] -= 20
            validation_results["is_valid"] = False
        
        # Check capacity declaration
        if not execution_details.get("capacity_declared", False):
            validation_results["issues"].append({
                "type": "capacity_requirement",
                "message": "Mental capacity must be declared"
            })
            validation_results["score"] -= 15
            validation_results["is_valid"] = False
        else:
            validation_results["requirements_met"].append("Capacity requirement satisfied")
        
        return {
            "success": True,
            "validation": validation_results
        }
        
    except Exception as e:
        logger.error(f"Execution validation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Execution validation failed: {str(e)}")

@router.get("/statutory-references/{document_type}")
async def get_statutory_references(document_type: str):
    """Get relevant statutory references for document type"""
    try:
        # Ontario statutory references
        references = {
            "will": {
                "primary_statute": "Succession Law Reform Act, R.S.O. 1990, c. S.26",
                "relevant_sections": [
                    "Section 3 - Requirements for valid will",
                    "Section 4 - Witness requirements", 
                    "Section 5 - Testamentary capacity",
                    "Section 15 - Revocation of wills"
                ],
                "related_statutes": [
                    "Estates Act, R.S.O. 1990, c. E.21",
                    "Trustee Act, R.S.O. 1990, c. T.23"
                ]
            },
            "poa_property": {
                "primary_statute": "Substitute Decisions Act, 1992, S.O. 1992, c. 30",
                "relevant_sections": [
                    "Section 7 - Requirements for power of attorney for property",
                    "Section 8 - Capacity requirements",
                    "Section 9 - Execution requirements",
                    "Section 32 - Duties of attorney"
                ],
                "related_statutes": [
                    "Mental Health Act, R.S.O. 1990, c. M.7"
                ]
            },
            "poa_personal_care": {
                "primary_statute": "Substitute Decisions Act, 1992, S.O. 1992, c. 30",
                "relevant_sections": [
                    "Section 9 - Requirements for power of attorney for personal care",
                    "Section 45 - Capacity for personal care",
                    "Section 46 - Duties of attorney for personal care"
                ],
                "related_statutes": [
                    "Health Care Consent Act, 1996, S.O. 1996, c. 2, Sched. A"
                ]
            }
        }
        
        reference = references.get(document_type)
        if not reference:
            raise HTTPException(status_code=404, detail="Statutory references not found")
        
        return {
            "success": True,
            "document_type": document_type,
            "statutory_references": reference
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Statutory references retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"References retrieval failed: {str(e)}")