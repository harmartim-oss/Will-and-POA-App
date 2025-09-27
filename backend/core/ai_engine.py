try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

try:
    import torch
    from transformers import (
        pipeline, AutoTokenizer, AutoModelForSequenceClassification,
        AutoModelForQuestionAnswering, AutoModelForCausalLM
    )
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

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

from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import json
import asyncio
from dataclasses import dataclass

from .legal_knowledge import OntarioLegalKnowledgeBase
from .nlp_models import OntarioLegalNLPModels
from .case_law_analyzer import OntarioCaseLawAnalyzer

logger = logging.getLogger(__name__)

@dataclass
class AIAnalysisResult:
    document_type: str
    requirements: List[Dict[str, Any]]
    compliance_issues: List[Dict[str, Any]]
    risk_assessment: Dict[str, Any]
    recommendations: List[str]
    confidence_score: float
    processing_time: float

class OntarioLegalAIEngine:
    def __init__(self):
        self.nlp = None
        self.legal_classifier = None
        self.entity_recognizer = None
        self.sentence_transformer = None
        self.openai_client = None
        self.legal_knowledge = OntarioLegalKnowledgeBase()
        self.nlp_models = OntarioLegalNLPModels()
        self.case_law_analyzer = OntarioCaseLawAnalyzer()
        
        # Ontario-specific legal categories
        self.legal_categories = {
            "wills": ["testamentary", "executor", "beneficiary", "estate"],
            "poa_property": ["attorney", "property", "financial", "power"],
            "poa_personal_care": ["healthcare", "medical", "personal care"],
            "estate_administration": ["probate", "estate", "administrator"],
            "trusts": ["trustee", "beneficiary", "trust agreement"]
        }
        
        # Enhanced AI capabilities
        self.compliance_checker = None
        self.risk_assessor = None
        self.document_intelligence = None
        
        self.is_initialized = False

    async def initialize(self):
        """Initialize AI models and components"""
        try:
            logger.info("Initializing Ontario Legal AI Engine...")
            
            # Load spaCy model with legal enhancements
            if SPACY_AVAILABLE:
                try:
                    self.nlp = spacy.load("en_core_web_lg")
                except OSError:
                    # Fallback to smaller model if large model not available
                    try:
                        self.nlp = spacy.load("en_core_web_sm")
                    except OSError:
                        logger.warning("No spaCy model found. Some features will be limited.")
                        self.nlp = None
            else:
                logger.warning("spaCy not available. NLP features will be limited.")
                self.nlp = None
            
            if self.nlp:
                self._add_legal_patterns()
            
            # Initialize transformer models
            await self.nlp_models.initialize()
            
            # Initialize sentence transformer for semantic similarity
            if SENTENCE_TRANSFORMERS_AVAILABLE:
                try:
                    self.sentence_transformer = SentenceTransformer('all-mpnet-base-v2')
                except Exception as e:
                    logger.warning(f"Could not load sentence transformer: {e}")
                    self.sentence_transformer = None
            else:
                logger.warning("sentence-transformers not available. Semantic similarity features will be limited.")
                self.sentence_transformer = None
            
            # Initialize legal knowledge base
            await self.legal_knowledge.initialize()
            
            # Initialize case law analyzer
            await self.case_law_analyzer.initialize()
            
            self.is_initialized = True
            logger.info("AI Engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize AI Engine: {str(e)}")
            # Don't raise - allow system to continue with limited functionality
            self.is_initialized = False

    def _add_legal_patterns(self):
        """Add Ontario-specific legal patterns to spaCy"""
        if not self.nlp:
            return
            
        patterns = [
            {"label": "LEGAL_ACT", "pattern": "Wills Act"},
            {"label": "LEGAL_ACT", "pattern": "Substitute Decisions Act"},
            {"label": "LEGAL_ACT", "pattern": "Estates Act"},
            {"label": "LEGAL_ACT", "pattern": "Succession Law Reform Act"},
            {"label": "COURT", "pattern": "Ontario Superior Court"},
            {"label": "COURT", "pattern": "Court of Appeal for Ontario"},
            {"label": "LEGAL_ROLE", "pattern": "executor"},
            {"label": "LEGAL_ROLE", "pattern": "attorney"},
            {"label": "LEGAL_ROLE", "pattern": "guardian"},
            {"label": "LEGAL_ROLE", "pattern": "trustee"}
        ]
        
        try:
            ruler = self.nlp.add_pipe("entity_ruler", before="ner")
            ruler.add_patterns(patterns)
        except Exception as e:
            logger.warning(f"Could not add legal patterns: {e}")

    async def analyze_document_intent(self, text: str) -> Dict[str, Any]:
        """Analyze document intent and classify legal category"""
        start_time = datetime.now()
        
        # Basic analysis if spaCy not available
        if not self.nlp:
            return self._basic_analysis(text, start_time)
        
        # Preprocess text
        doc = self.nlp(text.lower())
        
        # Extract entities
        entities = self._extract_legal_entities(doc)
        
        # Classify document type
        document_type = self._classify_document_type(text)
        
        # Extract key requirements
        requirements = self._extract_requirements(text, document_type)
        
        # Analyze sentiment and tone
        sentiment = self._analyze_legal_sentiment(text)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "document_type": document_type,
            "confidence": self._calculate_confidence(text, document_type),
            "entities": entities,
            "requirements": requirements,
            "sentiment": sentiment,
            "processing_time": processing_time
        }

    def _basic_analysis(self, text: str, start_time: datetime) -> Dict[str, Any]:
        """Basic analysis when advanced NLP is not available"""
        document_type = "unknown"
        
        # Simple keyword-based classification
        text_lower = text.lower()
        if any(word in text_lower for word in ["will", "testament", "executor", "bequest"]):
            document_type = "will"
        elif any(word in text_lower for word in ["power of attorney", "attorney for property"]):
            document_type = "poa_property"
        elif any(word in text_lower for word in ["personal care", "healthcare decisions"]):
            document_type = "poa_personal_care"
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "document_type": document_type,
            "confidence": 0.6,  # Lower confidence for basic analysis
            "entities": [],
            "requirements": [],
            "sentiment": {"sentiment": "NEUTRAL", "confidence": 0.5},
            "processing_time": processing_time
        }

    def _extract_legal_entities(self, doc) -> List[Dict[str, Any]]:
        """Extract legal-specific entities from text"""
        entities = []
        
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char,
                "explanation": self._get_entity_explanation(ent.label_)
            })
        
        # Extract custom legal entities
        for token in doc:
            if token.ent_type_ == "LEGAL_ACT":
                entities.append({
                    "text": token.text,
                    "label": "LEGAL_ACT",
                    "explanation": "Ontario legislation"
                })
        
        return entities

    def _get_entity_explanation(self, label: str) -> str:
        """Get explanation for entity label"""
        explanations = {
            "PERSON": "Individual person mentioned in document",
            "ORG": "Organization or institution",
            "MONEY": "Monetary amount or financial value",
            "DATE": "Date or time reference",
            "LEGAL_ACT": "Legal statute or act",
            "COURT": "Legal court or tribunal",
            "LEGAL_ROLE": "Legal role or position"
        }
        return explanations.get(label, "Legal entity")

    def _classify_document_type(self, text: str) -> str:
        """Classify the type of legal document using ML"""
        if self.sentence_transformer:
            try:
                # Convert text to embeddings
                embeddings = self.sentence_transformer.encode([text])
                
                # Use pre-trained classifier for document types
                predictions = self.nlp_models.classify_document(embeddings)
                
                return predictions[0] if predictions else "unknown"
            except Exception as e:
                logger.warning(f"ML classification failed: {e}")
        
        # Fallback to keyword-based classification
        text_lower = text.lower()
        if any(word in text_lower for word in ["will", "testament", "executor", "bequest"]):
            return "will"
        elif any(word in text_lower for word in ["power of attorney", "attorney for property"]):
            return "poa_property"
        elif any(word in text_lower for word in ["personal care", "healthcare decisions"]):
            return "poa_personal_care"
        
        return "unknown"

    def _extract_requirements(self, text: str, document_type: str) -> List[Dict[str, Any]]:
        """Extract legal requirements based on document type"""
        requirements = []
        
        if document_type == "will":
            requirements = self._extract_will_requirements(text)
        elif document_type == "poa_property":
            requirements = self._extract_poa_property_requirements(text)
        elif document_type == "poa_personal_care":
            requirements = self._extract_poa_care_requirements(text)
        
        return requirements

    def _extract_will_requirements(self, text: str) -> List[Dict[str, Any]]:
        """Extract specific requirements for Ontario wills"""
        requirements = []
        
        # Check for testamentary intent
        if any(phrase in text.lower() for phrase in ["last will", "testament", "declare this"]):
            requirements.append({
                "type": "testamentary_intent",
                "status": "present",
                "requirement": "Must show testamentary intent",
                "compliance": "compliant"
            })
        
        # Check for revocation clause
        if "revoke" in text.lower():
            requirements.append({
                "type": "revocation",
                "status": "present",
                "requirement": "Revocation of previous wills",
                "compliance": "compliant"
            })
        
        # Check for executor appointment
        if any(term in text.lower() for term in ["executor", "appoint", "nominate"]):
            requirements.append({
                "type": "executor_appointment",
                "status": "present", 
                "requirement": "Appointment of executor",
                "compliance": "compliant"
            })
        
        # Check for proper execution (Ontario requirements)
        execution_reqs = self._check_execution_requirements(text)
        requirements.extend(execution_reqs)
        
        return requirements

    def _extract_poa_property_requirements(self, text: str) -> List[Dict[str, Any]]:
        """Extract requirements for Power of Attorney for Property"""
        requirements = []
        
        # Check for capacity clause
        if any(phrase in text.lower() for phrase in ["mentally capable", "capacity", "sound mind"]):
            requirements.append({
                "type": "capacity_clause",
                "status": "present",
                "requirement": "Statement of mental capacity",
                "compliance": "compliant"
            })
        
        return requirements

    def _extract_poa_care_requirements(self, text: str) -> List[Dict[str, Any]]:
        """Extract requirements for Power of Attorney for Personal Care"""
        requirements = []
        
        # Check for healthcare decisions scope
        if any(phrase in text.lower() for phrase in ["healthcare", "medical", "personal care"]):
            requirements.append({
                "type": "healthcare_scope",
                "status": "present",
                "requirement": "Clear scope of healthcare decisions",
                "compliance": "compliant"
            })
        
        return requirements

    def _check_execution_requirements(self, text: str) -> List[Dict[str, Any]]:
        """Check Ontario execution requirements"""
        requirements = []
        
        # Witness requirements
        witness_count = text.lower().count("witness")
        if witness_count >= 2:
            requirements.append({
                "type": "witnesses",
                "status": "present",
                "requirement": "Two witnesses required",
                "compliance": "compliant",
                "details": f"Found {witness_count} witness references"
            })
        else:
            requirements.append({
                "type": "witnesses",
                "status": "missing",
                "requirement": "Two witnesses required",
                "compliance": "non_compliant",
                "details": "Insufficient witness references"
            })
        
        return requirements

    def _analyze_legal_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment in legal context"""
        # Use legal-specific sentiment analysis
        result = self.nlp_models.analyze_sentiment(text)
        
        return {
            "sentiment": result["label"],
            "confidence": result["score"],
            "legal_implications": self._interpret_legal_sentiment(result)
        }

    def _interpret_legal_sentiment(self, sentiment_result: Dict) -> List[str]:
        """Interpret sentiment in legal context"""
        implications = []
        
        if sentiment_result["label"] == "NEGATIVE":
            implications.append("Document may contain contentious clauses")
            implications.append("Consider mediation or dispute resolution")
        
        if sentiment_result["label"] == "POSITIVE":
            implications.append("Document appears to be cooperative")
            implications.append("Likely to facilitate smooth execution")
        
        return implications

    async def generate_legal_recommendations(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Generate AI-powered legal recommendations"""
        recommendations = []
        
        # Based on document type
        if analysis_result["document_type"] == "will":
            recommendations.extend([
                "Consider adding a residuary clause",
                "Review executor appointment for conflicts",
                "Ensure proper witnessing per Ontario requirements",
                "Consider adding a guardianship clause if minor children"
            ])
        
        # Based on compliance issues
        compliance_issues = analysis_result.get("compliance_issues", [])
        for issue in compliance_issues:
            recommendations.append(f"Address: {issue.get('description', 'Unknown issue')}")
        
        # AI-generated specific recommendations
        try:
            ai_recs = await self.nlp_models.generate_recommendations(analysis_result)
            recommendations.extend(ai_recs)
        except Exception as e:
            logger.warning(f"Could not generate AI recommendations: {e}")
        
        return list(set(recommendations))  # Remove duplicates

    def _calculate_confidence(self, text: str, document_type: str) -> float:
        """Calculate confidence score for analysis"""
        # Simple confidence calculation (can be enhanced)
        base_confidence = 0.7
        
        if self.nlp:
            # Increase confidence based on entity recognition
            doc = self.nlp(text)
            entity_count = len(doc.ents)
            
            if entity_count > 5:
                base_confidence += 0.2
        
        # Adjust based on document length
        word_count = len(text.split())
        if word_count > 100:
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)

    def is_ready(self) -> bool:
        """Check if AI engine is ready"""
        return self.is_initialized

    async def health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check"""
        return {
            "status": "healthy" if self.is_initialized else "not_ready",
            "models_loaded": {
                "spacy": self.nlp is not None,
                "sentence_transformer": self.sentence_transformer is not None,
                "openai": self.openai_client is not None,
                "legal_knowledge": self.legal_knowledge.is_ready(),
                "case_law": self.case_law_analyzer.is_ready()
            },
            "timestamp": datetime.now().isoformat()
        }

    async def analyze_document_requirements(self, document_type: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract legal requirements based on user situation using advanced AI"""
        try:
            requirements = []
            
            # Use case law analysis for requirements
            case_analysis = self.case_law_analyzer.analyze_legal_issue(
                f"Requirements for {document_type}", document_type
            )
            
            if document_type == "will":
                requirements.extend(self._analyze_will_requirements(user_data))
            elif document_type == "poa_property":
                requirements.extend(self._analyze_poa_property_requirements(user_data))
            elif document_type == "poa_personal_care":
                requirements.extend(self._analyze_poa_care_requirements(user_data))
            
            return {
                "requirements": requirements,
                "case_law_guidance": case_analysis,
                "ai_recommendations": await self._generate_ai_recommendations(document_type, user_data)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing document requirements: {str(e)}")
            return {"requirements": [], "error": str(e)}

    def _analyze_will_requirements(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze will-specific requirements"""
        requirements = []
        
        # Age and capacity requirements
        age = user_data.get("age", 0)
        if age < 18:
            requirements.append({
                "type": "age_requirement",
                "description": "Must be 18 years or older to make a will",
                "met": False,
                "critical": True
            })
        
        # Mental capacity assessment
        if user_data.get("has_cognitive_concerns", False):
            requirements.append({
                "type": "capacity_assessment",
                "description": "Medical assessment of testamentary capacity required",
                "met": False,
                "critical": True,
                "recommendation": "Obtain medical opinion on capacity"
            })
        
        # Executor requirements
        executors = user_data.get("executors", [])
        if not executors:
            requirements.append({
                "type": "executor_appointment",
                "description": "At least one executor must be appointed",
                "met": False,
                "critical": True
            })
        
        # Witness requirements
        requirements.append({
            "type": "witness_requirement",
            "description": "Two witnesses required for will execution",
            "met": False,
            "critical": True,
            "details": "Witnesses must be present when will is signed"
        })
        
        return requirements

    def _analyze_poa_property_requirements(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze POA property-specific requirements"""
        requirements = []
        
        # Attorney appointment
        attorneys = user_data.get("attorneys", [])
        if not attorneys:
            requirements.append({
                "type": "attorney_appointment",
                "description": "At least one attorney must be appointed",
                "met": False,
                "critical": True
            })
        
        # Capacity for property decisions
        requirements.append({
            "type": "property_capacity",
            "description": "Capacity to make property decisions required",
            "met": True,
            "critical": True,
            "assessment_needed": user_data.get("has_cognitive_concerns", False)
        })
        
        # Witness requirements
        requirements.append({
            "type": "witness_requirement",
            "description": "Witness required for POA execution",
            "met": False,
            "critical": True
        })
        
        return requirements

    def _analyze_poa_care_requirements(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze POA personal care-specific requirements"""
        requirements = []
        
        # Attorney appointment
        attorneys = user_data.get("attorneys", [])
        if not attorneys:
            requirements.append({
                "type": "attorney_appointment",
                "description": "At least one attorney for personal care must be appointed",
                "met": False,
                "critical": True
            })
        
        # Capacity for personal care decisions
        requirements.append({
            "type": "personal_care_capacity",
            "description": "Capacity to make personal care decisions required",
            "met": True,
            "critical": True
        })
        
        # Healthcare directive considerations
        if user_data.get("has_healthcare_preferences", False):
            requirements.append({
                "type": "healthcare_directive",
                "description": "Healthcare preferences should be clearly documented",
                "met": False,
                "recommendation": "Include specific healthcare instructions"
            })
        
        return requirements

    async def _generate_ai_recommendations(self, document_type: str, user_data: Dict[str, Any]) -> List[str]:
        """Generate AI-powered recommendations"""
        recommendations = []
        
        # Use NLP models for recommendations if available
        if self.nlp_models.is_ready():
            try:
                analysis_result = {
                    "document_type": document_type,
                    "user_data": user_data
                }
                ai_recommendations = await self.nlp_models.generate_recommendations(analysis_result)
                recommendations.extend(ai_recommendations)
            except Exception as e:
                logger.warning(f"AI recommendation generation failed: {str(e)}")
        
        # Fallback to rule-based recommendations
        if not recommendations:
            recommendations = self._get_fallback_recommendations(document_type, user_data)
        
        return recommendations

    def _get_fallback_recommendations(self, document_type: str, user_data: Dict[str, Any]) -> List[str]:
        """Fallback recommendations when AI is not available"""
        recommendations = []
        
        if document_type == "will":
            recommendations.extend([
                "Consider appointing alternate executors",
                "Clearly specify distribution of assets",
                "Include funeral and burial instructions",
                "Review beneficiary designations on registered accounts"
            ])
        elif document_type in ["poa_property", "poa_personal_care"]:
            recommendations.extend([
                "Appoint alternate attorneys",
                "Provide clear instructions for decision-making",
                "Consider any restrictions on attorney powers",
                "Discuss your wishes with appointed attorneys"
            ])
        
        return recommendations

    async def validate_compliance(self, document_content: str, document_type: str) -> Dict[str, Any]:
        """Real-time compliance checking against Ontario law"""
        try:
            compliance_issues = []
            
            # Check against relevant legislation
            if document_type == "will":
                compliance_issues.extend(self._check_will_compliance(document_content))
            elif document_type == "poa_property":
                compliance_issues.extend(self._check_poa_compliance(document_content, "property"))
            elif document_type == "poa_personal_care":
                compliance_issues.extend(self._check_poa_compliance(document_content, "personal_care"))
            
            # Calculate compliance score
            total_checks = 10  # Base number of compliance checks
            issues_count = len([issue for issue in compliance_issues if issue.get("severity") == "critical"])
            compliance_score = max(0, (total_checks - issues_count) / total_checks * 100)
            
            return {
                "compliance_score": compliance_score,
                "issues": compliance_issues,
                "status": "compliant" if compliance_score >= 80 else "non_compliant",
                "recommendations": self._get_compliance_recommendations(compliance_issues)
            }
            
        except Exception as e:
            logger.error(f"Compliance validation failed: {str(e)}")
            return {"error": str(e), "compliance_score": 0}

    def _check_will_compliance(self, content: str) -> List[Dict[str, Any]]:
        """Check will compliance with Ontario Succession Law Reform Act"""
        issues = []
        content_lower = content.lower()
        
        # Check for essential elements
        if "executor" not in content_lower:
            issues.append({
                "type": "missing_executor",
                "severity": "critical",
                "message": "No executor appointment found",
                "statute": "Succession Law Reform Act, s. 3"
            })
        
        if "witness" not in content_lower:
            issues.append({
                "type": "missing_witnesses",
                "severity": "critical", 
                "message": "No witness references found",
                "statute": "Succession Law Reform Act, s. 4"
            })
        
        if "revoke" not in content_lower:
            issues.append({
                "type": "missing_revocation",
                "severity": "medium",
                "message": "Should include revocation of previous wills",
                "recommendation": "Add clause revoking all previous wills"
            })
        
        return issues

    def _check_poa_compliance(self, content: str, poa_type: str) -> List[Dict[str, Any]]:
        """Check POA compliance with Substitute Decisions Act"""
        issues = []
        content_lower = content.lower()
        
        if "attorney" not in content_lower:
            issues.append({
                "type": "missing_attorney",
                "severity": "critical",
                "message": "No attorney appointment found",
                "statute": "Substitute Decisions Act, s. 7"
            })
        
        if poa_type == "personal_care" and "healthcare" not in content_lower:
            issues.append({
                "type": "missing_healthcare_provisions",
                "severity": "medium",
                "message": "Consider including healthcare decision provisions",
                "recommendation": "Add specific healthcare instructions"
            })
        
        return issues

    def _get_compliance_recommendations(self, issues: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on compliance issues"""
        recommendations = []
        
        for issue in issues:
            if issue.get("recommendation"):
                recommendations.append(issue["recommendation"])
            elif issue.get("type") == "missing_executor":
                recommendations.append("Appoint a qualified executor to manage your estate")
            elif issue.get("type") == "missing_witnesses":
                recommendations.append("Ensure proper witnessing according to Ontario law")
        
        return recommendations

    async def analyze_document(self, text: str, document_type: str, case_context: str = None) -> Dict[str, Any]:
        """Main document analysis method called by API"""
        try:
            # Use existing analyze_document_intent method
            basic_analysis = await self.analyze_document_intent(text)
            
            # Add compliance analysis
            compliance_issues = self._check_document_compliance(text, document_type)
            
            # Generate recommendations
            recommendations = self._get_compliance_recommendations(compliance_issues)
            
            # Add case context analysis if provided
            if case_context:
                context_analysis = await self._analyze_case_context(case_context)
                recommendations.extend(context_analysis.get("recommendations", []))
            
            return {
                "document_type": document_type,
                "confidence": basic_analysis.get("confidence", 0.5),
                "entities": basic_analysis.get("entities", []),
                "requirements": self._get_document_requirements(document_type),
                "compliance_issues": compliance_issues,
                "recommendations": recommendations,
                "sentiment": basic_analysis.get("sentiment", {"label": "NEUTRAL", "score": 0.5})
            }
            
        except Exception as e:
            logger.error(f"Document analysis failed: {str(e)}")
            return {
                "document_type": document_type,
                "confidence": 0.1,
                "entities": [],
                "requirements": [],
                "compliance_issues": [{"type": "analysis_error", "message": str(e)}],
                "recommendations": ["Please review document manually"],
                "sentiment": {"label": "NEUTRAL", "score": 0.5}
            }

    async def generate_document_recommendations(self, document_type: str, user_data: Dict[str, Any]) -> List[str]:
        """Generate AI recommendations for document generation"""
        try:
            recommendations = []
            
            if document_type == "will":
                recommendations.extend(self._get_will_recommendations(user_data))
            elif document_type == "poa_property":
                recommendations.extend(self._get_poa_property_recommendations(user_data))
            elif document_type == "poa_personal_care":
                recommendations.extend(self._get_poa_personal_care_recommendations(user_data))
            
            # Add general recommendations
            recommendations.extend([
                "Consider consulting with an Ontario lawyer for complex provisions",
                "Ensure all parties understand the document implications",
                "Keep copies of all signed documents in a secure location"
            ])
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to generate recommendations: {str(e)}")
            return ["Consider legal consultation"]

    async def answer_legal_question(self, question: str, context: str = "", document_type: str = None) -> Dict[str, Any]:
        """Answer legal questions using AI"""
        try:
            # Simple keyword-based responses - in production would use more sophisticated AI
            answer = "Based on Ontario law, "
            confidence = 0.5
            
            question_lower = question.lower()
            
            if "will" in question_lower or "testament" in question_lower:
                answer += "a valid will in Ontario must be in writing, signed by the testator, and witnessed by two people present at the same time."
                confidence = 0.8
            elif "power of attorney" in question_lower:
                answer += "powers of attorney in Ontario are governed by the Substitute Decisions Act and must meet specific requirements for validity."
                confidence = 0.8
            elif "executor" in question_lower:
                answer += "an executor has a fiduciary duty to administer the estate according to the will and Ontario law."
                confidence = 0.7
            else:
                answer += "please consult with a qualified Ontario lawyer for specific legal advice."
                confidence = 0.3
            
            return {
                "answer": answer,
                "confidence": confidence,
                "sources": ["Ontario Wills Act", "Substitute Decisions Act"],
                "disclaimer": "This is general information only and not legal advice."
            }
            
        except Exception as e:
            logger.error(f"Failed to answer legal question: {str(e)}")
            return {
                "answer": "I apologize, but I cannot provide an answer at this time. Please consult with a qualified lawyer.",
                "confidence": 0.1,
                "sources": [],
                "disclaimer": "This is general information only and not legal advice."
            }

    async def generate_query_recommendations(self, query: str, relevant_cases: List[Dict[str, Any]], 
                                           ai_answer: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on query and case law"""
        try:
            recommendations = []
            
            # Add case-based recommendations
            if relevant_cases:
                recommendations.append(f"Review {len(relevant_cases)} relevant cases for similar situations")
                
                for case in relevant_cases[:3]:  # Top 3 cases
                    case_name = case.get("case_name", "Unknown case")
                    recommendations.append(f"Consider precedent from {case_name}")
            
            # Add confidence-based recommendations
            confidence = ai_answer.get("confidence", 0.5)
            if confidence < 0.6:
                recommendations.append("Consider seeking additional legal research or consultation")
            
            # Add general recommendations
            recommendations.extend([
                "Verify current law as legislation may have changed",
                "Consider consulting with an Ontario lawyer for specific advice",
                "Review any applicable regulations or court rules"
            ])
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to generate query recommendations: {str(e)}")
            return ["Consider legal consultation"]

    def _get_will_recommendations(self, user_data: Dict[str, Any]) -> List[str]:
        """Get will-specific recommendations"""
        recommendations = []
        
        if user_data.get("has_minor_children") and not user_data.get("guardian_appointed"):
            recommendations.append("Consider appointing a guardian for minor children")
        
        if not user_data.get("backup_executor"):
            recommendations.append("Consider appointing an alternate executor")
        
        if user_data.get("complex_assets"):
            recommendations.append("Consider establishing trusts for complex asset management")
        
        return recommendations

    def _get_poa_property_recommendations(self, user_data: Dict[str, Any]) -> List[str]:
        """Get POA property-specific recommendations"""
        recommendations = []
        
        if not user_data.get("backup_attorney"):
            recommendations.append("Consider appointing an alternate attorney")
        
        if user_data.get("significant_assets"):
            recommendations.append("Consider specific instructions for asset management")
        
        recommendations.append("Ensure attorney understands their duties and limitations")
        
        return recommendations

    def _get_poa_personal_care_recommendations(self, user_data: Dict[str, Any]) -> List[str]:
        """Get POA personal care-specific recommendations"""
        recommendations = []
        
        if not user_data.get("healthcare_wishes_specified"):
            recommendations.append("Consider including specific healthcare wishes")
        
        if user_data.get("has_specific_treatments"):
            recommendations.append("Include detailed treatment preferences")
        
        recommendations.append("Discuss wishes with appointed attorney in advance")
        
        return recommendations

    async def _analyze_case_context(self, context: str) -> Dict[str, Any]:
        """Analyze additional case context"""
        try:
            # Simple context analysis
            recommendations = []
            
            if "complex" in context.lower():
                recommendations.append("Due to complexity, consider professional legal review")
            
            if "urgent" in context.lower():
                recommendations.append("Expedite document preparation and execution")
            
            return {
                "context_type": "general",
                "recommendations": recommendations
            }
            
        except Exception as e:
            logger.error(f"Context analysis failed: {str(e)}")
            return {"context_type": "unknown", "recommendations": []}

    def _get_document_requirements(self, document_type: str) -> List[Dict[str, Any]]:
        """Get statutory requirements for document type"""
        requirements = []
        
        if document_type == "will":
            requirements = [
                {"requirement": "Must be in writing", "statute": "Wills Act, s. 4"},
                {"requirement": "Signed by testator", "statute": "Wills Act, s. 4"},
                {"requirement": "Two witnesses required", "statute": "Wills Act, s. 5"},
                {"requirement": "Testator must be 18+ years old", "statute": "Wills Act, s. 1"}
            ]
        elif document_type == "poa_property":
            requirements = [
                {"requirement": "Must be in writing", "statute": "Substitute Decisions Act, s. 2"},
                {"requirement": "Grantor must be 18+ years old", "statute": "Substitute Decisions Act, s. 2"},
                {"requirement": "Two witnesses required", "statute": "Substitute Decisions Act, s. 10"}
            ]
        elif document_type == "poa_personal_care":
            requirements = [
                {"requirement": "Must be in writing", "statute": "Substitute Decisions Act, s. 45"},
                {"requirement": "Grantor must be 16+ years old", "statute": "Substitute Decisions Act, s. 45"},
                {"requirement": "Two witnesses required", "statute": "Substitute Decisions Act, s. 46"}
            ]
        
        return requirements