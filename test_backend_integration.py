"""
Test script to verify backend integration with enhanced document manager
"""

import requests
import json
import time
import asyncio
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

async def test_enhanced_features():
    """Test the enhanced document management features"""
    
    # Test document generation
    print("Testing document generation...")
    
    will_request = {
        "document_type": "will",
        "content": {
            "testator_name": "John Smith",
            "testator_address": "123 Main Street, Toronto, ON M1A 1A1",
            "executor_name": "Jane Smith",
            "executor_address": "456 Oak Avenue, Toronto, ON M2B 2B2",
            "residuary_beneficiary": "My children equally",
            "specific_bequests": [
                {
                    "item": "my vintage watch collection",
                    "beneficiary": "my son Michael"
                }
            ]
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/documents/generate",
            json=will_request,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Document generation successful")
            print(f"Document ID: {result.get('document_id')}")
            print(f"Content preview: {result.get('content', '')[:200]}...")
        else:
            print(f"✗ Document generation failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
        print("Make sure the backend server is running on port 8000")
        return False
    
    # Test template retrieval
    print("\nTesting template retrieval...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/documents/templates/will")
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Template retrieval successful")
            print(f"Template sections: {result.get('template', {}).get('sections', [])}")
        else:
            print(f"✗ Template retrieval failed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Template retrieval error: {e}")
    
    # Test document validation
    print("\nTesting document validation...")
    
    validation_request = {
        "document_type": "will",
        "content": {
            "testator_name": "John Smith",
            "executor_name": "Jane Smith",
            "witnesses": ["Witness 1", "Witness 2"]
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/documents/validate",
            json=validation_request
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Document validation successful")
            validation = result.get('validation', {})
            print(f"Compliance score: {validation.get('compliance_score', 'N/A')}")
            print(f"Legal issues: {len(validation.get('legal_issues', []))}")
        else:
            print(f"✗ Document validation failed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Validation error: {e}")
    
    # Test legal research
    print("\nTesting legal research...")
    
    research_request = {
        "query": "Ontario will execution requirements",
        "document_type": "will"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/documents/legal-research",
            json=research_request
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Legal research successful")
            research = result.get('research_result', {})
            print(f"Cases found: {len(research.get('relevant_cases', []))}")
            print(f"Confidence: {research.get('confidence', 'N/A')}")
        else:
            print(f"✗ Legal research failed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Legal research error: {e}")
    
    # Test court form generation
    print("\nTesting court form generation...")
    
    court_form_data = {
        "deceased_name": "Robert Johnson",
        "applicant_name": "Mary Johnson",
        "relationship": "Spouse",
        "estate_value": "750000",
        "applicant_address": "789 Pine Street, Ottawa, ON K1A 0A1"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/documents/court-forms/74",
            json=court_form_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Court form generation successful")
            print(f"Form document ID: {result.get('document_id')}")
        else:
            print(f"✗ Court form generation failed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Court form error: {e}")
    
    print("\n" + "="*50)
    print("Integration test completed!")
    return True

def test_server_connectivity():
    """Test if the server is running and accessible"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        return True
    except requests.exceptions.RequestException:
        return False

if __name__ == "__main__":
    print("Enhanced Document Manager Backend Integration Test")
    print("="*50)
    
    # Check server connectivity
    if not test_server_connectivity():
        print("⚠️  Backend server is not running or not accessible")
        print("   Start the server with: cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000")
        print("   Then run this test again")
        exit(1)
    
    # Run tests
    asyncio.run(test_enhanced_features())
    
    print("\nTo start the backend server manually:")
    print("cd /home/runner/work/Will-and-POA-App/Will-and-POA-App/backend")
    print("python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload")