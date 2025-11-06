#!/bin/bash

# DualMind AI Chatbot Management Script
# Cross-platform compatible: Linux, macOS, Windows (Git Bash/WSL)
# Usage: ./dualmind.sh [start|stop|restart|status|logs|test|help]

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PORT=8000
PID_FILE="/tmp/dualmind_server.pid"
LOG_FILE="/tmp/dualmind_server.log"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Detect OS and environment
detect_os() {
    case "$(uname -s)" in
        Linux*)     OS="Linux";;
        Darwin*)    OS="macOS";;
        CYGWIN*|MINGW*|MSYS*)    OS="Windows";;
        *)          OS="Unknown";;
    esac
}

# Detect Python command
detect_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}❌ Python not found. Please install Python 3.9+${NC}"
        exit 1
    fi
}

# Get virtual environment activation script path
get_venv_activate() {
    # Check for Unix-style activation (Linux, macOS, Git Bash, WSL)
    if [ -f ".venv/bin/activate" ]; then
        echo ".venv/bin/activate"
    # Check for Windows-style activation (in case running in certain contexts)
    elif [ -f ".venv/Scripts/activate" ]; then
        echo ".venv/Scripts/activate"
    else
        echo ""
    fi
}

# Initialize
detect_os
detect_python

# Banner
print_banner() {
    echo -e "${PURPLE}"
    echo "============================================================"
    echo "           🧠 DualMind AI Chatbot Manager"
    echo "============================================================"
    echo -e "${NC}"
}

# Check if server is running
is_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            return 0
        else
            rm -f "$PID_FILE"
            return 1
        fi
    fi
    
    # Also check by port
    if lsof -ti:$PORT > /dev/null 2>&1; then
        return 0
    fi
    
    return 1
}

# Start the chatbot
start_server() {
    echo -e "${CYAN}Starting DualMind AI Chatbot...${NC}"
    
    if is_running; then
        echo -e "${YELLOW}⚠️  Chatbot is already running!${NC}"
        echo -e "   Use ${GREEN}./dualmind.sh status${NC} to check"
        return 1
    fi
    
    cd "$SCRIPT_DIR"
    
    # Check if virtual environment exists
    if [ ! -d ".venv" ]; then
        echo -e "${YELLOW}⚠️  Virtual environment not found. Creating...${NC}"
        $PYTHON_CMD -m venv .venv
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Failed to create virtual environment.${NC}"
            echo -e "${YELLOW}   Try: $PYTHON_CMD -m pip install --upgrade pip${NC}"
            return 1
        fi
    fi
    
    # Get virtual environment activation script
    VENV_ACTIVATE=$(get_venv_activate)
    if [ -z "$VENV_ACTIVATE" ]; then
        echo -e "${RED}❌ Virtual environment activation script not found.${NC}"
        return 1
    fi
    
    # Activate virtual environment
    source "$VENV_ACTIVATE"
    
    # Verify Python is from virtual environment
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to activate virtual environment.${NC}"
        return 1
    fi
    
    # Check if requirements file exists
    REQUIREMENTS_FILE="$SCRIPT_DIR/doc/requirements.txt"
    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"
    fi
    
    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        echo -e "${RED}❌ requirements.txt not found.${NC}"
        deactivate
        return 1
    fi
    
    # Check if requirements are installed
    if ! $PYTHON_CMD -c "import fastapi" 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Dependencies not installed. Installing...${NC}"
        pip install -r "$REQUIREMENTS_FILE"
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Failed to install dependencies.${NC}"
            deactivate
            return 1
        fi
    fi
    
    # Start the server in background
    nohup $PYTHON_CMD src/server.py > "$LOG_FILE" 2>&1 &
    SERVER_PID=$!
    echo $SERVER_PID > "$PID_FILE"
    
    # Deactivate virtual environment (server continues running)
    deactivate
    
    # Wait a moment and check if it started successfully
    sleep 3
    
    if is_running; then
        echo -e "${GREEN}✅ DualMind AI Chatbot started successfully!${NC}"
        echo ""
        echo -e "${BLUE}📍 Access Points:${NC}"
        echo -e "   ${CYAN}Main Page:${NC}    http://localhost:$PORT"
        echo -e "   ${CYAN}Cloud Mode:${NC}   http://localhost:$PORT/"
        echo -e "   ${CYAN}Local Mode:${NC}   http://localhost:$PORT/local"
        echo -e "   ${CYAN}Health Check:${NC} http://localhost:$PORT/health"
        echo ""
        echo -e "${BLUE}📝 Logs:${NC} $LOG_FILE"
        echo -e "${BLUE}🔧 PID:${NC}  $(cat $PID_FILE)"
        echo ""
        echo -e "${GREEN}🚀 Open http://localhost:$PORT in your browser!${NC}"
    else
        echo -e "${RED}❌ Failed to start server. Check logs: $LOG_FILE${NC}"
        rm -f "$PID_FILE"
        return 1
    fi
}

