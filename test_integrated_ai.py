#!/usr/bin/env python3
"""
Test Suite for Integrated AI Services
Tests the comprehensive AI service integration including NLP, legal research, and document analysis
"""

import asyncio
import sys
import json
import logging
from typing import Dict, Any
from datetime import datetime

# Add backend to path for imports
sys.path.append('backend')

from services.integrated_ai_service import IntegratedAIService, get_integrated_ai_service
from services.nlp_service import get_nlp_service
from services.legal_research_service import LegalResearchService

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IntegratedAITester:
    """Comprehensive test suite for integrated AI services"""
    
    def __init__(self):
        self.ai_service = None
        self.test_results = []
        
    async def setup(self):
        """Initialize the AI service for testing"""
        try:
            self.ai_service = get_integrated_ai_service()
            await self.ai_service.initialize()
            logger.info("✅ AI service initialized successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to initialize AI service: {e}")
            return False
    
    async def test_comprehensive_analysis(self):
        """Test comprehensive document analysis"""
        test_name = "Comprehensive Document Analysis"
        logger.info(f"🧪 Running test: {test_name}")
        
        try:
            # Test data - sample will content
            test_document = """
            Ontario Last Will and Testament
            
            I, John Smith, of 123 Main Street, Toronto, Ontario, being of sound mind and disposing memory, 
            do hereby make, publish and declare this to be my last will and testament.
            
            I appoint my spouse, Mary Smith, as my executor.
            
            I give, devise and bequeath all my real and personal property to my spouse Mary Smith.
            
            In witness whereof I have hereunto set my hand this 15th day of January, 2024.
            
            Signed: John Smith
            """
            
            result = await self.ai_service.analyze_document_comprehensive(
                document_text=test_document,
                document_type="will",
                user_context={
                    "client_name": "John Smith",
                    "document_date": "2024-01-15"
                }
            )
            
            # Validate result structure
            assert hasattr(result, 'nlp_analysis'), "Missing NLP analysis"
            assert hasattr(result, 'legal_research'), "Missing legal research"
            assert hasattr(result, 'ai_suggestions'), "Missing AI suggestions"
            assert hasattr(result, 'compliance_score'), "Missing compliance score"
            assert hasattr(result, 'confidence_score'), "Missing confidence score"
            
            # Validate score ranges
            assert 0 <= result.compliance_score <= 1, "Compliance score out of range"
            assert 0 <= result.confidence_score <= 1, "Confidence score out of range"
            
            logger.info(f"✅ {test_name} passed")
            logger.info(f"   Compliance Score: {result.compliance_score:.2f}")
            logger.info(f"   Confidence Score: {result.confidence_score:.2f}")
            logger.info(f"   Suggestions Count: {len(result.ai_suggestions)}")
            
            self.test_results.append({
                'test': test_name,
                'status': 'PASSED',
                'compliance_score': result.compliance_score,
                'confidence_score': result.confidence_score,
                'suggestions_count': len(result.ai_suggestions)
            })
            
            return True
            
        except Exception as e:
            logger.error(f"❌ {test_name} failed: {e}")
            self.test_results.append({
                'test': test_name,
                'status': 'FAILED',
                'error': str(e)
            })
            return False
    
    async def test_nlp_only_analysis(self):
        """Test NLP-only analysis functionality"""
        test_name = "NLP-Only Analysis"
        logger.info(f"🧪 Running test: {test_name}")
        
        try:
            test_text = "I appoint John Doe as my executor and trustee of this will."
            
            nlp_result = await self.ai_service._analyze_nlp(test_text, "will")
            
            # Validate NLP result structure
            assert isinstance(nlp_result, dict), "NLP result should be a dictionary"
            assert 'entities' in nlp_result, "Missing entities in NLP result"
            assert 'sentiment' in nlp_result, "Missing sentiment in NLP result"
            assert 'readability_score' in nlp_result, "Missing readability score"
            
            logger.info(f"✅ {test_name} passed")
            logger.info(f"   Entities found: {len(nlp_result.get('entities', []))}")
            logger.info(f"   Readability score: {nlp_result.get('readability_score', 0)}")
            
            self.test_results.append({
                'test': test_name,
                'status': 'PASSED',
                'entities_count': len(nlp_result.get('entities', [])),
                'readability_score': nlp_result.get('readability_score', 0)
            })
            
            return True
            
        except Exception as e:
            logger.error(f"❌ {test_name} failed: {e}")
            self.test_results.append({
                'test': test_name,
                'status': 'FAILED',
                'error': str(e)
            })
            return False
    
    async def test_service_status(self):
        """Test service status functionality"""
        test_name = "Service Status Check"
        logger.info(f"🧪 Running test: {test_name}")
        
        try:
            status = self.ai_service.get_service_status()
            
            # Validate status structure
            assert isinstance(status, dict), "Status should be a dictionary"
            assert 'initialized' in status, "Missing initialized status"
            assert 'nlp_service' in status, "Missing NLP service status"
            assert 'research_service' in status, "Missing research service status"
            assert 'ai_service' in status, "Missing AI service status"
            assert 'timestamp' in status, "Missing timestamp"
            
            logger.info(f"✅ {test_name} passed")
            logger.info(f"   Initialized: {status['initialized']}")
            logger.info(f"   All services available: {all([status['nlp_service'], status['research_service'], status['ai_service']])}")
            
            self.test_results.append({
                'test': test_name,
                'status': 'PASSED',
                'initialized': status['initialized'],
                'all_services_available': all([status['nlp_service'], status['research_service'], status['ai_service']])
            })
            
            return True
            
        except Exception as e:
            logger.error(f"❌ {test_name} failed: {e}")
            self.test_results.append({
                'test': test_name,
                'status': 'FAILED',
                'error': str(e)
            })
            return False
    
    async def test_error_handling(self):
        """Test error handling with invalid inputs"""
        test_name = "Error Handling"
        logger.info(f"🧪 Running test: {test_name}")
        
        try:
            # Test with empty document text
            result = await self.ai_service.analyze_document_comprehensive(
                document_text="",
                document_type="will",
                user_context={}
            )
            
            # Should return a result even with empty input (graceful degradation)
            assert result is not None, "Should return result even with empty input"
            assert hasattr(result, 'confidence_score'), "Missing confidence score"
            
            # Test with invalid document type
            result2 = await self.ai_service.analyze_document_comprehensive(
                document_text="Test document",
                document_type="invalid_type",
                user_context={}
            )
            
            assert result2 is not None, "Should handle invalid document type"
            
            logger.info(f"✅ {test_name} passed")
            logger.info("   Error handling works correctly - graceful degradation")
            
            self.test_results.append({
                'test': test_name,
                'status': 'PASSED',
                'graceful_degradation': True
            })
            
            return True
            
        except Exception as e:
            logger.error(f"❌ {test_name} failed: {e}")
            self.test_results.append({
                'test': test_name,
                'status': 'FAILED',
                'error': str(e)
            })
            return False
    
    def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASSED'])
        total_tests = len(self.test_results)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'test_results': self.test_results
        }
        
        return report
    
    async def run_all_tests(self):
        """Run the complete test suite"""
        logger.info("🚀 Starting Integrated AI Service Test Suite")
        logger.info("=" * 60)
        
        # Initialize services
        if not await self.setup():
            logger.error("❌ Test suite failed - could not initialize services")
            return False
        
        # Run all tests
        tests = [
            self.test_comprehensive_analysis,
            self.test_nlp_only_analysis,
            self.test_service_status,
            self.test_error_handling
        ]
        
        for test in tests:
            await test()
            await asyncio.sleep(0.1)  # Small delay between tests
        
        # Generate and display report
        report = self.generate_test_report()
        
        logger.info("=" * 60)
        logger.info("📊 TEST SUITE RESULTS")
        logger.info("=" * 60)
        logger.info(f"Total Tests: {report['total_tests']}")
        logger.info(f"Passed: {report['passed_tests']}")
        logger.info(f"Failed: {report['failed_tests']}")
        logger.info(f"Success Rate: {report['success_rate']:.1f}%")
        
        if report['failed_tests'] > 0:
            logger.info("\n❌ FAILED TESTS:")
            for result in report['test_results']:
                if result['status'] == 'FAILED':
                    logger.info(f"   - {result['test']}: {result.get('error', 'Unknown error')}")
        
        # Save detailed report
        with open('integrated_ai_test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        logger.info(f"\n📄 Detailed report saved to: integrated_ai_test_report.json")
        
        return report['success_rate'] == 100.0

async def main():
    """Main test execution function"""
    tester = IntegratedAITester()
    success = await tester.run_all_tests()
    
    if success:
        logger.info("\n🎉 ALL TESTS PASSED! Integrated AI services are working correctly.")
        return 0
    else:
        logger.error("\n💥 SOME TESTS FAILED! Please check the errors above.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("\n⚠️  Test suite interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n💥 Test suite failed with unexpected error: {e}")
        sys.exit(1)