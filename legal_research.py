"""
Legal Research API Routes
Provides endpoints for legal case research and citation analysis
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import logging
from typing import Dict, Any

from ..services.legal_research_service import get_legal_research_service
from ..services.auth_service import token_required

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
legal_research_bp = Blueprint('legal_research', __name__, url_prefix='/api/legal-research')

@legal_research_bp.route('/search-cases', methods=['POST'])
@cross_origin()
@token_required
def search_cases():
    """
    Search for legal cases using various criteria
    
    Expected JSON payload:
    {
        "query": "Natural language search query",
        "concept": "Legal concept to search for",
        "jurisdiction": "on",
        "limit": 20,
        "date_range": {
            "start": "2020-01-01",
            "end": "2024-12-31"
        }
    }
    
    Returns:
    {
        "success": true,
        "cases": [...],
        "total_results": 15,
        "search_metadata": {...}
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request data is required'
            }), 400
        
        research_service = get_legal_research_service()
        
        # Extract search parameters
        query = data.get('query', '')
        concept = data.get('concept', '')
        jurisdiction = data.get('jurisdiction', 'on')
        limit = min(data.get('limit', 20), 100)  # Cap at 100
        date_range = data.get('date_range')
        
        # Convert date range if provided
        date_tuple = None
        if date_range and 'start' in date_range and 'end' in date_range:
            date_tuple = (date_range['start'], date_range['end'])
        
        # Perform search based on available parameters
        if query:
            # Natural language search
            cases = research_service.search_by_natural_language(query, limit)
        elif concept:
            # Concept-based search
            cases = research_service.search_cases_by_concept(concept, jurisdiction, limit, date_tuple)
        else:
            return jsonify({
                'success': False,
                'error': 'Either query or concept is required'
            }), 400
        
        # Convert cases to serializable format
        cases_data = []
        for case in cases:
            case_dict = {
                'database_id': case.database_id,
                'case_id': case.case_id,
                'title': case.title,
                'citation': case.citation,
                'url': case.url,
                'decision_date': case.decision_date,
                'keywords': case.keywords,
                'summary': case.summary,
                'relevance_score': case.relevance_score,
                'jurisdiction': case.jurisdiction,
                'court_level': case.court_level
            }
            cases_data.append(case_dict)
        
        return jsonify({
            'success': True,
            'cases': cases_data,
            'total_results': len(cases_data),
            'search_metadata': {
                'query': query,
                'concept': concept,
                'jurisdiction': jurisdiction,
                'date_range': date_range
            }
        })
        
    except Exception as e:
        logger.error(f"Error searching cases: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error during case search'
        }), 500

