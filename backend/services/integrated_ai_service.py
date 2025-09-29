"""
Integrated AI Service for Legal Document Processing
Combines NLP, legal research, and AI analysis in a unified interface
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime

from .nlp_service import LegalNLPService, get_nlp_service
from .legal_research_service import LegalResearchService
from .enhanced_ai_legal_service import EnhancedAILegalService

logger = logging.getLogger(__name__)

@dataclass
class IntegratedAnalysisResult:
    """Comprehensive analysis result from all AI services"""
    nlp_analysis: Dict[str, Any]
    legal_research: Dict[str, Any]
    ai_suggestions: List[str]
    compliance_score: float
    risk_assessment: Dict[str, Any]
    document_improvements: List[str]
    legal_citations: List[Dict[str, Any]]
    confidence_score: float

class IntegratedAIService:
    """
    Unified AI service that combines all legal AI capabilities
    """
    
    def __init__(self):
        self.nlp_service = get_nlp_service()
        self.research_service = LegalResearchService()
        self.ai_service = EnhancedAILegalService()
        self.initialized = False
        
    async def initialize(self):
        """Initialize all AI services"""
        try:
            logger.info("Initializing integrated AI service...")
            # Initialize services that need async setup
            if hasattr(self.research_service, 'initialize'):
                await self.research_service.initialize()
            if hasattr(self.ai_service, 'initialize'):
                await self.ai_service.initialize()
            self.initialized = True
            logger.info("Integrated AI service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize integrated AI service: {e}")
            raise
    
    async def analyze_document_comprehensive(
        self, 
        document_text: str, 
        document_type: str,
        user_context: Optional[Dict[str, Any]] = None
    ) -> IntegratedAnalysisResult:
        """
        Perform comprehensive document analysis using all available AI services
        """
        if not self.initialized:
            await self.initialize()
            
        try:
            # Run analyses in parallel for better performance
            tasks = [
                self._analyze_nlp(document_text, document_type),
                self._research_legal_context(document_text, document_type),
                self._generate_ai_suggestions(document_text, document_type, user_context)
            ]
            
            nlp_result, research_result, ai_result = await asyncio.gather(*tasks)
            
            # Calculate overall confidence and compliance scores
            confidence_score = self._calculate_confidence_score(nlp_result, research_result, ai_result)
            compliance_score = self._calculate_compliance_score(nlp_result, research_result, ai_result)
            
            # Generate integrated recommendations
            improvements = self._generate_integrated_improvements(
                nlp_result, research_result, ai_result, document_type
            )
            
            return IntegratedAnalysisResult(
                nlp_analysis=nlp_result,
                legal_research=research_result,
                ai_suggestions=ai_result.get('suggestions', []),
                compliance_score=compliance_score,
                risk_assessment=ai_result.get('risk_assessment', {}),
                document_improvements=improvements,
                legal_citations=research_result.get('citations', []),
                confidence_score=confidence_score
            )
            
        except Exception as e:
            logger.error(f"Comprehensive document analysis failed: {e}")
            # Return a basic result to prevent complete failure
            return IntegratedAnalysisResult(
                nlp_analysis={},
                legal_research={},
                ai_suggestions=[],
                compliance_score=0.0,
                risk_assessment={},
                document_improvements=[],
                legal_citations=[],
                confidence_score=0.0
            )
    
    async def _analyze_nlp(self, text: str, doc_type: str) -> Dict[str, Any]:
        """Perform NLP analysis"""
        try:
            analysis = self.nlp_service.analyze_legal_text(text)
            return {
                'entities': [entity.__dict__ if hasattr(entity, '__dict__') else entity for entity in analysis.entities],
                'sentiment': analysis.sentiment,
                'readability_score': analysis.readability_score,
                'legal_concepts': analysis.legal_concepts,
                'complexity_score': analysis.complexity_score,
                'word_count': analysis.word_count
            }
        except Exception as e:
            logger.error(f"NLP analysis failed: {e}")
            return {}
    
    async def _research_legal_context(self, text: str, doc_type: str) -> Dict[str, Any]:
        """Research legal context and find relevant cases"""
        try:
            # Extract key terms for research
            key_terms = self.nlp_service.extract_key_information(text)
            search_query = self._build_research_query(key_terms, doc_type)
            
            # Perform legal research
            research_results = await self.research_service.search_cases_async(
                query=search_query,
                jurisdiction="ontario",
                max_results=5
            )
            
            return {
                'search_query': search_query,
                'cases': research_results.get('cases', []),
                'citations': research_results.get('citations', []),
                'total_results': research_results.get('total_results', 0)
            }
        except Exception as e:
            logger.error(f"Legal research failed: {e}")
            return {}
    
    async def _generate_ai_suggestions(
        self, 
        text: str, 
        doc_type: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate AI-powered suggestions and risk assessment"""
        try:
            # Use the enhanced AI service for suggestions
            suggestions = []
            risk_assessment = {}
            
            if hasattr(self.ai_service, 'analyze_document'):
                ai_analysis = await self.ai_service.analyze_document(
                    document_content=text,
                    document_type=doc_type,
                    client_info=context or {}
                )
                suggestions = ai_analysis.get('suggestions', [])
                risk_assessment = ai_analysis.get('risk_assessment', {})
            
            return {
                'suggestions': suggestions,
                'risk_assessment': risk_assessment,
                'ai_confidence': risk_assessment.get('confidence', 0.5)
            }
        except Exception as e:
            logger.error(f"AI suggestion generation failed: {e}")
            return {'suggestions': [], 'risk_assessment': {}}
    
    def _build_research_query(self, key_terms: Dict[str, Any], doc_type: str) -> str:
        """Build an effective search query for legal research"""
        query_parts = []
        
        # Add document type specific terms
        if doc_type == 'will':
            query_parts.append('will testament ontario')
        elif 'power_of_attorney' in doc_type or 'poa' in doc_type:
            query_parts.append('power of attorney ontario')
            
        # Add extracted legal concepts
        legal_concepts = key_terms.get('legal_concepts', [])
        if legal_concepts:
            query_parts.extend(legal_concepts[:3])  # Top 3 concepts
            
        # Add entities (people, organizations, etc.)
        entities = key_terms.get('entities', [])
        entity_terms = [entity.get('text', '') for entity in entities 
                       if entity.get('label') in ['ORG', 'PERSON', 'LAW']]
        query_parts.extend(entity_terms[:2])  # Top 2 relevant entities
        
        return ' '.join(query_parts).strip()
    
    def _calculate_confidence_score(
        self, 
        nlp_result: Dict[str, Any], 
        research_result: Dict[str, Any], 
        ai_result: Dict[str, Any]
    ) -> float:
        """Calculate overall confidence score"""
        scores = []
        
        # NLP confidence based on complexity and readability
        if nlp_result.get('readability_score'):
            scores.append(min(nlp_result['readability_score'] / 100, 1.0))
            
        # Research confidence based on number of relevant cases found
        case_count = len(research_result.get('cases', []))
        if case_count > 0:
            scores.append(min(case_count / 5, 1.0))  # Max score at 5 cases
            
        # AI confidence
        ai_confidence = ai_result.get('ai_confidence', 0.5)
        scores.append(ai_confidence)
        
        return sum(scores) / len(scores) if scores else 0.5
    
    def _calculate_compliance_score(
        self, 
        nlp_result: Dict[str, Any], 
        research_result: Dict[str, Any], 
        ai_result: Dict[str, Any]
    ) -> float:
        """Calculate legal compliance score"""
        base_score = 0.7  # Base compliance assumption
        
        # Adjust based on risk factors
        risk_factors = ai_result.get('risk_assessment', {}).get('risk_factors', [])
        critical_risks = len([r for r in risk_factors if r.get('severity') == 'critical'])
        
        # Reduce score for critical risks
        score_reduction = critical_risks * 0.1
        
        # Increase score for good legal concept coverage
        legal_concepts = nlp_result.get('legal_concepts', [])
        if len(legal_concepts) >= 3:
            base_score += 0.1
            
        # Increase score for relevant case law found
        cases_found = len(research_result.get('cases', []))
        if cases_found > 0:
            base_score += 0.1
            
        return max(0.0, min(1.0, base_score - score_reduction))
    
    def _generate_integrated_improvements(
        self,
        nlp_result: Dict[str, Any],
        research_result: Dict[str, Any], 
        ai_result: Dict[str, Any],
        doc_type: str
    ) -> List[str]:
        """Generate integrated improvement suggestions"""
        improvements = []
        
        # Add AI suggestions
        improvements.extend(ai_result.get('suggestions', []))
        
        # Add NLP-based improvements
        complexity_score = nlp_result.get('complexity_score', 0)
        if complexity_score > 0.8:
            improvements.append("Consider simplifying language for better clarity")
            
        readability = nlp_result.get('readability_score', 0)
        if readability < 50:
            improvements.append("Improve readability by using shorter sentences and simpler words")
            
        # Add research-based improvements
        case_count = len(research_result.get('cases', []))
        if case_count == 0:
            improvements.append("Consider adding references to relevant Ontario case law")
        elif case_count > 0:
            improvements.append(f"Found {case_count} relevant cases that could strengthen your document")
            
        # Document-specific improvements
        if doc_type == 'will':
            if 'executor' not in nlp_result.get('legal_concepts', []):
                improvements.append("Ensure executor appointment is clearly specified")
        elif 'poa' in doc_type:
            if 'attorney' not in nlp_result.get('legal_concepts', []):
                improvements.append("Clearly define attorney powers and limitations")
                
        return list(set(improvements))  # Remove duplicates
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get status of all integrated services"""
        return {
            'initialized': self.initialized,
            'nlp_service': hasattr(self, 'nlp_service') and self.nlp_service is not None,
            'research_service': hasattr(self, 'research_service') and self.research_service is not None,
            'ai_service': hasattr(self, 'ai_service') and self.ai_service is not None,
            'timestamp': datetime.now().isoformat()
        }

# Global instance
_integrated_ai_service = None

def get_integrated_ai_service() -> IntegratedAIService:
    """Get global integrated AI service instance"""
    global _integrated_ai_service
    if _integrated_ai_service is None:
        _integrated_ai_service = IntegratedAIService()
    return _integrated_ai_service