#!/usr/bin/env python3
"""
Test Ontario Sole Practitioner Enhancement Package
"""

import asyncio
import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

async def test_security_manager():
    """Test the Ontario Legal Security Manager"""
    print("🔐 Testing Ontario Legal Security Manager...")
    
    try:
        from backend.core.sole_practitioner_security import OntarioLegalSecurityManager
        
        # Initialize security manager
        security_manager = OntarioLegalSecurityManager()
        await security_manager.initialize()
        print("✓ Security manager initialized")
        
        # Test data encryption
        test_data = "This is confidential legal document data for John Doe's will"
        encrypted_package = await security_manager.encrypt_legal_data(test_data, "confidential")
        print("✓ Data encryption successful")
        
        # Test data decryption
        decrypted_data = await security_manager.decrypt_legal_data(encrypted_package)
        assert decrypted_data == test_data, "Decryption failed - data mismatch"
        print("✓ Data decryption successful")
        
        # Test lawyer authentication
        lawyer_info = {
            "lsuc_number": "12345",
            "name": "Jane Smith",
            "practice_areas": ["Wills & Estates", "Real Estate"]
        }
        auth_result = await security_manager.create_lawyer_authentication(lawyer_info)
        assert "access_token" in auth_result
        assert "lawyer_profile" in auth_result
        print("✓ Lawyer authentication creation successful")
        
        # Test assistant authentication
        assistant_info = {
            "assistant_id": "ASST001",
            "name": "Mary Johnson"
        }
        assistant_auth = await security_manager.create_assistant_authentication(assistant_info, "12345")
        assert "access_token" in assistant_auth
        assert "assistant_profile" in assistant_auth
        print("✓ Assistant authentication creation successful")
        
        # Test audit trail
        audit_id = await security_manager.generate_document_audit_trail(
            "doc_001", "created", "12345", {"ip_address": "192.168.1.100"}
        )
        assert audit_id is not None
        print("✓ Audit trail generation successful")
        
        # Test data retention policy
        retention_policy = await security_manager.enforce_data_retention_policy("wills", "client_001")
        assert retention_policy["retention_period_years"] == 7
        print("✓ Data retention policy enforcement successful")
        
        print("🎉 All security manager tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Security manager test failed: {str(e)}")
        return False

async def test_practice_manager():
    """Test the Ontario Practice Manager"""
    print("\n📋 Testing Ontario Practice Manager...")
    
    try:
        from backend.core.practice_management import OntarioPracticeManager
        
        # Create temporary database
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_practice.db")
        
        try:
            # Initialize practice manager
            practice_manager = OntarioPracticeManager(db_path)
            await practice_manager.initialize()
            print("✓ Practice manager initialized")
            
            # Test client creation
            client_data = {
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "416-555-0123",
                "address": "123 Main St, Toronto, ON M1A 1A1",
                "created_by": "LSUC12345"
            }
            client_id = await practice_manager.create_client(client_data)
            assert client_id.startswith("client_")
            print("✓ Client creation successful")
            
            # Test matter creation
            matter_data = {
                "client_id": client_id,
                "matter_name": "Estate Planning - Will and POA",
                "matter_type": "wills_estates",
                "responsible_lawyer": "LSUC12345",
                "estimated_value": 2500.00,
                "hourly_rate": 400.00,
                "billing_type": "hourly"
            }
            matter_id = await practice_manager.create_matter(matter_data)
            assert matter_id.startswith("matter_")
            print("✓ Matter creation successful")
            
            # Test time entry
            time_entry = {
                "matter_id": matter_id,
                "lawyer_id": "LSUC12345",
                "date_worked": "2024-01-15",
                "duration_minutes": 120,
                "description": "Initial client consultation for will preparation",
                "activity_type": "consultation",
                "billable": True,
                "hourly_rate": 400.00
            }
            entry_id = await practice_manager.add_time_entry(time_entry)
            assert entry_id.startswith("time_")
            print("✓ Time entry creation successful")
            
            # Test document association
            doc_assoc_id = await practice_manager.associate_document_with_matter(
                matter_id, "doc_001", "will", "Last Will and Testament - John Doe", "LSUC12345"
            )
            assert doc_assoc_id.startswith("assoc_")
            print("✓ Document association successful")
            
            # Test deadline creation
            from datetime import datetime, timedelta
            deadline_data = {
                "matter_id": matter_id,
                "deadline_type": "document_execution",
                "description": "Will execution appointment",
                "due_date": (datetime.now() + timedelta(days=14)).date(),
                "responsible_lawyer": "LSUC12345",
                "priority": "high"
            }
            deadline_id = await practice_manager.add_deadline(deadline_data)
            assert deadline_id.startswith("deadline_")
            print("✓ Deadline creation successful")
            
            # Test client matters retrieval
            matters = await practice_manager.get_client_matters(client_id)
            assert len(matters) == 1
            print("✓ Client matters retrieval successful")
            
            # Test time summary
            time_summary = await practice_manager.get_time_summary(matter_id)
            assert time_summary["total_hours"] == 2.0
            assert time_summary["total_billable_amount"] == 800.0
            print("✓ Time summary calculation successful")
            
            # Test upcoming deadlines
            deadlines = await practice_manager.get_upcoming_deadlines("LSUC12345", 30)
            assert len(deadlines) >= 1
            print("✓ Upcoming deadlines retrieval successful")
            
            print("🎉 All practice manager tests passed!")
            return True
            
        finally:
            # Clean up temporary files
            shutil.rmtree(temp_dir, ignore_errors=True)
            
    except Exception as e:
        print(f"❌ Practice manager test failed: {str(e)}")
        return False

