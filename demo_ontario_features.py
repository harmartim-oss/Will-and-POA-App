#!/usr/bin/env python3
"""
Demo: Ontario Sole Practitioner Enhancement Package Features
Demonstrates the key capabilities of the enhancement package
"""

import asyncio
import sys
import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

async def demo_ontario_features():
    """Comprehensive demo of Ontario enhancement features"""
    print("🎯 Ontario Sole Practitioner Enhancement Package Demo")
    print("=" * 60)
    
    # Initialize components
    from backend.core.sole_practitioner_security import OntarioLegalSecurityManager
    from backend.core.practice_management import OntarioPracticeManager
    from backend.services.enhanced_auth_service import EnhancedAuthService
    from flask import Flask
    
    # Create temporary database
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "demo_practice.db")
    
    try:
        # Initialize services
        print("\n🔧 Initializing Ontario Legal Services...")
        security_manager = OntarioLegalSecurityManager()
        practice_manager = OntarioPracticeManager(db_path)
        
        # Initialize Flask app for auth service
        app = Flask(__name__)
        app.config['JWT_SECRET_KEY'] = 'demo_secret_key'
        
        with app.app_context():
            auth_service = EnhancedAuthService(app)
            
            await security_manager.initialize()
            await practice_manager.initialize()
            await auth_service.initialize_async_components()
        
        print("✅ All services initialized successfully")
        
        # Demo 1: Lawyer Registration and Authentication
        print("\n" + "="*50)
        print("📝 DEMO 1: Lawyer Registration & Authentication")
        print("="*50)
        
        lawyer_data = {
            "lsuc_number": "L12345",
            "name": "Sarah Johnson",
            "email": "sarah.johnson@lawfirm.com",
            "password": "SecureP@ss123",
            "firm_name": "Johnson Legal Services",
            "practice_areas": ["Wills & Estates", "Real Estate", "Corporate"]
        }
        
        with app.app_context():
            registration_result = await auth_service.register_lawyer(lawyer_data)
            print(f"✅ Lawyer registered: {registration_result['lawyer_profile']['name']}")
            print(f"   LSUC Number: {registration_result['lawyer_profile']['lsuc_number']}")
            print(f"   Security Level: {registration_result['lawyer_profile']['security_level']}")
            
            # Authenticate the lawyer
            auth_result = await auth_service.authenticate_legal_user({
                "user_type": "lawyer",
                "lsuc_number": "L12345",
                "password": "SecureP@ss123"
            })
            print(f"✅ Lawyer authenticated successfully")
            lawyer_token = auth_result['access_token']
        
        # Demo 2: Assistant Registration
        print(f"\n   👩‍💼 Registering Legal Assistant...")
        assistant_data = {
            "assistant_id": "ASST001",
            "name": "Michael Chen",
            "email": "michael.chen@lawfirm.com"
        }
        
        with app.app_context():
            assistant_result = await auth_service.register_assistant(assistant_data, "L12345")
            print(f"✅ Assistant registered: {assistant_result['assistant_profile']['name']}")
            print(f"   Supervising Lawyer: {assistant_result['assistant_profile']['supervising_lawyer']}")
            print(f"   Permissions: Document draft/review, Client data view")
        
        # Demo 3: Document Encryption and Security
        print("\n" + "="*50)
        print("🔐 DEMO 2: Document Encryption & Security")
        print("="*50)
        
        # Create a sample will document
        will_content = """
LAST WILL AND TESTAMENT

I, JOHN ROBERT SMITH, of the City of Toronto, in the Province of Ontario, being of sound mind and disposing memory, do hereby make, publish and declare this to be my Last Will and Testament.

1. REVOCATION: I hereby revoke all former Wills and Codicils by me made.

2. APPOINTMENT OF EXECUTOR: I hereby appoint my wife, MARY ELIZABETH SMITH, to be the sole Executor of this my Will.

3. BURIAL: I direct that my body be buried in Mount Pleasant Cemetery, Toronto.

4. BEQUESTS: I give, devise and bequeath all my property, both real and personal, to my wife, MARY ELIZABETH SMITH, absolutely.

IN WITNESS WHEREOF I have hereunto set my hand this 15th day of January, 2024.

________________________
JOHN ROBERT SMITH
        """
        
        print("📄 Original Will Content (excerpt):")
        print(will_content[:200] + "...")
        
        # Encrypt the document
        encrypted_package = await security_manager.encrypt_legal_data(
            will_content, 
            classification="confidential"
        )
        
        print(f"\n🔒 Document encrypted successfully")
        print(f"   Classification: {encrypted_package['metadata']['classification']}")
        print(f"   Encrypted at: {encrypted_package['metadata']['encrypted_at']}")
        print(f"   Data hash: {encrypted_package['metadata']['data_hash'][:16]}...")
        
        # Decrypt the document
        decrypted_content = await security_manager.decrypt_legal_data(encrypted_package)
        print(f"✅ Document decrypted and verified (integrity check passed)")
        
        # Generate audit trail
        audit_id = await security_manager.generate_document_audit_trail(
            document_id="will_001",
            action="created",
            user_id="L12345",
            details={
                "ip_address": "192.168.1.100",
                "client_name": "John Robert Smith",
                "document_type": "will"
            }
        )
        print(f"📋 Audit trail created: {audit_id}")
        
        # Demo 4: Practice Management
        print("\n" + "="*50)
        print("📊 DEMO 3: Practice Management System")
        print("="*50)
        
        # Create a client
        client_data = {
            "full_name": "John Robert Smith",
            "preferred_name": "John",
            "email": "john.smith@email.com",
            "phone": "416-555-0123",
            "address": "123 Main Street, Toronto, ON M5V 1A1",
            "date_of_birth": "1965-03-15",
            "client_type": "individual",
            "created_by": "L12345",
            "notes": "Referred by Mary Johnson. Needs will and POA.",
            "preferred_language": "English"
        }
        
        client_id = await practice_manager.create_client(client_data)
        print(f"👤 Client created: {client_data['full_name']} (ID: {client_id})")
        
        # Create a matter
        matter_data = {
            "client_id": client_id,
            "matter_name": "Estate Planning Package - Will and POA",
            "matter_type": "wills_estates",
            "matter_description": "Preparation of Last Will and Testament and Powers of Attorney",
            "responsible_lawyer": "L12345",
            "assistant_assigned": "ASST001",
            "opened_date": datetime.now().date(),
            "estimated_value": 2500.00,
            "hourly_rate": 450.00,
            "billing_type": "fixed_fee",
            "priority": "normal"
        }
        
        matter_id = await practice_manager.create_matter(matter_data)
        print(f"📁 Matter created: {matter_data['matter_name']} (ID: {matter_id})")
        
        # Add time entries
        time_entries = [
            {
                "matter_id": matter_id,
                "lawyer_id": "L12345",
                "date_worked": datetime.now().date(),
                "duration_minutes": 90,
                "description": "Initial client consultation - discussed estate planning goals",
                "activity_type": "client_meeting",
                "billable": True,
                "hourly_rate": 450.00
            },
            {
                "matter_id": matter_id,
                "lawyer_id": "L12345", 
                "date_worked": datetime.now().date(),
                "duration_minutes": 120,
                "description": "Will drafting and review",
                "activity_type": "document_preparation",
                "billable": True,
                "hourly_rate": 450.00
            },
            {
                "matter_id": matter_id,
                "lawyer_id": "ASST001",
                "date_worked": datetime.now().date(),
                "duration_minutes": 45,
                "description": "Document formatting and client file organization",
                "activity_type": "administrative",
                "billable": True,
                "hourly_rate": 150.00
            }
        ]
        
        total_time = 0
        for entry in time_entries:
            entry_id = await practice_manager.add_time_entry(entry)
            total_time += entry['duration_minutes']
            print(f"⏰ Time entry: {entry['duration_minutes']}min - {entry['description'][:50]}...")
        
        print(f"📊 Total time logged: {total_time // 60}h {total_time % 60}min")
        
        # Associate document with matter
        doc_assoc_id = await practice_manager.associate_document_with_matter(
            matter_id, "will_001", "will", "Last Will and Testament - John Smith.docx", "L12345"
        )
        print(f"📎 Document associated with matter: {doc_assoc_id}")
        
        # Add deadline
        deadline_data = {
            "matter_id": matter_id,
            "deadline_type": "document_execution",
            "description": "Client appointment for will execution and signing",
            "due_date": (datetime.now() + timedelta(days=7)).date(),
            "reminder_date": (datetime.now() + timedelta(days=5)).date(),
            "priority": "high",
            "responsible_lawyer": "L12345",
            "notes": "Ensure two witnesses available for signing"
        }
        
        deadline_id = await practice_manager.add_deadline(deadline_data)
        print(f"📅 Deadline added: {deadline_data['description']}")
        
        # Demo 5: Billing and Reporting
        print("\n" + "="*50)
        print("💰 DEMO 4: Billing & Financial Management")
        print("="*50)
        
        # Get time summary
        time_summary = await practice_manager.get_time_summary(matter_id)
        print(f"📈 Time Summary for Matter:")
        print(f"   Total Hours: {time_summary['total_hours']}")
        print(f"   Billable Hours: {time_summary['billable_hours']}")
        print(f"   Total Billable Amount: ${time_summary['total_billable_amount']:.2f}")
        
        # Generate invoice
        invoice_id = await practice_manager.generate_invoice({
            "matter_id": matter_id,
            "client_id": client_id,
            "total_amount": time_summary['total_billable_amount'],
            "due_date": (datetime.now() + timedelta(days=30)).date(),
            "payment_terms": "30 days",
            "notes": "Estate planning package - will and POA preparation",
            "created_by": "L12345"
        })
        
        print(f"🧾 Invoice generated: {invoice_id}")
        print(f"   Amount: ${time_summary['total_billable_amount']:.2f}")
        print(f"   HST (13%): ${time_summary['total_billable_amount'] * 0.13:.2f}")
        print(f"   Total with HST: ${time_summary['total_billable_amount'] * 1.13:.2f}")
        
        # Demo 6: Compliance and Data Retention
        print("\n" + "="*50)
        print("⚖️ DEMO 5: Ontario Legal Compliance")
        print("="*50)
        
        # Data retention policy
        retention_policy = await security_manager.enforce_data_retention_policy(
            "wills", client_id
        )
        
        print(f"📋 Data Retention Policy Applied:")
        print(f"   Document Type: Wills")
        print(f"   Retention Period: {retention_policy['retention_period_years']} years")
        print(f"   Legal Basis: {retention_policy['retention_reason']}")
        print(f"   Destruction Date: {retention_policy['destruction_date'].strftime('%Y-%m-%d')}")
        print(f"   Backup Retention: {retention_policy['backup_retention']} years")
        
        # Get upcoming deadlines
        upcoming_deadlines = await practice_manager.get_upcoming_deadlines("L12345", 30)
        print(f"\n📅 Upcoming Deadlines (next 30 days): {len(upcoming_deadlines)}")
        for deadline in upcoming_deadlines:
            print(f"   • {deadline['due_date']}: {deadline['description']}")
        
        # Demo Summary
        print("\n" + "="*60)
        print("🎉 ONTARIO ENHANCEMENT PACKAGE DEMO COMPLETE")
        print("="*60)
        
        print("\n✅ Features Demonstrated:")
        print("   🔐 Enterprise Security: Document encryption, audit trails")
        print("   👨‍⚖️ Legal Authentication: Lawyer/assistant role management")
        print("   📊 Practice Management: Clients, matters, time tracking")
        print("   💰 Billing System: Time entries, invoicing, HST calculation")
        print("   ⚖️ Ontario Compliance: Data retention, deadline management")
        print("   📋 Audit Trails: Comprehensive logging for regulatory compliance")
        
        print("\n🚀 Ready for Ontario Legal Practice:")
        print("   • LSUC-compliant credential verification framework")
        print("   • 7-year document retention (Ontario Limitations Act)")
        print("   • Professional conduct requirements for staff supervision")
        print("   • Secure document handling with AES-256 encryption")
        print("   • Complete practice management workflow")
        
        print(f"\n📄 Generated Files:")
        print(f"   • Practice Database: {db_path}")
        print(f"   • Encrypted Document: {len(encrypted_package['encrypted_data'])} bytes")
        print(f"   • Audit Trail: {audit_id}")
        print(f"   • Invoice: {invoice_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Clean up temporary files
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    print("🚀 Starting Ontario Legal Enhancement Demo...")
    success = asyncio.run(demo_ontario_features())
    
    if success:
        print("\n🎯 Demo completed successfully!")
        print("📚 See ONTARIO_ENHANCEMENT_INTEGRATION_GUIDE.md for integration details")
        print("🧪 Run 'python test_ontario_enhancements.py' for comprehensive tests")
    else:
        print("\n❌ Demo encountered errors")
    
    sys.exit(0 if success else 1)