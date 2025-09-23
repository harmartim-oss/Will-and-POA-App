"""
Enhanced AI Integration Service
Demonstrates how to integrate Enhanced Legal AI with existing services
"""

import logging
from typing import Dict, List, Any, Optional
from .enhanced_legal_ai import EnhancedLegalAI
from .enhanced_ai_legal_service import EnhancedAILegalService

logger = logging.getLogger(__name__)

class EnhancedAIIntegrationService:
    """
    Service that combines Enhanced Legal AI with existing AI legal services
    """
    
    def __init__(self):
        self.enhanced_ai = EnhancedLegalAI()
        self.legacy_ai_service = EnhancedAILegalService()
        self.is_initialized = False
    
    async def initialize(self):
        """Initialize both AI systems"""
        try:
            logger.info("Initializing Enhanced AI Integration Service...")
            
            # Initialize enhanced AI
            await self.enhanced_ai.initialize()
            
            # Legacy service is already initialized in __init__
            
            self.is_initialized = True
            logger.info("Enhanced AI Integration Service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize integration service: {str(e)}")
            raise
    
    async def comprehensive_document_analysis(self, document_type: str, document_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive document analysis using both AI systems
        """
        try:
            logger.info(f"Performing comprehensive analysis for {document_type}")
            
            # Get legacy analysis
            legacy_analysis = await self.legacy_ai_service.analyze_document(document_type, document_content)
            
            # Get enhanced risk analysis
            enhanced_risk = await self.enhanced_ai.analyze_legal_risk(
                document_content=str(document_content),
                document_type=document_type,
                client_situation=document_content.get("client_situation", {})
            )
            
            # Combine results
            combined_analysis = {
                "document_type": document_type,
                "legacy_analysis": {
                    "compliance_score": legacy_analysis.compliance_score,
                    "legal_issues": legacy_analysis.legal_issues,
                    "recommendations": legacy_analysis.recommendations,
                    "risk_assessment": legacy_analysis.risk_assessment
                },
                "enhanced_analysis": {
                    "risk_level": enhanced_risk["overall_risk_level"],
                    "risk_factors": enhanced_risk["risk_factors"],
                    "mitigation_strategies": enhanced_risk["mitigation_strategies"],
                    "monitoring_recommendations": enhanced_risk["monitoring_recommendations"]
                },
                "combined_recommendations": self._merge_recommendations(
                    legacy_analysis.recommendations,
                    enhanced_risk["mitigation_strategies"]
                )
            }
            
            return combined_analysis
            
        except Exception as e:
            logger.error(f"Comprehensive analysis failed: {str(e)}")
            raise
    
    async def enhanced_case_research_and_prediction(self, query: str, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Combine legal research with case outcome prediction
        """
        try:
            logger.info(f"Performing enhanced research and prediction for: {query}")
            
            # Perform legal research
            research_result = await self.enhanced_ai.perform_legal_research(
                query=query,
                jurisdiction="Ontario",
                max_results=10
            )
            
            # Predict case outcome
            prediction_result = await self.enhanced_ai.predict_case_outcome(case_data)
            
            # Generate legal argument based on research
            argument_result = await self.enhanced_ai.generate_legal_argument(
                topic=query,
                position=f"Based on research, the likely outcome is {prediction_result.predicted_outcome}",
                supporting_facts=case_data.get("facts", "").split(". ") if case_data.get("facts") else []
            )
            
            return {
                "research": {
                    "query": research_result.query,
                    "relevant_cases": research_result.relevant_cases,
                    "statutes": research_result.statutes,
                    "confidence": research_result.confidence
                },
                "prediction": {
                    "predicted_outcome": prediction_result.predicted_outcome,
                    "probability": prediction_result.probability,
                    "confidence_level": prediction_result.confidence_level,
                    "similar_cases": prediction_result.similar_cases
                },
                "legal_argument": {
                    "argument": argument_result["argument"],
                    "strength_score": argument_result["strength_score"],
                    "supporting_authorities": argument_result["supporting_authorities"]
                },
                "combined_confidence": self._calculate_combined_confidence(
                    research_result.confidence,
                    prediction_result.confidence_level,
                    argument_result["strength_score"]
                )
            }
            
        except Exception as e:
            logger.error(f"Enhanced research and prediction failed: {str(e)}")
            raise
    
    async def strategic_case_planning(self, case_facts: Dict[str, Any], legal_issues: List[str], 
                                   desired_outcome: str) -> Dict[str, Any]:
        """
        Comprehensive case planning with strategy and risk assessment
        """
        try:
            logger.info("Performing strategic case planning")
            
            # Get case strategy
            strategy_result = await self.enhanced_ai.suggest_case_strategy(
                case_facts=case_facts,
                legal_issues=legal_issues,
                desired_outcome=desired_outcome
            )
            
            # Predict case outcome
            prediction_result = await self.enhanced_ai.predict_case_outcome(case_facts)
            
            # Analyze risks
            risk_result = await self.enhanced_ai.analyze_legal_risk(
                document_content=str(case_facts),
                document_type="case_file",
                client_situation=case_facts.get("client_situation", {})
            )
            
            return {
                "strategic_plan": {
                    "recommended_strategy": strategy_result["recommended_strategy"],
                    "alternative_strategies": strategy_result["alternative_strategies"],
                    "implementation_timeline": strategy_result["implementation_timeline"],
                    "key_milestones": strategy_result["key_milestones"]
                },
                "outcome_analysis": {
                    "predicted_outcome": prediction_result.predicted_outcome,
                    "success_probability": prediction_result.success_probability,
                    "confidence_level": prediction_result.confidence_level
                },
                "risk_assessment": {
                    "overall_risk_level": risk_result["overall_risk_level"],
                    "mitigation_strategies": risk_result["mitigation_strategies"]
                },
                "overall_recommendation": self._generate_overall_recommendation(
                    strategy_result, prediction_result, risk_result
                )
            }
            
        except Exception as e:
            logger.error(f"Strategic case planning failed: {str(e)}")
            raise
    
    def _merge_recommendations(self, legacy_recommendations: List[str], 
                             enhanced_strategies: List[str]) -> List[str]:
        """Merge recommendations from both systems"""
        combined = list(legacy_recommendations)
        
        # Add enhanced strategies that aren't duplicated
        for strategy in enhanced_strategies:
            if not any(strategy.lower() in rec.lower() for rec in combined):
                combined.append(strategy)
        
        return combined[:10]  # Limit to top 10 recommendations
    
    def _calculate_combined_confidence(self, research_confidence: float, 
                                     prediction_confidence: str, argument_strength: float) -> Dict[str, Any]:
        """Calculate combined confidence score"""
        # Convert prediction confidence to numeric
        confidence_map = {"low": 0.3, "medium": 0.6, "high": 0.9}
        prediction_numeric = confidence_map.get(prediction_confidence, 0.5)
        
        # Calculate weighted average
        combined_score = (research_confidence * 0.4 + prediction_numeric * 0.4 + argument_strength * 0.2)
        
        # Determine overall confidence level
        if combined_score >= 0.8:
            level = "high"
        elif combined_score >= 0.6:
            level = "medium"
        else:
            level = "low"
        
        return {
            "score": combined_score,
            "level": level,
            "components": {
                "research": research_confidence,
                "prediction": prediction_numeric,
                "argument": argument_strength
            }
        }
    
    def _generate_overall_recommendation(self, strategy_result: Dict, 
                                       prediction_result: Any, risk_result: Dict) -> str:
        """Generate overall case recommendation"""
        strategy_name = strategy_result["recommended_strategy"]["strategy"]
        success_prob = strategy_result["success_probability"]
        risk_level = risk_result["overall_risk_level"]
        
        if risk_level == "HIGH" and success_prob < 0.6:
            return f"CAUTION: Recommended strategy is {strategy_name}, but high risk and moderate success probability suggest careful consideration of alternatives."
        elif risk_level == "LOW" and success_prob > 0.8:
            return f"STRONG RECOMMENDATION: Proceed with {strategy_name} strategy. Low risk and high success probability indicate favorable prospects."
        else:
            return f"MODERATE RECOMMENDATION: {strategy_name} strategy appears viable with {success_prob:.0%} success probability and {risk_level.lower()} risk level."
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status of integrated AI systems"""
        return {
            "integration_service": self.is_initialized,
            "enhanced_ai": self.enhanced_ai.is_initialized,
            "legacy_ai_service": True,  # Always available
            "available_features": [
                "comprehensive_document_analysis",
                "enhanced_case_research_and_prediction", 
                "strategic_case_planning"
            ]
        }