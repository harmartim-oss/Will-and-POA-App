#!/usr/bin/env python3
"""
Test script for the integrated Ontario Legal AI System
Demonstrates the new AI capabilities
"""

import asyncio
import json
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.core.database_manager import DatabaseManager
from backend.core.blockchain_authenticator import BlockchainAuthenticator
from backend.core.ontario_legal_knowledge import OntarioLegalKnowledgeBase
from backend.core.ontario_document_generator import OntarioLegalDocumentGenerator
from backend.core.ai_engine import OntarioLegalAIEngine

async def test_ai_integration():
    """Test the integrated AI system components"""
    print("🧪 Testing Ontario Legal AI System Integration")
    print("=" * 50)
    
    # Test Database Manager
    print("\n📊 Testing Database Manager...")
    database = DatabaseManager("test_ai_integration.db")
    await database.initialize()
    
    # Test analysis logging
    request_id = await database.log_analysis_request("test_user", "will", 1000)
    print(f"✓ Analysis request logged: {request_id}")
    
    # Test Blockchain Authenticator
    print("\n🔗 Testing Blockchain Authenticator...")
    blockchain = BlockchainAuthenticator()
    await blockchain.initialize()
    
    # Test document storage
    test_document = "This is my last will and testament..."
    blockchain_hash = await blockchain.store_document_hash("test_doc_1", test_document)
    print(f"✓ Document stored on blockchain: {blockchain_hash}")
    
    # Test verification
    verification = await blockchain.verify_document("test_doc_1", test_document)
    print(f"✓ Document verification: {verification['verified']}")
    
    # Test Legal Knowledge Base
    print("\n📚 Testing Enhanced Legal Knowledge Base...")
    knowledge_base = OntarioLegalKnowledgeBase()
    await knowledge_base.initialize()
    
    # Test case law search
    cases = knowledge_base.search_case_law("testamentary capacity")
    print(f"✓ Found {len(cases)} cases related to testamentary capacity")
    
    # Test legal definitions
    definition = knowledge_base.get_legal_definition("executor")
    if definition:
        print(f"✓ Legal definition retrieved: {definition['definition'][:50]}...")
    
    # Test Document Generator
    print("\n📝 Testing Document Generator...")
    doc_generator = OntarioLegalDocumentGenerator()
    await doc_generator.initialize()
    
    # Test document generation
    user_data = {
        "full_name": "John Doe",
        "address": "123 Main St, Toronto, ON",
        "executor_name": "Jane Doe",
        "executor_address": "456 Oak Ave, Toronto, ON",
        "residuary_beneficiary": "my spouse, Jane Doe"
    }
    
    documents = await doc_generator.generate_legal_documents(
        document_type="will",
        user_data=user_data,
        ai_recommendations=["Consider appointing an alternate executor"]
    )
    
    print(f"✓ Will generated: {len(documents['text_content'])} characters")
    print(f"✓ PDF version: {len(documents['pdf_content'])} characters")
    
    # Test AI Engine
    print("\n🤖 Testing AI Engine...")
    ai_engine = OntarioLegalAIEngine()
    await ai_engine.initialize()
    
    # Test document analysis
    test_will_text = """
    I, John Smith, being of sound mind, do hereby make this my last will and testament.
    I appoint my wife Mary Smith as executor of this will.
    I leave all my property to my children equally.
    """
    
    analysis = await ai_engine.analyze_document(test_will_text, "will")
    print(f"✓ Document analysis completed")
    print(f"  - Document type: {analysis['document_type']}")
    print(f"  - Confidence: {analysis['confidence']:.2f}")
    print(f"  - Compliance issues: {len(analysis['compliance_issues'])}")
    print(f"  - Recommendations: {len(analysis['recommendations'])}")
    
    # Test legal question answering
    legal_answer = await ai_engine.answer_legal_question("What are the requirements for a valid will in Ontario?")
    print(f"✓ Legal question answered")
    print(f"  - Answer: {legal_answer['answer'][:100]}...")
    print(f"  - Confidence: {legal_answer['confidence']:.2f}")
    
    # Integration Test - Full Workflow
    print("\n🔄 Testing Full AI Workflow...")
    
    # 1. Analyze document
    workflow_analysis = await ai_engine.analyze_document(test_will_text, "will", "Simple will case")
    
    # 2. Store analysis
    analysis_id = await database.store_analysis("test_user", workflow_analysis, 0.5)
    
    # 3. Generate improved document with AI recommendations
    ai_recommendations = await ai_engine.generate_document_recommendations("will", user_data)
    improved_documents = await doc_generator.generate_legal_documents(
        "will", user_data, ai_recommendations
    )
    
    # 4. Store document
    doc_id = await database.store_document("test_user", "will", improved_documents, ai_recommendations)
    
    # 5. Create blockchain record
    final_blockchain_hash = await blockchain.store_document_hash(doc_id, improved_documents['text_content'])
    
    print(f"✓ Complete workflow executed:")
    print(f"  - Analysis ID: {analysis_id}")
    print(f"  - Document ID: {doc_id}")
    print(f"  - Blockchain Hash: {final_blockchain_hash}")
    print(f"  - AI Recommendations: {len(ai_recommendations)}")
    
    # Test system statistics
    print("\n📈 System Statistics...")
    blockchain_stats = await blockchain.get_blockchain_stats()
    print(f"✓ Blockchain: {blockchain_stats['total_documents']} documents, {blockchain_stats['total_transactions']} transactions")
    
    user_docs = await database.get_user_documents("test_user")
    user_analyses = await database.get_analysis_history("test_user")
    print(f"✓ Database: {len(user_docs)} documents, {len(user_analyses)} analyses for test user")
    
    print("\n🎉 All tests completed successfully!")
    print("The Ontario Legal AI System is fully integrated and operational.")
    
    # Cleanup
    await database.close()

if __name__ == "__main__":
    asyncio.run(test_ai_integration())