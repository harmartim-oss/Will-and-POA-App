import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)

class OntarioRiskAssessor:
    """Risk assessor for Ontario legal documents"""
    
    def __init__(self):
        self.risk_factors = {}
        self.is_initialized = False

    async def initialize(self):
        """Initialize the risk assessor"""
        try:
            logger.info("Initializing Ontario Risk Assessor...")
            
            # Load risk assessment factors
            self._load_risk_factors()
            
            self.is_initialized = True
            logger.info("Risk Assessor initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Risk Assessor: {str(e)}")
            self.is_initialized = False

    def _load_risk_factors(self):
        """Load risk assessment factors"""
        self.risk_factors = {
            "will": {
                "capacity_risks": {
                    "elderly_testator": {"weight": 0.3, "description": "Elderly testator may face capacity challenges"},
                    "medical_conditions": {"weight": 0.4, "description": "Medical conditions affecting mental capacity"},
                    "sudden_changes": {"weight": 0.5, "description": "Sudden changes to existing will"}
                },
                "execution_risks": {
                    "witness_issues": {"weight": 0.6, "description": "Witness-related execution problems"},
                    "improper_procedure": {"weight": 0.7, "description": "Improper execution procedure"},
                    "undue_influence": {"weight": 0.8, "description": "Potential undue influence"}
                },
                "content_risks": {
                    "ambiguous_language": {"weight": 0.4, "description": "Ambiguous or unclear language"},
                    "incomplete_provisions": {"weight": 0.3, "description": "Incomplete or missing provisions"},
                    "conflicting_clauses": {"weight": 0.6, "description": "Conflicting or contradictory clauses"}
                }
            },
            "poa_property": {
                "attorney_risks": {
                    "conflict_of_interest": {"weight": 0.7, "description": "Attorney has conflict of interest"},
                    "financial_benefit": {"weight": 0.8, "description": "Attorney stands to benefit financially"},
                    "inadequate_oversight": {"weight": 0.5, "description": "Inadequate oversight of attorney"}
                },
                "scope_risks": {
                    "overly_broad_powers": {"weight": 0.6, "description": "Overly broad powers granted"},
                    "unclear_limitations": {"weight": 0.4, "description": "Unclear limitations on powers"},
                    "missing_safeguards": {"weight": 0.5, "description": "Missing protective safeguards"}
                },
                "capacity_risks": {
                    "declining_capacity": {"weight": 0.6, "description": "Grantor's declining mental capacity"},
                    "pressure_situations": {"weight": 0.7, "description": "Evidence of pressure or coercion"}
                }
            },
            "poa_personal_care": {
                "healthcare_risks": {
                    "unclear_preferences": {"weight": 0.5, "description": "Unclear healthcare preferences"},
                    "conflicting_instructions": {"weight": 0.6, "description": "Conflicting healthcare instructions"},
                    "emergency_situations": {"weight": 0.4, "description": "Unclear emergency decision authority"}
                },
                "attorney_risks": {
                    "emotional_conflict": {"weight": 0.6, "description": "Emotional conflicts affecting decisions"},
                    "geographical_distance": {"weight": 0.3, "description": "Attorney located far from grantor"},
                    "lack_of_knowledge": {"weight": 0.5, "description": "Attorney lacks healthcare knowledge"}
                }
            }
        }

    def assess_risk(self, document_type: str, document_content: str, user_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Perform comprehensive risk assessment"""
        if document_type not in self.risk_factors:
            return {
                "status": "unknown",
                "overall_risk": "unknown",
                "risk_factors": [],
                "message": "Unknown document type for risk assessment"
            }
        
        user_info = user_info or {}
        identified_risks = []
        total_risk_score = 0.0
        
        # Assess each risk category
        for category, risks in self.risk_factors[document_type].items():
            category_risks = self._assess_category_risks(category, risks, document_content, user_info)
            identified_risks.extend(category_risks)
            
            # Calculate category risk score
            category_score = sum(risk["score"] for risk in category_risks)
            total_risk_score += category_score
        
        # Determine overall risk level
        overall_risk = self._determine_risk_level(total_risk_score)
        
        return {
            "status": "completed",
            "overall_risk": overall_risk,
            "risk_score": total_risk_score,
            "risk_factors": identified_risks,
            "recommendations": self._generate_risk_recommendations(identified_risks, overall_risk),
            "mitigation_strategies": self._suggest_mitigation_strategies(identified_risks)
        }

    def _assess_category_risks(self, category: str, risks: Dict[str, Dict], content: str, user_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Assess risks within a specific category"""
        identified_risks = []
        content_lower = content.lower()
        
        for risk_name, risk_data in risks.items():
            risk_detected = False
            risk_score = 0.0
            
            # Check for specific risk indicators
            if risk_name == "elderly_testator":
                age = user_info.get("age")
                if age and age > 75:
                    risk_detected = True
                    risk_score = risk_data["weight"] * (min(age - 75, 15) / 15)  # Scale with age
            
            elif risk_name == "medical_conditions":
                medical_indicators = ["dementia", "alzheimer", "cognitive", "mental health", "medication"]
                if any(indicator in content_lower for indicator in medical_indicators):
                    risk_detected = True
                    risk_score = risk_data["weight"]
            
            elif risk_name == "sudden_changes":
                change_indicators = ["change", "different", "new", "recent"]
                if any(indicator in content_lower for indicator in change_indicators):
                    risk_detected = True
                    risk_score = risk_data["weight"] * 0.7  # Moderate risk
            
            elif risk_name == "witness_issues":
                if "witness" not in content_lower or content_lower.count("witness") < 2:
                    risk_detected = True
                    risk_score = risk_data["weight"]
            
            elif risk_name == "ambiguous_language":
                ambiguous_indicators = ["maybe", "perhaps", "unclear", "ambiguous", "confusing"]
                if any(indicator in content_lower for indicator in ambiguous_indicators):
                    risk_detected = True
                    risk_score = risk_data["weight"]
            
            elif risk_name == "conflict_of_interest":
                conflict_indicators = ["benefit", "inherit", "receive", "related", "family"]
                if any(indicator in content_lower for indicator in conflict_indicators):
                    risk_detected = True
                    risk_score = risk_data["weight"] * 0.6  # Moderate detection
            
            elif risk_name == "overly_broad_powers":
                broad_indicators = ["all", "any", "unlimited", "complete", "total"]
                if any(indicator in content_lower for indicator in broad_indicators):
                    risk_detected = True
                    risk_score = risk_data["weight"] * 0.5
            
            elif risk_name == "unclear_preferences":
                if document_content and len(document_content.strip()) < 100:  # Very short content
                    risk_detected = True
                    risk_score = risk_data["weight"]
            
            # Add more risk detection logic as needed
            
            if risk_detected:
                identified_risks.append({
                    "name": risk_name,
                    "category": category,
                    "description": risk_data["description"],
                    "score": risk_score,
                    "severity": self._categorize_risk_severity(risk_score)
                })
        
        return identified_risks

    def _determine_risk_level(self, total_score: float) -> str:
        """Determine overall risk level based on total score"""
        if total_score < 0.3:
            return "low"
        elif total_score < 0.7:
            return "medium"
        elif total_score < 1.2:
            return "high"
        else:
            return "critical"

    def _categorize_risk_severity(self, score: float) -> str:
        """Categorize individual risk severity"""
        if score < 0.3:
            return "low"
        elif score < 0.6:
            return "medium"
        else:
            return "high"

    def _generate_risk_recommendations(self, risks: List[Dict[str, Any]], overall_risk: str) -> List[str]:
        """Generate recommendations based on identified risks"""
        recommendations = []
        
        # Overall risk recommendations
        if overall_risk == "critical":
            recommendations.append("Seek immediate legal consultation before proceeding")
            recommendations.append("Consider comprehensive review of all document provisions")
        elif overall_risk == "high":
            recommendations.append("Obtain professional legal advice")
            recommendations.append("Review and address high-severity risk factors")
        elif overall_risk == "medium":
            recommendations.append("Consider legal consultation for complex provisions")
            recommendations.append("Address identified risk factors before execution")
        
        # Specific risk recommendations
        for risk in risks:
            if risk["severity"] == "high":
                if "capacity" in risk["name"]:
                    recommendations.append("Obtain medical assessment of mental capacity")
                elif "witness" in risk["name"]:
                    recommendations.append("Ensure proper witness procedures are followed")
                elif "conflict" in risk["name"]:
                    recommendations.append("Address potential conflicts of interest")
                elif "ambiguous" in risk["name"]:
                    recommendations.append("Clarify ambiguous language in document")
        
        return list(set(recommendations))  # Remove duplicates

    def _suggest_mitigation_strategies(self, risks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Suggest specific mitigation strategies"""
        strategies = []
        
        for risk in risks:
            strategy = {
                "risk": risk["name"],
                "strategies": []
            }
            
            if "capacity" in risk["name"]:
                strategy["strategies"].extend([
                    "Obtain capacity assessment from qualified professional",
                    "Document decision-making process thoroughly",
                    "Consider involving independent witnesses"
                ])
            
            elif "witness" in risk["name"]:
                strategy["strategies"].extend([
                    "Ensure two independent witnesses are present",
                    "Verify witnesses understand their role",
                    "Consider using professional witnesses"
                ])
            
            elif "conflict" in risk["name"]:
                strategy["strategies"].extend([
                    "Disclose all potential conflicts openly",
                    "Consider appointing independent attorney",
                    "Implement additional oversight measures"
                ])
            
            elif "ambiguous" in risk["name"]:
                strategy["strategies"].extend([
                    "Revise unclear language for precision",
                    "Define all technical or legal terms",
                    "Have document reviewed by third party"
                ])
            
            if strategy["strategies"]:
                strategies.append(strategy)
        
        return strategies

    def is_ready(self) -> bool:
        """Check if risk assessor is ready"""
        return self.is_initialized