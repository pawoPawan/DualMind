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

# Detect Python command and verify version
detect_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}❌ Python not found. Please install Python 3.9+${NC}"
        exit 1
    fi
    
    # Verify Python version (3.9+)
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
        echo -e "${RED}❌ Python 3.9+ required. Found: $PYTHON_VERSION${NC}"
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

# Check if a port is in use (cross-platform)
check_port() {
    local port=$1
    if command -v lsof &> /dev/null; then
        # Unix/macOS/Git Bash with lsof
        lsof -ti:$port > /dev/null 2>&1
        return $?
    elif command -v netstat &> /dev/null; then
        # Windows/Git Bash with netstat
        netstat -an | grep ":$port " | grep -i "LISTEN" > /dev/null 2>&1
        return $?
    elif command -v ss &> /dev/null; then
        # Modern Linux with ss
        ss -ln | grep ":$port " > /dev/null 2>&1
        return $?
    else
        # Fallback: try to bind to port (less reliable)
        $PYTHON_CMD -c "import socket; s=socket.socket(); s.bind(('', $port)); s.close()" 2>/dev/null
        return $((1-$?))
    fi
}

# Get PID of process using port (cross-platform)
get_port_pid() {
    local port=$1
    if command -v lsof &> /dev/null; then
        lsof -ti:$port 2>/dev/null
    elif command -v netstat &> /dev/null; then
        # Windows-style netstat
        netstat -ano | grep ":$port " | grep "LISTENING" | awk '{print $5}' | head -1
    fi
}

# Check for optional dependencies
check_optional_deps() {
    MISSING_DEPS=()
    
    # Check for curl (for health checks)
    if ! command -v curl &> /dev/null; then
        MISSING_DEPS+=("curl (for health checks)")
    fi
    
    # Warn about pandoc (for pypandoc in requirements)
    if ! command -v pandoc &> /dev/null; then
        MISSING_DEPS+=("pandoc (for document conversion)")
    fi
    
    # Export for use in other functions
    export MISSING_DEPS
}

# Initialize
detect_os
detect_python
check_optional_deps

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
    
    # Also check by port (cross-platform)
    if check_port $PORT; then
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
            echo -e "${YELLOW}   Possible fixes:${NC}"
            echo -e "${YELLOW}   1. Install python3-venv: apt-get install python3-venv${NC}"
            echo -e "${YELLOW}   2. Upgrade pip: $PYTHON_CMD -m pip install --upgrade pip${NC}"
            echo -e "${YELLOW}   3. Install virtualenv: $PYTHON_CMD -m pip install virtualenv${NC}"
            return 1
        fi
        echo -e "${GREEN}✓ Virtual environment created${NC}"
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
    
    # Upgrade pip to latest version (prevents many installation issues)
    echo -e "${CYAN}Checking pip version...${NC}"
    pip install --upgrade pip --quiet 2>&1 | grep -v "Requirement already satisfied" || true
    
    # Check if requirements file exists
    REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"
    
    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        echo -e "${RED}❌ requirements.txt not found.${NC}"
        deactivate
        return 1
    fi
    
    # Warn about optional missing dependencies
    if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
        echo -e "${YELLOW}⚠️  Optional dependencies missing (features may be limited):${NC}"
        for dep in "${MISSING_DEPS[@]}"; do
            echo -e "   ${YELLOW}• $dep${NC}"
        done
        echo -e "${CYAN}   Install them for full functionality, but server will work without them.${NC}"
    fi
    
    # Check if requirements are installed
    if ! $PYTHON_CMD -c "import fastapi" 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Dependencies not installed. Installing...${NC}"
        echo -e "${CYAN}   This may take a few minutes on first run...${NC}"
        pip install -r "$REQUIREMENTS_FILE"
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Failed to install dependencies.${NC}"
            echo -e "${YELLOW}   Try manually: pip install -r $REQUIREMENTS_FILE${NC}"
            deactivate
            return 1
        fi
        echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
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
    
    # Also kill any process on the port (cross-platform)
    PORT_PID=$(get_port_pid $PORT)
    if [ ! -z "$PORT_PID" ]; then
        echo -e "   Freeing port $PORT..."
        kill -9 $PORT_PID 2>/dev/null
    fi
    
    # Kill any remaining server processes (cross-platform)
    if command -v pkill &> /dev/null; then
        pkill -9 -f "server.py" 2>/dev/null
    else
        # Fallback for systems without pkill (like some Windows setups)
        ps aux 2>/dev/null | grep "server.py" | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null || true
    fi
    
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
    echo -e "${BLUE}Environment:${NC}"
    echo -e "  Platform:  $OS"
    echo -e "  Python:    $PYTHON_CMD ($PYTHON_VERSION)"
    
    # Show warnings if any
    if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
        echo -e "  ${YELLOW}Optional:  Missing${NC}"
        for dep in "${MISSING_DEPS[@]}"; do
            echo -e "             ${YELLOW}• $dep${NC}"
        done
    else
        echo -e "  ${GREEN}Optional:  All dependencies available${NC}"
    fi
    
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

