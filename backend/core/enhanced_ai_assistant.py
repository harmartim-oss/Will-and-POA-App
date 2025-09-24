# backend/core/enhanced_ai_assistant.py
import spacy
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import asyncio
import json
import re
from dataclasses import dataclass
import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

@dataclass
class AIAssistantResponse:
    answer: str
    confidence: float
    legal_sources: List[str]
    case_law_references: List[str]
    statutes_referenced: List[str]
    warnings: List[str]
    recommendations: List[str]

class OntarioEnhancedAIAssistant:
    """Advanced AI assistant for Ontario sole practitioner"""
    
    def __init__(self):
        self.nlp = None
        self.legal_classifier = None
        self.sentence_transformer = None
        self.ontario_knowledge = None
        self.is_initialized = False
        
        # Ontario-specific legal categories
        self.legal_categories = {
            "wills_estates": ["will", "estate", "executor", "probate", "intestate"],
            "real_estate": ["property", "title", "mortgage", "transfer", "closing"],
            "corporate": ["incorporation", "shareholder", "director", "by-law"],
            "family": ["divorce", "custody", "support", "marriage", "separation"],
            "civil_litigation": ["statement of claim", "defence", "discovery", "motion"],
            "employment": ["termination", "wrongful dismissal", "severance", "constructive dismissal"],
            "contract": ["agreement", "breach", "termination", "enforceable"],
            "poa": ["power of attorney", "attorney", "incapacity", "guardianship"]
        }
    
    async def initialize(self):
        """Initialize enhanced AI assistant"""
        try:
            logger.info("🤖 Initializing Enhanced Ontario AI Assistant...")
            # Load spaCy with legal enhancements
            try:
                self.nlp = spacy.load("en_core_web_lg")
            except OSError:
                # Fallback to smaller model if large model not available
                logger.warning("Large spaCy model not available, using smaller model")
                try:
                    self.nlp = spacy.load("en_core_web_sm")
                except OSError:
                    logger.warning("spaCy models not available, initializing without NLP")
                    self.nlp = None
            
            if self.nlp:
                self._add_legal_patterns()
            
            # Initialize sentence transformer with fallback
            try:
                self.sentence_transformer = SentenceTransformer('all-mpnet-base-v2')
            except Exception as e:
                logger.warning(f"Sentence transformer not available: {e}")
                self.sentence_transformer = None
            
            # Initialize legal classifier with fallback
            try:
                self.legal_classifier = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli"
                )
            except Exception as e:
                logger.warning(f"Legal classifier not available: {e}")
                self.legal_classifier = None
            
            self.is_initialized = True
            logger.info("✓ Enhanced AI Assistant initialized")
        except Exception as e:
            logger.error(f"AI Assistant initialization failed: {str(e)}")
            # Initialize in fallback mode
            self.is_initialized = True
            logger.info("✓ Enhanced AI Assistant initialized in fallback mode")
    
    def _add_legal_patterns(self):
        """Add Ontario-specific legal patterns"""
        if not self.nlp:
            return
            
        patterns = [
            {"label": "LEGAL_DOCUMENT", "pattern": "will"},
            {"label": "LEGAL_DOCUMENT", "pattern": "power of attorney"},
            {"label": "LEGAL_DOCUMENT", "pattern": "statement of claim"},
            {"label": "LEGAL_DOCUMENT", "pattern": "affidavit"},
            {"label": "LEGAL_ROLE", "pattern": "executor"},
            {"label": "LEGAL_ROLE", "pattern": "attorney"},
            {"label": "LEGAL_ROLE", "pattern": "guardian"},
            {"label": "LEGAL_ACT", "pattern": "Wills Act"},
            {"label": "LEGAL_ACT", "pattern": "Substitute Decisions Act"},
            {"label": "LEGAL_ACT", "pattern": "Family Law Act"},
            {"label": "COURT", "pattern": "Ontario Superior Court"},
            {"label": "COURT", "pattern": "Small Claims Court"},
            {"label": "COURT", "pattern": "Court of Appeal"}
        ]
        
        try:
            ruler = self.nlp.add_pipe("entity_ruler", before="ner")
            ruler.add_patterns(patterns)
        except Exception as e:
            logger.warning(f"Could not add legal patterns: {e}")
    
    async def analyze_legal_question(self, question: str, context: Dict[str, Any] = None) -> AIAssistantResponse:
        """Analyze legal question with Ontario-specific knowledge"""
        try:
            # Classify legal area
            legal_area = await self._classify_legal_area(question)
            
            # Extract key entities
            entities = self._extract_legal_entities(question)
            
            # Get relevant statutes
            statutes = await self._get_relevant_statutes(legal_area, entities)
            
            # Get relevant case law
            case_law = await self._get_relevant_case_law(legal_area, entities)
            
            # Generate legal analysis
            analysis = await self._generate_legal_analysis(question, legal_area, entities, statutes, case_law)
            
            # Create response
            response = AIAssistantResponse(
                answer=analysis["answer"],
                confidence=analysis["confidence"],
                legal_sources=statutes,
                case_law_references=case_law,
                statutes_referenced=statutes,
                warnings=analysis.get("warnings", []),
                recommendations=analysis.get("recommendations", [])
            )
            
            return response
        except Exception as e:
            logger.error(f"Legal question analysis failed: {str(e)}")
            return AIAssistantResponse(
                answer=f"I encountered an error analyzing your question: {str(e)}",
                confidence=0.0,
                legal_sources=[],
                case_law_references=[],
                statutes_referenced=[],
                warnings=["Analysis failed - consult with a lawyer"],
                recommendations=["Seek professional legal advice"]
            )
    
    async def _classify_legal_area(self, question: str) -> str:
        """Classify the legal area of the question"""
        if not self.legal_classifier:
            # Fallback classification using keyword matching
            question_lower = question.lower()
            for area, keywords in self.legal_categories.items():
                if any(keyword in question_lower for keyword in keywords):
                    return area
            return "general"
        
        try:
            candidate_labels = list(self.legal_categories.keys())
            result = self.legal_classifier(question, candidate_labels)
            return result['labels'][0] if result['scores'][0] > 0.5 else "general"
        except Exception as e:
            logger.warning(f"Legal classification failed: {e}")
            return "general"
    
    def _extract_legal_entities(self, question: str) -> List[str]:
        """Extract legal entities from the question"""
        if not self.nlp:
            # Fallback entity extraction using simple pattern matching
            entities = []
            question_lower = question.lower()
            for category, keywords in self.legal_categories.items():
                for keyword in keywords:
                    if keyword in question_lower:
                        entities.append(keyword)
            return entities
        
        try:
            doc = self.nlp(question)
            entities = []
            
            # Extract named entities
            for ent in doc.ents:
                entities.append(ent.text)
            
            # Extract legal-specific patterns
            for token in doc:
                if token._.get("is_legal_term"):
                    entities.append(token.text)
            
            return entities
        except Exception as e:
            logger.warning(f"Entity extraction failed: {e}")
            return []
    
    async def _get_relevant_statutes(self, legal_area: str, entities: List[str]) -> List[str]:
        """Get relevant Ontario statutes"""
        ontario_statutes = {
            "wills_estates": ["Succession Law Reform Act", "Estates Act", "Trustee Act"],
            "real_estate": ["Land Titles Act", "Planning Act", "Condominium Act"],
            "corporate": ["Business Corporations Act", "Partnerships Act"],
            "family": ["Family Law Act", "Divorce Act", "Children's Law Reform Act"],
            "civil_litigation": ["Rules of Civil Procedure", "Courts of Justice Act"],
            "employment": ["Employment Standards Act", "Human Rights Code"],
            "contract": ["Sale of Goods Act", "Consumer Protection Act"],
            "poa": ["Substitute Decisions Act", "Powers of Attorney Act"]
        }
        
        return ontario_statutes.get(legal_area, ["General Legal Principles"])
    
    async def _get_relevant_case_law(self, legal_area: str, entities: List[str]) -> List[str]:
        """Get relevant case law references"""
        # Mock case law - in practice, this would query legal databases
        mock_cases = [
            f"Sample Case v. Ontario (2023) - relevant to {legal_area}",
            f"Legal Precedent Inc. v. Smith (2022) - {legal_area} principles"
        ]
        return mock_cases
    
    async def _generate_legal_analysis(self, question: str, legal_area: str, entities: List[str], 
                                     statutes: List[str], case_law: List[str]) -> Dict[str, Any]:
        """Generate legal analysis"""
        analysis = {
            "answer": f"Based on Ontario law in the area of {legal_area}, the key considerations are: "
                     f"The relevant statutes include {', '.join(statutes)}. "
                     f"Please consult with a qualified Ontario lawyer for specific legal advice.",
            "confidence": 0.7,
            "warnings": [
                "This is general information only and not legal advice",
                "Ontario law is complex and fact-specific",
                "Consult with a qualified lawyer for your specific situation"
            ],
            "recommendations": [
                "Review the relevant statutes mentioned",
                "Consider the specific facts of your situation",
                "Seek professional legal advice from an Ontario lawyer"
            ]
        }
        
        return analysis
    
    def is_ready(self) -> bool:
        """Check if AI assistant is ready"""
        return self.is_initialized