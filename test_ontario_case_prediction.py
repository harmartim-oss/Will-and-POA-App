"""
Test Ontario Case Outcome Prediction Integration
Tests the enhanced AI legal service for case outcome prediction based on Ontario precedents
"""

import asyncio
import unittest
from typing import Dict, Any

from backend.services.enhanced_ai_legal_service import EnhancedAILegalService

class TestOntarioCasePrediction(unittest.TestCase):
    """Test suite for Ontario case outcome prediction functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.ai_service = EnhancedAILegalService()
    
    def test_service_initialization(self):
        """Test that the service initializes correctly"""
        self.assertTrue(self.ai_service.is_ready())
        self.assertIsInstance(self.ai_service.case_database, dict)
        self.assertIn("estate_law", self.ai_service.case_database)
        self.assertIn("poa_law", self.ai_service.case_database)
    
    async def test_will_challenge_prediction(self):
        """Test prediction for will challenge cases"""
        case_facts = {
            "facts": [
                "Elderly testator with capacity concerns",
                "Will properly executed with witnesses",
                "Family disputes over inheritance"
            ],
            "parties": [
                {"name": "John Doe", "role": "Testator"},
                {"name": "Jane Doe", "role": "Beneficiary"}
            ],
            "legal_issues": ["testamentary capacity"],
            "estate_value": "500000"
        }
        
        prediction = await self.ai_service.predict_case_outcome(case_facts, "will_challenge")
        
        # Verify response structure
        self.assertIsInstance(prediction, dict)
        self.assertIn("outcome_prediction", prediction)
        self.assertIn("confidence_score", prediction)
        self.assertIn("similar_cases", prediction)
        self.assertIn("settlement_recommendation", prediction)
        self.assertIn("estimated_timeline", prediction)
        
        # Verify outcome prediction structure
        outcome = prediction["outcome_prediction"]
        self.assertIn("predicted_outcome", outcome)
        self.assertIn("probability", outcome)
        self.assertIsInstance(outcome["probability"], (int, float))
        self.assertTrue(0 <= outcome["probability"] <= 1)
    
    async def test_poa_validity_prediction(self):
        """Test prediction for POA validity cases"""
        case_facts = {
            "facts": [
                "POA executed with proper witnesses",
                "Grantor had capacity at time of execution",
                "No evidence of undue influence"
            ],
            "parties": [
                {"name": "Mary Smith", "role": "Grantor"},
                {"name": "Bob Smith", "role": "Attorney"}
            ],
            "legal_issues": ["poa_validity"]
        }
        
        prediction = await self.ai_service.predict_case_outcome(case_facts, "poa_validity")
        
        self.assertIsInstance(prediction, dict)
        self.assertIn("outcome_prediction", prediction)
        self.assertTrue(0 <= prediction["confidence_score"] <= 1)
    
    async def test_key_facts_extraction(self):
        """Test extraction of key facts from case data"""
        case_facts = {
            "facts": ["Fact 1", "Fact 2"],
            "parties": [{"name": "John", "role": "Testator"}],
            "legal_issues": ["capacity"],
            "estate_value": "100000"
        }
        
        key_facts = await self.ai_service._extract_key_facts(case_facts)
        
        self.assertIsInstance(key_facts, list)
        self.assertTrue(len(key_facts) > 0)
        self.assertIn("Fact 1", key_facts)
        self.assertIn("Estate value: $100000", key_facts)
    
    async def test_similar_cases_finding(self):
        """Test finding similar cases functionality"""
        key_facts = ["testamentary capacity", "undue influence", "elderly testator"]
        
        similar_cases = await self.ai_service._find_similar_cases(key_facts, "will_challenge")
        
        self.assertIsInstance(similar_cases, list)
        # Should find some similar cases from the database
        if similar_cases:
            case = similar_cases[0]
            self.assertIn("similarity_score", case)
            self.assertIn("case_name", case)
            self.assertIn("outcome", case)
    
    async def test_outcome_analysis(self):
        """Test case outcome analysis"""
        # Mock similar cases
        similar_cases = [
            {"outcome": "will_upheld", "similarity_score": 0.8},
            {"outcome": "will_invalid", "similarity_score": 0.6},
            {"outcome": "will_upheld", "similarity_score": 0.7}
        ]
        
        analysis = await self.ai_service._analyze_case_outcomes(similar_cases)
        
        self.assertIsInstance(analysis, dict)
        self.assertIn("outcome_distribution", analysis)
        self.assertIn("success_rate", analysis)
        self.assertIn("common_factors", analysis)
        
        # Check that probabilities sum approximately to 1
        distribution = analysis["outcome_distribution"]
        total_prob = sum(distribution.values())
        self.assertAlmostEqual(total_prob, 1.0, places=1)
    
    def test_case_type_classification(self):
        """Test case type classification"""
        self.assertEqual(self.ai_service._classify_case_type("will challenge"), "estate_law")
        self.assertEqual(self.ai_service._classify_case_type("power of attorney"), "poa_law")
        self.assertEqual(self.ai_service._classify_case_type("capacity assessment"), "capacity_law")
        self.assertEqual(self.ai_service._classify_case_type("other"), "general")
    
    def test_case_similarity_calculation(self):
        """Test case similarity calculation"""
        key_facts = ["testamentary capacity", "undue influence"]
        case = {
            "summary": "Case involving testamentary capacity issues",
            "key_factors": ["capacity", "influence", "witness_credibility"]
        }
        
        similarity = self.ai_service._calculate_case_similarity(key_facts, case)
        
        self.assertIsInstance(similarity, (int, float))
        self.assertTrue(similarity >= 0)
    
    async def test_settlement_recommendation(self):
        """Test settlement recommendation generation"""
        # Test high-risk case
        recommendation = self.ai_service._generate_settlement_recommendation(
            "uncertain", 0.4, ["undue influence", "capacity issues"]
        )
        
        self.assertIn("recommendation", recommendation)
        self.assertIn("settlement_range", recommendation)
        self.assertEqual(recommendation["recommendation"], "Consider settlement")
        
        # Test low-risk case
        recommendation = self.ai_service._generate_settlement_recommendation(
            "successful", 0.9, []
        )
        
        self.assertEqual(recommendation["recommendation"], "Proceed with litigation")
    
    async def test_timeline_estimation(self):
        """Test case timeline estimation"""
        key_facts = ["complex estate", "multiple parties"]
        
        timeline = self.ai_service._estimate_case_timeline("litigation", key_facts)
        
        self.assertIn("estimated_months", timeline)
        self.assertIn("phases", timeline)
        self.assertIsInstance(timeline["estimated_months"], int)
        self.assertTrue(timeline["estimated_months"] > 0)
    
    def test_confidence_calculation(self):
        """Test prediction confidence calculation"""
        similar_cases = [
            {"similarity_score": 0.8},
            {"similarity_score": 0.6}
        ]
        outcome_analysis = {
            "outcome_distribution": {"successful": 0.8, "unsuccessful": 0.2}
        }
        
        confidence = self.ai_service._calculate_prediction_confidence(similar_cases, outcome_analysis)
        
        self.assertIsInstance(confidence, (int, float))
        self.assertTrue(0 <= confidence <= 1)
    
    async def test_legal_area_classification(self):
        """Test legal area classification"""
        text = "This case involves a will challenge based on testamentary capacity"
        
        legal_area = await self.ai_service._classify_legal_area(text)
        
        self.assertIsInstance(legal_area, str)
        self.assertIn(legal_area, ["wills_estates", "poa", "general"])
    
    def test_entity_extraction(self):
        """Test legal entity extraction"""
        text = "John Smith v. Mary Johnson, decided on 2023-01-15"
        
        entities = self.ai_service._extract_legal_entities(text)
        
        self.assertIsInstance(entities, list)
        if entities:
            entity = entities[0]
            self.assertIn("text", entity)
            self.assertIn("label", entity)
    
    async def test_statute_retrieval(self):
        """Test relevant statute retrieval"""
        statutes = await self.ai_service._get_relevant_statutes("wills_estates", [])
        
        self.assertIsInstance(statutes, list)
        self.assertIn("Wills Act", statutes)
        self.assertIn("Succession Law Reform Act", statutes)
    
    async def test_error_handling(self):
        """Test error handling in prediction"""
        # Test with empty case facts
        prediction = await self.ai_service.predict_case_outcome({}, None)
        
        # Should still return a valid response structure
        self.assertIsInstance(prediction, dict)
        self.assertIn("outcome_prediction", prediction)

# Async test runner
async def run_async_tests():
    """Run all async tests"""
    test_instance = TestOntarioCasePrediction()
    test_instance.setUp()
    
    async_test_methods = [
        test_instance.test_will_challenge_prediction,
        test_instance.test_poa_validity_prediction,
        test_instance.test_key_facts_extraction,
        test_instance.test_similar_cases_finding,
        test_instance.test_outcome_analysis,
        test_instance.test_settlement_recommendation,
        test_instance.test_timeline_estimation,
        test_instance.test_legal_area_classification,
        test_instance.test_statute_retrieval,
        test_instance.test_error_handling
    ]
    
    print("🧪 Running Ontario Case Prediction Tests...")
    
    for i, test_method in enumerate(async_test_methods, 1):
        try:
            await test_method()
            print(f"✅ Test {i}/{len(async_test_methods)}: {test_method.__name__} - PASSED")
        except Exception as e:
            print(f"❌ Test {i}/{len(async_test_methods)}: {test_method.__name__} - FAILED: {e}")
    
    # Run sync tests
    print("\n🧪 Running Synchronous Tests...")
    sync_tests = [
        test_instance.test_service_initialization,
        test_instance.test_case_type_classification,
        test_instance.test_case_similarity_calculation,
        test_instance.test_confidence_calculation,
        test_instance.test_entity_extraction
    ]
    
    for i, test_method in enumerate(sync_tests, 1):
        try:
            test_method()
            print(f"✅ Sync Test {i}/{len(sync_tests)}: {test_method.__name__} - PASSED")
        except Exception as e:
            print(f"❌ Sync Test {i}/{len(sync_tests)}: {test_method.__name__} - FAILED: {e}")
    
    print("\n🎉 All Ontario Case Prediction Tests Completed!")

if __name__ == "__main__":
    asyncio.run(run_async_tests())