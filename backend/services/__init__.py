# Services module
from .nlp_service import LegalNLPService, get_nlp_service
from .legal_research_service import LegalResearchService
from .integrated_ai_service import IntegratedAIService, get_integrated_ai_service

__all__ = [
    'LegalNLPService',
    'get_nlp_service', 
    'LegalResearchService',
    'IntegratedAIService',
    'get_integrated_ai_service'
]