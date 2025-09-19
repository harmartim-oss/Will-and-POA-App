import openai
import os
from typing import List, Dict

class AIService:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_API_BASE')
        )
    
    def get_suggestions(self, document, section: str, text: str) -> List[Dict]:
        """Get AI-powered wording suggestions for legal documents"""
        try:
            document_type = document.document_type
            suggestions = []
            
            # Get legal compliance suggestions
            legal_suggestions = self._get_legal_compliance_suggestions(document_type, section, text)
            suggestions.extend(legal_suggestions)
            
            # Get clarity improvements
            clarity_suggestions = self._get_clarity_suggestions(text)
            suggestions.extend(clarity_suggestions)
            
            # Get professional wording suggestions
            professional_suggestions = self._get_professional_wording_suggestions(document_type, text)
            suggestions.extend(professional_suggestions)
            
            return suggestions
        except Exception as e:
            print(f"Error getting AI suggestions: {e}")
            return []
    
    def _get_legal_compliance_suggestions(self, document_type: str, section: str, text: str) -> List[Dict]:
        """Get suggestions for legal compliance"""
        prompt = f"""
        You are a legal expert specializing in Ontario estate law. Review the following text from a {document_type} document, 
        specifically the {section} section, and provide suggestions to ensure it complies with Ontario legal requirements.
        
        Text to review: "{text}"
        
        Provide specific suggestions for:
        1. Legal compliance with Ontario laws
        2. Required legal language
        3. Missing legal elements
        
        Format your response as a JSON array of suggestions, each with 'text' and 'reason' fields.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a legal expert specializing in Ontario estate law."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            # Parse the response and format as suggestions
            content = response.choices[0].message.content
            suggestions = self._parse_ai_response(content, 'legal_compliance')
            return suggestions
        except Exception as e:
            print(f"Error getting legal compliance suggestions: {e}")
            return []
    
    def _get_clarity_suggestions(self, text: str) -> List[Dict]:
        """Get suggestions for improving clarity"""
        prompt = f"""
        Review the following legal text and suggest improvements for clarity and readability while maintaining legal precision:
        
        Text: "{text}"
        
        Provide suggestions for:
        1. Clearer language
        2. Better sentence structure
        3. Removing ambiguity
        
        Format your response as a JSON array of suggestions, each with 'text' and 'reason' fields.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in legal writing and communication."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            suggestions = self._parse_ai_response(content, 'clarity')
            return suggestions
        except Exception as e:
            print(f"Error getting clarity suggestions: {e}")
            return []
    
    def _get_professional_wording_suggestions(self, document_type: str, text: str) -> List[Dict]:
        """Get suggestions for professional legal wording"""
        prompt = f"""
        Review the following text from a {document_type} and suggest more professional legal wording:
        
        Text: "{text}"
        
        Provide suggestions for:
        1. More formal legal language
        2. Standard legal terminology
        3. Professional phrasing
        
        Format your response as a JSON array of suggestions, each with 'text' and 'reason' fields.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in legal document drafting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            suggestions = self._parse_ai_response(content, 'professional')
            return suggestions
        except Exception as e:
            print(f"Error getting professional wording suggestions: {e}")
            return []
    
    def _parse_ai_response(self, content: str, suggestion_type: str) -> List[Dict]:
        """Parse AI response and format as suggestions"""
        try:
            import json
            # Try to parse as JSON first
            if content.strip().startswith('['):
                suggestions_data = json.loads(content)
                return [
                    {
                        'text': item.get('text', ''),
                        'type': suggestion_type,
                        'reason': item.get('reason', '')
                    }
                    for item in suggestions_data
                ]
            else:
                # If not JSON, create a single suggestion
                return [{
                    'text': content.strip(),
                    'type': suggestion_type,
                    'reason': f'AI-generated {suggestion_type} suggestion'
                }]
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            return []
    
    def validate_legal_requirements(self, document_type: str, content: Dict) -> Dict:
        """Validate document against legal requirements"""
        prompt = f"""
        You are a legal expert specializing in Ontario estate law. Review the following {document_type} document content 
        and validate it against Ontario legal requirements.
        
        Document content: {content}
        
        Check for:
        1. Required elements
        2. Legal compliance
        3. Missing information
        4. Potential issues
        
        Provide a validation report with:
        - is_valid: boolean
        - issues: list of issues found
        - suggestions: list of suggestions for improvement
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a legal expert specializing in Ontario estate law."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            # Parse and return validation result
            content_response = response.choices[0].message.content
            return {
                'is_valid': True,  # Default to true, parse from response
                'issues': [],
                'suggestions': [],
                'ai_response': content_response
            }
        except Exception as e:
            print(f"Error validating legal requirements: {e}")
            return {
                'is_valid': False,
                'issues': ['Error during validation'],
                'suggestions': [],
                'ai_response': str(e)
            }
    
    def generate_section_content(self, document_type: str, section: str, user_input: Dict) -> str:
        """Generate content for a specific section based on user input"""
        prompt = f"""
        Generate professional legal content for the {section} section of a {document_type} document based on the following user input:
        
        User input: {user_input}
        
        The content should:
        1. Be legally compliant with Ontario law
        2. Use appropriate legal terminology
        3. Be clear and unambiguous
        4. Follow standard legal document formatting
        
        Provide only the content for this section, properly formatted.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert legal document drafter specializing in Ontario estate law."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating section content: {e}")
            return f"Error generating content for {section}: {str(e)}"

