"""
NLP API Routes for Legal Text Analysis
Provides endpoints for advanced legal text processing and analysis
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import logging
from typing import Dict, Any

from ..services.nlp_service import get_nlp_service
from ..services.auth_service import token_required

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
nlp_bp = Blueprint('nlp', __name__, url_prefix='/api/nlp')

@nlp_bp.route('/analyze', methods=['POST'])
@cross_origin()
@token_required
def analyze_text():
    """
    Analyze legal text using advanced NLP techniques
    
    Expected JSON payload:
    {
        "text": "Legal text to analyze",
        "document_type": "will|power_of_attorney|general"
    }
    
    Returns:
    {
        "success": true,
        "analysis": {
            "entities": [...],
            "sentiment": {...},
            "readability_score": 0.75,
            "legal_concepts": [...],
            "suggestions": [...],
            "risk_factors": [...],
            "compliance_issues": [...],
            "metrics": {...}
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Text is required'
            }), 400
        
        text = data['text']
        document_type = data.get('document_type', 'general')
        
        if not text.strip():
            return jsonify({
                'success': False,
                'error': 'Text cannot be empty'
            }), 400
        
        # Get NLP service
        nlp_service = get_nlp_service()
        
        # Perform analysis
        analysis = nlp_service.analyze_legal_text(text)
        
        # Convert to serializable format
        analysis_dict = {
            'entities': [
                {
                    'text': entity.text,
                    'label': entity.label,
                    'start': entity.start,
                    'end': entity.end,
                    'confidence': entity.confidence,
                    'description': entity.description
                }
                for entity in analysis.entities
            ],
            'sentiment': analysis.sentiment,
            'readability_score': analysis.readability_score,
            'legal_concepts': analysis.legal_concepts,
            'suggestions': analysis.suggestions,
            'risk_factors': analysis.risk_factors,
            'compliance_issues': analysis.compliance_issues,
            'metrics': {
                'word_count': analysis.word_count,
                'sentence_count': analysis.sentence_count,
                'complexity_score': analysis.complexity_score
            }
        }
        
        return jsonify({
            'success': True,
            'analysis': analysis_dict,
            'document_type': document_type
        })
        
    except Exception as e:
        logger.error(f"Error analyzing text: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error during text analysis'
        }), 500

@nlp_bp.route('/suggest-wording', methods=['POST'])
@cross_origin()
@token_required
def suggest_wording():
    """
    Get wording suggestions for legal text
    
    Expected JSON payload:
    {
        "text": "User input text",
        "document_type": "will|power_of_attorney|general",
        "context": "Optional context information"
    }
    
    Returns:
    {
        "success": true,
        "suggestions": [
            "Suggestion 1",
            "Suggestion 2",
            ...
        ],
        "improved_text": "Suggested improved version"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Text is required'
            }), 400
        
        text = data['text']
        document_type = data.get('document_type', 'general')
        context = data.get('context', '')
        
        if not text.strip():
            return jsonify({
                'success': False,
                'error': 'Text cannot be empty'
            }), 400
        
        # Get NLP service
        nlp_service = get_nlp_service()
        
        # Get wording suggestions
        suggestions = nlp_service.suggest_legal_wording(text, document_type)
        
        # Generate improved text (simplified version)
        improved_text = _generate_improved_text(text, suggestions, document_type)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions,
            'improved_text': improved_text,
            'original_text': text,
            'document_type': document_type
        })
        
    except Exception as e:
        logger.error(f"Error generating wording suggestions: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error during suggestion generation'
        }), 500

@nlp_bp.route('/extract-info', methods=['POST'])
@cross_origin()
@token_required
def extract_information():
    """
    Extract key information from legal text
    
    Expected JSON payload:
    {
        "text": "Legal text to process",
        "extraction_type": "entities|key_info|all"
    }
    
    Returns:
    {
        "success": true,
        "extracted_info": {
            "entities_by_type": {...},
            "key_people": [...],
            "organizations": [...],
            "dates": [...],
            "monetary_amounts": [...],
            "legal_concepts": [...],
            "document_metrics": {...}
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Text is required'
            }), 400
        
        text = data['text']
        extraction_type = data.get('extraction_type', 'all')
        
        if not text.strip():
            return jsonify({
                'success': False,
                'error': 'Text cannot be empty'
            }), 400
        
        # Get NLP service
        nlp_service = get_nlp_service()
        
        # Extract information
        extracted_info = nlp_service.extract_key_information(text)
        
        return jsonify({
            'success': True,
            'extracted_info': extracted_info,
            'extraction_type': extraction_type
        })
        
    except Exception as e:
        logger.error(f"Error extracting information: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error during information extraction'
        }), 500

