"""
Enhanced AI Features for Legal Practice
Advanced AI-powered legal research, case prediction, and document analysis
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json

# Optional dependencies with fallbacks
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class LegalResearchResult:
    query: str
    relevant_cases: List[Dict[str, Any]]
    statutes: List[Dict[str, Any]]
    analysis: str
    confidence: float
    recommendations: List[str]

@dataclass
class CasePrediction:
    case_outcome: str
    probability: float
    key_factors: List[str]
    similar_cases: List[Dict[str, Any]]
    confidence_level: str

@dataclass
class DocumentAnalysis:
    document_type: str
    compliance_score: float
    legal_issues: List[str]
    recommendations: List[str]
    risk_assessment: Dict[str, Any]
    suggested_improvements: List[str]

class EnhancedAILegalService:
    """
    Advanced AI service for legal research, case prediction, and document analysis
    """
    
    def __init__(self):
        self.case_database = self._load_case_database()
        self.statute_database = self._load_statute_database()
        self.legal_precedents = self._load_legal_precedents()
        self.is_initialized = True
        
        # Initialize AI components
        self.legal_categories = {
            "wills_estates": "Wills and Estates",
            "poa": "Power of Attorney",
            "real_estate": "Real Estate",
            "family": "Family Law",
            "corporate": "Corporate Law",
            "civil_litigation": "Civil Litigation",
            "employment": "Employment Law",
            "contract": "Contract Law",
            "general": "General Legal"
        }
        
        # Mock NLP components (in real implementation, these would be initialized)
        self.legal_classifier = self._mock_legal_classifier
        self.nlp = self._mock_nlp_processor
        
    def _load_case_database(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load simulated case law database"""
        return {
            "estate_law": [
                {
                    "case_name": "Smith v. Estate of Johnson",
                    "citation": "2020 ONSC 123",
                    "summary": "Successful will challenge based on undue influence",
                    "key_factors": ["undue_influence", "capacity", "witness_credibility", "family_pressure"],
                    "outcome": "will_invalid",
                    "court": "Ontario Superior Court",
                    "year": 2020,
                    "estate_value": 500000
                },
                {
                    "case_name": "Brown Estate Re",
                    "citation": "2019 ONCA 456", 
                    "summary": "Proper executor appointment procedures",
                    "key_factors": ["executor_duties", "court_approval", "estate_administration"],
                    "outcome": "appointment_confirmed",
                    "court": "Court of Appeal for Ontario",
                    "year": 2019,
                    "estate_value": 250000
                },
                {
                    "case_name": "Thompson v. Thompson Estate",
                    "citation": "2021 ONSC 789",
                    "summary": "Will upheld despite capacity concerns",
                    "key_factors": ["medical_evidence", "proper_execution", "independent_legal_advice"],
                    "outcome": "will_upheld",
                    "court": "Ontario Superior Court", 
                    "year": 2021,
                    "estate_value": 750000
                },
                {
                    "case_name": "Wilson v. Wilson",
                    "citation": "2022 ONSC 234",
                    "summary": "Testamentary capacity successfully challenged",
                    "key_factors": ["dementia", "lack_of_capacity", "undue_influence", "suspicious_circumstances"],
                    "outcome": "will_invalid",
                    "court": "Ontario Superior Court",
                    "year": 2022,
                    "estate_value": 1200000
                },
                {
                    "case_name": "Davies Estate Re",
                    "citation": "2023 ONSC 345",
                    "summary": "Complex estate administration approved",
                    "key_factors": ["complex_assets", "multiple_beneficiaries", "proper_documentation"],
                    "outcome": "successful",
                    "court": "Ontario Superior Court",
                    "year": 2023,
                    "estate_value": 2000000
                }
            ],
            "poa_law": [
                {
                    "case_name": "Wilson v. Attorney General",
                    "citation": "2021 ONSC 789",
                    "summary": "POA validity requirements and capacity assessment",
                    "key_factors": ["mental_capacity", "witness_requirements", "attorney_duties"],
                    "outcome": "poa_valid",
                    "court": "Ontario Superior Court",
                    "year": 2021
                },
                {
                    "case_name": "Anderson v. Anderson POA",
                    "citation": "2020 ONSC 567",
                    "summary": "POA invalidated due to capacity issues",
                    "key_factors": ["lack_of_capacity", "no_independent_advice", "suspicious_circumstances"],
                    "outcome": "poa_invalid",
                    "court": "Ontario Superior Court",
                    "year": 2020
                },
                {
                    "case_name": "Public Guardian v. Roberts",
                    "citation": "2022 ONSC 123",
                    "summary": "Attorney breach of fiduciary duty",
                    "key_factors": ["financial_abuse", "conflict_of_interest", "inadequate_records"],
                    "outcome": "poa_revoked",
                    "court": "Ontario Superior Court",
                    "year": 2022
                },
                {
                    "case_name": "Miller POA Validation",
                    "citation": "2023 ONSC 456",
                    "summary": "Properly executed POA upheld",
                    "key_factors": ["proper_execution", "witness_present", "capacity_confirmed", "independent_advice"],
                    "outcome": "poa_valid",
                    "court": "Ontario Superior Court",
                    "year": 2023
                }
            ],
            "capacity_law": [
                {
                    "case_name": "Re: Mental Capacity Assessment",
                    "citation": "2021 ONSC 678",
                    "summary": "Standards for capacity assessment established",
                    "key_factors": ["medical_evaluation", "cognitive_testing", "functional_assessment"],
                    "outcome": "capacity_confirmed",
                    "court": "Ontario Superior Court",
                    "year": 2021
                },
                {
                    "case_name": "Johnson Capacity Challenge",
                    "citation": "2020 ONSC 890",
                    "summary": "Capacity found lacking for financial decisions",
                    "key_factors": ["dementia", "poor_judgment", "vulnerability"],
                    "outcome": "incapacity_found",
                    "court": "Ontario Superior Court",
                    "year": 2020
                }
            ]
        }
    
    def _load_statute_database(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load relevant Ontario statutes"""
        return {
            "estate_law": [
                {
                    "statute": "Succession Law Reform Act",
                    "section": "s. 3",
                    "description": "Requirements for valid will execution",
                    "key_provisions": ["age_requirement", "witness_requirements", "signature_requirements"]
                },
                {
                    "statute": "Estates Act",
                    "section": "s. 29",
                    "description": "Estate administration procedures",
                    "key_provisions": ["executor_duties", "court_oversight", "beneficiary_rights"]
                }
            ],
            "poa_law": [
                {
                    "statute": "Substitute Decisions Act",
                    "section": "s. 10",
                    "description": "Requirements for valid power of attorney",
                    "key_provisions": ["capacity_requirements", "witness_requirements", "attorney_duties"]
                }
            ]
        }
    
    def _load_legal_precedents(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load legal precedents and principles"""
        return {
            "will_execution": [
                {
                    "principle": "Proper witnessing is essential",
                    "authority": "Banks v. Goodfellow",
                    "application": "Two witnesses must be present simultaneously"
                }
            ],
            "capacity_assessment": [
                {
                    "principle": "Testamentary capacity test",
                    "authority": "Banks v. Goodfellow",
                    "application": "Must understand nature of act, extent of property, claims of beneficiaries"
                }
            ]
        }
    
    async def conduct_legal_research(self, query: str, document_type: str = None) -> LegalResearchResult:
        """Conduct AI-powered legal research"""
        try:
            logger.info(f"Conducting legal research for query: {query}")
            
            # Determine relevant legal area
            legal_area = self._classify_legal_area(query, document_type)
            
            # Search relevant cases
            relevant_cases = self._search_cases(query, legal_area)
            
            # Search relevant statutes
            relevant_statutes = self._search_statutes(query, legal_area)
            
            # Generate analysis
            analysis = await self._generate_legal_analysis(query, relevant_cases, relevant_statutes)
            
            # Calculate confidence score
            confidence = self._calculate_research_confidence(relevant_cases, relevant_statutes)
            
            # Generate recommendations
            recommendations = self._generate_research_recommendations(query, relevant_cases, relevant_statutes)
            
            return LegalResearchResult(
                query=query,
                relevant_cases=relevant_cases,
                statutes=relevant_statutes,
                analysis=analysis,
                confidence=confidence,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Legal research failed: {str(e)}")
            return LegalResearchResult(
                query=query,
                relevant_cases=[],
                statutes=[],
                analysis="Research analysis unavailable due to error",
                confidence=0.0,
                recommendations=["Consult with legal professional for detailed research"]
            )
    
    async def predict_case_outcome(self, case_facts: Dict[str, Any], case_type: str = None) -> Dict[str, Any]:
        """Predict case outcome based on Ontario precedents"""
        try:
            # Extract key facts
            key_facts = await self._extract_key_facts(case_facts)
            
            # Find similar cases
            similar_cases = await self._find_similar_cases(key_facts, case_type)
            
            # Analyze outcomes
            outcome_analysis = await self._analyze_case_outcomes(similar_cases)
            
            # Generate prediction
            prediction = await self._generate_outcome_prediction(
                key_facts, similar_cases, outcome_analysis
            )
            
            # Calculate confidence
            confidence = self._calculate_prediction_confidence(similar_cases, outcome_analysis)
            
            return {
                "case_type": case_type,
                "key_facts": key_facts,
                "similar_cases": similar_cases[:5],
                "outcome_prediction": prediction,
                "confidence_score": confidence,
                "risk_factors": prediction.get("risk_factors", []),
                "settlement_recommendation": prediction.get("settlement_recommendation"),
                "estimated_timeline": prediction.get("estimated_timeline"),
                "prediction_date": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Case outcome prediction failed: {str(e)}")
            raise
    
    async def analyze_document(self, document_type: str, document_content: Dict[str, Any]) -> DocumentAnalysis:
        """Perform comprehensive document analysis"""
        try:
            logger.info(f"Analyzing {document_type} document")
            
            # Calculate compliance score
            compliance_score = await self._calculate_compliance_score(document_type, document_content)
            
            # Identify legal issues
            legal_issues = self._identify_legal_issues(document_type, document_content)
            
            # Generate recommendations
            recommendations = self._generate_document_recommendations(document_type, document_content, legal_issues)
            
            # Perform risk assessment
            risk_assessment = await self._perform_risk_assessment(document_type, document_content)
            
            # Suggest improvements
            suggested_improvements = self._suggest_improvements(document_type, document_content, compliance_score)
            
            return DocumentAnalysis(
                document_type=document_type,
                compliance_score=compliance_score,
                legal_issues=legal_issues,
                recommendations=recommendations,
                risk_assessment=risk_assessment,
                suggested_improvements=suggested_improvements
            )
            
        except Exception as e:
            logger.error(f"Document analysis failed: {str(e)}")
            return DocumentAnalysis(
                document_type=document_type,
                compliance_score=0.0,
                legal_issues=["Analysis error occurred"],
                recommendations=["Manual review recommended"],
                risk_assessment={"error": "Analysis failed"},
                suggested_improvements=["Professional legal review required"]
            )
    
    def _classify_legal_area(self, query: str, document_type: str = None) -> str:
        """Classify query into legal area"""
        query_lower = query.lower()
        
        if document_type:
            if "will" in document_type:
                return "estate_law"
            elif "poa" in document_type:
                return "poa_law"
        
        # Keyword-based classification
        if any(keyword in query_lower for keyword in ["will", "estate", "executor", "beneficiary"]):
            return "estate_law"
        elif any(keyword in query_lower for keyword in ["power of attorney", "poa", "attorney", "substitute decision"]):
            return "poa_law"
        
        return "general"
    
    def _search_cases(self, query: str, legal_area: str) -> List[Dict[str, Any]]:
        """Search for relevant cases"""
        cases = self.case_database.get(legal_area, [])
        query_terms = query.lower().split()
        
        relevant_cases = []
        for case in cases:
            # Simple relevance scoring based on keyword matching
            relevance_score = 0
            case_text = f"{case['case_name']} {case['summary']} {' '.join(case['key_factors'])}".lower()
            
            for term in query_terms:
                if term in case_text:
                    relevance_score += 1
            
            if relevance_score > 0:
                case_copy = case.copy()
                case_copy['relevance_score'] = relevance_score
                relevant_cases.append(case_copy)
        
        # Sort by relevance
        relevant_cases.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return relevant_cases[:5]  # Return top 5 most relevant cases
    
    def _search_statutes(self, query: str, legal_area: str) -> List[Dict[str, Any]]:
        """Search for relevant statutes"""
        statutes = self.statute_database.get(legal_area, [])
        query_terms = query.lower().split()
        
        relevant_statutes = []
        for statute in statutes:
            # Simple relevance scoring
            relevance_score = 0
            statute_text = f"{statute['statute']} {statute['description']} {' '.join(statute['key_provisions'])}".lower()
            
            for term in query_terms:
                if term in statute_text:
                    relevance_score += 1
            
            if relevance_score > 0:
                statute_copy = statute.copy()
                statute_copy['relevance_score'] = relevance_score
                relevant_statutes.append(statute_copy)
        
        relevant_statutes.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return relevant_statutes[:3]  # Return top 3 most relevant statutes
    
    async def _generate_legal_analysis(self, query: str, cases: List[Dict[str, Any]], statutes: List[Dict[str, Any]]) -> str:
        """Generate comprehensive legal analysis"""
        analysis_parts = [
            f"Legal Analysis for: {query}",
            "",
            "CASE LAW ANALYSIS:"
        ]
        
        if cases:
            for case in cases:
                analysis_parts.append(f"- {case['case_name']}: {case['summary']}")
        else:
            analysis_parts.append("- No directly relevant cases found in database")
        
        analysis_parts.extend([
            "",
            "STATUTORY ANALYSIS:"
        ])
        
        if statutes:
            for statute in statutes:
                analysis_parts.append(f"- {statute['statute']} {statute['section']}: {statute['description']}")
        else:
            analysis_parts.append("- No directly relevant statutes found in database")
        
        analysis_parts.extend([
            "",
            "LEGAL CONCLUSIONS:",
            "Based on the available case law and statutory provisions, this analysis provides guidance on the legal issues identified. For definitive legal advice, consultation with a qualified Ontario lawyer is recommended."
        ])
        
        return "\n".join(analysis_parts)
    
    def _calculate_research_confidence(self, cases: List[Dict[str, Any]], statutes: List[Dict[str, Any]]) -> float:
        """Calculate confidence score for research results"""
        case_score = min(len(cases) * 0.2, 0.6)  # Max 0.6 for cases
        statute_score = min(len(statutes) * 0.15, 0.4)  # Max 0.4 for statutes
        
        return case_score + statute_score
    
    def _generate_research_recommendations(self, query: str, cases: List[Dict[str, Any]], statutes: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on research"""
        recommendations = []
        
        if cases:
            recommendations.append("Review identified case precedents for similar fact patterns")
        
        if statutes:
            recommendations.append("Ensure compliance with relevant statutory requirements")
        
        recommendations.extend([
            "Consider consulting with a qualified Ontario lawyer",
            "Review current legal developments in this area",
            "Document all relevant facts and circumstances"
        ])
        
        return recommendations
    
    def _extract_key_factors(self, case_facts: Dict[str, Any], legal_issue: str) -> List[str]:
        """Extract key factors from case facts"""
        factors = []
        
        # Common factors for different legal issues
        if "will" in legal_issue.lower():
            if case_facts.get("testator_age"):
                factors.append(f"testator_age_{case_facts['testator_age']}")
            if case_facts.get("witnesses_present"):
                factors.append("proper_witnessing")
            if case_facts.get("capacity_concerns"):
                factors.append("capacity_issues")
        
        elif "poa" in legal_issue.lower():
            if case_facts.get("grantor_capacity"):
                factors.append("grantor_capacity")
            if case_facts.get("witness_present"):
                factors.append("witness_present")
            if case_facts.get("attorney_relationship"):
                factors.append(f"attorney_{case_facts['attorney_relationship']}")
        
        return factors
    
    def _find_similar_cases(self, case_facts: Dict[str, Any], legal_issue: str) -> List[Dict[str, Any]]:
        """Find similar cases based on facts"""
        legal_area = self._classify_legal_area(legal_issue)
        cases = self.case_database.get(legal_area, [])
        
        similar_cases = []
        key_factors = self._extract_key_factors(case_facts, legal_issue)
        
        for case in cases:
            similarity_score = 0
            for factor in key_factors:
                if factor in case.get('key_factors', []):
                    similarity_score += 1
            
            if similarity_score > 0:
                case_copy = case.copy()
                case_copy['similarity_score'] = similarity_score
                similar_cases.append(case_copy)
        
        similar_cases.sort(key=lambda x: x['similarity_score'], reverse=True)
        return similar_cases[:3]
    
    def _predict_outcome(self, key_factors: List[str], similar_cases: List[Dict[str, Any]]) -> tuple:
        """Predict case outcome based on factors and similar cases"""
        if not similar_cases:
            return "uncertain", 0.5
        
        # Simple prediction based on similar case outcomes
        outcomes = [case['outcome'] for case in similar_cases]
        most_common_outcome = max(set(outcomes), key=outcomes.count)
        
        # Calculate probability based on similarity
        total_similarity = sum(case['similarity_score'] for case in similar_cases)
        matching_similarity = sum(
            case['similarity_score'] for case in similar_cases 
            if case['outcome'] == most_common_outcome
        )
        
        probability = matching_similarity / total_similarity if total_similarity > 0 else 0.5
        
        return most_common_outcome, probability
    
    def _determine_confidence_level(self, probability: float, num_similar_cases: int) -> str:
        """Determine confidence level for prediction"""
        if num_similar_cases >= 3 and probability >= 0.8:
            return "high"
        elif num_similar_cases >= 2 and probability >= 0.6:
            return "medium"
        else:
            return "low"
    
    async def _calculate_compliance_score(self, document_type: str, content: Dict[str, Any]) -> float:
        """Calculate document compliance score"""
        score = 0.0
        max_score = 100.0
        
        if document_type == "will":
            # Check essential elements
            if content.get("testator_name"):
                score += 20
            if content.get("executor_name"):
                score += 20
            if content.get("beneficiaries"):
                score += 20
            if content.get("signature_date"):
                score += 15
            if content.get("witnesses"):
                score += 25
        
        elif "poa" in document_type:
            # Check POA elements
            if content.get("grantor_name"):
                score += 25
            if content.get("attorney_name"):
                score += 25
            if content.get("powers_specified"):
                score += 25
            if content.get("signature_date"):
                score += 15
            if content.get("witness"):
                score += 10
        
        return score / max_score
    
    def _identify_legal_issues(self, document_type: str, content: Dict[str, Any]) -> List[str]:
        """Identify potential legal issues in document"""
        issues = []
        
        if document_type == "will":
            if not content.get("witnesses") or len(content.get("witnesses", [])) < 2:
                issues.append("Insufficient witnesses (minimum 2 required)")
            
            if not content.get("executor_name"):
                issues.append("No executor appointed")
            
            if not content.get("residuary_clause"):
                issues.append("Missing residuary clause")
        
        elif "poa" in document_type:
            if not content.get("witness"):
                issues.append("Missing witness signature")
            
            if not content.get("powers_specified"):
                issues.append("Powers not clearly specified")
            
            if document_type == "poa_property" and not content.get("substitute_attorney"):
                issues.append("Consider appointing substitute attorney")
        
        return issues
    
    def _generate_document_recommendations(self, document_type: str, content: Dict[str, Any], issues: List[str]) -> List[str]:
        """Generate recommendations for document improvement"""
        recommendations = []
        
        if issues:
            recommendations.append("Address identified legal issues before finalization")
        
        if document_type == "will":
            recommendations.extend([
                "Ensure proper execution with two witnesses present simultaneously",
                "Consider appointing alternate executor",
                "Review beneficiary designations for completeness"
            ])
        
        elif "poa" in document_type:
            recommendations.extend([
                "Verify grantor capacity at time of execution",
                "Ensure witness understands their role and responsibilities",
                "Consider specific instructions for attorney guidance"
            ])
        
        recommendations.append("Have document reviewed by qualified Ontario lawyer")
        
        return recommendations
    
    async def _perform_risk_assessment(self, document_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive risk assessment"""
        risks = {
            "high_risk": [],
            "medium_risk": [],
            "low_risk": [],
            "overall_risk_level": "low"
        }
        
        if document_type == "will":
            if not content.get("witnesses") or len(content.get("witnesses", [])) < 2:
                risks["high_risk"].append("Invalid execution due to insufficient witnesses")
            
            if content.get("complex_bequests"):
                risks["medium_risk"].append("Complex bequest provisions may require clarification")
        
        elif "poa" in document_type:
            if not content.get("capacity_assessment"):
                risks["medium_risk"].append("Grantor capacity not formally assessed")
        
        # Determine overall risk level
        if risks["high_risk"]:
            risks["overall_risk_level"] = "high"
        elif risks["medium_risk"]:
            risks["overall_risk_level"] = "medium"
        
        return risks
    
    def _suggest_improvements(self, document_type: str, content: Dict[str, Any], compliance_score: float) -> List[str]:
        """Suggest specific improvements for document"""
        improvements = []
        
        if compliance_score < 0.8:
            improvements.append("Address missing required elements to improve compliance")
        
        if document_type == "will":
            improvements.extend([
                "Consider adding specific funeral and burial instructions",
                "Review tax implications of bequests",
                "Ensure all assets are addressed in distribution scheme"
            ])
        
        elif "poa" in document_type:
            improvements.extend([
                "Consider adding detailed care preferences (for personal care POA)",
                "Specify any limitations on attorney's powers",
                "Include instructions for capacity assessment"
            ])
        
        return improvements

    async def _extract_key_facts(self, case_facts: Dict[str, Any]) -> List[str]:
        """Extract key facts from case data for prediction"""
        key_facts = []
        
        # Extract factual elements
        if "facts" in case_facts:
            if isinstance(case_facts["facts"], list):
                key_facts.extend(case_facts["facts"])
            else:
                key_facts.extend(case_facts["facts"].split(". "))
        
        # Extract party information
        if "parties" in case_facts:
            for party in case_facts["parties"]:
                if isinstance(party, dict):
                    key_facts.append(f"Party: {party.get('name', 'Unknown')} - {party.get('role', 'Unknown role')}")
                else:
                    key_facts.append(f"Party: {party}")
        
        # Extract legal issues
        if "legal_issues" in case_facts:
            if isinstance(case_facts["legal_issues"], list):
                key_facts.extend([f"Legal issue: {issue}" for issue in case_facts["legal_issues"]])
            else:
                key_facts.append(f"Legal issue: {case_facts['legal_issues']}")
        
        # Extract financial information
        if "estate_value" in case_facts:
            key_facts.append(f"Estate value: ${case_facts['estate_value']}")
        
        # Extract capacity issues
        if "capacity_concerns" in case_facts:
            key_facts.append(f"Capacity concerns: {case_facts['capacity_concerns']}")
        
        # Extract witness information
        if "witnesses" in case_facts:
            key_facts.append(f"Witnesses: {len(case_facts['witnesses'])} present")
        
        return key_facts
    
    async def _find_similar_cases(self, key_facts: List[str], case_type: str) -> List[Dict[str, Any]]:
        """Find similar cases based on key facts and case type"""
        # Determine legal area
        legal_area = self._classify_case_type(case_type) if case_type else "general"
        cases = self.case_database.get(legal_area, [])
        
        similar_cases = []
        
        for case in cases:
            similarity_score = self._calculate_case_similarity(key_facts, case)
            
            if similarity_score > 0:
                case_copy = case.copy()
                case_copy['similarity_score'] = similarity_score
                case_copy['relevance_percentage'] = min(similarity_score * 20, 100)  # Convert to percentage
                similar_cases.append(case_copy)
        
        # Sort by similarity score
        similar_cases.sort(key=lambda x: x['similarity_score'], reverse=True)
        return similar_cases[:10]  # Return top 10 most similar cases
    
    def _classify_case_type(self, case_type: str) -> str:
        """Classify case type into legal area"""
        if not case_type:
            return "general"
        
        case_type_lower = case_type.lower()
        
        if any(keyword in case_type_lower for keyword in ["will", "estate", "probate", "testamentary"]):
            return "estate_law"
        elif any(keyword in case_type_lower for keyword in ["poa", "power of attorney", "substitute"]):
            return "poa_law"
        elif any(keyword in case_type_lower for keyword in ["capacity", "mental", "cognitive"]):
            return "capacity_law"
        else:
            return "general"
    
    def _calculate_case_similarity(self, key_facts: List[str], case: Dict[str, Any]) -> float:
        """Calculate similarity between current case facts and database case"""
        similarity_score = 0.0
        
        # Get case text for comparison
        case_text = f"{case.get('summary', '')} {' '.join(case.get('key_factors', []))}"
        case_text_lower = case_text.lower()
        
        # Check for keyword matches
        for fact in key_facts:
            fact_lower = fact.lower()
            words = fact_lower.split()
            
            for word in words:
                if len(word) > 3 and word in case_text_lower:  # Only count meaningful words
                    similarity_score += 0.1
        
        # Bonus for exact phrase matches
        for fact in key_facts:
            if fact.lower() in case_text_lower:
                similarity_score += 0.5
        
        return similarity_score
    
    async def _analyze_case_outcomes(self, similar_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze outcomes of similar cases"""
        if not similar_cases:
            return {
                "outcome_distribution": {},
                "success_rate": 0.5,
                "common_factors": [],
                "risk_indicators": []
            }
        
        # Analyze outcome distribution
        outcomes = {}
        total_weight = 0
        
        for case in similar_cases:
            outcome = case.get('outcome', 'unknown')
            weight = case.get('similarity_score', 1.0)
            
            if outcome not in outcomes:
                outcomes[outcome] = 0
            outcomes[outcome] += weight
            total_weight += weight
        
        # Normalize outcomes
        outcome_distribution = {}
        if total_weight > 0:
            for outcome, weight in outcomes.items():
                outcome_distribution[outcome] = weight / total_weight
        
        # Calculate success rate (assuming positive outcomes)
        positive_outcomes = ["will_upheld", "poa_valid", "successful", "favorable", "approved"]
        success_rate = sum(outcome_distribution.get(outcome, 0) for outcome in positive_outcomes)
        
        # Extract common factors
        common_factors = self._extract_common_factors(similar_cases)
        
        # Identify risk indicators
        risk_indicators = self._identify_risk_indicators(similar_cases)
        
        return {
            "outcome_distribution": outcome_distribution,
            "success_rate": success_rate,
            "common_factors": common_factors,
            "risk_indicators": risk_indicators,
            "total_cases_analyzed": len(similar_cases)
        }
    
    def _extract_common_factors(self, similar_cases: List[Dict[str, Any]]) -> List[str]:
        """Extract common factors from similar cases"""
        factor_counts = {}
        
        for case in similar_cases:
            for factor in case.get('key_factors', []):
                if factor not in factor_counts:
                    factor_counts[factor] = 0
                factor_counts[factor] += case.get('similarity_score', 1.0)
        
        # Return factors that appear in multiple cases
        threshold = len(similar_cases) * 0.3  # At least 30% of cases
        common_factors = [factor for factor, count in factor_counts.items() if count >= threshold]
        
        return sorted(common_factors, key=lambda f: factor_counts[f], reverse=True)[:5]
    
    def _identify_risk_indicators(self, similar_cases: List[Dict[str, Any]]) -> List[str]:
        """Identify risk indicators from case analysis"""
        risk_indicators = []
        
        # Analyze cases with negative outcomes
        negative_outcomes = ["will_invalid", "poa_invalid", "unsuccessful", "dismissed", "denied"]
        
        for case in similar_cases:
            if case.get('outcome') in negative_outcomes:
                # Extract factors that led to negative outcomes
                for factor in case.get('key_factors', []):
                    if any(risk_word in factor.lower() for risk_word in 
                          ["undue influence", "lack of capacity", "improper execution", "conflict", "fraud"]):
                        risk_indicators.append(factor)
        
        return list(set(risk_indicators))  # Remove duplicates
    
    async def _generate_outcome_prediction(self, key_facts: List[str], similar_cases: List[Dict[str, Any]], 
                                         outcome_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive outcome prediction"""
        outcome_distribution = outcome_analysis.get("outcome_distribution", {})
        success_rate = outcome_analysis.get("success_rate", 0.5)
        
        # Determine most likely outcome
        if outcome_distribution:
            predicted_outcome = max(outcome_distribution.keys(), key=lambda k: outcome_distribution[k])
            probability = outcome_distribution[predicted_outcome]
        else:
            predicted_outcome = "uncertain"
            probability = 0.5
        
        # Generate risk factors
        risk_factors = outcome_analysis.get("risk_indicators", [])
        
        # Generate settlement recommendation
        settlement_recommendation = self._generate_settlement_recommendation(
            predicted_outcome, probability, risk_factors
        )
        
        # Estimate timeline
        estimated_timeline = self._estimate_case_timeline(predicted_outcome, key_facts)
        
        return {
            "predicted_outcome": predicted_outcome,
            "probability": probability,
            "risk_factors": risk_factors,
            "settlement_recommendation": settlement_recommendation,
            "estimated_timeline": estimated_timeline,
            "key_strengths": self._identify_case_strengths(key_facts, similar_cases),
            "key_weaknesses": self._identify_case_weaknesses(key_facts, risk_factors)
        }
    
    def _generate_settlement_recommendation(self, predicted_outcome: str, probability: float, 
                                          risk_factors: List[str]) -> Dict[str, Any]:
        """Generate settlement recommendation based on prediction"""
        if probability < 0.6 or len(risk_factors) > 2:
            return {
                "recommendation": "Consider settlement",
                "reasoning": "High risk of unfavorable outcome or significant risk factors present",
                "settlement_range": "60-80% of claimed amount",
                "priority": "high"
            }
        elif probability < 0.8:
            return {
                "recommendation": "Evaluate settlement options",
                "reasoning": "Moderate certainty of outcome warrants settlement consideration",
                "settlement_range": "75-90% of claimed amount",
                "priority": "medium"
            }
        else:
            return {
                "recommendation": "Proceed with litigation",
                "reasoning": "High probability of favorable outcome",
                "settlement_range": "90-100% of claimed amount",
                "priority": "low"
            }
    
    def _estimate_case_timeline(self, predicted_outcome: str, key_facts: List[str]) -> Dict[str, Any]:
        """Estimate case timeline based on complexity and predicted outcome"""
        base_timeline = 6  # months
        
        # Adjust based on complexity
        complexity_factors = ["capacity", "undue influence", "multiple parties", "complex estate"]
        complexity_score = sum(1 for factor in complexity_factors 
                             if any(factor in fact.lower() for fact in key_facts))
        
        timeline_months = base_timeline + (complexity_score * 3)
        
        if "settlement" in predicted_outcome.lower():
            timeline_months = timeline_months // 2  # Settlements are faster
        
        return {
            "estimated_months": timeline_months,
            "phases": {
                "discovery": f"{timeline_months // 3} months",
                "mediation": f"{timeline_months // 4} months", 
                "trial_prep": f"{timeline_months // 3} months",
                "trial": "2-4 weeks"
            },
            "factors_affecting_timeline": [
                "Court scheduling",
                "Discovery complexity",
                "Settlement negotiations",
                "Expert witness availability"
            ]
        }
    
    def _identify_case_strengths(self, key_facts: List[str], similar_cases: List[Dict[str, Any]]) -> List[str]:
        """Identify strengths in the case"""
        strengths = []
        
        # Look for positive indicators in facts
        positive_indicators = ["proper execution", "witnesses present", "capacity assessment", 
                             "independent legal advice", "medical evaluation"]
        
        for fact in key_facts:
            for indicator in positive_indicators:
                if indicator in fact.lower():
                    strengths.append(f"Strong evidence: {fact}")
        
        # Check if similar successful cases share characteristics
        successful_cases = [case for case in similar_cases 
                          if case.get('outcome') in ["will_upheld", "poa_valid", "successful"]]
        
        if len(successful_cases) > len(similar_cases) // 2:
            strengths.append("Favorable precedents in similar cases")
        
        return strengths[:5]  # Limit to top 5 strengths
    
    def _identify_case_weaknesses(self, key_facts: List[str], risk_factors: List[str]) -> List[str]:
        """Identify weaknesses in the case"""
        weaknesses = []
        
        # Add risk factors as weaknesses
        weaknesses.extend(risk_factors)
        
        # Look for weakness indicators in facts
        weakness_indicators = ["no witnesses", "capacity concerns", "family dispute", 
                             "late will changes", "beneficiary involved in preparation"]
        
        for fact in key_facts:
            for indicator in weakness_indicators:
                if indicator in fact.lower():
                    weaknesses.append(f"Potential issue: {fact}")
        
        return weaknesses[:5]  # Limit to top 5 weaknesses
    
    def _calculate_prediction_confidence(self, similar_cases: List[Dict[str, Any]], 
                                       outcome_analysis: Dict[str, Any]) -> float:
        """Calculate confidence score for the prediction"""
        if not similar_cases:
            return 0.3  # Low confidence with no similar cases
        
        # Base confidence on number of similar cases
        case_confidence = min(len(similar_cases) * 0.1, 0.6)
        
        # Adjust based on outcome distribution clarity
        outcome_distribution = outcome_analysis.get("outcome_distribution", {})
        if outcome_distribution:
            max_probability = max(outcome_distribution.values())
            distribution_confidence = max_probability * 0.4
        else:
            distribution_confidence = 0.1
        
        # Adjust based on similarity scores
        avg_similarity = sum(case.get('similarity_score', 0) for case in similar_cases) / len(similar_cases)
        similarity_confidence = min(avg_similarity * 0.1, 0.2)
        
        total_confidence = case_confidence + distribution_confidence + similarity_confidence
        return min(total_confidence, 0.95)  # Cap at 95% confidence

    async def _classify_legal_area(self, text: str) -> str:
        """Classify text into legal area"""
        try:
            # Use zero-shot classification
            candidate_labels = list(self.legal_categories.keys())
            result = self.legal_classifier(text, candidate_labels)
            
            # Return highest confidence category
            if result["scores"][0] > 0.3:  # Threshold
                return result["labels"][0]
            return "general"
        except Exception as e:
            logger.error(f"Legal area classification failed: {str(e)}")
            return "general"

    def _extract_legal_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract legal entities from text"""
        try:
            doc = self.nlp(text)
            entities = []
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                })
            return entities
        except Exception as e:
            logger.error(f"Entity extraction failed: {str(e)}")
            return []

    async def _get_relevant_statutes(self, legal_area: str, entities: List[Dict[str, Any]]) -> List[str]:
        """Get relevant Ontario statutes"""
        try:
            # Map legal areas to statutes
            statute_map = {
                "wills_estates": ["Wills Act", "Succession Law Reform Act", "Estates Act"],
                "real_estate": ["Land Titles Act", "Registry Act", "Conveyancing and Law of Property Act"],
                "corporate": ["Business Corporations Act", "Corporations Act"],
                "family": ["Family Law Act", "Children's Law Reform Act", "Divorce Act (Canada)"],
                "civil_litigation": ["Courts of Justice Act", "Rules of Civil Procedure"],
                "employment": ["Employment Standards Act", "Human Rights Code"],
                "contract": ["Consumer Protection Act", "Business Practices Act"],
                "poa": ["Substitute Decisions Act", "Health Care Consent Act"]
            }
            return statute_map.get(legal_area, ["General statute research required"])
        except Exception as e:
            logger.error(f"Statute retrieval failed: {str(e)}")
            return []

    async def _get_relevant_case_law(self, legal_area: str, entities: List[Dict[str, Any]]) -> List[str]:
        """Get relevant Ontario case law"""
        try:
            # This would integrate with actual case law database
            case_law_map = {
                "wills_estates": ["Banks v. Goodfellow", "Re: Smith Estate", "Johnson v. Johnson"],
                "real_estate": ["Toronto-Dominion Bank v. Wise", "Ferguson v. Ferguson"],
                "family": ["Miglin v. Miglin", "Chamberlain v. Chamberlain"],
                "employment": ["Wallace v. United Grain Growers", "Honda Canada Inc. v. Keays"],
                "contract": ["Tercon Contractors Ltd. v. British Columbia", "BG Checo International Ltd. v. British Columbia Hydro"]
            }
            return case_law_map.get(legal_area, ["Case law research required"])
        except Exception as e:
            logger.error(f"Case law retrieval failed: {str(e)}")
            return []

    async def _generate_legal_analysis(self, question: str, legal_area: str, entities: List[Dict[str, Any]],
                                     statutes: List[str], case_law: List[str]) -> Dict[str, Any]:
        """Generate legal analysis"""
        try:
            # Create analysis prompt
            analysis_prompt = f"""
    Analyze this Ontario legal question: {question}
    Legal Area: {legal_area}
    Key Entities: {json.dumps(entities)}
    Relevant Statutes: {json.dumps(statutes)}  
    Relevant Case Law: {json.dumps(case_law)}
    Provide:
    1. Legal analysis
    2. Applicable law
    3. Key considerations
    4. Warnings
    5. Recommendations
    """
            
            # Generate analysis (simplified)
            analysis = {
                "answer": f"Based on Ontario law regarding {legal_area}, here's the analysis...",
                "confidence": 0.8,
                "warnings": ["This is AI-generated analysis - consult with a lawyer"],
                "recommendations": ["Seek professional legal advice for your specific situation"]
            }
            return analysis
        except Exception as e:
            logger.error(f"Legal analysis generation failed: {str(e)}")
            return {
                "answer": "Unable to generate analysis",
                "confidence": 0.0,
                "warnings": ["Analysis failed"],
                "recommendations": ["Consult with a lawyer"]
            }

    async def _get_document_template(self, document_type: str) -> Dict[str, Any]:
        """Get document template for Ontario"""
        templates = {
            "will": {
                "title": "Last Will and Testament",
                "required_sections": ["identification", "revocation", "appointment", "distribution", "execution"],
                "optional_sections": ["guardian", "trust", "charitable_bequests"]
            },
            "poa_property": {
                "title": "Power of Attorney for Property", 
                "required_sections": ["appointment", "powers", "limitations", "execution"],
                "optional_sections": ["substitute_attorney", "compensation", "reporting"]
            },
            "poa_personal_care": {
                "title": "Power of Attorney for Personal Care",
                "required_sections": ["appointment", "healthcare_powers", "limitations", "execution"],
                "optional_sections": ["living_will", "organ_donation", "mental_health"]
            }
        }
        return templates.get(document_type, {"title": "Legal Document", "required_sections": [], "optional_sections": []})

    async def _analyze_document_requirements(self, document_type: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze document requirements"""
        try:
            analyzed = {
                "document_type": document_type,
                "complexity": "standard",
                "estimated_time": 30,  # minutes
                "required_information": [],
                "optional_information": [],
                "compliance_requirements": []
            }
            
            # Analyze based on document type
            if document_type == "will":
                analyzed["required_information"] = ["client_assets", "beneficiaries", "executor", "guardian"]
                analyzed["compliance_requirements"] = ["witness_requirements", "execution_requirements"]
                analyzed["complexity"] = "high" if len(requirements.get("assets", [])) > 10 else "standard"
            
            return analyzed
        except Exception as e:
            logger.error(f"Document requirements analysis failed: {str(e)}")
            return {"error": str(e)}

    async def _generate_document_draft(self, template: Dict[str, Any], requirements: Dict[str, Any]) -> str:
        """Generate document draft"""
        try:
            # Create draft based on template and requirements
            draft_content = f"""
    {template['title']}
    
    This document is drafted based on the following requirements:
    {json.dumps(requirements, indent=2)}
    
    [Document content would be generated here with proper legal language]
    """
            return draft_content
        except Exception as e:
            logger.error(f"Document draft generation failed: {str(e)}")
            return "Document draft generation failed"

    def is_ready(self) -> bool:
        return self.is_initialized

    def _mock_legal_classifier(self, text: str, candidate_labels: List[str]) -> Dict[str, Any]:
        """Mock legal classifier for testing"""
        # Simple keyword-based classification
        text_lower = text.lower()
        scores = []
        
        for label in candidate_labels:
            score = 0.0
            if "will" in text_lower and "wills_estates" in label:
                score = 0.8
            elif "poa" in text_lower or "power of attorney" in text_lower and "poa" in label:
                score = 0.8
            elif "family" in text_lower and "family" in label:
                score = 0.7
            else:
                score = 0.3
            scores.append(score)
        
        # Sort by score
        sorted_pairs = sorted(zip(candidate_labels, scores), key=lambda x: x[1], reverse=True)
        
        return {
            "labels": [pair[0] for pair in sorted_pairs],
            "scores": [pair[1] for pair in sorted_pairs]
        }

    def _mock_nlp_processor(self, text: str):
        """Mock NLP processor for entity extraction"""
        class MockEntity:
            def __init__(self, text, label, start, end):
                self.text = text
                self.label_ = label
                self.start_char = start
                self.end_char = end
        
        class MockDoc:
            def __init__(self, text):
                self.ents = []
                # Simple entity extraction based on patterns
                import re
                
                # Find person names (capitalized words)
                person_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
                for match in re.finditer(person_pattern, text):
                    self.ents.append(MockEntity(match.group(), 'PERSON', match.start(), match.end()))
                
                # Find dates
                date_pattern = r'\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}/\d{4}\b'
                for match in re.finditer(date_pattern, text):
                    self.ents.append(MockEntity(match.group(), 'DATE', match.start(), match.end()))
        
        return MockDoc(text)