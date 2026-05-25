#!/bin/bash
#
# Webshare FastAPI Startup Script
# Usage: ./start.sh [dev|prod]
#

set -e

# Configuration
VENV_DIR="venv"
PYTHON_CMD="python3"
APP_MODULE="app.main:app"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
MODE=${1:-prod}

echo "======================================"
echo "🚀 Webshare FastAPI Server"
echo "======================================"
echo ""

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found${NC}"
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv $VENV_DIR
    echo -e "${GREEN}✓ Virtual environment created${NC}"
    echo ""
fi

# Activate venv
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Check if requirements are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Dependencies not installed${NC}"
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
    echo ""
fi

# Create data folder if not exists
if [ ! -d "data" ]; then
    echo "Creating 'data' folder..."
    mkdir -p data
    echo -e "${GREEN}✓ Data folder created${NC}"
    echo ""
fi

# Run server based on mode
if [ "$MODE" = "dev" ]; then
    echo -e "${YELLOW}🔧 Starting in DEVELOPMENT mode...${NC}"
    echo ""
    uvicorn $APP_MODULE --host 0.0.0.0 --port 8080 --reload
else
    echo -e "${GREEN}🚀 Starting in PRODUCTION mode...${NC}"
    echo ""
    uvicorn $APP_MODULE --host 0.0.0.0 --port 8080 --workers 4 --log-level info
fi
