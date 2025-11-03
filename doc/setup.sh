#!/bin/bash

echo "================================"
echo "Google ADK Chatbot Setup"
echo "================================"
echo ""

# Check Python
echo "Checking Python..."
python3 --version || { echo "Python 3 not found!"; exit 1; }

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activatept 

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r doc/requirements.txt

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Get your Google API key: https://makersuite.google.com/app/apikey"
echo "2. Edit .env and add your API key"
echo "3. Activate environment: source venv/bin/activate"
echo "4. Run server: python src/server.py  (or use: ./dualmind.sh start)"
echo "5. Open browser: http://localhost:8000"
echo ""

