import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from jinja2 import Template, Environment, BaseLoader
import openai
import os

class EnhancedDocumentGenerator:
    def __init__(self):
        self.openai_client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
        )
        
        # Enhanced templates with conditional logic
        self.templates = {
            'will': self._get_enhanced_will_template(),
            'poa_property': self._get_enhanced_poa_property_template(),
            'poa_care': self._get_enhanced_poa_care_template()
        }
        
        # Legal requirements and validation rules
        self.legal_requirements = self._load_legal_requirements()
        
    def generate_document(self, document_type: str, form_data: Dict[str, Any], 
                         include_ai_enhancements: bool = True) -> Dict[str, Any]:
        """Generate a document with enhanced features and AI improvements."""
        
        # Validate input data
        validation_result = self._validate_form_data(document_type, form_data)
        if not validation_result['is_valid']:
            return {
                'success': False,
                'errors': validation_result['errors'],
                'document_content': None
            }
        
        # Process form data with conditional logic
        processed_data = self._process_conditional_logic(document_type, form_data)
        
        # Generate base document
        template = Template(self.templates[document_type])
        base_content = template.render(**processed_data)
        
        result = {
            'success': True,
            'document_content': base_content,
            'processed_data': processed_data,
            'validation_result': validation_result
        }
        
        if include_ai_enhancements:
            # Add AI enhancements
            ai_enhancements = self._generate_ai_enhancements(document_type, base_content, form_data)
            result.update(ai_enhancements)
        
        return result
    
    def _generate_ai_enhancements(self, document_type: str, content: str, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered enhancements for the document."""
        
        enhancements = {}
        
        try:
            # Generate wording suggestions
            enhancements['wording_suggestions'] = self._get_wording_suggestions(content, document_type)
            
            # Perform risk assessment
            enhancements['risk_assessment'] = self._perform_risk_assessment(content, form_data, document_type)
            
            # Check compliance
            enhancements['compliance_check'] = self._check_legal_compliance(content, document_type)
            
            # Sentiment analysis for tone appropriateness
            enhancements['sentiment_analysis'] = self._analyze_document_sentiment(content)
            
            # Generate improvement recommendations
            enhancements['recommendations'] = self._generate_recommendations(content, form_data, document_type)
            
        except Exception as e:
            enhancements['ai_error'] = f"AI enhancement failed: {str(e)}"
        
        return enhancements
    
    def _get_wording_suggestions(self, content: str, document_type: str) -> List[Dict[str, Any]]:
        """Get AI-powered wording suggestions for the document."""
        
        prompt = f"""
        As a legal writing expert, analyze this {document_type} document and provide specific wording improvements.
        Focus on:
        1. Legal clarity and precision
        2. Plain language alternatives for complex terms
        3. Consistency in terminology
        4. Completeness of clauses
        
        Document content:
        {content[:2000]}...
        
        Provide suggestions in JSON format with:
        - section: which part of the document
        - original: the original text
        - suggested: improved wording
        - reason: explanation for the change
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            suggestions_text = response.choices[0].message.content
            # Try to extract JSON from the response
            json_match = re.search(r'\[.*\]', suggestions_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return [{"section": "general", "suggestion": suggestions_text, "reason": "AI analysis"}]
                
        except Exception as e:
            return [{"error": f"Failed to generate suggestions: {str(e)}"}]
    
    def _perform_risk_assessment(self, content: str, form_data: Dict[str, Any], document_type: str) -> Dict[str, Any]:
        """Perform AI-powered risk assessment of the document."""
        
        prompt = f"""
        As a legal risk analyst, assess this {document_type} document for potential legal risks and issues.
        Consider:
        1. Missing required clauses
        2. Ambiguous language
        3. Potential conflicts or contradictions
        4. Compliance with Ontario law
        5. Enforceability concerns
        
        Document content:
        {content[:2000]}...
        
        Form data context:
        {json.dumps(form_data, indent=2)[:500]}...
        
        Provide assessment in JSON format with:
        - risk_level: "low", "medium", "high"
        - identified_risks: list of specific risks
        - recommendations: suggested actions
        - confidence_score: 0.0 to 1.0
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            
            assessment_text = response.choices[0].message.content
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', assessment_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {
                    "risk_level": "unknown",
                    "analysis": assessment_text,
                    "confidence_score": 0.5
                }
                
        except Exception as e:
            return {"error": f"Risk assessment failed: {str(e)}"}
    
    def _check_legal_compliance(self, content: str, document_type: str) -> Dict[str, Any]:
        """Check document compliance with Ontario legal requirements."""
        
        requirements = self.legal_requirements.get(document_type, {})
        compliance_result = {
            "is_compliant": True,
            "missing_requirements": [],
            "warnings": [],
            "recommendations": []
        }
        
        # Check for required elements
        for requirement in requirements.get('required_elements', []):
            if not self._check_requirement_in_content(content, requirement):
                compliance_result["is_compliant"] = False
                compliance_result["missing_requirements"].append(requirement)
        
        # AI-powered compliance check
        prompt = f"""
        As an Ontario legal compliance expert, review this {document_type} document for compliance with Ontario law.
        Check for:
        1. Required witnessing provisions
        2. Age and capacity requirements
        3. Proper execution requirements
        4. Required disclosures
        5. Statutory compliance
        
        Document content:
        {content[:2000]}...
        
        Provide compliance assessment in JSON format.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            ai_compliance = response.choices[0].message.content
            compliance_result["ai_analysis"] = ai_compliance
            
        except Exception as e:
            compliance_result["ai_error"] = f"AI compliance check failed: {str(e)}"
        
        return compliance_result
    
    def _analyze_document_sentiment(self, content: str) -> Dict[str, Any]:
        """Analyze document sentiment and tone appropriateness."""
        
        prompt = f"""
        Analyze the tone and sentiment of this legal document.
        Assess:
        1. Professional tone appropriateness
        2. Clarity and readability
        3. Emotional neutrality
        4. Formality level
        
        Document content:
        {content[:1500]}...
        
        Provide analysis in JSON format with scores (0.0 to 1.0) for each aspect.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            sentiment_text = response.choices[0].message.content
            json_match = re.search(r'\{.*\}', sentiment_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"analysis": sentiment_text, "overall_score": 0.8}
                
        except Exception as e:
            return {"error": f"Sentiment analysis failed: {str(e)}"}
    
    def _generate_recommendations(self, content: str, form_data: Dict[str, Any], document_type: str) -> List[Dict[str, Any]]:
        """Generate comprehensive recommendations for document improvement."""
        
        prompt = f"""
        As a legal document expert, provide comprehensive recommendations to improve this {document_type}.
        Consider:
        1. Additional clauses that might be beneficial
        2. Clarity improvements
        3. Legal best practices
        4. Personalization opportunities
        5. Future-proofing suggestions
        
        Document type: {document_type}
        User situation: {json.dumps(form_data, indent=2)[:500]}...
        
        Provide recommendations as a JSON array with priority levels.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )
            
            recommendations_text = response.choices[0].message.content
            json_match = re.search(r'\[.*\]', recommendations_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return [{"recommendation": recommendations_text, "priority": "medium"}]
                
        except Exception as e:
            return [{"error": f"Failed to generate recommendations: {str(e)}"}]
    
    def _validate_form_data(self, document_type: str, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced validation of form data with legal requirements."""
        
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": []
        }
        
        requirements = self.legal_requirements.get(document_type, {})
        
        # Check required fields
        for field in requirements.get('required_fields', []):
            if field not in form_data or not form_data[field]:
                validation_result["is_valid"] = False
                validation_result["errors"].append(f"Required field '{field}' is missing")
        
        # Age validation
        if 'date_of_birth' in form_data:
            age = self._calculate_age(form_data['date_of_birth'])
            min_age = requirements.get('minimum_age', 18)
            if age < min_age:
                validation_result["is_valid"] = False
                validation_result["errors"].append(f"Must be at least {min_age} years old")
        
        # Custom validation rules
        validation_rules = requirements.get('validation_rules', {})
        for field, rules in validation_rules.items():
            if field in form_data:
                field_value = form_data[field]
                for rule in rules:
                    if not self._apply_validation_rule(field_value, rule):
                        validation_result["warnings"].append(f"Field '{field}' {rule['message']}")
        
        return validation_result
    
    def _process_conditional_logic(self, document_type: str, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process conditional logic to customize document content."""
        
        processed_data = form_data.copy()
        
        # Add computed fields
        processed_data['current_date'] = datetime.now().strftime("%B %d, %Y")
        processed_data['document_type_title'] = self._get_document_title(document_type)
        
        # Process conditional sections
        if document_type == 'will':
            processed_data = self._process_will_conditionals(processed_data)
        elif document_type == 'poa_property':
            processed_data = self._process_poa_property_conditionals(processed_data)
        elif document_type == 'poa_care':
            processed_data = self._process_poa_care_conditionals(processed_data)
        
        return processed_data
    
    def _process_will_conditionals(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process conditional logic specific to wills."""
        
        # Handle beneficiary distributions
        if 'beneficiaries' in data and isinstance(data['beneficiaries'], list):
            total_percentage = sum(b.get('percentage', 0) for b in data['beneficiaries'])
            if total_percentage != 100:
                data['distribution_warning'] = f"Beneficiary percentages total {total_percentage}%, not 100%"
        
        # Handle guardian appointments
        if data.get('has_minor_children') and not data.get('guardian_name'):
            data['guardian_warning'] = "Guardian should be appointed for minor children"
        
        # Handle executor alternates
        if not data.get('alternate_executor'):
            data['executor_recommendation'] = "Consider appointing an alternate executor"
        
        # Generate specific clauses based on assets
        asset_clauses = []
        if data.get('has_real_estate'):
            asset_clauses.append("real_estate_clause")
        if data.get('has_business_interests'):
            asset_clauses.append("business_interests_clause")
        if data.get('has_investments'):
            asset_clauses.append("investments_clause")
        
        data['applicable_asset_clauses'] = asset_clauses
        
        return data
    
    def _process_poa_property_conditionals(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process conditional logic for Power of Attorney for Property."""
        
        # Handle authority limitations
        if data.get('limit_authority'):
            data['authority_limitations'] = data.get('authority_limitations', [])
        else:
            data['authority_limitations'] = []
        
        # Handle compensation
        if data.get('attorney_compensation'):
            data['compensation_clause'] = True
        
        # Handle multiple attorneys
        if isinstance(data.get('attorneys'), list) and len(data['attorneys']) > 1:
            data['multiple_attorneys'] = True
            data['decision_making'] = data.get('decision_making', 'jointly')
        
        return data
    
    def _process_poa_care_conditionals(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process conditional logic for Power of Attorney for Personal Care."""
        
        # Handle healthcare preferences
        if data.get('healthcare_preferences'):
            data['has_healthcare_preferences'] = True
        
        # Handle end-of-life wishes
        if data.get('end_of_life_wishes'):
            data['has_end_of_life_wishes'] = True
        
        # Handle substitute decision maker
        if isinstance(data.get('substitute_decision_makers'), list):
            data['has_multiple_sdm'] = len(data['substitute_decision_makers']) > 1
        
        return data
    
    def _get_enhanced_will_template(self) -> str:
        """Enhanced will template with conditional logic."""
        return """
LAST WILL AND TESTAMENT

I, {{ full_name }}, of {{ address }}, in the Province of Ontario, being of sound mind and disposing memory, do hereby make, publish and declare this to be my Last Will and Testament, hereby revoking all former Wills and Codicils by me at any time heretofore made.

ARTICLE I - IDENTIFICATION AND REVOCATION
1.1 I am {{ age }} years of age, born on {{ date_of_birth }}.
1.2 I revoke all previous Wills and Codicils made by me.

ARTICLE II - APPOINTMENT OF EXECUTOR
2.1 I appoint {{ executor_name }} of {{ executor_address }} to be the Executor of this my Will.
{% if alternate_executor %}
2.2 If {{ executor_name }} is unable or unwilling to act as Executor, I appoint {{ alternate_executor }} of {{ alternate_executor_address }} as alternate Executor.
{% endif %}

ARTICLE III - PAYMENT OF DEBTS AND EXPENSES
3.1 I direct my Executor to pay all my just debts, funeral expenses, and testamentary expenses as soon as conveniently may be after my death.

{% if has_minor_children and guardian_name %}
ARTICLE IV - APPOINTMENT OF GUARDIAN
4.1 If at the time of my death any of my children are minors, I appoint {{ guardian_name }} of {{ guardian_address }} to be the Guardian of the person and property of such minor children.
{% if alternate_guardian %}
4.2 If {{ guardian_name }} is unable or unwilling to act as Guardian, I appoint {{ alternate_guardian }} as alternate Guardian.
{% endif %}
{% endif %}

ARTICLE V - DISTRIBUTION OF ESTATE
{% if beneficiaries %}
5.1 I give, devise and bequeath my estate to the following beneficiaries:
{% for beneficiary in beneficiaries %}
   - {{ beneficiary.percentage }}% to {{ beneficiary.name }} of {{ beneficiary.address }}
   {% if beneficiary.relationship %}({{ beneficiary.relationship }}){% endif %}
{% endfor %}
{% endif %}

{% if specific_bequests %}
ARTICLE VI - SPECIFIC BEQUESTS
{% for bequest in specific_bequests %}
6.{{ loop.index }} I give {{ bequest.item }} to {{ bequest.recipient }}.
{% endfor %}
{% endif %}

{% if 'real_estate_clause' in applicable_asset_clauses %}
ARTICLE VII - REAL ESTATE PROVISIONS
7.1 With respect to any real estate forming part of my estate, I authorize my Executor to sell, lease, mortgage, or otherwise deal with such property as they deem advisable.
{% endif %}

{% if 'business_interests_clause' in applicable_asset_clauses %}
ARTICLE VIII - BUSINESS INTERESTS
8.1 With respect to any business interests forming part of my estate, I authorize my Executor to continue, sell, or wind up such business as they deem to be in the best interests of my estate.
{% endif %}

ARTICLE IX - POWERS OF EXECUTOR
9.1 I give to my Executor all powers conferred by law and such additional powers as may be necessary for the proper administration of my estate.

ARTICLE X - EXECUTION
10.1 IN WITNESS WHEREOF, I have hereunto set my hand this {{ current_date }}.

_________________________
{{ full_name }}, Testator

SIGNED, PUBLISHED AND DECLARED by the above-named Testator as and for their Last Will and Testament, in the presence of us, both present at the same time, who at their request, in their presence, and in the presence of each other, have hereunto subscribed our names as witnesses.

Witness 1:                          Witness 2:
_________________________          _________________________
Name: ___________________          Name: ___________________
Address: ________________          Address: ________________
        ________________                  ________________

{% if distribution_warning %}
IMPORTANT NOTICE: {{ distribution_warning }}
{% endif %}
{% if guardian_warning %}
IMPORTANT NOTICE: {{ guardian_warning }}
{% endif %}
{% if executor_recommendation %}
RECOMMENDATION: {{ executor_recommendation }}
{% endif %}
"""
    
    def _get_enhanced_poa_property_template(self) -> str:
        """Enhanced Power of Attorney for Property template."""
        return """
CONTINUING POWER OF ATTORNEY FOR PROPERTY

I, {{ full_name }}, of {{ address }}, in the Province of Ontario, appoint {{ attorney_name }} of {{ attorney_address }} to be my attorney for property.

{% if multiple_attorneys %}
I appoint the following persons to be my attorneys for property:
{% for attorney in attorneys %}
- {{ attorney.name }} of {{ attorney.address }}
{% endfor %}

{% if decision_making == 'jointly' %}
My attorneys must act jointly in making decisions.
{% elif decision_making == 'severally' %}
My attorneys may act severally (independently) in making decisions.
{% elif decision_making == 'majority' %}
My attorneys must act by majority decision.
{% endif %}
{% endif %}

AUTHORITY GRANTED:
I give my attorney(s) authority to do on my behalf anything in respect of property that I could do if capable of managing property, except make a will, subject to the law and to any conditions or restrictions contained in this document.

{% if authority_limitations %}
LIMITATIONS ON AUTHORITY:
My attorney(s) shall NOT have authority to:
{% for limitation in authority_limitations %}
- {{ limitation }}
{% endfor %}
{% endif %}

{% if compensation_clause %}
COMPENSATION:
I authorize my attorney(s) to be compensated for their services in accordance with the guidelines established by the Ontario Superior Court of Justice.
{% endif %}

CONDITIONS AND RESTRICTIONS:
1. This power of attorney shall continue despite any mental incapacity on my part.
2. My attorney(s) shall keep accurate records of all transactions.
3. My attorney(s) shall act honestly and in good faith and in my best interests.

EFFECTIVE DATE:
This power of attorney comes into effect on {{ effective_date | default('the date it is signed') }}.

SIGNED this {{ current_date }}.

_________________________
{{ full_name }}

WITNESS:
I am at least 18 years of age and I am not the attorney or the attorney's spouse or partner.

_________________________
Witness Signature

_________________________
Witness Name (print)

_________________________
Witness Address
"""
    
    def _get_enhanced_poa_care_template(self) -> str:
        """Enhanced Power of Attorney for Personal Care template."""
        return """
POWER OF ATTORNEY FOR PERSONAL CARE

I, {{ full_name }}, of {{ address }}, in the Province of Ontario, appoint {{ attorney_name }} of {{ attorney_address }} to be my attorney for personal care.

{% if has_multiple_sdm %}
SUBSTITUTE DECISION MAKERS:
If {{ attorney_name }} is unable or unwilling to act, I appoint the following persons in order of priority:
{% for sdm in substitute_decision_makers %}
{{ loop.index }}. {{ sdm.name }} of {{ sdm.address }}
{% endfor %}
{% endif %}

AUTHORITY GRANTED:
I give my attorney authority to make decisions concerning my personal care, including healthcare, nutrition, shelter, clothing, hygiene and safety.

{% if has_healthcare_preferences %}
HEALTHCARE PREFERENCES:
{{ healthcare_preferences }}
{% endif %}

{% if has_end_of_life_wishes %}
END-OF-LIFE WISHES:
{{ end_of_life_wishes }}
{% endif %}

CONDITIONS:
1. This power of attorney comes into effect only when I become mentally incapable of making decisions about my personal care.
2. My attorney shall consult with me to the extent possible and shall encourage me to participate in decisions.
3. My attorney shall act in accordance with my known wishes and values.

SIGNED this {{ current_date }}.

_________________________
{{ full_name }}

WITNESS:
I am at least 18 years of age.

_________________________
Witness Signature

_________________________
Witness Name (print)

_________________________
Witness Address
"""
    
    def _load_legal_requirements(self) -> Dict[str, Any]:
        """Load legal requirements for different document types."""
        return {
            'will': {
                'minimum_age': 18,
                'required_fields': ['full_name', 'address', 'executor_name', 'executor_address'],
                'required_elements': ['testator_signature', 'witness_signatures', 'date'],
                'validation_rules': {
                    'full_name': [{'type': 'min_length', 'value': 2, 'message': 'should be at least 2 characters'}],
                    'executor_name': [{'type': 'min_length', 'value': 2, 'message': 'should be at least 2 characters'}]
                }
            },
            'poa_property': {
                'minimum_age': 18,
                'required_fields': ['full_name', 'address', 'attorney_name', 'attorney_address'],
                'required_elements': ['grantor_signature', 'witness_signature', 'date'],
                'validation_rules': {}
            },
            'poa_care': {
                'minimum_age': 16,
                'required_fields': ['full_name', 'address', 'attorney_name', 'attorney_address'],
                'required_elements': ['grantor_signature', 'witness_signature', 'date'],
                'validation_rules': {}
            }
        }
    
    def _calculate_age(self, date_of_birth: str) -> int:
        """Calculate age from date of birth."""
        try:
            birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d')
            today = datetime.now()
            return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        except:
            return 0
    
    def _apply_validation_rule(self, value: Any, rule: Dict[str, Any]) -> bool:
        """Apply a validation rule to a field value."""
        rule_type = rule.get('type')
        rule_value = rule.get('value')
        
        if rule_type == 'min_length' and isinstance(value, str):
            return len(value) >= rule_value
        elif rule_type == 'max_length' and isinstance(value, str):
            return len(value) <= rule_value
        elif rule_type == 'pattern' and isinstance(value, str):
            return bool(re.match(rule_value, value))
        
        return True
    
    def _check_requirement_in_content(self, content: str, requirement: str) -> bool:
        """Check if a requirement is present in the document content."""
        requirement_patterns = {
            'testator_signature': r'_+\s*\n.*testator',
            'witness_signatures': r'witness.*signature|_+.*witness',
            'date': r'\d{1,2}.*\d{4}|current_date'
        }
        
        pattern = requirement_patterns.get(requirement, requirement.lower())
        return bool(re.search(pattern, content, re.IGNORECASE))
    
    def _get_document_title(self, document_type: str) -> str:
        """Get the formal title for a document type."""
        titles = {
            'will': 'Last Will and Testament',
            'poa_property': 'Continuing Power of Attorney for Property',
            'poa_care': 'Power of Attorney for Personal Care'
        }
        return titles.get(document_type, document_type.title())

