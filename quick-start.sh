#!/bin/bash

# Ontario Wills & Power of Attorney Creator - Quick Start Script
# This script helps you get the application running quickly

echo "🏛️  Ontario Wills & Power of Attorney Creator - Quick Start"
echo "=========================================================="

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Please run this script from the ontario-wills-complete directory"
    exit 1
fi

# Check for required tools
echo "🔍 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    echo "   Please install Python 3.11+ and try again"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed"
    echo "   Please install Node.js 18+ and try again"
    exit 1
fi

# Check for pnpm, install if not available
if ! command -v pnpm &> /dev/null; then
    echo "📦 Installing pnpm..."
    npm install -g pnpm
fi

echo "✅ Prerequisites check complete"

# Ask for OpenAI API key
echo ""
echo "🔑 OpenAI API Configuration"
echo "The application uses OpenAI for AI-powered suggestions."
echo "You can get an API key from: https://platform.openai.com/api-keys"
echo ""
read -p "Enter your OpenAI API key (or press Enter to skip): " OPENAI_KEY

# Setup backend
echo ""
echo "🔧 Setting up backend..."
cd ontario-wills-backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Set environment variables
if [ ! -z "$OPENAI_KEY" ]; then
    export OPENAI_API_KEY="$OPENAI_KEY"
    echo "export OPENAI_API_KEY=\"$OPENAI_KEY\"" >> venv/bin/activate
fi

cd ..

# Setup frontend
echo ""
echo "🎨 Setting up frontend..."
cd ontario-wills-frontend

echo "Installing Node.js dependencies..."
pnpm install

echo "Building frontend for production..."
pnpm run build

# Copy build to backend
echo "Copying frontend build to backend..."
cp -r dist/* ../ontario-wills-backend/src/static/

cd ..

echo ""
echo "🚀 Setup complete!"
echo ""
echo "To start the application:"
echo "1. cd ontario-wills-backend"
echo "2. source venv/bin/activate"
if [ -z "$OPENAI_KEY" ]; then
    echo "3. export OPENAI_API_KEY=\"your-api-key-here\""
    echo "4. python src/main.py"
else
    echo "3. python src/main.py"
fi
echo ""
echo "The application will be available at: http://localhost:5000"
echo ""
echo "📚 For detailed documentation, see:"
echo "   - README.md (setup and usage)"
echo "   - DEPLOYMENT_GUIDE.md (production deployment)"
echo "   - ontario_wills_app_documentation.md (complete documentation)"
echo ""

# Ask if user wants to start the application now
read -p "Would you like to start the application now? (y/n): " START_NOW

if [ "$START_NOW" = "y" ] || [ "$START_NOW" = "Y" ]; then
    echo ""
    echo "🚀 Starting the application..."
    cd ontario-wills-backend
    source venv/bin/activate
    
    if [ -z "$OPENAI_KEY" ]; then
        echo "⚠️  Note: OpenAI API key not set. AI features will not work."
        echo "   Set OPENAI_API_KEY environment variable to enable AI features."
    fi
    
    echo "Starting server at http://localhost:5000"
    echo "Press Ctrl+C to stop the server"
    python src/main.py
else
    echo ""
    echo "✅ Setup complete! Follow the instructions above to start the application."
fi