# Stop the chatbot
stop_server() {
    echo -e "${CYAN}Stopping DualMind AI Chatbot...${NC}"
    
    if ! is_running; then
        echo -e "${YELLOW}⚠️  Chatbot is not running.${NC}"
        return 0
    fi
    
    # Kill by PID file
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        echo -e "   Stopping process $PID..."
        kill -15 $PID 2>/dev/null
        sleep 2
        
        # Force kill if still running
        if ps -p $PID > /dev/null 2>&1; then
            echo -e "   Force stopping..."
            kill -9 $PID 2>/dev/null
        fi
        
        rm -f "$PID_FILE"
    fi
    
    # Also kill any process on the port
    PORT_PID=$(lsof -ti:$PORT)
    if [ ! -z "$PORT_PID" ]; then
        echo -e "   Freeing port $PORT..."
        kill -9 $PORT_PID 2>/dev/null
    fi
    
    # Kill any remaining server processes
    pkill -9 -f "python3 server.py" 2>/dev/null
    
    sleep 1
    
    if ! is_running; then
        echo -e "${GREEN}✅ DualMind AI Chatbot stopped successfully!${NC}"
    else
        echo -e "${RED}❌ Failed to stop server completely.${NC}"
        return 1
    fi
}

# Restart the chatbot
restart_server() {
    echo -e "${CYAN}Restarting DualMind AI Chatbot...${NC}"
    stop_server
    sleep 2
    start_server
}

