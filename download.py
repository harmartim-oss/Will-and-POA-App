"""
Download API Routes
Provides endpoints for document download, export, and sharing functionality
"""

from flask import Blueprint, request, jsonify, send_file, make_response
from flask_cors import cross_origin
import logging
import os
import tempfile
import zipfile
from typing import Dict, Any
from datetime import datetime
import io
import json

from ..services.enhanced_document_generator import get_enhanced_document_generator
from ..services.poa_generator import get_poa_generator
from ..services.cloud_storage_service import get_cloud_storage_service
from ..services.auth_service import token_required

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
download_bp = Blueprint('download', __name__, url_prefix='/api/download')

@download_bp.route('/document/<document_id>', methods=['GET'])
@cross_origin()
@token_required
def download_document(current_user, document_id: str):
    """
    Download a document in specified format
    
    Query parameters:
    - format: pdf, docx, json (default: pdf)
    - include_metadata: true/false (default: false)
    
    Returns:
    Document file for download
    """
    try:
        format_type = request.args.get('format', 'pdf').lower()
        include_metadata = request.args.get('include_metadata', 'false').lower() == 'true'
        
        if format_type not in ['pdf', 'docx', 'json']:
            return jsonify({
                'success': False,
                'error': 'Invalid format. Supported formats: pdf, docx, json'
            }), 400
        
        # Get document data (in real implementation, fetch from database)
        document_data = _get_mock_document_data(document_id, current_user['id'])
        
        if not document_data:
            return jsonify({
                'success': False,
                'error': 'Document not found'
            }), 404
        
        # Generate document in requested format
        if format_type == 'json':
            return _generate_json_download(document_data, include_metadata)
        else:
            return _generate_document_download(document_data, format_type, include_metadata)
        
    except Exception as e:
        logger.error(f"Error downloading document: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error during download'
        }), 500

@download_bp.route('/bulk', methods=['POST'])
@cross_origin()
@token_required
def bulk_download(current_user):
    """
    Download multiple documents as a ZIP file
    
    Expected JSON payload:
    {
        "document_ids": ["doc1", "doc2", "doc3"],
        "format": "pdf",
        "include_metadata": false,
        "archive_name": "my_documents"
    }
    
    Returns:
    ZIP file containing requested documents
    """
    try:
        data = request.get_json()
        
        if not data or 'document_ids' not in data:
            return jsonify({
                'success': False,
                'error': 'Document IDs are required'
            }), 400
        
        document_ids = data['document_ids']
        format_type = data.get('format', 'pdf').lower()
        include_metadata = data.get('include_metadata', False)
        archive_name = data.get('archive_name', 'documents')
        
        if not document_ids:
            return jsonify({
                'success': False,
                'error': 'At least one document ID is required'
            }), 400
        
        if len(document_ids) > 50:  # Limit bulk downloads
            return jsonify({
                'success': False,
                'error': 'Maximum 50 documents allowed per bulk download'
            }), 400
        
        # Create ZIP file with documents
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for doc_id in document_ids:
                try:
                    # Get document data
                    document_data = _get_mock_document_data(doc_id, current_user['id'])
                    
                    if document_data:
                        # Generate document content
                        if format_type == 'json':
                            content = json.dumps(document_data, indent=2, default=str)
                            filename = f"{document_data['title']}.json"
                        else:
                            # Generate PDF or DOCX
                            temp_file = _generate_document_file(document_data, format_type)
                            with open(temp_file, 'rb') as f:
                                content = f.read()
                            filename = f"{document_data['title']}.{format_type}"
                            os.unlink(temp_file)  # Clean up temp file
                        
                        # Add to ZIP
                        zip_file.writestr(filename, content)
                        
                        # Add metadata if requested
                        if include_metadata:
                            metadata = {
                                'document_id': doc_id,
                                'title': document_data['title'],
                                'type': document_data['type'],
                                'created_date': document_data.get('created_date'),
                                'last_modified': document_data.get('last_modified'),
                                'version': document_data.get('version', 1)
                            }
                            metadata_content = json.dumps(metadata, indent=2, default=str)
                            zip_file.writestr(f"{document_data['title']}_metadata.json", metadata_content)
                
                except Exception as e:
                    logger.warning(f"Failed to include document {doc_id} in bulk download: {e}")
                    # Continue with other documents
        
        zip_buffer.seek(0)
        
        # Create response
        response = make_response(zip_buffer.getvalue())
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = f'attachment; filename="{archive_name}.zip"'
        
        return response
        
    except Exception as e:
        logger.error(f"Error in bulk download: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error during bulk download'
        }), 500

