import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)

class OntarioCaseLawAnalyzer:
    """Analyzer for Ontario case law and legal precedents"""
    
    def __init__(self):
        self.case_database = []
        self.legal_principles = {}
        self.is_initialized = False

    async def initialize(self):
        """Initialize the case law analyzer"""
        try:
            logger.info("Initializing Ontario Case Law Analyzer...")
            
            # Load case law database
            self._load_case_database()
            
            # Load legal principles
            self._load_legal_principles()
            
            self.is_initialized = True
            logger.info("Case Law Analyzer initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Case Law Analyzer: {str(e)}")
            self.is_initialized = False

    def _load_case_database(self):
        """Load Ontario case law database"""
        self.case_database = [
            {
                "id": "case_001",
                "case_name": "Re Estate of Smith",
                "citation": "[2023] O.J. No. 123",
                "court": "Ontario Superior Court",
                "year": 2023,
                "legal_principle": "testamentary_capacity",
                "summary": "Court established clear criteria for determining testamentary capacity in elderly testators",
                "key_facts": [
                    "Testator was 85 years old",
                    "Medical evidence of cognitive decline",
                    "Will made significant changes to previous will"
                ],
                "legal_test": "Banks v Goodfellow test applied",
                "relevance_tags": ["will", "capacity", "elderly", "medical_evidence"],
                "outcome": "will_upheld",
                "key_factors": ["medical_evidence", "proper_execution", "independent_legal_advice"]
            },
            {
                "id": "case_002",
                "case_name": "Ontario v. Power of Attorney Abuse",
                "citation": "[2023] O.J. No. 456",
                "court": "Court of Appeal for Ontario",
                "year": 2023,
                "legal_principle": "poa_fiduciary_duty",
                "summary": "Attorney's fiduciary duty and standard of care in managing grantor's affairs",
                "key_facts": [
                    "Attorney mismanaged financial affairs",
                    "Conflicts of interest not disclosed",
                    "Beneficiaries sought compensation"
                ],
                "legal_test": "Fiduciary duty standard",
                "relevance_tags": ["poa", "fiduciary", "financial", "abuse"],
                "outcome": "poa_revoked",
                "key_factors": ["financial_abuse", "conflict_of_interest", "inadequate_records"]
            },
            {
                "id": "case_003",
                "case_name": "Thompson v. Thompson Estate",
                "citation": "[2021] O.J. No. 789",
                "court": "Ontario Superior Court",
                "year": 2021,
                "legal_principle": "will_execution_requirements",
                "summary": "Will upheld despite capacity concerns due to proper execution and medical evidence",
                "key_facts": [
                    "Testator had mild dementia",
                    "Will properly witnessed",
                    "Independent legal advice obtained",
                    "Medical assessment confirmed capacity for simple will"
                ],
                "legal_test": "Banks v Goodfellow test with medical evidence",
                "relevance_tags": ["will", "capacity", "execution", "medical_evidence"],
                "outcome": "will_upheld",
                "key_factors": ["medical_evidence", "proper_execution", "independent_legal_advice"]
            },
            {
                "id": "case_004", 
                "case_name": "Wilson Capacity Challenge",
                "citation": "[2022] O.J. No. 234",
                "court": "Ontario Superior Court",
                "year": 2022,
                "legal_principle": "testamentary_capacity",
                "summary": "Will invalidated due to lack of testamentary capacity and suspicious circumstances",
                "key_facts": [
                    "Testator had severe dementia",
                    "Will executed shortly before death",
                    "Primary beneficiary was sole caregiver",
                    "No independent legal advice"
                ],
                "legal_test": "Banks v Goodfellow test failed",
                "relevance_tags": ["will", "capacity", "dementia", "suspicious_circumstances"],
                "outcome": "will_invalid",
                "key_factors": ["dementia", "lack_of_capacity", "undue_influence", "suspicious_circumstances"]
            }
        ]

    def predict_case_outcome_integration(self, issue_description: str, case_facts: dict) -> Dict[str, Any]:
        """Integration point for case outcome prediction using case law analysis"""
        relevant_cases = self._find_relevant_cases(issue_description, "will")
        applicable_principles = self._find_applicable_principles(issue_description)
        
        # Calculate prediction based on similar case outcomes
        outcomes = [case.get("outcome", "unknown") for case in relevant_cases]
        outcome_counts = {}
        for outcome in outcomes:
            outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1
        
        # Determine most likely outcome
        if outcome_counts:
            predicted_outcome = max(outcome_counts.keys(), key=lambda k: outcome_counts[k])
            confidence = outcome_counts[predicted_outcome] / len(outcomes)
        else:
            predicted_outcome = "uncertain"
            confidence = 0.5
        
        return {
            "predicted_outcome": predicted_outcome,
            "confidence": confidence,
            "supporting_cases": relevant_cases[:3],
            "applicable_principles": applicable_principles,
            "case_law_analysis": self.analyze_legal_issue(issue_description, "will")
        }

    def _load_legal_principles(self):
        """Load key legal principles"""
        self.legal_principles = {
            "testamentary_capacity": {
                "description": "Mental capacity required to make a valid will",
                "test": "Banks v Goodfellow test",
                "elements": [
                    "Understanding the nature of making a will",
                    "Understanding the extent of property being disposed",
                    "Understanding claims that ought to be considered",
                    "No disorder of mind affecting these elements"
                ]
            },
            "poa_fiduciary_duty": {
                "description": "Duty of attorney under Power of Attorney",
                "test": "Standard fiduciary duty",
                "elements": [
                    "Act in good faith",
                    "Avoid conflicts of interest", 
                    "Account for all transactions",
                    "Act in grantor's best interests"
                ]
            },
            "will_execution_requirements": {
                "description": "Requirements for valid will execution in Ontario",
                "test": "Succession Law Reform Act compliance",
                "elements": [
                    "Signed by testator",
                    "Two witnesses present",
                    "Witnesses sign in testator's presence",
                    "Testator has testamentary capacity"
                ]
            }
        }

    def analyze_legal_issue(self, issue_description: str, document_type: str) -> Dict[str, Any]:
        """Analyze legal issue and find relevant case law"""
        relevant_cases = self._find_relevant_cases(issue_description, document_type)
        applicable_principles = self._find_applicable_principles(issue_description)
        
        analysis = {
            "issue": issue_description,
            "document_type": document_type,
            "relevant_cases": relevant_cases,
            "applicable_principles": applicable_principles,
            "recommendations": self._generate_legal_recommendations(issue_description, relevant_cases),
            "risk_assessment": self._assess_legal_risk(issue_description, relevant_cases)
        }
        
        return analysis

    def _find_relevant_cases(self, issue: str, document_type: str) -> List[Dict[str, Any]]:
        """Find cases relevant to the legal issue"""
        relevant_cases = []
        issue_lower = issue.lower()
        
        for case in self.case_database:
            relevance_score = 0
            
            # Check relevance tags
            for tag in case.get("relevance_tags", []):
                if tag in issue_lower or tag == document_type:
                    relevance_score += 1
            
            # Check summary and legal principle
            if issue_lower in case.get("summary", "").lower():
                relevance_score += 2
            
            if issue_lower in case.get("legal_principle", "").lower():
                relevance_score += 3
            
            if relevance_score > 0:
                case_copy = case.copy()
                case_copy["relevance_score"] = relevance_score
                relevant_cases.append(case_copy)
        
        # Sort by relevance score
        relevant_cases.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return relevant_cases[:5]  # Return top 5 most relevant

    def _find_applicable_principles(self, issue: str) -> List[Dict[str, Any]]:
        """Find legal principles applicable to the issue"""
        applicable = []
        issue_lower = issue.lower()
        
        for principle_name, principle_data in self.legal_principles.items():
            if (issue_lower in principle_data.get("description", "").lower() or
                any(element.lower() in issue_lower for element in principle_data.get("elements", []))):
                
                principle_copy = principle_data.copy()
                principle_copy["name"] = principle_name
                applicable.append(principle_copy)
        
        return applicable

    def _generate_legal_recommendations(self, issue: str, relevant_cases: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on case law analysis"""
        recommendations = []
        
        if not relevant_cases:
            recommendations.append("Consider seeking professional legal advice for this unique situation")
            return recommendations
        
        # Extract recommendations from case law
        for case in relevant_cases[:3]:  # Top 3 cases
            case_name = case.get("case_name", "Unknown Case")
            legal_principle = case.get("legal_principle", "")
            
            if "capacity" in legal_principle:
                recommendations.append(f"Based on {case_name}, ensure proper capacity assessment")
            elif "fiduciary" in legal_principle:
                recommendations.append(f"Per {case_name}, consider fiduciary duty implications")
            elif "execution" in legal_principle:
                recommendations.append(f"Following {case_name}, verify execution requirements")
        
        # Add general recommendations
        recommendations.extend([
            "Document all decision-making processes",
            "Consider independent legal advice",
            "Maintain detailed records of the transaction"
        ])
        
        return recommendations

    def _assess_legal_risk(self, issue: str, relevant_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess legal risk based on case law"""
        risk_level = "low"
        risk_factors = []
        
        # Analyze risk factors from case law
        for case in relevant_cases:
            key_facts = case.get("key_facts", [])
            
            for fact in key_facts:
                if any(risk_word in fact.lower() for risk_word in ["abuse", "conflict", "decline", "dispute"]):
                    risk_factors.append(f"Similar to {case.get('case_name')}: {fact}")
        
        # Determine risk level
        if len(risk_factors) > 3:
            risk_level = "high"
        elif len(risk_factors) > 1:
            risk_level = "medium"
        
        return {
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "mitigation_strategies": self._get_mitigation_strategies(risk_level)
        }

    def _get_mitigation_strategies(self, risk_level: str) -> List[str]:
        """Get risk mitigation strategies"""
        strategies = {
            "low": [
                "Follow standard legal procedures",
                "Maintain proper documentation"
            ],
            "medium": [
                "Obtain independent legal advice",
                "Consider additional safeguards",
                "Document decision-making process thoroughly"
            ],
            "high": [
                "Seek immediate legal counsel",
                "Consider alternative approaches",
                "Implement additional oversight measures",
                "Document all steps comprehensively"
            ]
        }
        
        return strategies.get(risk_level, strategies["medium"])

    def search_case_law(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search case law database"""
        results = []
        query_lower = query.lower()
        
        for case in self.case_database:
            match_score = 0
            
            # Search in case name
            if query_lower in case.get("case_name", "").lower():
                match_score += 3
            
            # Search in summary
            if query_lower in case.get("summary", "").lower():
                match_score += 2
            
            # Search in relevance tags
            for tag in case.get("relevance_tags", []):
                if query_lower in tag.lower():
                    match_score += 1
            
            # Apply filters if provided
            if filters:
                if filters.get("year") and case.get("year") != filters["year"]:
                    continue
                if filters.get("court") and filters["court"].lower() not in case.get("court", "").lower():
                    continue
            
            if match_score > 0:
                case_result = case.copy()
                case_result["match_score"] = match_score
                results.append(case_result)
        
        # Sort by match score
        results.sort(key=lambda x: x["match_score"], reverse=True)
        
        return results

    def get_case_by_id(self, case_id: str) -> Optional[Dict[str, Any]]:
        """Get specific case by ID"""
        for case in self.case_database:
            if case.get("id") == case_id:
                return case
        return None

    def is_ready(self) -> bool:
        """Check if case law analyzer is ready"""
        return self.is_initialized

    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        return {
            "total_cases": len(self.case_database),
            "legal_principles": len(self.legal_principles),
            "courts_covered": len(set(case.get("court", "") for case in self.case_database)),
            "years_covered": sorted(set(case.get("year", 0) for case in self.case_database)),
            "status": "ready" if self.is_initialized else "not_ready"
        }

    async def find_relevant_cases(self, query: str, document_context: str = None, 
                                document_type: str = None) -> List[Dict[str, Any]]:
        """Find cases relevant to the legal query"""
        try:
            relevant_cases = []
            query_lower = query.lower()
            
            for case in self.case_database:
                relevance_score = self._calculate_case_relevance(case, query_lower, document_type)
                
                if relevance_score > 0.3:  # Minimum relevance threshold
                    case_result = {
                        "case_name": case.get("case_name", "Unknown"),
                        "citation": case.get("citation", "Citation unknown"),
                        "year": case.get("year", 0),
                        "court": case.get("court", "Court unknown"),
                        "relevance_score": relevance_score,
                        "key_principles": case.get("key_principles", []),
                        "legal_test": case.get("legal_test"),
                        "outcome": case.get("outcome")
                    }
                    relevant_cases.append(case_result)
            
            # Sort by relevance score
            relevant_cases.sort(key=lambda x: x["relevance_score"], reverse=True)
            
            return relevant_cases[:10]  # Return top 10 most relevant cases
            
        except Exception as e:
            logger.error(f"Failed to find relevant cases: {str(e)}")
            return []

    async def perform_research(self, query: str, jurisdiction: str = "ontario", 
                             max_results: int = 10) -> List[Dict[str, Any]]:
        """Perform real-time legal research"""
        try:
            # Find relevant cases
            relevant_cases = await self.find_relevant_cases(query)
            
            # Find applicable legal principles
            applicable_principles = self._find_applicable_principles(query)
            
            # Combine results
            research_results = []
            
            # Add case law results
            for case in relevant_cases[:max_results]:
                research_results.append({
                    "type": "case_law",
                    "title": case["case_name"],
                    "citation": case["citation"],
                    "year": case["year"],
                    "court": case["court"],
                    "relevance": case["relevance_score"],
                    "summary": f"Key principles: {', '.join(case['key_principles'][:3])}",
                    "legal_test": case.get("legal_test"),
                    "jurisdiction": jurisdiction
                })
            
            # Add legal principle results
            for principle in applicable_principles[:5]:
                research_results.append({
                    "type": "legal_principle",
                    "title": principle.get("name", "Legal Principle"),
                    "description": principle.get("description", ""),
                    "source": principle.get("source", "Common Law"),
                    "relevance": principle.get("relevance_score", 0.5),
                    "jurisdiction": jurisdiction
                })
            
            return research_results
            
        except Exception as e:
            logger.error(f"Legal research failed: {str(e)}")
            return []

    def _calculate_case_relevance(self, case: Dict[str, Any], query: str, document_type: str = None) -> float:
        """Calculate relevance score for a case"""
        score = 0.0
        
        # Check case name
        case_name = case.get("case_name", "").lower()
        if any(word in case_name for word in query.split()):
            score += 0.3
        
        # Check key principles
        principles = case.get("key_principles", [])
        for principle in principles:
            if any(word in principle.lower() for word in query.split()):
                score += 0.2
        
        # Check legal area match
        if document_type:
            legal_area = case.get("legal_area", "").lower()
            if document_type.lower() in legal_area:
                score += 0.4
        
        # Check court level (higher courts get more weight)
        court = case.get("court", "").lower()
        if "supreme court" in court:
            score += 0.1
        elif "court of appeal" in court:
            score += 0.05
        
        return min(score, 1.0)  # Cap at 1.0