# Show server status
show_status() {
    print_banner
    
    if is_running; then
        echo -e "${GREEN}✅ Status: RUNNING${NC}"
        echo ""
        
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            echo -e "${BLUE}Process ID:${NC} $PID"
        fi
        
        echo -e "${BLUE}Port:${NC}       $PORT"
        
        # Check if responding
        if curl -s http://localhost:$PORT/health > /dev/null 2>&1; then
            echo -e "${BLUE}Health:${NC}     ${GREEN}Healthy ✓${NC}"
            
            # Get version info
            VERSION=$(curl -s http://localhost:$PORT/health | $PYTHON_CMD -c "import sys, json; print(json.load(sys.stdin).get('version', 'unknown'))" 2>/dev/null)
            if [ ! -z "$VERSION" ]; then
                echo -e "${BLUE}Version:${NC}    $VERSION"
            fi
        else
            echo -e "${BLUE}Health:${NC}     ${YELLOW}Starting...${NC}"
        fi
        
        echo ""
        echo -e "${BLUE}📍 URLs:${NC}"
        echo -e "   Main:   http://localhost:$PORT"
        echo -e "   Local:  http://localhost:$PORT/local"
        echo -e "   Health: http://localhost:$PORT/health"
        
        if [ -f "$LOG_FILE" ]; then
            echo ""
            echo -e "${BLUE}📝 Logs:${NC} $LOG_FILE"
            echo -e "${BLUE}   Last 5 lines:${NC}"
            tail -5 "$LOG_FILE" | while read line; do
                echo -e "   ${CYAN}│${NC} $line"
            done
        fi
        
    else
        echo -e "${RED}❌ Status: STOPPED${NC}"
        echo ""
        echo -e "To start: ${GREEN}./dualmind.sh start${NC}"
    fi
    
    echo ""
    echo "============================================================"
}

# Show logs
show_logs() {
    if [ ! -f "$LOG_FILE" ]; then
        echo -e "${YELLOW}⚠️  No logs found.${NC}"
        return 1
    fi
    
    echo -e "${CYAN}📝 Showing logs (press Ctrl+C to exit):${NC}"
    echo "============================================================"
    tail -f "$LOG_FILE"
}

# Run all tests
run_tests() {
    print_banner
    echo -e "${CYAN}🧪 Running DualMind Test Suite...${NC}"
    echo ""
    
    # Check if test runner exists
    TEST_RUNNER="$SCRIPT_DIR/tests/run_all_tests.py"
    if [ ! -f "$TEST_RUNNER" ]; then
        echo -e "${RED}❌ Test runner not found: $TEST_RUNNER${NC}"
        return 1
    fi
    
    # Run the tests
    $PYTHON_CMD "$TEST_RUNNER"
    TEST_EXIT_CODE=$?
    
    echo ""
    if [ $TEST_EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✅ All tests completed successfully!${NC}"
    else
        echo -e "${RED}❌ Some tests failed. Review output above.${NC}"
    fi
    
    return $TEST_EXIT_CODE
}

# Show help
show_help() {
    print_banner
    echo -e "${BLUE}Platform:${NC} $OS"
    echo -e "${BLUE}Python:${NC}   $PYTHON_CMD"
    echo ""
    echo -e "${BLUE}Usage:${NC}"
    echo -e "  ./dualmind.sh [command]"
    echo ""
    echo -e "${BLUE}Commands:${NC}"
    echo -e "  ${GREEN}start${NC}      Start the chatbot server"
    echo -e "  ${GREEN}stop${NC}       Stop the chatbot server"
    echo -e "  ${GREEN}restart${NC}    Restart the chatbot server"
    echo -e "  ${GREEN}status${NC}     Show server status and info"
    echo -e "  ${GREEN}logs${NC}       Show server logs (live tail)"
    echo -e "  ${GREEN}test${NC}       Run all automated tests"
    echo -e "  ${GREEN}help${NC}       Show this help message"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo -e "  ./dualmind.sh start     ${CYAN}# Start the server${NC}"
    echo -e "  ./dualmind.sh status    ${CYAN}# Check if running${NC}"
    echo -e "  ./dualmind.sh restart   ${CYAN}# Restart the server${NC}"
    echo -e "  ./dualmind.sh logs      ${CYAN}# Watch logs in real-time${NC}"
    echo -e "  ./dualmind.sh test      ${CYAN}# Run all tests${NC}"
    echo ""
    echo -e "${BLUE}Platform Support:${NC}"
    echo -e "  ${GREEN}✓${NC} Linux (native bash)"
    echo -e "  ${GREEN}✓${NC} macOS (native bash)"
    echo -e "  ${GREEN}✓${NC} Windows (Git Bash or WSL)"
    echo ""
    echo -e "${BLUE}Quick Access:${NC}"
    echo -e "  After starting, open: ${CYAN}http://localhost:$PORT${NC}"
    echo ""
    echo -e "${BLUE}Customization:${NC}"
    echo -e "  Edit ${GREEN}src/branding_config.py${NC} to customize names, colors, and text"
    echo ""
    echo "============================================================"
}

# Main script logic
main() {
    case "$1" in
        start)
            print_banner
            start_server
            ;;
        stop)
            print_banner
            stop_server
            ;;
        restart)
            print_banner
            restart_server
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs
            ;;
        test)
            run_tests
            ;;
        help|--help|-h)
            show_help
            ;;
        "")
            show_help
            ;;
        *)
            echo -e "${RED}❌ Unknown command: $1${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"