async def test_enhanced_auth_service():
    """Test the Enhanced Auth Service"""
    print("\n🔐 Testing Enhanced Auth Service...")
    
    try:
        from backend.services.enhanced_auth_service import EnhancedAuthService
        from flask import Flask
        
        # Create minimal Flask app for context
        app = Flask(__name__)
        app.config['JWT_SECRET_KEY'] = 'test_secret_key'
        
        with app.app_context():
            # Initialize auth service
            auth_service = EnhancedAuthService(app)
            await auth_service.initialize_async_components()
            print("✓ Enhanced auth service initialized")
            
            # Test lawyer registration
            lawyer_data = {
                "lsuc_number": "12345",
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "password": "secure_password",
                "practice_areas": ["Wills & Estates"]
            }
            
            registration_result = await auth_service.register_lawyer(lawyer_data)
            assert registration_result["success"] == True
            assert "access_token" in registration_result
            print("✓ Lawyer registration successful")
            
            # Test lawyer authentication
            auth_credentials = {
                "user_type": "lawyer",
                "lsuc_number": "12345",
                "password": "secure_password"
            }
            
            auth_result = await auth_service.authenticate_legal_user(auth_credentials)
            assert auth_result["success"] == True
            assert "access_token" in auth_result
            print("✓ Lawyer authentication successful")
            
            # Test assistant registration
            assistant_data = {
                "assistant_id": "ASST001",
                "name": "Mary Johnson",
                "email": "mary.johnson@example.com"
            }
            
            assistant_result = await auth_service.register_assistant(assistant_data, "12345")
            assert assistant_result["success"] == True
            assert "access_token" in assistant_result
            print("✓ Assistant registration successful")
        
        print("🎉 All enhanced auth service tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Enhanced auth service test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def run_all_tests():
    """Run all tests for the Ontario Sole Practitioner Enhancement Package"""
    print("🚀 Starting Ontario Sole Practitioner Enhancement Package Tests\n")
    
    results = []
    
    # Test security manager
    results.append(await test_security_manager())
    
    # Test practice manager
    results.append(await test_practice_manager())
    
    # Test enhanced auth service
    results.append(await test_enhanced_auth_service())
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed_tests = sum(results)
    total_tests = len(results)
    
    print(f"✅ Tests passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Ontario Sole Practitioner Enhancement Package is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)