@download_bp.route('/shared/<share_token>', methods=['GET'])
@cross_origin()
def download_shared_document(share_token: str):
    """
    Download a document via share link
    
    Query parameters:
    - password: Password if required
    - format: pdf, docx (default: pdf)
    
    Returns:
    Shared document file
    """
    try:
        password = request.args.get('password')
        format_type = request.args.get('format', 'pdf').lower()
        
        # Get cloud storage service
        storage_service = get_cloud_storage_service()
        
        # Validate share link and get document info
        document_info = storage_service.access_shared_document(share_token, password)
        
        if not document_info or not document_info.get('access_granted'):
            return jsonify({
                'success': False,
                'error': 'Invalid or expired share link'
            }), 403
        
        # Get document data
        document_data = _get_mock_document_data(document_info['document_id'], None)
        
        if not document_data:
            return jsonify({
                'success': False,
                'error': 'Shared document not found'
            }), 404
        
        # Generate and return document
        return _generate_document_download(document_data, format_type, include_metadata=False)
        
    except Exception as e:
        logger.error(f"Error downloading shared document: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error during shared download'
        }), 500

@download_bp.route('/backup/<backup_id>', methods=['GET'])
@cross_origin()
@token_required
def download_backup(current_user, backup_id: str):
    """
    Download a backup archive
    
    Returns:
    ZIP file containing backup
    """
    try:
        # Get cloud storage service
        storage_service = get_cloud_storage_service()
        
        # Create temporary directory for restoration
        with tempfile.TemporaryDirectory() as temp_dir:
            # Restore backup to temp directory
            success = storage_service.restore_from_backup(backup_id, current_user['id'], temp_dir)
            
            if not success:
                return jsonify({
                    'success': False,
                    'error': 'Backup not found or restoration failed'
                }), 404
            
            # Create ZIP file from restored files
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, temp_dir)
                        zip_file.write(file_path, arc_name)
            
            zip_buffer.seek(0)
            
            # Create response
            response = make_response(zip_buffer.getvalue())
            response.headers['Content-Type'] = 'application/zip'
            response.headers['Content-Disposition'] = f'attachment; filename="backup_{backup_id}.zip"'
            
            return response
        
    except Exception as e:
        logger.error(f"Error downloading backup: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error during backup download'
        }), 500

@download_bp.route('/template/<template_type>', methods=['GET'])
@cross_origin()
def download_template(template_type: str):
    """
    Download a document template
    
    Query parameters:
    - format: pdf, docx (default: pdf)
    
    Returns:
    Template document file
    """
    try:
        format_type = request.args.get('format', 'pdf').lower()
        
        if template_type not in ['will', 'power_of_attorney_property', 'power_of_attorney_care']:
            return jsonify({
                'success': False,
                'error': 'Invalid template type'
            }), 400
        
        # Generate template with placeholder data
        template_data = _get_template_data(template_type)
        
        # Generate document
        return _generate_document_download(template_data, format_type, include_metadata=False)
        
    except Exception as e:
        logger.error(f"Error downloading template: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error during template download'
        }), 500

@download_bp.route('/export-data', methods=['GET'])
@cross_origin()
@token_required
def export_user_data(current_user):
    """
    Export all user data (GDPR compliance)
    
    Returns:
    ZIP file containing all user documents and data
    """
    try:
        # Get all user documents (in real implementation, query database)
        user_documents = _get_user_documents(current_user['id'])
        
        # Create comprehensive export
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add user profile data
            profile_data = {
                'user_id': current_user['id'],
                'email': current_user.get('email'),
                'created_date': current_user.get('created_date'),
                'export_date': datetime.now().isoformat(),
                'export_type': 'complete_user_data'
            }
            zip_file.writestr('user_profile.json', json.dumps(profile_data, indent=2, default=str))
            
            # Add documents
            for doc_data in user_documents:
                try:
                    # Add PDF version
                    pdf_file = _generate_document_file(doc_data, 'pdf')
                    with open(pdf_file, 'rb') as f:
                        zip_file.writestr(f"documents/{doc_data['title']}.pdf", f.read())
                    os.unlink(pdf_file)
                    
                    # Add JSON data
                    zip_file.writestr(f"documents/{doc_data['title']}_data.json", 
                                    json.dumps(doc_data, indent=2, default=str))
                
                except Exception as e:
                    logger.warning(f"Failed to export document {doc_data.get('id')}: {e}")
            
            # Add export summary
            summary = {
                'export_date': datetime.now().isoformat(),
                'total_documents': len(user_documents),
                'document_types': list(set(doc.get('type') for doc in user_documents)),
                'export_format': 'complete_archive'
            }
            zip_file.writestr('export_summary.json', json.dumps(summary, indent=2, default=str))
        
        zip_buffer.seek(0)
        
        # Create response
        response = make_response(zip_buffer.getvalue())
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = f'attachment; filename="user_data_export_{current_user["id"]}.zip"'
        
        return response
        
    except Exception as e:
        logger.error(f"Error exporting user data: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error during data export'
        }), 500

