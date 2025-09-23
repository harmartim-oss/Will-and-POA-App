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
                "legal_knowledge": self.legal_knowledge.is_ready(),
                "case_law": self.case_law_analyzer.is_ready()
            },
            "timestamp": datetime.now().isoformat()
        }