"""
Test suite for Enhanced Document Manager
"""

import asyncio
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from backend.services.enhanced_document_manager import EnhancedDocumentManager
    from backend.services.enhanced_ai_legal_service import EnhancedAILegalService
except ImportError as e:
    print(f"Import error: {e}")
    print("Running without full test suite...")

async def run_simple_test():
    """Run a simple functionality test"""
    print("Running enhanced document manager test...")
    
    # Test document manager
    temp_dir = tempfile.mkdtemp()
    try:
        from backend.services.enhanced_document_manager import EnhancedDocumentManager
        from backend.services.enhanced_ai_legal_service import EnhancedAILegalService
        
        manager = EnhancedDocumentManager(
            storage_path=str(Path(temp_dir) / "storage"),
            client_docs_path=str(Path(temp_dir) / "client_docs")
        )
        
        await manager.initialize()
        print("✓ Document manager initialized successfully")
        
        # Test will generation
        fields = {
            "testator_name": "John Doe",
            "testator_address": "123 Main St, Toronto, ON",
            "executor_name": "Jane Smith",
            "residuary_beneficiary": "My children equally"
        }
        
        content = await manager.generate_document("will", fields)
        print("✓ Will document generated successfully")
        print(f"Content preview: {content[:200]}...")
        
        # Test POA generation
        poa_fields = {
            "grantor_name": "Mary Johnson",
            "grantor_address": "456 Oak Ave, Ottawa, ON",
            "attorney_name": "Robert Wilson"
        }
        
        poa_content = await manager.generate_document("poa_property", poa_fields)
        print("✓ POA document generated successfully")
        
        # Test AI service
        ai_service = EnhancedAILegalService()
        result = await ai_service.conduct_legal_research("will validity", "will")
        print("✓ Legal research completed successfully")
        print(f"Research confidence: {result.confidence}")
        
        # Test document analysis
        analysis = await ai_service.analyze_document("will", fields)
        print("✓ Document analysis completed successfully")
        print(f"Compliance score: {analysis.compliance_score}")
        
        # Test court form generation
        court_data = {
            "deceased_name": "William Brown",
            "applicant_name": "Susan Brown",
            "relationship": "Spouse",
            "estate_value": "500000"
        }
        
        court_doc_id = await manager.create_ontario_court_form("74", court_data)
        print(f"✓ Court form created successfully: {court_doc_id}")
        
        # Test document statistics
        stats = await manager.get_document_statistics()
        print(f"✓ Document statistics retrieved: {stats}")
        
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        raise
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    print("All tests passed!")

if __name__ == "__main__":
    asyncio.run(run_simple_test())