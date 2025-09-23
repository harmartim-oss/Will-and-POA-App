# Ontario Legal Document AI Backend

This directory contains the comprehensive AI-powered backend infrastructure for the Ontario Legal Document system as specified in the requirements.

## 🚀 Quick Start

From the project root directory, run:

```bash
./start-backend.sh
```

Or manually:

```bash
cd backend
pip install -r requirements.txt
python3 main.py
```

## 🎯 Features Implemented

### ✅ Core AI Engine (`core/ai_engine.py`)
- **Document Intent Analysis**: Classifies legal document types (wills, POA, etc.)
- **Entity Recognition**: Extracts legal entities and roles
- **Requirements Extraction**: Identifies legal requirements based on document type
- **Sentiment Analysis**: Analyzes document tone and language
- **Confidence Scoring**: Provides confidence levels for AI analysis
- **Graceful Degradation**: Works with or without heavy AI libraries

### ✅ Legal Knowledge Base (`core/legal_knowledge.py`)
- **Ontario Legal Templates**: Pre-built templates for wills, POA documents
- **Legal Requirements Database**: Ontario-specific legal requirements
- **Case Law Integration**: Placeholder for Ontario case law database
- **Compliance Validation**: Validates documents against Ontario law

### ✅ NLP Models (`core/nlp_models.py`)
- **Transformer Models**: Support for BERT, GPT-2, and other transformers
- **Sentiment Analysis**: Legal document sentiment analysis
- **Text Summarization**: Document summarization capabilities
- **Question Answering**: Legal Q&A functionality
- **Recommendation Generation**: AI-powered legal recommendations

### ✅ Compliance Checker (`core/compliance_checker.py`)
- **Ontario Law Compliance**: Checks against Ontario legal requirements
- **Age Requirements**: Validates testator/grantor age requirements
- **Witness Requirements**: Ensures proper witnessing procedures
- **Capacity Assessment**: Validates mental capacity declarations
- **Risk Scoring**: Provides compliance scores and recommendations

### ✅ Risk Assessor (`core/risk_assessor.py`)
- **Risk Factor Analysis**: Identifies potential legal risks
- **Mitigation Strategies**: Suggests risk mitigation approaches
- **Risk Scoring**: Quantifies overall document risk levels
- **Category-Based Assessment**: Analyzes capacity, execution, and content risks

### ✅ Case Law Analyzer (`core/case_law_analyzer.py`)
- **Legal Precedent Analysis**: Analyzes relevant Ontario case law
- **Risk Assessment**: Evaluates legal risks based on precedents
- **Recommendation Engine**: Generates recommendations from case law
- **Legal Principle Matching**: Matches issues to applicable legal principles

### ✅ Document Generator (`core/document_generator.py`)
- **Template System**: Manages Ontario legal document templates
- **Structure Analysis**: Analyzes document completeness and structure
- **Insight Generation**: Provides comprehensive document insights
- **Issue Identification**: Identifies potential document problems

## 🛠 API Endpoints

### Health & Status
- `GET /health` - System health check
- `GET /` - Root endpoint with system info

### AI Analysis
- `POST /api/ai/analyze` - Comprehensive AI document analysis
- `POST /api/ai/risk-assessment` - Risk assessment analysis
- `GET /api/ai/legal-knowledge/{query}` - Search legal knowledge base
- `POST /api/ai/generate-recommendations` - Generate AI recommendations

### Document Management
- `POST /api/documents/generate` - Generate legal documents
- `GET /api/documents/templates/{document_type}` - Get document templates
- `GET /api/documents/requirements/{document_type}` - Get legal requirements
- `POST /api/documents/validate` - Validate document content
- `POST /api/documents/upload` - Upload documents for analysis

### Compliance & Legal
- `POST /api/compliance/check` - Check legal compliance
- `GET /api/compliance/requirements/{document_type}` - Get compliance requirements
- `POST /api/compliance/validate-execution` - Validate execution requirements
- `GET /api/compliance/statutory-references/{document_type}` - Get statutory references

