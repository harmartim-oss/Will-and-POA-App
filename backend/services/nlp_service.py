"""
Advanced NLP Service for Legal Text Analysis
Integrates spaCy, Blackstone, and other open-source NLP libraries for legal document processing
"""

import spacy
import re
import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
import requests
from urllib.parse import quote
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LegalEntity:
    """Represents a legal entity extracted from text"""
    text: str
    label: str
    start: int
    end: int
    confidence: float = 0.0
    description: str = ""

@dataclass
class LegalAnalysis:
    """Comprehensive legal text analysis results"""
    entities: List[LegalEntity]
    sentiment: Dict[str, float]
    readability_score: float
    legal_concepts: List[str]
    suggestions: List[str]
    risk_factors: List[str]
    compliance_issues: List[str]
    word_count: int
    sentence_count: int
    complexity_score: float

class LegalNLPService:
    """
    Advanced NLP service for legal text analysis using spaCy and specialized legal models
    """
    
    def __init__(self):
        self.nlp = None
        self.blackstone_nlp = None
        self.legal_terms = self._load_legal_terms()
        self.ontario_legal_requirements = self._load_ontario_requirements()
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize spaCy models and legal-specific pipelines"""
        try:
            # Try to load Blackstone legal model first
            try:
                import blackstone
                self.blackstone_nlp = spacy.load("en_blackstone_proto")
                logger.info("Blackstone legal model loaded successfully")
            except (ImportError, OSError) as e:
                logger.warning(f"Blackstone model not available: {e}")
                self.blackstone_nlp = None
            
            # Load standard English model as fallback
            try:
                self.nlp = spacy.load("en_core_web_sm")
                logger.info("Standard English model loaded successfully")
            except OSError:
                logger.warning("Standard English model not found, downloading...")
                spacy.cli.download("en_core_web_sm")
                self.nlp = spacy.load("en_core_web_sm")
            
            # Add custom legal entity recognition
            self._add_legal_entity_patterns()
            
        except Exception as e:
            logger.error(f"Error initializing NLP models: {e}")
            raise
    
    def _load_legal_terms(self) -> Dict[str, List[str]]:
        """Load legal terminology and concepts"""
        return {
            "estate_planning": [
                "executor", "executrix", "beneficiary", "testator", "testatrix",
                "devise", "bequest", "legacy", "residue", "intestate", "probate",
                "codicil", "revoke", "revocation", "guardian", "trustee"
            ],
            "power_of_attorney": [
                "attorney", "grantor", "principal", "substitute decision maker",
                "continuing power of attorney", "power of attorney for property",
                "power of attorney for personal care", "incapacity", "capacity"
            ],
            "legal_concepts": [
                "whereas", "heretofore", "hereinafter", "aforementioned",
                "notwithstanding", "pursuant to", "in consideration of",
                "subject to", "provided that", "in the event that"
            ],
            "ontario_specific": [
                "Succession Law Reform Act", "Substitute Decisions Act",
                "Ontario Court of Justice", "Superior Court of Justice",
                "Public Guardian and Trustee", "Office of the Public Guardian"
            ]
        }
    
    def _load_ontario_requirements(self) -> Dict[str, Any]:
        """Load Ontario-specific legal requirements"""
        return {
            "will_requirements": {
                "minimum_age": 18,
                "witness_requirements": {
                    "minimum_witnesses": 2,
                    "witness_age": 18,
                    "witness_restrictions": [
                        "Cannot be beneficiary",
                        "Cannot be spouse of beneficiary",
                        "Must be present when testator signs"
                    ]
                },
                "signature_requirements": [
                    "Testator must sign in presence of witnesses",
                    "Witnesses must sign in presence of testator",
                    "All signatures must be on same document"
                ]
            },
            "poa_requirements": {
                "property": {
                    "minimum_age": 18,
                    "witness_requirements": {
                        "minimum_witnesses": 2,
                        "restrictions": [
                            "Cannot be attorney",
                            "Cannot be spouse/partner of attorney",
                            "Cannot be child of grantor if attorney is spouse"
                        ]
                    }
                },
                "personal_care": {
                    "minimum_age": 16,
                    "witness_requirements": {
                        "minimum_witnesses": 2,
                        "restrictions": [
                            "Cannot be attorney",
                            "Cannot be spouse/partner of attorney"
                        ]
                    }
                }
            }
        }
    
    def _add_legal_entity_patterns(self):
        """Add custom legal entity recognition patterns"""
        if not self.nlp:
            return
        
        # Add entity ruler for legal terms
        if "entity_ruler" not in self.nlp.pipe_names:
            ruler = self.nlp.add_pipe("entity_ruler", before="ner")
            
            patterns = []
            
            # Add patterns for legal roles
            legal_roles = [
                "executor", "executrix", "beneficiary", "testator", "testatrix",
                "attorney", "grantor", "principal", "trustee", "guardian"
            ]
            
            for role in legal_roles:
                patterns.append({"label": "LEGAL_ROLE", "pattern": role})
                patterns.append({"label": "LEGAL_ROLE", "pattern": role.title()})
            
            # Add patterns for legal documents
            legal_docs = [
                "Last Will and Testament", "Power of Attorney", "Codicil",
                "Trust Agreement", "Estate Plan"
            ]
            
            for doc in legal_docs:
                patterns.append({"label": "LEGAL_DOCUMENT", "pattern": doc})
            
            # Add patterns for Ontario legislation
            ontario_acts = [
                "Succession Law Reform Act", "Substitute Decisions Act",
                "Estates Act", "Trustee Act"
            ]
            
            for act in ontario_acts:
                patterns.append({"label": "LEGISLATION", "pattern": act})
            
            ruler.add_patterns(patterns)
    
    def analyze_legal_text(self, text: str) -> LegalAnalysis:
        """
        Perform comprehensive legal text analysis
        
        Args:
            text: Legal text to analyze
            
        Returns:
            LegalAnalysis object with comprehensive results
        """
        try:
            # Choose the best available model
            nlp_model = self.blackstone_nlp if self.blackstone_nlp else self.nlp
            
            if not nlp_model:
                raise ValueError("No NLP model available")
            
            # Process text
            doc = nlp_model(text)
            
            # Extract entities
            entities = self._extract_legal_entities(doc)
            
            # Analyze sentiment and tone
            sentiment = self._analyze_legal_sentiment(text, doc)
            
            # Calculate readability
            readability_score = self._calculate_readability(text)
            
            # Extract legal concepts
            legal_concepts = self._extract_legal_concepts(doc)
            
            # Generate suggestions
            suggestions = self._generate_suggestions(text, doc)
            
            # Identify risk factors
            risk_factors = self._identify_risk_factors(text, doc)
            
            # Check compliance
            compliance_issues = self._check_compliance(text, doc)
            
            # Calculate metrics
            word_count = len([token for token in doc if not token.is_space])
            sentence_count = len(list(doc.sents))
            complexity_score = self._calculate_complexity(doc)
            
            return LegalAnalysis(
                entities=entities,
                sentiment=sentiment,
                readability_score=readability_score,
                legal_concepts=legal_concepts,
                suggestions=suggestions,
                risk_factors=risk_factors,
                compliance_issues=compliance_issues,
                word_count=word_count,
                sentence_count=sentence_count,
                complexity_score=complexity_score
            )
            
        except Exception as e:
            logger.error(f"Error analyzing legal text: {e}")
            raise
    
    def _extract_legal_entities(self, doc) -> List[LegalEntity]:
        """Extract legal entities from processed document"""
        entities = []
        
        for ent in doc.ents:
            entity = LegalEntity(
                text=ent.text,
                label=ent.label_,
                start=ent.start_char,
                end=ent.end_char,
                confidence=getattr(ent, 'confidence', 0.8),
                description=self._get_entity_description(ent.label_)
            )
            entities.append(entity)
        
        return entities
    
    def _get_entity_description(self, label: str) -> str:
        """Get description for entity label"""
        descriptions = {
            "PERSON": "Individual person mentioned in the document",
            "ORG": "Organization or institution",
            "GPE": "Geopolitical entity (country, city, state)",
            "MONEY": "Monetary amount",
            "DATE": "Date or time period",
            "LEGAL_ROLE": "Legal role or position",
            "LEGAL_DOCUMENT": "Type of legal document",
            "LEGISLATION": "Legal statute or act"
        }
        return descriptions.get(label, "Legal entity")
    
    def _analyze_legal_sentiment(self, text: str, doc) -> Dict[str, float]:
        """Analyze sentiment and tone appropriate for legal documents"""
        # Simple rule-based sentiment for legal text
        positive_indicators = [
            "grant", "bestow", "give", "provide", "ensure", "protect",
            "authorize", "empower", "benefit", "advantage"
        ]
        
        negative_indicators = [
            "revoke", "deny", "prohibit", "restrict", "limit", "exclude",
            "terminate", "void", "invalid", "breach"
        ]
        
        neutral_indicators = [
            "whereas", "therefore", "pursuant", "notwithstanding",
            "subject to", "in accordance with"
        ]
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_indicators if word in text_lower)
        negative_count = sum(1 for word in negative_indicators if word in text_lower)
        neutral_count = sum(1 for word in neutral_indicators if word in text_lower)
        
        total = positive_count + negative_count + neutral_count
        
        if total == 0:
            return {"positive": 0.5, "negative": 0.5, "neutral": 0.0, "formality": 0.5}
        
        # Calculate formality based on legal language usage
        formal_terms = len([token for token in doc if token.text.lower() in self.legal_terms["legal_concepts"]])
        formality = min(1.0, formal_terms / len(doc) * 10)
        
        return {
            "positive": positive_count / total,
            "negative": negative_count / total,
            "neutral": neutral_count / total,
            "formality": formality
        }
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate readability score for legal text"""
        # Simplified Flesch Reading Ease calculation
        sentences = len(re.findall(r'[.!?]+', text))
        words = len(text.split())
        syllables = sum(self._count_syllables(word) for word in text.split())
        
        if sentences == 0 or words == 0:
            return 0.0
        
        avg_sentence_length = words / sentences
        avg_syllables_per_word = syllables / words
        
        # Flesch Reading Ease formula
        score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        
        # Normalize to 0-1 scale
        return max(0.0, min(1.0, score / 100))
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word"""
        word = word.lower()
        vowels = "aeiouy"
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Handle silent 'e'
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
        
        return max(1, syllable_count)
    
    def _extract_legal_concepts(self, doc) -> List[str]:
        """Extract legal concepts and terminology"""
        concepts = set()
        
        # Extract from predefined legal terms
        text_lower = doc.text.lower()
        for category, terms in self.legal_terms.items():
            for term in terms:
                if term.lower() in text_lower:
                    concepts.add(term)
        
        # Extract noun phrases that might be legal concepts
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) > 1 and any(token.pos_ in ["NOUN", "PROPN"] for token in chunk):
                concepts.add(chunk.text)
        
        return list(concepts)
    
    def _generate_suggestions(self, text: str, doc) -> List[str]:
        """Generate suggestions for improving legal text"""
        suggestions = []
        
        # Check for common issues
        if len(doc.text.split()) < 50:
            suggestions.append("Consider adding more detail to ensure legal clarity")
        
        # Check for passive voice (simplified)
        passive_indicators = ["was", "were", "been", "being"]
        if any(word in text.lower() for word in passive_indicators):
            suggestions.append("Consider using active voice for clearer legal language")
        
        # Check for ambiguous terms
        ambiguous_terms = ["thing", "stuff", "it", "this", "that"]
        for term in ambiguous_terms:
            if f" {term} " in text.lower():
                suggestions.append(f"Replace ambiguous term '{term}' with specific legal terminology")
        
        # Check for missing legal formalities
        if "witness" not in text.lower() and "will" in text.lower():
            suggestions.append("Ensure proper witness requirements are addressed")
        
        # Check for date formats
        if re.search(r'\d{1,2}/\d{1,2}/\d{2,4}', text):
            suggestions.append("Consider using full date format (e.g., 'January 1, 2024') for legal clarity")
        
        return suggestions
    
    def _identify_risk_factors(self, text: str, doc) -> List[str]:
        """Identify potential legal risk factors"""
        risks = []
        
        # Check for incomplete information
        placeholders = ["[", "]", "___", "TBD", "to be determined"]
        if any(placeholder in text for placeholder in placeholders):
            risks.append("Document contains placeholder text that must be completed")
        
        # Check for conflicting information
        if "revoke" in text.lower() and "grant" in text.lower():
            risks.append("Document may contain conflicting provisions")
        
        # Check for missing essential elements
        if "will" in text.lower():
            essential_elements = ["executor", "beneficiary", "signature"]
            missing = [elem for elem in essential_elements if elem not in text.lower()]
            if missing:
                risks.append(f"Will may be missing essential elements: {', '.join(missing)}")
        
        # Check for potential capacity issues
        capacity_concerns = ["mental", "capacity", "competent", "sound mind"]
        if any(concern in text.lower() for concern in capacity_concerns):
            risks.append("Document references capacity - ensure proper assessment")
        
        return risks
    
    def _check_compliance(self, text: str, doc) -> List[str]:
        """Check compliance with Ontario legal requirements"""
        issues = []
        
        # Check will-specific compliance
        if "will" in text.lower():
            # Check for witness requirements
            if "witness" not in text.lower():
                issues.append("Will must include witness requirements per Ontario law")
            
            # Check for executor appointment
            if "executor" not in text.lower() and "executrix" not in text.lower():
                issues.append("Will should appoint an executor")
        
        # Check POA-specific compliance
        if "power of attorney" in text.lower():
            if "witness" not in text.lower():
                issues.append("Power of Attorney must include witness requirements")
            
            if "incapacity" not in text.lower() and "continuing" in text.lower():
                issues.append("Continuing POA should address incapacity provisions")
        
        # Check for required Ontario references
        ontario_refs = ["ontario", "succession law reform act", "substitute decisions act"]
        if not any(ref in text.lower() for ref in ontario_refs):
            issues.append("Consider referencing applicable Ontario legislation")
        
        return issues
    
    def _calculate_complexity(self, doc) -> float:
        """Calculate text complexity score"""
        # Factors: sentence length, word length, legal terminology density
        avg_sentence_length = len(doc) / len(list(doc.sents)) if list(doc.sents) else 0
        avg_word_length = sum(len(token.text) for token in doc if not token.is_space) / len([t for t in doc if not t.is_space])
        
        # Legal terminology density
        legal_term_count = sum(1 for token in doc if token.text.lower() in 
                              [term for terms in self.legal_terms.values() for term in terms])
        legal_density = legal_term_count / len(doc) if len(doc) > 0 else 0
        
        # Normalize and combine factors
        sentence_complexity = min(1.0, avg_sentence_length / 30)  # 30 words = high complexity
        word_complexity = min(1.0, avg_word_length / 10)  # 10 chars = high complexity
        
        return (sentence_complexity + word_complexity + legal_density) / 3
    
    def suggest_legal_wording(self, user_input: str, document_type: str) -> List[str]:
        """Suggest improved legal wording for user input"""
        suggestions = []
        
        # Analyze user input
        analysis = self.analyze_legal_text(user_input)
        
        # Generate context-specific suggestions
        if document_type.lower() == "will":
            suggestions.extend(self._suggest_will_wording(user_input, analysis))
        elif "power of attorney" in document_type.lower():
            suggestions.extend(self._suggest_poa_wording(user_input, analysis))
        
        # General legal writing improvements
        suggestions.extend(self._suggest_general_improvements(user_input, analysis))
        
        return suggestions[:10]  # Limit to top 10 suggestions
    
    def _suggest_will_wording(self, text: str, analysis: LegalAnalysis) -> List[str]:
        """Suggest will-specific wording improvements"""
        suggestions = []
        
        # Common will clauses
        if "give" in text.lower() and "bequeath" not in text.lower():
            suggestions.append("Consider using 'give, devise and bequeath' for more formal legal language")
        
        if "children" in text.lower() and "issue" not in text.lower():
            suggestions.append("Consider using 'children and issue' to include grandchildren")
        
        if "money" in text.lower():
            suggestions.append("Specify exact amounts or percentages for monetary bequests")
        
        return suggestions
    
    def _suggest_poa_wording(self, text: str, analysis: LegalAnalysis) -> List[str]:
        """Suggest power of attorney-specific wording improvements"""
        suggestions = []
        
        if "authorize" in text.lower() and "empower" not in text.lower():
            suggestions.append("Consider using 'authorize and empower' for comprehensive delegation")
        
        if "property" in text.lower() and "real and personal" not in text.lower():
            suggestions.append("Specify 'real and personal property' for clarity")
        
        if "decisions" in text.lower() and "substitute decision maker" not in text.lower():
            suggestions.append("Consider referencing 'substitute decision maker' per Ontario law")
        
        return suggestions
    
    def _suggest_general_improvements(self, text: str, analysis: LegalAnalysis) -> List[str]:
        """Suggest general legal writing improvements"""
        suggestions = []
        
        # Formality improvements
        if analysis.sentiment["formality"] < 0.5:
            suggestions.append("Consider using more formal legal language")
        
        # Clarity improvements
        if analysis.readability_score < 0.3:
            suggestions.append("Consider simplifying sentence structure for better clarity")
        
        # Completeness improvements
        if analysis.word_count < 20:
            suggestions.append("Consider adding more specific details")
        
        return suggestions
    
    def extract_key_information(self, text: str) -> Dict[str, Any]:
        """Extract key information from legal text"""
        analysis = self.analyze_legal_text(text)
        
        # Organize entities by type
        entities_by_type = {}
        for entity in analysis.entities:
            if entity.label not in entities_by_type:
                entities_by_type[entity.label] = []
            entities_by_type[entity.label].append(entity.text)
        
        # Extract dates
        dates = entities_by_type.get("DATE", [])
        
        # Extract people
        people = entities_by_type.get("PERSON", [])
        
        # Extract organizations
        organizations = entities_by_type.get("ORG", [])
        
        # Extract monetary amounts
        money = entities_by_type.get("MONEY", [])
        
        return {
            "entities_by_type": entities_by_type,
            "key_people": people,
            "organizations": organizations,
            "dates": dates,
            "monetary_amounts": money,
            "legal_concepts": analysis.legal_concepts,
            "document_metrics": {
                "word_count": analysis.word_count,
                "sentence_count": analysis.sentence_count,
                "readability_score": analysis.readability_score,
                "complexity_score": analysis.complexity_score
            }
        }

# Initialize global NLP service instance
nlp_service = LegalNLPService()

def get_nlp_service() -> LegalNLPService:
    """Get the global NLP service instance"""
    return nlp_service

