#!/bin/bash

echo "================================"
echo "Google ADK Chatbot Setup"
echo "================================"
echo ""

# Detect Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Python 3.9+ not found!"
    exit 1
fi

# Check Python
echo "Checking Python..."
$PYTHON_CMD --version || { echo "Python 3 not found!"; exit 1; }

# Create virtual environment
echo "Creating virtual environment..."
$PYTHON_CMD -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "Error: Could not find virtual environment activation script"
    exit 1
fi 

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
echo "3. Use the management script (recommended): ./dualmind.sh start"
echo "   Or activate environment manually:"
echo "   - Linux/macOS: source venv/bin/activate"
echo "   - Windows Git Bash: source venv/Scripts/activate"
echo "4. Open browser: http://localhost:8000"
echo ""
echo "For more options, run: ./dualmind.sh help"
echo ""

