#!/bin/bash

# Startup script for Ontario Legal Document AI Backend

echo "🚀 Starting Ontario Legal Document AI Backend..."

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo "❌ Error: backend/main.py not found. Please run this script from the project root directory."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing Python dependencies..."
cd backend
pip install -r requirements.txt

# Optional: Install additional AI dependencies if user wants them
read -p "🤖 Install full AI dependencies? (y/N): " install_ai
if [[ $install_ai =~ ^[Yy]$ ]]; then
    echo "🧠 Installing AI/ML packages (this may take a while)..."
    pip install sentence-transformers openai langchain faiss-cpu pdfplumber pypdf2
    echo "✅ AI dependencies installed!"
else
    echo "⚠️  Skipping AI dependencies. Backend will run with limited AI features."
fi

echo ""
echo "🎯 Backend setup complete!"
echo ""
echo "To start the backend server:"
echo "  cd backend && python3 main.py"
echo ""
echo "Or run with uvicorn for production:"
echo "  cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo "API Documentation will be available at: http://localhost:8000/api/docs"
echo "Health check: http://localhost:8000/health"
echo ""