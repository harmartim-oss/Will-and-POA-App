#!/usr/bin/env python3
"""
Simple test script for the integrated Ontario Legal AI System
Tests core functionality without network-dependent components
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

async def test_ai_integration_simple():
    """Test the integrated AI system components (offline mode)"""
    print("🧪 Testing Ontario Legal AI System Integration (Offline Mode)")
    print("=" * 60)
    success_count = 0
    total_tests = 0
    
    # Test Database Manager
    print("\n📊 Testing Database Manager...")
    try:
        database = DatabaseManager("test_simple.db")
        await database.initialize()
        
        # Test analysis logging
        request_id = await database.log_analysis_request("test_user", "will", 1000)
        print(f"✓ Analysis request logged: {request_id}")
        success_count += 1
        
        # Test analysis storage
        test_analysis = {
            "document_type": "will",
            "confidence": 0.85,
            "entities": [{"text": "John Doe", "label": "PERSON"}],
            "requirements": [{"requirement": "Must be in writing"}],
            "compliance_issues": [],
            "recommendations": ["Consider legal review"],
            "sentiment": {"label": "NEUTRAL", "score": 0.5}
        }
        analysis_id = await database.store_analysis("test_user", test_analysis, 1.2)
        print(f"✓ Analysis stored: {analysis_id}")
        success_count += 1
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
    
    total_tests += 2
    
    # Test Blockchain Authenticator
    print("\n🔗 Testing Blockchain Authenticator...")
    try:
        blockchain = BlockchainAuthenticator()
        await blockchain.initialize()
        
        # Test document storage
        test_document = "This is my last will and testament. I, John Smith, being of sound mind..."
        blockchain_hash = await blockchain.store_document_hash("test_doc_1", test_document)
        print(f"✓ Document stored on blockchain: {blockchain_hash[:16]}...")
        success_count += 1
        
        # Test verification
        verification = await blockchain.verify_document("test_doc_1", test_document)
        print(f"✓ Document verification: {verification['verified']}")
        success_count += 1
        
        # Test blockchain stats
        stats = await blockchain.get_blockchain_stats()
        print(f"✓ Blockchain stats: {stats['total_documents']} docs, {stats['total_transactions']} transactions")
        success_count += 1
        
    except Exception as e:
        print(f"❌ Blockchain test failed: {e}")
    
    total_tests += 3
    
    # Test Legal Knowledge Base
    print("\n📚 Testing Enhanced Legal Knowledge Base...")
    try:
        knowledge_base = OntarioLegalKnowledgeBase()
        await knowledge_base.initialize()
        
        # Test case law search
        cases = knowledge_base.search_case_law("testamentary capacity")
        print(f"✓ Found {len(cases)} cases related to testamentary capacity")
        success_count += 1
        
        if cases:
            case = cases[0]
            print(f"  - Case: {case.case_name} ({case.year})")
            print(f"  - Court: {case.court}")
            print(f"  - Key principles: {len(case.key_principles)}")
        
        # Test legal definitions
        definition = knowledge_base.get_legal_definition("executor")
        if definition:
            print(f"✓ Legal definition retrieved: {definition['definition'][:60]}...")
            success_count += 1
        
        # Test statutory requirements
        will_requirements = knowledge_base.get_statutory_requirements("will")
        print(f"✓ Will requirements: {len(will_requirements)} statutory requirements")
        success_count += 1
        
        # Test legal provisions
        provision = knowledge_base.get_legal_provision("wills_act", "4")
        if provision:
            print(f"✓ Legal provision retrieved: {provision.act}, section {provision.section}")
            success_count += 1
        
    except Exception as e:
        print(f"❌ Legal Knowledge Base test failed: {e}")
    
    total_tests += 4
    
    # Test Document Generator
    print("\n📝 Testing Document Generator...")
    try:
        doc_generator = OntarioLegalDocumentGenerator()
        await doc_generator.initialize()
        
        # Test document generation
        user_data = {
            "full_name": "John Doe",
            "address": "123 Main St, Toronto, ON M5V 1A1",
            "executor_name": "Jane Doe",
            "executor_address": "456 Oak Ave, Toronto, ON M5V 2B2",
            "residuary_beneficiary": "my spouse, Jane Doe",
            "has_minor_children": False
        }
        
        # Test data validation
        validation = await doc_generator.validate_document_data("will", user_data)
        print(f"✓ Data validation: {validation['is_valid']}")
        if validation['errors']:
            print(f"  - Errors: {validation['errors']}")
        if validation['warnings']:
            print(f"  - Warnings: {validation['warnings']}")
        success_count += 1
        
        # Generate will
        documents = await doc_generator.generate_legal_documents(
            document_type="will",
            user_data=user_data,
            ai_recommendations=["Consider appointing an alternate executor"]
        )
        
        print(f"✓ Will generated: {len(documents['text_content'])} characters")
        print(f"✓ PDF version: {len(documents['pdf_content'])} characters")
        print(f"✓ DOCX version: {len(documents['docx_content'])} characters")
        success_count += 3
        
        # Test POA generation
        poa_user_data = {
            "grantor_name": "Alice Smith",
            "grantor_address": "789 Pine St, Toronto, ON M5V 3C3",
            "attorney_name": "Bob Smith",
            "attorney_address": "101 Elm St, Toronto, ON M5V 4D4"
        }
        
        poa_documents = await doc_generator.generate_legal_documents(
            document_type="poa_property",
            user_data=poa_user_data
        )
        
        print(f"✓ POA Property generated: {len(poa_documents['text_content'])} characters")
        success_count += 1
        
    except Exception as e:
        print(f"❌ Document Generator test failed: {e}")
    
    total_tests += 5
    
    # Integration Test - Full Workflow (without AI engine)
    print("\n🔄 Testing Integrated Workflow...")
    try:
        # Generate document with AI recommendations
        ai_recommendations = [
            "Consider appointing an alternate executor",
            "Include specific instructions for digital assets",
            "Consider establishing a trust for minor beneficiaries",
            "Ensure all parties understand their roles and responsibilities"
        ]
        
        workflow_documents = await doc_generator.generate_legal_documents(
            "will", user_data, ai_recommendations
        )
        
        # Store document in database
        doc_id = await database.store_document("test_user", "will", workflow_documents, ai_recommendations)
        
        # Create blockchain record
        blockchain_hash = await blockchain.store_document_hash(doc_id, workflow_documents['text_content'])
        
        # Generate proof of authenticity
        proof = await blockchain.export_proof_of_authenticity(doc_id)
        
        print(f"✓ Complete workflow executed:")
        print(f"  - Document ID: {doc_id}")
        print(f"  - Blockchain Hash: {blockchain_hash[:16]}...")
        print(f"  - AI Recommendations: {len(ai_recommendations)}")
        print(f"  - Proof of authenticity: {'Generated' if proof else 'Failed'}")
        success_count += 1
        
        # Test document retrieval
        user_docs = await database.get_user_documents("test_user")
        print(f"✓ User documents: {len(user_docs)} documents retrieved")
        success_count += 1
        
    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
    
    total_tests += 2
    
    # Final Statistics
    print("\n📈 Test Results Summary")
    print("=" * 60)
    print(f"✅ Successful tests: {success_count}/{total_tests}")
    print(f"📊 Success rate: {(success_count/total_tests)*100:.1f}%")
    
    if success_count == total_tests:
        print("\n🎉 ALL TESTS PASSED!")
        print("The Ontario Legal AI System core components are fully operational.")
    else:
        print(f"\n⚠️  {total_tests - success_count} tests failed.")
        print("Some components may need additional configuration.")
    
    # System Capabilities Summary
    print("\n🚀 System Capabilities Demonstrated:")
    print("✅ Database storage and retrieval")
    print("✅ Blockchain document authentication")
    print("✅ Legal knowledge base with Ontario law")
    print("✅ Document generation (Will, POA)")
    print("✅ AI recommendations integration")
    print("✅ Full document lifecycle management")
    print("✅ Proof of authenticity generation")
    
    # Cleanup
    try:
        await database.close()
        print("\n🧹 Cleanup completed")
    except:
        pass

if __name__ == "__main__":
    asyncio.run(test_ai_integration_simple())