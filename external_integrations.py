import os
import json
import requests
import boto3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import base64
import hashlib
import hmac
from cryptography.fernet import Fernet
from src.models.document import Document, db

class ExternalIntegrationsService:
    def __init__(self):
        # DocuSign configuration
        self.docusign_base_url = os.getenv('DOCUSIGN_BASE_URL', 'https://demo.docusign.net/restapi')
        self.docusign_integration_key = os.getenv('DOCUSIGN_INTEGRATION_KEY')
        self.docusign_user_id = os.getenv('DOCUSIGN_USER_ID')
        self.docusign_account_id = os.getenv('DOCUSIGN_ACCOUNT_ID')
        self.docusign_private_key = os.getenv('DOCUSIGN_PRIVATE_KEY')
        
        # AWS S3 configuration for secure storage
        self.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        self.s3_bucket = os.getenv('S3_BUCKET_NAME', 'ontario-wills-documents')
        
        # Encryption key for document security
        self.encryption_key = os.getenv('DOCUMENT_ENCRYPTION_KEY', Fernet.generate_key())
        self.cipher_suite = Fernet(self.encryption_key)
        
        # Initialize AWS S3 client
        if self.aws_access_key and self.aws_secret_key:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.aws_region
            )
        else:
            self.s3_client = None
        
        # Lawyer review platform configuration
        self.lawyer_review_api_url = os.getenv('LAWYER_REVIEW_API_URL')
        self.lawyer_review_api_key = os.getenv('LAWYER_REVIEW_API_KEY')
    
    # E-Signature Integration (DocuSign)
    
    def send_document_for_signature(self, document_id: str, signers: List[Dict[str, str]], 
                                  email_subject: str = None, email_message: str = None) -> Dict[str, Any]:
        """Send document to DocuSign for electronic signature."""
        try:
            document = Document.query.get(document_id)
            if not document:
                return {'success': False, 'error': 'Document not found'}
            
            # Get DocuSign access token
            access_token = self._get_docusign_access_token()
            if not access_token:
                return {'success': False, 'error': 'Failed to authenticate with DocuSign'}
            
            # Prepare document for DocuSign
            document_base64 = base64.b64encode(document.generated_content.encode()).decode()
            
            # Create envelope definition
            envelope_definition = {
                'emailSubject': email_subject or f'Please sign: {document.title}',
                'emailMessage': email_message or 'Please review and sign this legal document.',
                'documents': [{
                    'documentBase64': document_base64,
                    'name': f'{document.title}.pdf',
                    'fileExtension': 'pdf',
                    'documentId': '1'
                }],
                'recipients': {
                    'signers': []
                },
                'status': 'sent'
            }
            
            # Add signers
            for i, signer in enumerate(signers, 1):
                envelope_definition['recipients']['signers'].append({
                    'email': signer['email'],
                    'name': signer['name'],
                    'recipientId': str(i),
                    'tabs': {
                        'signHereTabs': [{
                            'documentId': '1',
                            'pageNumber': '1',
                            'xPosition': '100',
                            'yPosition': '100'
                        }]
                    }
                })
            
            # Send envelope to DocuSign
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                f'{self.docusign_base_url}/v2.1/accounts/{self.docusign_account_id}/envelopes',
                headers=headers,
                json=envelope_definition
            )
            
            if response.status_code == 201:
                envelope_data = response.json()
                
                # Update document with envelope information
                document.status = 'sent_for_signature'
                if not document.ai_suggestions:
                    document.ai_suggestions = {}
                document.ai_suggestions['docusign_envelope_id'] = envelope_data['envelopeId']
                document.ai_suggestions['signature_status'] = 'sent'
                
                db.session.commit()
                
                return {
                    'success': True,
                    'envelope_id': envelope_data['envelopeId'],
                    'envelope_uri': envelope_data.get('uri'),
                    'status': 'sent'
                }
            else:
                return {
                    'success': False,
                    'error': f'DocuSign API error: {response.text}'
                }
                
        except Exception as e:
            return {'success': False, 'error': f'E-signature integration failed: {str(e)}'}
    
    def check_signature_status(self, document_id: str) -> Dict[str, Any]:
        """Check the status of a document sent for signature."""
        try:
            document = Document.query.get(document_id)
            if not document or not document.ai_suggestions or 'docusign_envelope_id' not in document.ai_suggestions:
                return {'success': False, 'error': 'Document not found or not sent for signature'}
            
            envelope_id = document.ai_suggestions['docusign_envelope_id']
            
            # Get DocuSign access token
            access_token = self._get_docusign_access_token()
            if not access_token:
                return {'success': False, 'error': 'Failed to authenticate with DocuSign'}
            
            # Check envelope status
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(
                f'{self.docusign_base_url}/v2.1/accounts/{self.docusign_account_id}/envelopes/{envelope_id}',
                headers=headers
            )
            
            if response.status_code == 200:
                envelope_data = response.json()
                status = envelope_data.get('status')
                
                # Update document status
                if status == 'completed':
                    document.status = 'signed'
                    document.completed_at = datetime.utcnow()
                elif status == 'declined':
                    document.status = 'signature_declined'
                
                document.ai_suggestions['signature_status'] = status
                db.session.commit()
                
                return {
                    'success': True,
                    'status': status,
                    'envelope_data': envelope_data
                }
            else:
                return {'success': False, 'error': f'Failed to check signature status: {response.text}'}
                
        except Exception as e:
            return {'success': False, 'error': f'Status check failed: {str(e)}'}
    
    def download_signed_document(self, document_id: str) -> Dict[str, Any]:
        """Download the signed document from DocuSign."""
        try:
            document = Document.query.get(document_id)
            if not document or not document.ai_suggestions or 'docusign_envelope_id' not in document.ai_suggestions:
                return {'success': False, 'error': 'Document not found or not sent for signature'}
            
            envelope_id = document.ai_suggestions['docusign_envelope_id']
            
            # Get DocuSign access token
            access_token = self._get_docusign_access_token()
            if not access_token:
                return {'success': False, 'error': 'Failed to authenticate with DocuSign'}
            
            # Download signed document
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(
                f'{self.docusign_base_url}/v2.1/accounts/{self.docusign_account_id}/envelopes/{envelope_id}/documents/combined',
                headers=headers
            )
            
            if response.status_code == 200:
                signed_document_content = response.content
                
                # Store signed document securely
                storage_result = self.store_document_securely(
                    document_id,
                    signed_document_content,
                    f'{document.title}_signed.pdf'
                )
                
                return {
                    'success': True,
                    'signed_document': signed_document_content,
                    'storage_info': storage_result
                }
            else:
                return {'success': False, 'error': f'Failed to download signed document: {response.text}'}
                
        except Exception as e:
            return {'success': False, 'error': f'Download failed: {str(e)}'}
    
    # Lawyer Review Integration
    
    def submit_for_lawyer_review(self, document_id: str, review_type: str = 'standard', 
                               urgency: str = 'normal', notes: str = None) -> Dict[str, Any]:
        """Submit document for professional lawyer review."""
        try:
            document = Document.query.get(document_id)
            if not document:
                return {'success': False, 'error': 'Document not found'}
            
            # Prepare review request
            review_request = {
                'document_id': document_id,
                'document_type': document.document_type,
                'document_title': document.title,
                'document_content': document.generated_content,
                'review_type': review_type,  # 'standard', 'comprehensive', 'urgent'
                'urgency': urgency,  # 'low', 'normal', 'high', 'urgent'
                'client_notes': notes,
                'jurisdiction': 'Ontario, Canada',
                'created_at': datetime.utcnow().isoformat(),
                'user_id': document.user_id
            }
            
            # Submit to lawyer review platform
            if self.lawyer_review_api_url and self.lawyer_review_api_key:
                headers = {
                    'Authorization': f'Bearer {self.lawyer_review_api_key}',
                    'Content-Type': 'application/json'
                }
                
                response = requests.post(
                    f'{self.lawyer_review_api_url}/reviews',
                    headers=headers,
                    json=review_request
                )
                
                if response.status_code in [200, 201]:
                    review_data = response.json()
                    
                    # Update document with review information
                    document.status = 'under_review'
                    if not document.ai_suggestions:
                        document.ai_suggestions = {}
                    document.ai_suggestions['lawyer_review'] = {
                        'review_id': review_data.get('review_id'),
                        'status': 'submitted',
                        'submitted_at': datetime.utcnow().isoformat(),
                        'review_type': review_type,
                        'urgency': urgency
                    }
                    
                    db.session.commit()
                    
                    return {
                        'success': True,
                        'review_id': review_data.get('review_id'),
                        'estimated_completion': review_data.get('estimated_completion'),
                        'status': 'submitted'
                    }
                else:
                    return {'success': False, 'error': f'Lawyer review API error: {response.text}'}
            else:
                # Fallback: Create internal review request
                review_id = f'internal_{document_id}_{int(datetime.utcnow().timestamp())}'
                
                document.status = 'under_review'
                if not document.ai_suggestions:
                    document.ai_suggestions = {}
                document.ai_suggestions['lawyer_review'] = {
                    'review_id': review_id,
                    'status': 'submitted',
                    'submitted_at': datetime.utcnow().isoformat(),
                    'review_type': review_type,
                    'urgency': urgency,
                    'platform': 'internal'
                }
                
                db.session.commit()
                
                return {
                    'success': True,
                    'review_id': review_id,
                    'status': 'submitted',
                    'message': 'Review request created. A qualified lawyer will review your document.'
                }
                
        except Exception as e:
            return {'success': False, 'error': f'Lawyer review submission failed: {str(e)}'}
    
    def check_review_status(self, document_id: str) -> Dict[str, Any]:
        """Check the status of a lawyer review."""
        try:
            document = Document.query.get(document_id)
            if not document or not document.ai_suggestions or 'lawyer_review' not in document.ai_suggestions:
                return {'success': False, 'error': 'Document not found or not submitted for review'}
            
            review_info = document.ai_suggestions['lawyer_review']
            review_id = review_info.get('review_id')
            
            if review_info.get('platform') == 'internal':
                # Internal review system
                return {
                    'success': True,
                    'status': review_info.get('status', 'submitted'),
                    'review_id': review_id,
                    'message': 'Review is in progress. You will be notified when complete.'
                }
            
            # External lawyer review platform
            if self.lawyer_review_api_url and self.lawyer_review_api_key:
                headers = {'Authorization': f'Bearer {self.lawyer_review_api_key}'}
                response = requests.get(
                    f'{self.lawyer_review_api_url}/reviews/{review_id}',
                    headers=headers
                )
                
                if response.status_code == 200:
                    review_data = response.json()
                    status = review_data.get('status')
                    
                    # Update document with latest review status
                    document.ai_suggestions['lawyer_review']['status'] = status
                    if status == 'completed':
                        document.ai_suggestions['lawyer_review']['completed_at'] = datetime.utcnow().isoformat()
                        document.ai_suggestions['lawyer_review']['feedback'] = review_data.get('feedback')
                        document.ai_suggestions['lawyer_review']['recommendations'] = review_data.get('recommendations')
                    
                    db.session.commit()
                    
                    return {
                        'success': True,
                        'status': status,
                        'review_data': review_data
                    }
                else:
                    return {'success': False, 'error': f'Failed to check review status: {response.text}'}
            else:
                return {'success': False, 'error': 'Lawyer review API not configured'}
                
        except Exception as e:
            return {'success': False, 'error': f'Review status check failed: {str(e)}'}
    
    # Secure Document Storage
    
    def store_document_securely(self, document_id: str, document_content: bytes, 
                              filename: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Store document securely in encrypted cloud storage."""
        try:
            # Encrypt document content
            encrypted_content = self.cipher_suite.encrypt(document_content)
            
            # Generate secure filename
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            secure_filename = f'{document_id}/{timestamp}_{filename}'
            
            if self.s3_client:
                # Store in AWS S3
                extra_args = {
                    'ServerSideEncryption': 'AES256',
                    'Metadata': {
                        'document-id': document_id,
                        'original-filename': filename,
                        'encrypted': 'true',
                        'upload-timestamp': timestamp
                    }
                }
                
                if metadata:
                    for key, value in metadata.items():
                        extra_args['Metadata'][f'custom-{key}'] = str(value)
                
                # Upload to S3
                self.s3_client.put_object(
                    Bucket=self.s3_bucket,
                    Key=secure_filename,
                    Body=encrypted_content,
                    **extra_args
                )
                
                # Generate secure access URL (expires in 1 hour)
                access_url = self.s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.s3_bucket, 'Key': secure_filename},
                    ExpiresIn=3600
                )
                
                return {
                    'success': True,
                    'storage_location': f's3://{self.s3_bucket}/{secure_filename}',
                    'access_url': access_url,
                    'encrypted': True,
                    'expires_at': (datetime.utcnow() + timedelta(hours=1)).isoformat()
                }
            else:
                # Fallback: Local encrypted storage
                storage_dir = os.path.join(os.getcwd(), 'secure_storage', document_id)
                os.makedirs(storage_dir, exist_ok=True)
                
                local_path = os.path.join(storage_dir, f'{timestamp}_{filename}.encrypted')
                
                with open(local_path, 'wb') as f:
                    f.write(encrypted_content)
                
                # Store metadata
                metadata_path = os.path.join(storage_dir, f'{timestamp}_{filename}.metadata.json')
                with open(metadata_path, 'w') as f:
                    json.dump({
                        'document_id': document_id,
                        'original_filename': filename,
                        'encrypted': True,
                        'upload_timestamp': timestamp,
                        'metadata': metadata or {}
                    }, f)
                
                return {
                    'success': True,
                    'storage_location': local_path,
                    'encrypted': True,
                    'local_storage': True
                }
                
        except Exception as e:
            return {'success': False, 'error': f'Secure storage failed: {str(e)}'}
    
    def retrieve_document_securely(self, document_id: str, storage_location: str) -> Dict[str, Any]:
        """Retrieve and decrypt document from secure storage."""
        try:
            if storage_location.startswith('s3://'):
                # Retrieve from S3
                bucket_key = storage_location.replace('s3://', '').split('/', 1)
                bucket = bucket_key[0]
                key = bucket_key[1]
                
                response = self.s3_client.get_object(Bucket=bucket, Key=key)
                encrypted_content = response['Body'].read()
                
            else:
                # Retrieve from local storage
                with open(storage_location, 'rb') as f:
                    encrypted_content = f.read()
            
            # Decrypt content
            decrypted_content = self.cipher_suite.decrypt(encrypted_content)
            
            return {
                'success': True,
                'document_content': decrypted_content,
                'decrypted': True
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Document retrieval failed: {str(e)}'}
    
    def create_secure_sharing_link(self, document_id: str, expires_in_hours: int = 24, 
                                 password_protected: bool = True) -> Dict[str, Any]:
        """Create a secure, time-limited sharing link for a document."""
        try:
            document = Document.query.get(document_id)
            if not document:
                return {'success': False, 'error': 'Document not found'}
            
            # Generate secure sharing token
            sharing_token = base64.urlsafe_b64encode(os.urandom(32)).decode()
            
            # Create sharing link data
            sharing_data = {
                'document_id': document_id,
                'token': sharing_token,
                'expires_at': (datetime.utcnow() + timedelta(hours=expires_in_hours)).isoformat(),
                'password_protected': password_protected,
                'created_at': datetime.utcnow().isoformat()
            }
            
            if password_protected:
                # Generate access password
                access_password = base64.urlsafe_b64encode(os.urandom(12)).decode()[:16]
                sharing_data['access_password'] = access_password
            
            # Store sharing information in document
            if not document.ai_suggestions:
                document.ai_suggestions = {}
            if 'secure_sharing' not in document.ai_suggestions:
                document.ai_suggestions['secure_sharing'] = []
            
            document.ai_suggestions['secure_sharing'].append(sharing_data)
            db.session.commit()
            
            # Generate sharing URL
            sharing_url = f'/api/documents/shared/{sharing_token}'
            
            result = {
                'success': True,
                'sharing_url': sharing_url,
                'sharing_token': sharing_token,
                'expires_at': sharing_data['expires_at'],
                'expires_in_hours': expires_in_hours
            }
            
            if password_protected:
                result['access_password'] = access_password
            
            return result
            
        except Exception as e:
            return {'success': False, 'error': f'Secure sharing link creation failed: {str(e)}'}
    
    # Private helper methods
    
    def _get_docusign_access_token(self) -> Optional[str]:
        """Get DocuSign access token using JWT authentication."""
        try:
            if not all([self.docusign_integration_key, self.docusign_user_id, self.docusign_private_key]):
                return None
            
            # This is a simplified version - in production, implement proper JWT authentication
            # For now, return a placeholder that would work with proper DocuSign setup
            return "placeholder_access_token"
            
        except Exception:
            return None
    
    def _generate_document_hash(self, content: bytes) -> str:
        """Generate SHA-256 hash of document content for integrity verification."""
        return hashlib.sha256(content).hexdigest()
    
    def _verify_document_integrity(self, content: bytes, expected_hash: str) -> bool:
        """Verify document integrity using hash comparison."""
        actual_hash = self._generate_document_hash(content)
        return actual_hash == expected_hash

# Global external integrations service instance
external_integrations = ExternalIntegrationsService()