### Blockchain (Placeholder)
- `POST /api/blockchain/record` - Record document on blockchain
- `GET /api/blockchain/verify/{transaction_id}` - Verify blockchain record
- `GET /api/blockchain/history/{document_id}` - Get document blockchain history

## 📊 Example API Usage

### Document Analysis
```bash
curl -X POST http://localhost:8000/api/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "document_type": "will",
    "content": "This is my last will and testament...",
    "analysis_type": "full"
  }'
```

### Compliance Check
```bash
curl -X POST http://localhost:8000/api/compliance/check \
  -H "Content-Type: application/json" \
  -d '{
    "document_type": "will",
    "content": "Document content...",
    "user_info": {"age": 35}
  }'
```

## 🧠 AI Model Support

### Current Status
- ✅ **Fallback Mode**: Works without AI libraries (rule-based analysis)
- ⚠️ **Transformer Models**: Available but requires internet connection
- ⚠️ **Sentence Transformers**: Optional for semantic similarity
- ⚠️ **spaCy Models**: Optional for advanced NLP

### Full AI Setup
To enable full AI capabilities:

```bash
pip install sentence-transformers openai langchain faiss-cpu
python -m spacy download en_core_web_sm
```

## 🔧 Configuration

### Environment Variables
```bash
# Optional - for enhanced AI features
OPENAI_API_KEY=your-openai-key
HUGGINGFACE_API_KEY=your-hf-key

# Database (when implemented)
DATABASE_URL=postgresql://user:pass@localhost/db
REDIS_URL=redis://localhost:6379

# Security
JWT_SECRET_KEY=your-secret-key
```

### Production Deployment
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🎯 Ontario Legal Compliance

The system is specifically designed for Ontario, Canada legal requirements:

- **Wills**: Succession Law Reform Act compliance
- **Power of Attorney for Property**: Substitute Decisions Act compliance  
- **Power of Attorney for Personal Care**: Health Care Consent Act compliance
- **Age Requirements**: 18+ for wills/POA property, 16+ for POA personal care
- **Witness Requirements**: Two witnesses for wills, witness/notary for POA
- **Capacity Requirements**: Mental capacity assessments

## 📈 System Architecture

```
backend/
├── main.py                 # FastAPI application entry point
├── core/                   # Core AI and legal components
│   ├── ai_engine.py       # Main AI analysis engine
│   ├── nlp_models.py      # NLP model management
│   ├── legal_knowledge.py # Legal knowledge base
│   ├── case_law_analyzer.py # Case law analysis
│   ├── compliance_checker.py # Legal compliance checking
│   ├── risk_assessor.py   # Risk assessment engine
│   └── document_generator.py # Document generation
├── api/routes/            # API route handlers
│   ├── ai.py             # AI analysis endpoints
│   ├── documents.py      # Document management endpoints
│   ├── compliance.py     # Compliance checking endpoints
│   └── blockchain.py     # Blockchain integration endpoints
├── models/                # Data models and schemas
│   └── schemas.py        # Pydantic request/response models
├── database/              # Database connections and models
│   └── connection.py     # Database connection management
└── requirements.txt       # Python dependencies
```

## 🚦 Status

- ✅ **Core Infrastructure**: Complete and tested
- ✅ **API Endpoints**: All endpoints functional
- ✅ **AI Engine**: Working with graceful degradation
- ✅ **Legal Knowledge**: Ontario-specific templates and requirements
- ✅ **Compliance Checking**: Ontario law compliance validation
- ✅ **Risk Assessment**: Comprehensive risk analysis
- ⚠️ **Database Integration**: Placeholder implementation
- ⚠️ **Full AI Models**: Optional/requires additional setup
- ⚠️ **Blockchain**: Placeholder implementation

## 📚 Documentation

- API Documentation: http://localhost:8000/api/docs (when running)
- Interactive API: http://localhost:8000/api/redoc (when running)
- Health Check: http://localhost:8000/health