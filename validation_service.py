from typing import Dict, List

class ValidationService:
    def __init__(self):
        self.ontario_requirements = {
            'will': {
                'required_fields': [
                    'personal_info.full_name',
                    'personal_info.address',
                    'executor.name',
                    'executor.address',
                    'residuary.beneficiary'
                ],
                'legal_requirements': [
                    'testator_age_18_or_over',
                    'mental_capacity',
                    'written_document',
                    'testator_signature',
                    'two_witnesses'
                ]
            },
            'poa_property': {
                'required_fields': [
                    'grantor_info.full_name',
                    'grantor_info.address',
                    'attorney.name',
                    'attorney.address'
                ],
                'legal_requirements': [
                    'grantor_age_18_or_over',
                    'mental_capacity',
                    'written_document',
                    'grantor_signature',
                    'two_witnesses'
                ]
            },
            'poa_care': {
                'required_fields': [
                    'grantor_info.full_name',
                    'grantor_info.address',
                    'attorney.name',
                    'attorney.address'
                ],
                'legal_requirements': [
                    'grantor_age_16_or_over',
                    'mental_capacity',
                    'written_document',
                    'grantor_signature',
                    'two_witnesses'
                ]
            }
        }
    
    def validate(self, document_type: str, content: Dict) -> Dict:
        """Validate document content against Ontario legal requirements"""
        if document_type not in self.ontario_requirements:
            return {
                'is_valid': False,
                'errors': [f'Unknown document type: {document_type}'],
                'warnings': [],
                'suggestions': []
            }
        
        requirements = self.ontario_requirements[document_type]
        errors = []
        warnings = []
        suggestions = []
        
        # Check required fields
        field_errors = self._validate_required_fields(content, requirements['required_fields'])
        errors.extend(field_errors)
        
        # Check legal requirements
        legal_errors, legal_warnings = self._validate_legal_requirements(
            document_type, content, requirements['legal_requirements']
        )
        errors.extend(legal_errors)
        warnings.extend(legal_warnings)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(document_type, content, errors, warnings)
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'suggestions': suggestions
        }
    
    def _validate_required_fields(self, content: Dict, required_fields: List[str]) -> List[str]:
        """Validate that all required fields are present"""
        errors = []
        
        for field_path in required_fields:
            if not self._get_nested_value(content, field_path):
                field_name = field_path.split('.')[-1].replace('_', ' ').title()
                errors.append(f'Required field missing: {field_name}')
        
        return errors
    
    def _validate_legal_requirements(self, document_type: str, content: Dict, requirements: List[str]) -> tuple:
        """Validate legal requirements"""
        errors = []
        warnings = []
        
        for requirement in requirements:
            if requirement == 'testator_age_18_or_over':
                age = content.get('personal_info', {}).get('age')
                if age and int(age) < 18:
                    errors.append('Testator must be at least 18 years old')
            
            elif requirement == 'grantor_age_18_or_over':
                age = content.get('grantor_info', {}).get('age')
                if age and int(age) < 18:
                    errors.append('Grantor must be at least 18 years old for Power of Attorney for Property')
            
            elif requirement == 'grantor_age_16_or_over':
                age = content.get('grantor_info', {}).get('age')
                if age and int(age) < 16:
                    errors.append('Grantor must be at least 16 years old for Power of Attorney for Personal Care')
            
            elif requirement == 'mental_capacity':
                # This would typically require professional assessment
                warnings.append('Mental capacity must be confirmed at time of signing')
            
            elif requirement == 'written_document':
                # Always satisfied for digital documents
                pass
            
            elif requirement == 'testator_signature':
                warnings.append('Document must be signed by testator in presence of two witnesses')
            
            elif requirement == 'grantor_signature':
                warnings.append('Document must be signed by grantor in presence of two witnesses')
            
            elif requirement == 'two_witnesses':
                warnings.append('Two witnesses must sign the document in presence of testator/grantor')
        
        return errors, warnings
    
    def _generate_suggestions(self, document_type: str, content: Dict, errors: List[str], warnings: List[str]) -> List[str]:
        """Generate suggestions for improvement"""
        suggestions = []
        
        if document_type == 'will':
            # Will-specific suggestions
            if not content.get('bequests'):
                suggestions.append('Consider adding specific bequests for personal items or monetary gifts')
            
            if not content.get('guardian') and self._has_minor_children(content):
                suggestions.append('Consider appointing a guardian for minor children')
            
            if not content.get('alternate_executor'):
                suggestions.append('Consider appointing an alternate executor')
        
        elif document_type in ['poa_property', 'poa_care']:
            # POA-specific suggestions
            if not content.get('alternate_attorney'):
                suggestions.append('Consider appointing an alternate attorney')
            
            if not content.get('conditions'):
                suggestions.append('Consider adding specific conditions or limitations on attorney powers')
        
        # General suggestions
        if errors:
            suggestions.append('Please complete all required fields before finalizing the document')
        
        if warnings:
            suggestions.append('Ensure all legal requirements are met when signing the document')
        
        return suggestions
    
    def _get_nested_value(self, data: Dict, path: str):
        """Get value from nested dictionary using dot notation"""
        keys = path.split('.')
        value = data
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        
        return value if value else None
    
    def _has_minor_children(self, content: Dict) -> bool:
        """Check if the person has minor children"""
        children = content.get('children', [])
        for child in children:
            age = child.get('age')
            if age and int(age) < 18:
                return True
        return False
    
    def get_legal_requirements_info(self, document_type: str) -> Dict:
        """Get information about legal requirements for a document type"""
        if document_type not in self.ontario_requirements:
            return {'error': f'Unknown document type: {document_type}'}
        
        requirements = self.ontario_requirements[document_type]
        
        info = {
            'document_type': document_type,
            'required_fields': requirements['required_fields'],
            'legal_requirements': requirements['legal_requirements'],
            'description': self._get_document_description(document_type),
            'signing_requirements': self._get_signing_requirements(document_type)
        }
        
        return info
    
    def _get_document_description(self, document_type: str) -> str:
        """Get description of document type"""
        descriptions = {
            'will': 'A legal document that specifies how a person\'s assets should be distributed after death.',
            'poa_property': 'A legal document that gives someone authority to make financial and property decisions on your behalf.',
            'poa_care': 'A legal document that gives someone authority to make personal care decisions on your behalf.'
        }
        return descriptions.get(document_type, '')
    
    def _get_signing_requirements(self, document_type: str) -> List[str]:
        """Get signing requirements for document type"""
        if document_type == 'will':
            return [
                'Must be signed by testator in presence of two witnesses',
                'Witnesses must sign in presence of testator and each other',
                'Witnesses cannot be beneficiaries of the will',
                'Testator must be of sound mind at time of signing'
            ]
        elif document_type in ['poa_property', 'poa_care']:
            return [
                'Must be signed by grantor in presence of two witnesses',
                'Witnesses must sign in presence of grantor',
                'Witnesses cannot be the attorney or their spouse',
                'Grantor must be mentally capable at time of signing'
            ]
        return []