def _get_mock_document_data(document_id: str, user_id: str) -> Dict[str, Any]:
    """Get mock document data (replace with database query in real implementation)"""
    return {
        'id': document_id,
        'title': 'Sample Last Will and Testament',
        'type': 'will',
        'user_id': user_id,
        'created_date': datetime.now().isoformat(),
        'last_modified': datetime.now().isoformat(),
        'version': 1,
        'data': {
            'testator': {
                'name': 'John Smith',
                'address': '123 Main St, Toronto, ON M1A 1A1',
                'date_of_birth': '1980-01-01'
            },
            'executors': [
                {
                    'name': 'Jane Smith',
                    'relationship': 'Spouse',
                    'address': '123 Main St, Toronto, ON M1A 1A1'
                }
            ],
            'beneficiaries': [
                {
                    'name': 'Jane Smith',
                    'relationship': 'Spouse',
                    'inheritance': 'Entire estate'
                }
            ]
        }
    }

def _get_template_data(template_type: str) -> Dict[str, Any]:
    """Get template data with placeholders"""
    base_data = {
        'id': 'template',
        'title': f'Template - {template_type.replace("_", " ").title()}',
        'type': template_type,
        'created_date': datetime.now().isoformat(),
        'version': 1
    }
    
    if template_type == 'will':
        base_data['data'] = {
            'testator': {
                'name': '[YOUR FULL NAME]',
                'address': '[YOUR ADDRESS]',
                'date_of_birth': '[YYYY-MM-DD]'
            },
            'executors': [
                {
                    'name': '[EXECUTOR NAME]',
                    'relationship': '[RELATIONSHIP]',
                    'address': '[EXECUTOR ADDRESS]'
                }
            ],
            'beneficiaries': [
                {
                    'name': '[BENEFICIARY NAME]',
                    'relationship': '[RELATIONSHIP]',
                    'inheritance': '[INHERITANCE DETAILS]'
                }
            ]
        }
    
    return base_data

def _get_user_documents(user_id: str) -> list:
    """Get all documents for a user (mock implementation)"""
    return [
        _get_mock_document_data('doc1', user_id),
        _get_mock_document_data('doc2', user_id)
    ]

def _generate_json_download(document_data: Dict[str, Any], include_metadata: bool):
    """Generate JSON download response"""
    if include_metadata:
        export_data = document_data
    else:
        export_data = document_data.get('data', document_data)
    
    json_content = json.dumps(export_data, indent=2, default=str)
    
    response = make_response(json_content)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Content-Disposition'] = f'attachment; filename="{document_data["title"]}.json"'
    
    return response

def _generate_document_download(document_data: Dict[str, Any], format_type: str, include_metadata: bool):
    """Generate document download in PDF or DOCX format"""
    try:
        # Generate document file
        temp_file = _generate_document_file(document_data, format_type)
        
        # Determine MIME type
        mime_type = 'application/pdf' if format_type == 'pdf' else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        
        # Create response
        response = send_file(
            temp_file,
            as_attachment=True,
            download_name=f"{document_data['title']}.{format_type}",
            mimetype=mime_type
        )
        
        # Clean up temp file after response
        @response.call_on_close
        def cleanup():
            try:
                os.unlink(temp_file)
            except:
                pass
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating document download: {e}")
        raise

def _generate_document_file(document_data: Dict[str, Any], format_type: str) -> str:
    """Generate document file and return temporary file path"""
    try:
        # Create temporary file
        temp_fd, temp_path = tempfile.mkstemp(suffix=f'.{format_type}')
        os.close(temp_fd)
        
        # Generate document based on type
        doc_type = document_data.get('type', 'will')
        
        if doc_type == 'will':
            generator = get_enhanced_document_generator()
            if format_type == 'pdf':
                generator.generate_pdf(document_data, temp_path)
            else:
                generator.generate_word_document(document_data, temp_path)
        
        elif 'power_of_attorney' in doc_type:
            poa_generator = get_poa_generator()
            # Convert document data to POA format
            poa_document = poa_generator.generate_poa_document(document_data.get('data', {}))
            
            if format_type == 'pdf':
                poa_generator.generate_pdf(poa_document, temp_path)
            else:
                poa_generator.generate_word_document(poa_document, temp_path)
        
        return temp_path
        
    except Exception as e:
        logger.error(f"Error generating document file: {e}")
        # Clean up temp file if it was created
        try:
            os.unlink(temp_path)
        except:
            pass
        raise

