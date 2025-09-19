"""
Legal Research Service
Integrates with CanLII API and other legal databases for comprehensive legal case research
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import re
import time
from urllib.parse import quote
import os
from functools import lru_cache

from .nlp_service import get_nlp_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LegalCase:
    """Represents a legal case from research"""
    database_id: str
    case_id: str
    title: str
    citation: str
    url: str
    decision_date: Optional[str] = None
    keywords: Optional[str] = None
    summary: Optional[str] = None
    relevance_score: float = 0.0
    jurisdiction: str = ""
    court_level: str = ""

@dataclass
class LegalCitation:
    """Represents a legal citation or reference"""
    cited_case_id: str
    citing_case_id: str
    citation_type: str  # "cited" or "citing"
    title: str
    citation: str
    relevance: str = ""

@dataclass
class LegalResearchResult:
    """Comprehensive legal research results"""
    query: str
    cases: List[LegalCase]
    related_legislation: List[Dict[str, Any]]
    citations: List[LegalCitation]
    search_metadata: Dict[str, Any]
    total_results: int
    search_time: float

class LegalResearchService:
    """
    Service for legal case research using CanLII API and other sources
    """
    
    def __init__(self):
        self.canlii_api_key = os.environ.get('CANLII_API_KEY')
        self.base_url = "https://api.canlii.org/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Ontario-Wills-App/2.0',
            'Accept': 'application/json'
        })
        
        # Cache for frequently accessed data
        self._court_databases = None
        self._legislation_databases = None
        
        # Rate limiting
        self._last_request_time = 0
        self._min_request_interval = 1.0  # Minimum 1 second between requests
        
        # Ontario-specific database IDs
        self.ontario_databases = {
            'onca': 'Ontario Court of Appeal',
            'onsc': 'Ontario Superior Court of Justice',
            'oncj': 'Ontario Court of Justice',
            'onscdc': 'Ontario Superior Court of Justice - Divisional Court',
            'onscsm': 'Ontario Superior Court of Justice - Small Claims Court',
            'onlat': 'Licence Appeal Tribunal',
            'onhrt': 'Human Rights Tribunal of Ontario',
            'onlrb': 'Ontario Labour Relations Board'
        }
        
        # Legal concepts mapping for estate planning
        self.estate_concepts = {
            'will': ['testament', 'testamentary', 'executor', 'beneficiary', 'devise', 'bequest'],
            'power_of_attorney': ['attorney', 'substitute decision maker', 'incapacity', 'continuing'],
            'estate_planning': ['succession', 'inheritance', 'probate', 'estate administration'],
            'capacity': ['mental capacity', 'competence', 'sound mind', 'cognitive ability'],
            'witnesses': ['witness', 'attestation', 'execution', 'signing']
        }
    
    def _rate_limit(self):
        """Implement rate limiting for API requests"""
        current_time = time.time()
        time_since_last = current_time - self._last_request_time
        
        if time_since_last < self._min_request_interval:
            sleep_time = self._min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self._last_request_time = time.time()
    
    def _make_api_request(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Make a rate-limited API request to CanLII"""
        if not self.canlii_api_key:
            logger.warning("CanLII API key not configured")
            return None
        
        self._rate_limit()
        
        if params is None:
            params = {}
        
        params['api_key'] = self.canlii_api_key
        
        try:
            url = f"{self.base_url}/{endpoint}"
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse API response: {e}")
            return None
    
    @lru_cache(maxsize=1)
    def get_court_databases(self) -> Dict[str, Dict[str, str]]:
        """Get list of available court databases"""
        if self._court_databases is not None:
            return self._court_databases
        
        result = self._make_api_request("caseBrowse/en/")
        
        if result and 'caseDatabases' in result:
            databases = {}
            for db in result['caseDatabases']:
                databases[db['databaseId']] = {
                    'name': db['name'],
                    'jurisdiction': db['jurisdiction']
                }
            
            self._court_databases = databases
            return databases
        
        return {}
    
    def search_cases_by_concept(self, concept: str, jurisdiction: str = "on", 
                               limit: int = 20, date_range: Optional[Tuple[str, str]] = None) -> List[LegalCase]:
        """
        Search for cases related to a legal concept
        
        Args:
            concept: Legal concept to search for
            jurisdiction: Jurisdiction code (default: "on" for Ontario)
            limit: Maximum number of results
            date_range: Optional tuple of (start_date, end_date) in YYYY-MM-DD format
            
        Returns:
            List of relevant legal cases
        """
        cases = []
        
        # Get Ontario databases
        ontario_dbs = [db_id for db_id, name in self.ontario_databases.items()]
        
        # Search each Ontario database
        for db_id in ontario_dbs[:3]:  # Limit to top 3 courts for performance
            db_cases = self._search_database_cases(db_id, concept, limit//3, date_range)
            cases.extend(db_cases)
        
        # Sort by relevance and limit results
        cases.sort(key=lambda x: x.relevance_score, reverse=True)
        return cases[:limit]
    
    def _search_database_cases(self, database_id: str, concept: str, limit: int,
                              date_range: Optional[Tuple[str, str]] = None) -> List[LegalCase]:
        """Search for cases in a specific database"""
        params = {
            'offset': 0,
            'resultCount': min(limit, 100)  # API max is 10,000, but we'll be conservative
        }
        
        # Add date range if specified
        if date_range:
            start_date, end_date = date_range
            params['decisionDateAfter'] = start_date
            params['decisionDateBefore'] = end_date
        
        result = self._make_api_request(f"caseBrowse/en/{database_id}/", params)
        
        if not result or 'cases' not in result:
            return []
        
        cases = []
        for case_data in result['cases']:
            # Calculate relevance score based on concept matching
            relevance_score = self._calculate_relevance(case_data, concept)
            
            if relevance_score > 0.1:  # Only include somewhat relevant cases
                case = LegalCase(
                    database_id=case_data['databaseId'],
                    case_id=case_data['caseId']['en'] if isinstance(case_data['caseId'], dict) else case_data['caseId'],
                    title=case_data['title'],
                    citation=case_data['citation'],
                    url=f"https://canlii.ca/t/{case_data.get('url', '').split('/')[-1]}" if 'url' in case_data else "",
                    relevance_score=relevance_score,
                    jurisdiction="on",
                    court_level=self._get_court_level(case_data['databaseId'])
                )
                cases.append(case)
        
        return cases
    
    def _calculate_relevance(self, case_data: Dict[str, Any], concept: str) -> float:
        """Calculate relevance score for a case based on concept matching"""
        score = 0.0
        
        # Check title for concept keywords
        title = case_data.get('title', '').lower()
        concept_lower = concept.lower()
        
        # Direct concept match
        if concept_lower in title:
            score += 0.8
        
        # Check for related terms
        if concept in self.estate_concepts:
            related_terms = self.estate_concepts[concept]
            for term in related_terms:
                if term.lower() in title:
                    score += 0.3
        
        # Check keywords if available
        keywords = case_data.get('keywords', '')
        if keywords:
            keywords_lower = keywords.lower()
            if concept_lower in keywords_lower:
                score += 0.5
            
            if concept in self.estate_concepts:
                for term in self.estate_concepts[concept]:
                    if term.lower() in keywords_lower:
                        score += 0.2
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _get_court_level(self, database_id: str) -> str:
        """Get court level based on database ID"""
        court_levels = {
            'onca': 'Appeal',
            'onsc': 'Superior',
            'oncj': 'Provincial',
            'onscdc': 'Divisional',
            'onscsm': 'Small Claims'
        }
        return court_levels.get(database_id, 'Other')
    
    def get_case_details(self, database_id: str, case_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed metadata for a specific case"""
        result = self._make_api_request(f"caseBrowse/en/{database_id}/{case_id}/")
        return result
    
    def get_case_citations(self, database_id: str, case_id: str) -> Dict[str, List[LegalCitation]]:
        """Get citation information for a case"""
        citations = {
            'cited_cases': [],
            'citing_cases': [],
            'cited_legislation': []
        }
        
        # Get cases cited by this case
        cited_result = self._make_api_request(f"caseCitator/en/{database_id}/{case_id}/citedCases")
        if cited_result and 'citedCases' in cited_result:
            for cited in cited_result['citedCases']:
                citation = LegalCitation(
                    cited_case_id=cited['caseId']['en'] if isinstance(cited['caseId'], dict) else cited['caseId'],
                    citing_case_id=case_id,
                    citation_type='cited',
                    title=cited['title'],
                    citation=cited['citation']
                )
                citations['cited_cases'].append(citation)
        
        # Get cases that cite this case
        citing_result = self._make_api_request(f"caseCitator/en/{database_id}/{case_id}/citingCases")
        if citing_result and 'citingCases' in citing_result:
            for citing in citing_result['citingCases']:
                citation = LegalCitation(
                    cited_case_id=case_id,
                    citing_case_id=citing['caseId']['en'] if isinstance(citing['caseId'], dict) else citing['caseId'],
                    citation_type='citing',
                    title=citing['title'],
                    citation=citing['citation']
                )
                citations['citing_cases'].append(citation)
        
        return citations
    
    def search_relevant_cases_for_document(self, document_text: str, document_type: str) -> LegalResearchResult:
        """
        Search for cases relevant to a specific document using NLP analysis
        
        Args:
            document_text: Text of the legal document
            document_type: Type of document (will, power_of_attorney, etc.)
            
        Returns:
            Comprehensive research results
        """
        start_time = time.time()
        
        # Use NLP service to extract legal concepts
        nlp_service = get_nlp_service()
        analysis = nlp_service.analyze_legal_text(document_text)
        
        # Extract key concepts for search
        search_concepts = self._extract_search_concepts(analysis, document_type)
        
        all_cases = []
        all_citations = []
        
        # Search for each concept
        for concept in search_concepts[:5]:  # Limit to top 5 concepts
            concept_cases = self.search_cases_by_concept(concept, limit=10)
            all_cases.extend(concept_cases)
        
        # Remove duplicates and sort by relevance
        unique_cases = {}
        for case in all_cases:
            key = f"{case.database_id}_{case.case_id}"
            if key not in unique_cases or case.relevance_score > unique_cases[key].relevance_score:
                unique_cases[key] = case
        
        final_cases = list(unique_cases.values())
        final_cases.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # Get citations for top cases
        for case in final_cases[:5]:  # Get citations for top 5 cases
            case_citations = self.get_case_citations(case.database_id, case.case_id)
            all_citations.extend(case_citations['cited_cases'])
            all_citations.extend(case_citations['citing_cases'])
        
        search_time = time.time() - start_time
        
        return LegalResearchResult(
            query=f"Document analysis: {document_type}",
            cases=final_cases[:20],  # Return top 20 cases
            related_legislation=self._get_related_legislation(document_type),
            citations=all_citations[:50],  # Return top 50 citations
            search_metadata={
                'concepts_searched': search_concepts,
                'nlp_analysis_summary': {
                    'entities_found': len(analysis.entities),
                    'legal_concepts': len(analysis.legal_concepts),
                    'complexity_score': analysis.complexity_score
                }
            },
            total_results=len(final_cases),
            search_time=search_time
        )
    
    def _extract_search_concepts(self, nlp_analysis, document_type: str) -> List[str]:
        """Extract relevant search concepts from NLP analysis"""
        concepts = []
        
        # Add document type as primary concept
        concepts.append(document_type)
        
        # Add legal concepts from NLP analysis
        concepts.extend(nlp_analysis.legal_concepts[:3])
        
        # Add document-specific concepts
        if document_type == 'will':
            concepts.extend(['executor', 'beneficiary', 'testamentary'])
        elif 'power_of_attorney' in document_type:
            concepts.extend(['attorney', 'substitute decision maker', 'incapacity'])
        
        # Add concepts based on entities found
        for entity in nlp_analysis.entities:
            if entity.label == 'LEGAL_ROLE':
                concepts.append(entity.text.lower())
        
        # Remove duplicates and return
        return list(set(concepts))
    
    def _get_related_legislation(self, document_type: str) -> List[Dict[str, Any]]:
        """Get related Ontario legislation for document type"""
        legislation = []
        
        if document_type == 'will':
            legislation.append({
                'title': 'Succession Law Reform Act',
                'jurisdiction': 'Ontario',
                'citation': 'RSO 1990, c S.26',
                'relevance': 'Primary legislation governing wills in Ontario'
            })
            legislation.append({
                'title': 'Estates Act',
                'jurisdiction': 'Ontario', 
                'citation': 'RSO 1990, c E.21',
                'relevance': 'Governs estate administration'
            })
        
        elif 'power_of_attorney' in document_type:
            legislation.append({
                'title': 'Substitute Decisions Act',
                'jurisdiction': 'Ontario',
                'citation': '1992, SO 1992, c 30',
                'relevance': 'Primary legislation governing powers of attorney in Ontario'
            })
        
        return legislation
    
    def search_by_natural_language(self, query: str, limit: int = 10) -> List[LegalCase]:
        """
        Search using natural language query
        
        Args:
            query: Natural language search query
            limit: Maximum number of results
            
        Returns:
            List of relevant cases
        """
        # Use NLP to extract concepts from query
        nlp_service = get_nlp_service()
        analysis = nlp_service.analyze_legal_text(query)
        
        # Extract key terms for search
        search_terms = []
        
        # Add legal concepts
        search_terms.extend(analysis.legal_concepts)
        
        # Add entities
        for entity in analysis.entities:
            if entity.label in ['LEGAL_ROLE', 'LEGAL_DOCUMENT']:
                search_terms.append(entity.text.lower())
        
        # If no specific legal terms found, use the query as-is
        if not search_terms:
            search_terms = [query.lower()]
        
        # Search for each term
        all_cases = []
        for term in search_terms[:3]:  # Limit to top 3 terms
            cases = self.search_cases_by_concept(term, limit=limit//len(search_terms[:3]))
            all_cases.extend(cases)
        
        # Remove duplicates and sort
        unique_cases = {}
        for case in all_cases:
            key = f"{case.database_id}_{case.case_id}"
            if key not in unique_cases or case.relevance_score > unique_cases[key].relevance_score:
                unique_cases[key] = case
        
        final_cases = list(unique_cases.values())
        final_cases.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return final_cases[:limit]
    
    def get_recent_ontario_cases(self, area: str = "estate", limit: int = 10) -> List[LegalCase]:
        """Get recent Ontario cases in a specific legal area"""
        # Calculate date range for recent cases (last 2 years)
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
        
        return self.search_cases_by_concept(area, limit=limit, date_range=(start_date, end_date))

# Initialize global legal research service
legal_research_service = LegalResearchService()

def get_legal_research_service() -> LegalResearchService:
    """Get the global legal research service instance"""
    return legal_research_service

