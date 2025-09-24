"""
Enhanced AI Legal Service with advanced Ontario legal intelligence
Implements advanced AI capabilities for legal document generation and analysis
"""

try:
    import spacy
    from transformers import pipeline
    ADVANCED_NLP_AVAILABLE = True
except ImportError:
    ADVANCED_NLP_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import asyncio

from .ai_engine import OntarioLegalAIEngine
from .legal_knowledge import OntarioLegalKnowledgeBase
from .case_law_analyzer import OntarioCaseLawAnalyzer

logger = logging.getLogger(__name__)

@dataclass
class DocumentAnalysis:
    """Comprehensive document analysis result"""
    document_type: str
    compliance_score: float
    risk_level: str
    issues: List[Dict[str, Any]]
    recommendations: List[str]
    legal_requirements: List[Dict[str, Any]]
    case_law_guidance: Dict[str, Any]
    ai_insights: Dict[str, Any]
    confidence: float
    processing_time: float

class EnhancedAILegalService:
    """Enhanced AI-powered legal service for Ontario documents"""
    
    def __init__(self):
        self.ai_engine = OntarioLegalAIEngine()
        self.legal_kb = OntarioLegalKnowledgeBase()
        self.case_law_analyzer = OntarioCaseLawAnalyzer()
        self.is_initialized = False
        
        # Advanced AI models
        self.legal_classifier = None
        self.sentence_transformer = None
        self.openai_client = None
        
        # Legal-specific NLP pipeline
        self.legal_ner_pipeline = None
        self.compliance_pipeline = None
        
    async def initialize(self):
        """Initialize all AI components"""
        try:
            logger.info("Initializing Enhanced AI Legal Service...")
            
            # Initialize core components
            await self.ai_engine.initialize()
            await self.legal_kb.initialize()
            await self.case_law_analyzer.initialize()
            
            # Initialize advanced AI models
            await self._initialize_advanced_models()
            
            self.is_initialized = True
            logger.info("Enhanced AI Legal Service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Enhanced AI Legal Service: {str(e)}")
            self.is_initialized = False
            
    async def _initialize_advanced_models(self):
        """Initialize advanced AI models with error handling"""
        if ADVANCED_NLP_AVAILABLE:
            try:
                # Legal document classifier
                self.legal_classifier = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli"
                )
                
                # Legal NER pipeline
                self.legal_ner_pipeline = pipeline(
                    "ner",
                    model="dbmdz/bert-large-cased-finetuned-conll03-english",
                    aggregation_strategy="simple"
                )
                
                logger.info("Advanced NLP models loaded successfully")
                
            except Exception as e:
                logger.warning(f"Failed to load advanced NLP models: {str(e)}")
        
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.sentence_transformer = SentenceTransformer('all-mpnet-base-v2')
                logger.info("Sentence transformer loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load sentence transformer: {str(e)}")
        
        if OPENAI_AVAILABLE:
            try:
                # Initialize OpenAI client if API key is available
                import os
                if os.getenv("OPENAI_API_KEY"):
                    self.openai_client = openai.OpenAI()
                    logger.info("OpenAI client initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {str(e)}")

    def analyze_document(self, document_type: str, content: Dict[str, Any]) -> DocumentAnalysis:
        """Comprehensive document analysis using advanced AI"""
        start_time = datetime.now()
        
        try:
            # Perform multi-layered analysis
            compliance_analysis = self._analyze_compliance(document_type, content)
            risk_assessment = self._assess_risk(document_type, content)
            legal_requirements = self._extract_legal_requirements(document_type, content)
            case_law_guidance = self._get_case_law_guidance(document_type, content)
            ai_insights = self._generate_ai_insights(document_type, content)
            
            # Calculate overall confidence
            confidence = self._calculate_confidence(
                compliance_analysis, risk_assessment, ai_insights
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return DocumentAnalysis(
                document_type=document_type,
                compliance_score=compliance_analysis.get("score", 0),
                risk_level=risk_assessment.get("level", "medium"),
                issues=compliance_analysis.get("issues", []),
                recommendations=self._generate_comprehensive_recommendations(
                    document_type, content, compliance_analysis, risk_assessment
                ),
                legal_requirements=legal_requirements,
                case_law_guidance=case_law_guidance,
                ai_insights=ai_insights,
                confidence=confidence,
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Document analysis failed: {str(e)}")
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return DocumentAnalysis(
                document_type=document_type,
                compliance_score=0,
                risk_level="high",
                issues=[{"type": "analysis_error", "message": str(e)}],
                recommendations=["Seek professional legal advice"],
                legal_requirements=[],
                case_law_guidance={},
                ai_insights={"error": str(e)},
                confidence=0.0,
                processing_time=processing_time
            )

    def _analyze_compliance(self, document_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Advanced compliance analysis using multiple techniques"""
        issues = []
        score = 100
        
        # Rule-based compliance checks
        rule_based_issues = self._rule_based_compliance_check(document_type, content)
        issues.extend(rule_based_issues)
        
        # AI-powered compliance analysis
        if self.legal_classifier:
            ai_compliance_issues = self._ai_compliance_analysis(document_type, content)
            issues.extend(ai_compliance_issues)
        
        # Calculate score based on issues
        critical_issues = len([i for i in issues if i.get("severity") == "critical"])
        major_issues = len([i for i in issues if i.get("severity") == "major"])
        minor_issues = len([i for i in issues if i.get("severity") == "minor"])
        
        score -= (critical_issues * 25) + (major_issues * 10) + (minor_issues * 5)
        score = max(0, score)
        
        return {
            "score": score,
            "issues": issues,
            "status": "compliant" if score >= 80 else "non_compliant"
        }

    def _rule_based_compliance_check(self, document_type: str, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Rule-based compliance checking"""
        issues = []
        
        if document_type == "will":
            # Will-specific compliance checks
            if not content.get("executors"):
                issues.append({
                    "type": "missing_executor",
                    "severity": "critical",
                    "message": "No executor appointed",
                    "statute": "Succession Law Reform Act, s. 3",
                    "remedy": "Appoint at least one qualified executor"
                })
            
            if not content.get("witnesses") or len(content.get("witnesses", [])) < 2:
                issues.append({
                    "type": "insufficient_witnesses",
                    "severity": "critical",
                    "message": "Insufficient witnesses (requires 2)",
                    "statute": "Succession Law Reform Act, s. 4",
                    "remedy": "Ensure two qualified witnesses are present"
                })
            
            if not content.get("testator_signature"):
                issues.append({
                    "type": "missing_signature",
                    "severity": "critical",
                    "message": "Testator signature required",
                    "statute": "Succession Law Reform Act, s. 4",
                    "remedy": "Will must be signed by testator"
                })
                
        elif document_type in ["poa_property", "poa_personal_care"]:
            # POA-specific compliance checks
            if not content.get("attorneys"):
                issues.append({
                    "type": "missing_attorney",
                    "severity": "critical",
                    "message": "No attorney appointed",
                    "statute": "Substitute Decisions Act, s. 7",
                    "remedy": "Appoint at least one qualified attorney"
                })
            
            if not content.get("grantor_signature"):
                issues.append({
                    "type": "missing_grantor_signature",
                    "severity": "critical",
                    "message": "Grantor signature required",
                    "statute": "Substitute Decisions Act, s. 10",
                    "remedy": "POA must be signed by grantor"
                })
        
        return issues

    def _ai_compliance_analysis(self, document_type: str, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """AI-powered compliance analysis"""
        issues = []
        
        try:
            # Convert content to text for analysis
            content_text = self._content_to_text(content)
            
            # Classify compliance issues using AI
            candidate_labels = [
                "missing required clause",
                "improper execution",
                "capacity concerns",
                "witness issues",
                "statutory non-compliance"
            ]
            
            classification_result = self.legal_classifier(
                content_text,
                candidate_labels,
                multi_label=True
            )
            
            # Process classification results
            for label, score in zip(classification_result["labels"], classification_result["scores"]):
                if score > 0.7:  # High confidence threshold
                    issues.append({
                        "type": "ai_detected_issue",
                        "severity": "major" if score > 0.8 else "minor",
                        "message": f"AI detected potential {label}",
                        "confidence": score,
                        "source": "ai_classifier"
                    })
                    
        except Exception as e:
            logger.warning(f"AI compliance analysis failed: {str(e)}")
        
        return issues

    def _assess_risk(self, document_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Advanced risk assessment using AI and case law"""
        risk_factors = []
        risk_score = 0
        
        # Case law-based risk assessment
        if self.case_law_analyzer.is_ready():
            case_law_risk = self._case_law_risk_assessment(document_type, content)
            risk_factors.extend(case_law_risk.get("factors", []))
            risk_score += case_law_risk.get("score", 0)
        
        # AI-based risk assessment
        if self.sentence_transformer:
            ai_risk = self._ai_risk_assessment(document_type, content)
            risk_factors.extend(ai_risk.get("factors", []))
            risk_score += ai_risk.get("score", 0)
        
        # Determine risk level
        if risk_score > 70:
            risk_level = "high"
        elif risk_score > 40:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "level": risk_level,
            "score": risk_score,
            "factors": risk_factors,
            "mitigation_strategies": self._get_risk_mitigation_strategies(risk_level, risk_factors)
        }

    def _case_law_risk_assessment(self, document_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Risk assessment based on case law analysis"""
        risk_factors = []
        risk_score = 0
        
        try:
            # Analyze similar cases
            issue_description = f"{document_type} document risk assessment"
            case_analysis = self.case_law_analyzer.analyze_legal_issue(issue_description, document_type)
            
            # Extract risk factors from case law
            for case in case_analysis.get("relevant_cases", []):
                key_factors = case.get("key_factors", [])
                for factor in key_factors:
                    if any(risk_term in factor.lower() for risk_term in ["abuse", "dispute", "challenge", "invalid"]):
                        risk_factors.append({
                            "type": "case_law_precedent",
                            "description": f"Similar to {case.get('case_name', 'case')}: {factor}",
                            "weight": case.get("relevance_score", 1)
                        })
                        risk_score += case.get("relevance_score", 1) * 10
                        
        except Exception as e:
            logger.warning(f"Case law risk assessment failed: {str(e)}")
        
        return {"factors": risk_factors, "score": min(risk_score, 50)}

    def _ai_risk_assessment(self, document_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """AI-based risk assessment using semantic analysis"""
        risk_factors = []
        risk_score = 0
        
        try:
            # Analyze content for risk indicators
            content_text = self._content_to_text(content)
            
            # Risk indicator patterns
            risk_patterns = [
                "complex family situation",
                "business interests",
                "foreign assets",
                "capacity concerns",
                "family disputes",
                "previous wills",
                "significant assets"
            ]
            
            # Use sentence similarity to detect risk patterns
            if self.sentence_transformer:
                content_embedding = self.sentence_transformer.encode([content_text])
                pattern_embeddings = self.sentence_transformer.encode(risk_patterns)
                
                # Calculate similarities
                from sklearn.metrics.pairwise import cosine_similarity
                similarities = cosine_similarity(content_embedding, pattern_embeddings)[0]
                
                for pattern, similarity in zip(risk_patterns, similarities):
                    if similarity > 0.6:  # Significant similarity
                        risk_factors.append({
                            "type": "ai_risk_indicator",
                            "description": f"Potential {pattern} detected",
                            "confidence": similarity,
                            "weight": similarity * 10
                        })
                        risk_score += similarity * 20
                        
        except Exception as e:
            logger.warning(f"AI risk assessment failed: {str(e)}")
        
        return {"factors": risk_factors, "score": min(risk_score, 50)}

    def _extract_legal_requirements(self, document_type: str, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract comprehensive legal requirements"""
        requirements = []
        
        # Get template requirements from knowledge base
        template = self.legal_kb.get_legal_template(document_type)
        if template:
            requirements.extend(template.get("requirements", []))
        
        # Add AI-generated requirements
        if self.ai_engine.is_ready():
            try:
                ai_requirements = asyncio.run(
                    self.ai_engine.analyze_document_requirements(document_type, content)
                )
                requirements.extend(ai_requirements.get("requirements", []))
            except Exception as e:
                logger.warning(f"AI requirements extraction failed: {str(e)}")
        
        return requirements

    def _get_case_law_guidance(self, document_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Get relevant case law guidance"""
        if not self.case_law_analyzer.is_ready():
            return {}
        
        try:
            issue_description = f"{document_type} document preparation and execution"
            return self.case_law_analyzer.analyze_legal_issue(issue_description, document_type)
        except Exception as e:
            logger.warning(f"Case law guidance failed: {str(e)}")
            return {}

    def _generate_ai_insights(self, document_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate advanced AI insights"""
        insights = {}
        
        try:
            # Entity extraction
            if self.legal_ner_pipeline:
                content_text = self._content_to_text(content)
                entities = self.legal_ner_pipeline(content_text)
                insights["entities"] = entities
            
            # Document complexity analysis
            insights["complexity_score"] = self._calculate_complexity_score(content)
            
            # Completeness assessment
            insights["completeness"] = self._assess_completeness(document_type, content)
            
            # Language clarity analysis
            insights["clarity_score"] = self._analyze_language_clarity(content)
            
        except Exception as e:
            logger.warning(f"AI insights generation failed: {str(e)}")
            insights["error"] = str(e)
        
        return insights

    def _generate_comprehensive_recommendations(
        self, 
        document_type: str, 
        content: Dict[str, Any],
        compliance_analysis: Dict[str, Any],
        risk_assessment: Dict[str, Any]
    ) -> List[str]:
        """Generate comprehensive recommendations"""
        recommendations = []
        
        # Compliance-based recommendations
        for issue in compliance_analysis.get("issues", []):
            if issue.get("remedy"):
                recommendations.append(issue["remedy"])
        
        # Risk-based recommendations
        recommendations.extend(
            risk_assessment.get("mitigation_strategies", [])
        )
        
        # Document-specific recommendations
        if document_type == "will":
            recommendations.extend([
                "Review beneficiary designations on registered accounts",
                "Consider tax implications of bequests",
                "Store will in secure location and inform executor"
            ])
        elif document_type in ["poa_property", "poa_personal_care"]:
            recommendations.extend([
                "Discuss powers and limitations with attorney",
                "Provide copy of POA to relevant institutions",
                "Review and update POA as circumstances change"
            ])
        
        # Remove duplicates and return
        return list(set(recommendations))

    def _content_to_text(self, content: Dict[str, Any]) -> str:
        """Convert content dictionary to text for analysis"""
        text_parts = []
        
        for key, value in content.items():
            if isinstance(value, str):
                text_parts.append(f"{key}: {value}")
            elif isinstance(value, list):
                text_parts.append(f"{key}: {', '.join(str(v) for v in value)}")
            elif isinstance(value, dict):
                text_parts.append(f"{key}: {json.dumps(value)}")
        
        return " ".join(text_parts)

    def _calculate_confidence(
        self, 
        compliance_analysis: Dict[str, Any],
        risk_assessment: Dict[str, Any],
        ai_insights: Dict[str, Any]
    ) -> float:
        """Calculate overall confidence in analysis"""
        confidence_factors = []
        
        # Compliance confidence
        if compliance_analysis.get("score", 0) > 80:
            confidence_factors.append(0.9)
        elif compliance_analysis.get("score", 0) > 60:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.5)
        
        # Risk assessment confidence
        if risk_assessment.get("level") == "low":
            confidence_factors.append(0.8)
        elif risk_assessment.get("level") == "medium":
            confidence_factors.append(0.6)
        else:
            confidence_factors.append(0.4)
        
        # AI insights confidence
        if ai_insights and not ai_insights.get("error"):
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.5)
        
        return sum(confidence_factors) / len(confidence_factors)

    def _calculate_complexity_score(self, content: Dict[str, Any]) -> float:
        """Calculate document complexity score"""
        complexity_score = 0
        
        # Number of beneficiaries/attorneys
        beneficiaries = content.get("beneficiaries", [])
        attorneys = content.get("attorneys", [])
        complexity_score += (len(beneficiaries) + len(attorneys)) * 5
        
        # Special provisions
        special_instructions = content.get("special_instructions", [])
        complexity_score += len(special_instructions) * 10
        
        # Asset complexity
        assets = content.get("assets", [])
        for asset in assets:
            if isinstance(asset, dict) and asset.get("type") in ["business", "foreign", "trust"]:
                complexity_score += 20
        
        return min(complexity_score, 100)

    def _assess_completeness(self, document_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Assess document completeness"""
        required_fields = self._get_required_fields(document_type)
        present_fields = []
        missing_fields = []
        
        for field in required_fields:
            if content.get(field):
                present_fields.append(field)
            else:
                missing_fields.append(field)
        
        completeness_score = len(present_fields) / len(required_fields) * 100 if required_fields else 100
        
        return {
            "score": completeness_score,
            "present_fields": present_fields,
            "missing_fields": missing_fields
        }

    def _get_required_fields(self, document_type: str) -> List[str]:
        """Get required fields for document type"""
        field_mappings = {
            "will": ["testator_name", "executors", "beneficiaries", "witnesses"],
            "poa_property": ["grantor_name", "attorneys", "powers"],
            "poa_personal_care": ["grantor_name", "attorneys", "healthcare_instructions"]
        }
        
        return field_mappings.get(document_type, [])

    def _analyze_language_clarity(self, content: Dict[str, Any]) -> float:
        """Analyze language clarity and readability"""
        # Simple readability analysis based on sentence length and complexity
        text = self._content_to_text(content)
        
        if not text:
            return 0
        
        sentences = text.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        
        # Simple scoring based on sentence length
        if avg_sentence_length < 15:
            return 90
        elif avg_sentence_length < 25:
            return 70
        else:
            return 50

    def _get_risk_mitigation_strategies(
        self, 
        risk_level: str, 
        risk_factors: List[Dict[str, Any]]
    ) -> List[str]:
        """Get risk mitigation strategies"""
        strategies = []
        
        if risk_level == "high":
            strategies.extend([
                "Seek immediate professional legal advice",
                "Consider alternative document structures",
                "Implement additional safeguards and oversight"
            ])
        elif risk_level == "medium":
            strategies.extend([
                "Consider professional legal review",
                "Document decision-making process thoroughly",
                "Implement standard safeguards"
            ])
        else:
            strategies.extend([
                "Follow standard legal procedures",
                "Maintain proper documentation"
            ])
        
        # Add specific strategies based on risk factors
        for factor in risk_factors:
            factor_type = factor.get("type", "")
            if "capacity" in factor.get("description", "").lower():
                strategies.append("Obtain medical capacity assessment")
            elif "family" in factor.get("description", "").lower():
                strategies.append("Consider family mediation or communication")
            elif "business" in factor.get("description", "").lower():
                strategies.append("Consult with business law specialist")
        
        return list(set(strategies))  # Remove duplicates

    def generate_document_insights(self, document_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive document insights"""
        try:
            analysis = self.analyze_document(document_type, content)
            
            return {
                "analysis_summary": {
                    "compliance_score": analysis.compliance_score,
                    "risk_level": analysis.risk_level,
                    "confidence": analysis.confidence
                },
                "key_recommendations": analysis.recommendations[:5],  # Top 5
                "critical_issues": [
                    issue for issue in analysis.issues 
                    if issue.get("severity") == "critical"
                ],
                "legal_guidance": analysis.case_law_guidance,
                "next_steps": self._generate_next_steps(analysis),
                "processing_metadata": {
                    "processing_time": analysis.processing_time,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Document insights generation failed: {str(e)}")
            return {"error": str(e)}

    def _generate_next_steps(self, analysis: DocumentAnalysis) -> List[str]:
        """Generate next steps based on analysis"""
        next_steps = []
        
        if analysis.compliance_score < 60:
            next_steps.append("Address critical compliance issues before proceeding")
        elif analysis.compliance_score < 80:
            next_steps.append("Review and resolve compliance concerns")
        
        if analysis.risk_level == "high":
            next_steps.append("Consult with legal professional immediately")
        elif analysis.risk_level == "medium":
            next_steps.append("Consider professional legal review")
        
        if analysis.confidence < 0.7:
            next_steps.append("Gather additional information or documentation")
        
        if not next_steps:
            next_steps.append("Proceed with document finalization and execution")
        
        return next_steps

    def is_ready(self) -> bool:
        """Check if service is ready"""
        return self.is_initialized

    async def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        return {
            "service_status": "ready" if self.is_initialized else "not_ready",
            "components": {
                "ai_engine": self.ai_engine.is_ready(),
                "legal_kb": self.legal_kb.is_ready(),
                "case_law_analyzer": self.case_law_analyzer.is_ready(),
                "advanced_models": {
                    "legal_classifier": self.legal_classifier is not None,
                    "sentence_transformer": self.sentence_transformer is not None,
                    "openai_client": self.openai_client is not None,
                    "legal_ner_pipeline": self.legal_ner_pipeline is not None
                }
            },
            "capabilities": {
                "compliance_analysis": True,
                "risk_assessment": True,
                "case_law_guidance": self.case_law_analyzer.is_ready(),
                "ai_insights": ADVANCED_NLP_AVAILABLE,
                "semantic_analysis": SENTENCE_TRANSFORMERS_AVAILABLE
            },
            "timestamp": datetime.now().isoformat()
        }