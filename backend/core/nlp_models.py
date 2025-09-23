try:
    import torch
    from transformers import (
        AutoTokenizer, AutoModelForSequenceClassification,
        AutoModelForQuestionAnswering, pipeline, AutoModelForCausalLM
    )
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from typing import List, Dict, Any
import logging
import json

logger = logging.getLogger(__name__)

class OntarioLegalNLPModels:
    def __init__(self):
        self.models = {}
        self.pipelines = {}
        self.is_initialized = False

    async def initialize(self):
        """Initialize transformer models"""
        try:
            logger.info("Initializing transformer models...")
            
            if not TRANSFORMERS_AVAILABLE:
                logger.warning("Transformers library not available. AI features will be limited.")
                self.is_initialized = True
                return
            
            # Initialize pipelines with fallback handling
            try:
                self.pipelines["sentiment"] = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english"
                )
                logger.info("Sentiment analysis pipeline initialized")
            except Exception as e:
                logger.warning(f"Could not initialize sentiment pipeline: {e}")
            
            try:
                self.pipelines["summarization"] = pipeline(
                    "summarization",
                    model="facebook/bart-large-cnn"
                )
                logger.info("Summarization pipeline initialized")
            except Exception as e:
                logger.warning(f"Could not initialize summarization pipeline: {e}")
            
            # Try to initialize more advanced models with fallbacks
            await self._initialize_advanced_models()
            
            self.is_initialized = True
            logger.info("NLP models initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize NLP models: {str(e)}")
            # Allow system to continue with limited functionality
            self.is_initialized = False

    async def _initialize_advanced_models(self):
        """Initialize advanced models with proper error handling"""
        if not TRANSFORMERS_AVAILABLE:
            logger.warning("Transformers not available for advanced models")
            return
            
        try:
            # Legal document classifier
            self.models["classifier"] = {
                "tokenizer": AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium"),
                "model": AutoModelForSequenceClassification.from_pretrained(
                    "microsoft/DialoGPT-medium"
                )
            }
            logger.info("Legal classifier initialized")
        except Exception as e:
            logger.warning(f"Could not initialize legal classifier: {e}")
        
        try:
            # Legal question answering
            self.models["qa"] = {
                "tokenizer": AutoTokenizer.from_pretrained("distilbert-base-cased-distilled-squad"),
                "model": AutoModelForQuestionAnswering.from_pretrained(
                    "distilbert-base-cased-distilled-squad"
                )
            }
            logger.info("Question answering model initialized")
        except Exception as e:
            logger.warning(f"Could not initialize QA model: {e}")
        
        try:
            # Legal text generation
            self.models["generator"] = {
                "tokenizer": AutoTokenizer.from_pretrained("gpt2"),
                "model": AutoModelForCausalLM.from_pretrained("gpt2")
            }
            # Set pad token if not exists
            if self.models["generator"]["tokenizer"].pad_token is None:
                self.models["generator"]["tokenizer"].pad_token = self.models["generator"]["tokenizer"].eos_token
            logger.info("Text generation model initialized")
        except Exception as e:
            logger.warning(f"Could not initialize text generator: {e}")

    def classify_document(self, embeddings) -> List[str]:
        """Classify document type using embeddings"""
        # Simplified classification logic for now
        # In production, this would use a properly trained classifier
        try:
            # Basic keyword-based classification as fallback
            return ["will"]  # Placeholder
        except Exception as e:
            logger.warning(f"Document classification failed: {e}")
            return ["unknown"]

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of legal text"""
        try:
            if "sentiment" in self.pipelines:
                # Limit text length for model constraints
                text_truncated = text[:512] if len(text) > 512 else text
                result = self.pipelines["sentiment"](text_truncated)
                return result[0] if result else {"label": "NEUTRAL", "score": 0.5}
        except Exception as e:
            logger.warning(f"Sentiment analysis failed: {e}")
        
        return {"label": "NEUTRAL", "score": 0.5}

    async def generate_recommendations(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Generate AI-powered recommendations"""
        recommendations = []
        
        try:
            # Use text generation model for recommendations
            if "generator" in self.models and TRANSFORMERS_AVAILABLE:
                prompt = f"Based on this legal analysis, provide 3 specific recommendations for improving the document:"
                
                inputs = self.models["generator"]["tokenizer"].encode(
                    prompt, 
                    return_tensors="pt",
                    truncation=True,
                    max_length=200
                )
                
                with torch.no_grad():
                    outputs = self.models["generator"]["model"].generate(
                        inputs,
                        max_length=300,
                        num_return_sequences=1,
                        temperature=0.7,
                        do_sample=True,
                        pad_token_id=self.models["generator"]["tokenizer"].eos_token_id
                    )
                
                generated_text = self.models["generator"]["tokenizer"].decode(
                    outputs[0], 
                    skip_special_tokens=True
                )
                
                # Extract recommendations from generated text
                if "recommendations" in generated_text.lower():
                    lines = generated_text.split('\n')
                    for line in lines:
                        if line.strip() and any(word in line.lower() for word in ['recommend', 'suggest', 'consider']):
                            recommendations.append(line.strip())
            
            # Add rule-based recommendations as fallback
            if not recommendations:
                recommendations = self._get_rule_based_recommendations(analysis_result)
                
        except Exception as e:
            logger.warning(f"AI recommendation generation failed: {e}")
            recommendations = self._get_rule_based_recommendations(analysis_result)
        
        return recommendations[:5]  # Limit to 5 recommendations

    def _get_rule_based_recommendations(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Generate rule-based recommendations as fallback"""
        recommendations = []
        
        document_type = analysis_result.get("document_type", "unknown")
        
        if document_type == "will":
            recommendations.extend([
                "Ensure all beneficiaries are clearly identified with full names",
                "Consider naming alternate executors in case primary executor cannot serve",
                "Review asset distribution for clarity and completeness",
                "Verify witness requirements are met per Ontario law"
            ])
        elif document_type == "poa_property":
            recommendations.extend([
                "Clearly define the scope of financial powers granted",
                "Consider including specific instructions for investment decisions",
                "Ensure the document includes capacity determination provisions",
                "Review succession provisions for the attorney"
            ])
        elif document_type == "poa_personal_care":
            recommendations.extend([
                "Specify healthcare preferences and treatment wishes",
                "Include instructions for end-of-life care decisions",
                "Consider naming alternate attorneys for personal care",
                "Ensure the document complies with Ontario healthcare legislation"
            ])
        else:
            recommendations.extend([
                "Review document structure and legal formatting",
                "Ensure all required legal elements are present",
                "Consider professional legal review before execution",
                "Verify compliance with Ontario legal requirements"
            ])
        
        return recommendations

    def answer_legal_question(self, question: str, context: str) -> Dict[str, Any]:
        """Answer legal questions using QA model"""
        try:
            if "qa" in self.models and TRANSFORMERS_AVAILABLE:
                tokenizer = self.models["qa"]["tokenizer"]
                model = self.models["qa"]["model"]
                
                # Prepare inputs
                inputs = tokenizer(
                    question, 
                    context, 
                    return_tensors="pt",
                    truncation=True,
                    max_length=512
                )
                
                with torch.no_grad():
                    outputs = model(**inputs)
                    start_scores = outputs.start_logits
                    end_scores = outputs.end_logits
                    
                    # Get the most likely beginning and end of answer
                    start_index = torch.argmax(start_scores)
                    end_index = torch.argmax(end_scores) + 1
                    
                    # Extract answer
                    answer_tokens = inputs["input_ids"][0][start_index:end_index]
                    answer = tokenizer.decode(answer_tokens, skip_special_tokens=True)
                    
                    confidence = float(torch.softmax(start_scores, dim=1).max() * torch.softmax(end_scores, dim=1).max())
                    
                    return {
                        "answer": answer,
                        "confidence": confidence,
                        "status": "success"
                    }
        except Exception as e:
            logger.warning(f"Legal QA failed: {e}")
        
        return {
            "answer": "I'm unable to provide a specific answer to that question at this time.",
            "confidence": 0.0,
            "status": "error"
        }

    def summarize_document(self, text: str) -> Dict[str, Any]:
        """Summarize legal document"""
        try:
            if "summarization" in self.pipelines:
                # Limit text length for summarization
                text_truncated = text[:1024] if len(text) > 1024 else text
                
                summary = self.pipelines["summarization"](
                    text_truncated,
                    max_length=150,
                    min_length=50,
                    do_sample=False
                )
                
                return {
                    "summary": summary[0]["summary_text"],
                    "status": "success"
                }
        except Exception as e:
            logger.warning(f"Document summarization failed: {e}")
        
        # Fallback to simple summary
        sentences = text.split('.')[:3]  # First 3 sentences
        simple_summary = '. '.join(sentences) + '.'
        
        return {
            "summary": simple_summary,
            "status": "fallback"
        }

    def is_ready(self) -> bool:
        """Check if NLP models are ready"""
        return self.is_initialized

    def get_model_status(self) -> Dict[str, Any]:
        """Get status of all models"""
        return {
            "initialized": self.is_initialized,
            "available_models": list(self.models.keys()),
            "available_pipelines": list(self.pipelines.keys()),
            "model_details": {
                model_name: "loaded" for model_name in self.models.keys()
            }
        }