@legal_research_bp.route('/analyze-document', methods=['POST'])
@cross_origin()
@token_required
def analyze_document_for_cases():
    """
    Analyze a document and find relevant legal cases
    
    Expected JSON payload:
    {
        "document_text": "Text of the legal document",
        "document_type": "will|power_of_attorney|general"
    }
    
    Returns:
    {
        "success": true,
        "research_results": {
            "cases": [...],
            "related_legislation": [...],
            "citations": [...],
            "search_metadata": {...}
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'document_text' not in data:
            return jsonify({
                'success': False,
                'error': 'Document text is required'
            }), 400
        
        document_text = data['document_text']
        document_type = data.get('document_type', 'general')
        
        if not document_text.strip():
            return jsonify({
                'success': False,
                'error': 'Document text cannot be empty'
            }), 400
        
        research_service = get_legal_research_service()
        
        # Perform comprehensive document analysis
        research_results = research_service.search_relevant_cases_for_document(
            document_text, document_type
        )
        
        # Convert to serializable format
        results_data = {
            'query': research_results.query,
            'cases': [
                {
                    'database_id': case.database_id,
                    'case_id': case.case_id,
                    'title': case.title,
                    'citation': case.citation,
                    'url': case.url,
                    'decision_date': case.decision_date,
                    'keywords': case.keywords,
                    'summary': case.summary,
                    'relevance_score': case.relevance_score,
                    'jurisdiction': case.jurisdiction,
                    'court_level': case.court_level
                }
                for case in research_results.cases
            ],
            'related_legislation': research_results.related_legislation,
            'citations': [
                {
                    'cited_case_id': citation.cited_case_id,
                    'citing_case_id': citation.citing_case_id,
                    'citation_type': citation.citation_type,
                    'title': citation.title,
                    'citation': citation.citation,
                    'relevance': citation.relevance
                }
                for citation in research_results.citations
            ],
            'search_metadata': research_results.search_metadata,
            'total_results': research_results.total_results,
            'search_time': research_results.search_time
        }
        
        return jsonify({
            'success': True,
            'research_results': results_data,
            'document_type': document_type
        })
        
    except Exception as e:
        logger.error(f"Error analyzing document for cases: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error during document analysis'
        }), 500

@legal_research_bp.route('/case-details/<database_id>/<case_id>', methods=['GET'])
@cross_origin()
@token_required
def get_case_details(database_id: str, case_id: str):
    """
    Get detailed information about a specific case
    
    Returns:
    {
        "success": true,
        "case_details": {...},
        "citations": {...}
    }
    """
    try:
        research_service = get_legal_research_service()
        
        # Get case details
        case_details = research_service.get_case_details(database_id, case_id)
        
        if not case_details:
            return jsonify({
                'success': False,
                'error': 'Case not found or API error'
            }), 404
        
        # Get citation information
        citations = research_service.get_case_citations(database_id, case_id)
        
        # Convert citations to serializable format
        citations_data = {}
        for citation_type, citation_list in citations.items():
            citations_data[citation_type] = [
                {
                    'cited_case_id': citation.cited_case_id,
                    'citing_case_id': citation.citing_case_id,
                    'citation_type': citation.citation_type,
                    'title': citation.title,
                    'citation': citation.citation,
                    'relevance': citation.relevance
                }
                for citation in citation_list
            ]
        
        return jsonify({
            'success': True,
            'case_details': case_details,
            'citations': citations_data
        })
        
    except Exception as e:
        logger.error(f"Error getting case details: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error while fetching case details'
        }), 500

@legal_research_bp.route('/recent-cases', methods=['GET'])
@cross_origin()
@token_required
def get_recent_cases():
    """
    Get recent Ontario cases in estate planning and related areas
    
    Query parameters:
    - area: Legal area (estate, will, power_of_attorney, etc.)
    - limit: Number of results (default: 10, max: 50)
    
    Returns:
    {
        "success": true,
        "recent_cases": [...],
        "area": "estate",
        "total_results": 10
    }
    """
    try:
        area = request.args.get('area', 'estate')
        limit = min(int(request.args.get('limit', 10)), 50)
        
        research_service = get_legal_research_service()
        
        # Get recent cases
        recent_cases = research_service.get_recent_ontario_cases(area, limit)
        
        # Convert to serializable format
        cases_data = []
        for case in recent_cases:
            case_dict = {
                'database_id': case.database_id,
                'case_id': case.case_id,
                'title': case.title,
                'citation': case.citation,
                'url': case.url,
                'decision_date': case.decision_date,
                'keywords': case.keywords,
                'summary': case.summary,
                'relevance_score': case.relevance_score,
                'jurisdiction': case.jurisdiction,
                'court_level': case.court_level
            }
            cases_data.append(case_dict)
        
        return jsonify({
            'success': True,
            'recent_cases': cases_data,
            'area': area,
            'total_results': len(cases_data)
        })
        
    except ValueError:
        return jsonify({
            'success': False,
            'error': 'Invalid limit parameter'
        }), 400
    except Exception as e:
        logger.error(f"Error getting recent cases: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error while fetching recent cases'
        }), 500

@legal_research_bp.route('/court-databases', methods=['GET'])
@cross_origin()
@token_required
def get_court_databases():
    """
    Get list of available court databases
    
    Returns:
    {
        "success": true,
        "databases": {...},
        "ontario_databases": {...}
    }
    """
    try:
        research_service = get_legal_research_service()
        
        # Get all databases
        all_databases = research_service.get_court_databases()
        
        # Filter Ontario databases
        ontario_databases = {
            db_id: info for db_id, info in all_databases.items()
            if info['jurisdiction'] == 'on'
        }
        
        return jsonify({
            'success': True,
            'databases': all_databases,
            'ontario_databases': ontario_databases,
            'total_databases': len(all_databases),
            'ontario_count': len(ontario_databases)
        })
        
    except Exception as e:
        logger.error(f"Error getting court databases: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error while fetching databases'
        }), 500

@legal_research_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Health check endpoint for legal research service"""
    try:
        research_service = get_legal_research_service()
        
        # Test basic functionality
        has_api_key = research_service.canlii_api_key is not None
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'api_key_configured': has_api_key,
            'ontario_databases_available': len(research_service.ontario_databases),
            'rate_limiting_enabled': True
        })
        
    except Exception as e:
        logger.error(f"Legal research service health check failed: {e}")
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500