@nlp_bp.route('/check-compliance', methods=['POST'])
@cross_origin()
@token_required
def check_compliance():
    """
    Check legal compliance for Ontario documents
    
    Expected JSON payload:
    {
        "text": "Document text to check",
        "document_type": "will|power_of_attorney_property|power_of_attorney_care",
        "user_info": {
            "age": 25,
            "province": "ontario"
        }
    }
    
    Returns:
    {
        "success": true,
        "compliance_check": {
            "is_compliant": true,
            "issues": [...],
            "warnings": [...],
            "requirements_met": [...],
            "requirements_missing": [...],
            "score": 0.85
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Text is required'
            }), 400
        
        text = data['text']
        document_type = data.get('document_type', 'will')
        user_info = data.get('user_info', {})
        
        if not text.strip():
            return jsonify({
                'success': False,
                'error': 'Text cannot be empty'
            }), 400
        
        # Get NLP service
        nlp_service = get_nlp_service()
        
        # Perform compliance check
        compliance_result = _check_document_compliance(text, document_type, user_info, nlp_service)
        
        return jsonify({
            'success': True,
            'compliance_check': compliance_result,
            'document_type': document_type
        })
        
    except Exception as e:
        logger.error(f"Error checking compliance: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error during compliance check'
        }), 500

@nlp_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Health check endpoint for NLP service"""
    try:
        nlp_service = get_nlp_service()
        
        # Test basic functionality
        test_text = "This is a test document."
        analysis = nlp_service.analyze_legal_text(test_text)
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'models_loaded': {
                'standard_model': nlp_service.nlp is not None,
                'blackstone_model': nlp_service.blackstone_nlp is not None
            },
            'test_analysis_successful': analysis is not None
        })
        
    except Exception as e:
        logger.error(f"NLP service health check failed: {e}")
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500

def _generate_improved_text(original_text: str, suggestions: list, document_type: str) -> str:
    """Generate improved version of text based on suggestions"""
    improved_text = original_text
    
    # Apply basic improvements based on suggestions
    replacements = {
        'give': 'give, devise and bequeath',
        'children': 'children and issue',
        'authorize': 'authorize and empower',
        'property': 'real and personal property'
    }
    
    for old, new in replacements.items():
        if old in improved_text.lower() and new not in improved_text.lower():
            # Case-sensitive replacement
            improved_text = improved_text.replace(old, new)
            improved_text = improved_text.replace(old.title(), new.title())
    
    return improved_text

def _check_document_compliance(text: str, document_type: str, user_info: dict, nlp_service) -> dict:
    """Check document compliance with Ontario legal requirements"""
    
    # Get basic analysis
    analysis = nlp_service.analyze_legal_text(text)
    
    issues = []
    warnings = []
    requirements_met = []
    requirements_missing = []
    
    user_age = user_info.get('age', 18)
    
    # Check age requirements
    if document_type == 'will' and user_age < 18:
        issues.append("Testator must be at least 18 years old to create a will in Ontario")
    elif document_type == 'power_of_attorney_property' and user_age < 18:
        issues.append("Grantor must be at least 18 years old for Power of Attorney for Property")
    elif document_type == 'power_of_attorney_care' and user_age < 16:
        issues.append("Grantor must be at least 16 years old for Power of Attorney for Personal Care")
    else:
        requirements_met.append("Age requirement satisfied")
    
    # Check witness requirements
    if 'witness' in text.lower():
        requirements_met.append("Witness requirements mentioned")
    else:
        requirements_missing.append("Witness requirements must be included")
    
    # Check signature requirements
    if 'sign' in text.lower() or 'signature' in text.lower():
        requirements_met.append("Signature requirements mentioned")
    else:
        requirements_missing.append("Signature requirements should be specified")
    
    # Document-specific checks
    if document_type == 'will':
        if 'executor' in text.lower() or 'executrix' in text.lower():
            requirements_met.append("Executor appointment included")
        else:
            requirements_missing.append("Executor should be appointed")
        
        if 'beneficiary' in text.lower():
            requirements_met.append("Beneficiaries mentioned")
        else:
            warnings.append("Consider specifying beneficiaries clearly")
    
    elif 'power_of_attorney' in document_type:
        if 'attorney' in text.lower():
            requirements_met.append("Attorney appointment included")
        else:
            requirements_missing.append("Attorney must be appointed")
        
        if 'incapacity' in text.lower():
            requirements_met.append("Incapacity provisions included")
        else:
            warnings.append("Consider including incapacity provisions")
    
    # Calculate compliance score
    total_checks = len(requirements_met) + len(requirements_missing)
    score = len(requirements_met) / total_checks if total_checks > 0 else 0.0
    
    # Reduce score for issues and warnings
    score -= len(issues) * 0.2
    score -= len(warnings) * 0.1
    score = max(0.0, min(1.0, score))
    
    is_compliant = len(issues) == 0 and len(requirements_missing) == 0
    
    return {
        'is_compliant': is_compliant,
        'issues': issues,
        'warnings': warnings,
        'requirements_met': requirements_met,
        'requirements_missing': requirements_missing,
        'score': round(score, 2)
    }

