# DualMind AI Chatbot Management Script for Windows
# Usage: .\dualmind.ps1 [start|stop|restart|status|logs|test|help]

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

# Configuration
$PORT = 8000
$PID_FILE = "$env:TEMP\dualmind_server.pid"
$LOG_FILE = "$env:TEMP\dualmind_server.log"
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

# Colors for output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Banner
function Print-Banner {
    Write-ColorOutput "============================================================" "Magenta"
    Write-ColorOutput "           🧠 DualMind AI Chatbot Manager" "Magenta"
    Write-ColorOutput "============================================================" "Magenta"
}

# Check if server is running
function Test-ServerRunning {
    # Check by PID file
    if (Test-Path $PID_FILE) {
        $PID = Get-Content $PID_FILE
        $process = Get-Process -Id $PID -ErrorAction SilentlyContinue
        if ($process) {
            return $true
        } else {
            Remove-Item $PID_FILE -ErrorAction SilentlyContinue
        }
    }
    
    # Check by port
    $connection = Get-NetTCPConnection -LocalPort $PORT -ErrorAction SilentlyContinue
    if ($connection) {
        return $true
    }
    
    return $false
}

# Start the chatbot
function Start-Server {
    Write-ColorOutput "`nStarting DualMind AI Chatbot..." "Cyan"
    
    if (Test-ServerRunning) {
        Write-ColorOutput "⚠️  Chatbot is already running!" "Yellow"
        Write-ColorOutput "   Use .\dualmind.ps1 status to check" "Gray"
        return $false
    }
    
    Set-Location $SCRIPT_DIR
    
    # Check if virtual environment exists
    if (-not (Test-Path ".venv")) {
        Write-ColorOutput "⚠️  Virtual environment not found. Creating..." "Yellow"
        python -m venv .venv
        if ($LASTEXITCODE -ne 0) {
            Write-ColorOutput "❌ Failed to create virtual environment." "Red"
            return $false
        }
    }
    
    # Activate virtual environment
    $venvActivate = Join-Path $SCRIPT_DIR ".venv\Scripts\Activate.ps1"
    if (-not (Test-Path $venvActivate)) {
        Write-ColorOutput "❌ Virtual environment activation script not found." "Red"
        return $false
    }
    
    # Check and install dependencies
    & $venvActivate
    
    $testImport = python -c "import fastapi" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-ColorOutput "⚠️  Dependencies not installed. Installing..." "Yellow"
        $requirementsPath = Join-Path $SCRIPT_DIR "requirements.txt"
        pip install -r $requirementsPath
        if ($LASTEXITCODE -ne 0) {
            Write-ColorOutput "❌ Failed to install dependencies." "Red"
            deactivate
            return $false
        }
    }
    
    # Start the server in background
    $serverScript = Join-Path $SCRIPT_DIR "src\server.py"
    $process = Start-Process -FilePath "python" -ArgumentList $serverScript -WindowStyle Hidden -PassThru -RedirectStandardOutput $LOG_FILE -RedirectStandardError $LOG_FILE
    $process.Id | Out-File -FilePath $PID_FILE -Encoding ASCII
    
    # Wait and check if started successfully
    Start-Sleep -Seconds 3
    
    if (Test-ServerRunning) {
        Write-ColorOutput "✅ DualMind AI Chatbot started successfully!" "Green"
        Write-Host ""
        Write-ColorOutput "📍 Access Points:" "Blue"
        Write-ColorOutput "   Main Page:    http://localhost:$PORT" "Cyan"
        Write-ColorOutput "   Cloud Mode:   http://localhost:$PORT/" "Cyan"
        Write-ColorOutput "   Local Mode:   http://localhost:$PORT/local" "Cyan"
        Write-ColorOutput "   Health Check: http://localhost:$PORT/health" "Cyan"
        Write-Host ""
        Write-ColorOutput "📝 Logs: $LOG_FILE" "Blue"
        Write-ColorOutput "🔧 PID:  $(Get-Content $PID_FILE)" "Blue"
        Write-Host ""
        Write-ColorOutput "🚀 Open http://localhost:$PORT in your browser!" "Green"
        return $true
    } else {
        Write-ColorOutput "❌ Failed to start server. Check logs: $LOG_FILE" "Red"
        Remove-Item $PID_FILE -ErrorAction SilentlyContinue
        return $false
    }
}

# Stop the chatbot
function Stop-Server {
    Write-ColorOutput "`nStopping DualMind AI Chatbot..." "Cyan"
    
    if (-not (Test-ServerRunning)) {
        Write-ColorOutput "⚠️  Chatbot is not running." "Yellow"
        return $true
    }
    
    # Kill by PID file
    if (Test-Path $PID_FILE) {
        $PID = Get-Content $PID_FILE
        Write-ColorOutput "   Stopping process $PID..." "Gray"
        
        $process = Get-Process -Id $PID -ErrorAction SilentlyContinue
        if ($process) {
            Stop-Process -Id $PID -Force -ErrorAction SilentlyContinue
        }
        
        Remove-Item $PID_FILE -ErrorAction SilentlyContinue
    }
    
    # Kill any process on the port
    $connection = Get-NetTCPConnection -LocalPort $PORT -ErrorAction SilentlyContinue
    if ($connection) {
        Write-ColorOutput "   Freeing port $PORT..." "Gray"
        $processId = $connection.OwningProcess
        Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
    }
    
    # Kill any remaining Python server processes
    Get-Process python -ErrorAction SilentlyContinue | Where-Object {
        $_.CommandLine -like "*server.py*"
    } | Stop-Process -Force -ErrorAction SilentlyContinue
    
    Start-Sleep -Seconds 1
    
    if (-not (Test-ServerRunning)) {
        Write-ColorOutput "✅ DualMind AI Chatbot stopped successfully!" "Green"
        return $true
    } else {
        Write-ColorOutput "❌ Failed to stop server completely." "Red"
        return $false
    }
}

# Restart the chatbot
function Restart-Server {
    Write-ColorOutput "`nRestarting DualMind AI Chatbot..." "Cyan"
    Stop-Server
    Start-Sleep -Seconds 2
    Start-Server
}

# Show server status
function Show-Status {
    Print-Banner
    
    if (Test-ServerRunning) {
        Write-ColorOutput "✅ Status: RUNNING" "Green"
        Write-Host ""
        
        if (Test-Path $PID_FILE) {
            $PID = Get-Content $PID_FILE
            Write-ColorOutput "Process ID: $PID" "Blue"
        }
        
        Write-ColorOutput "Port:       $PORT" "Blue"
        
        # Check if responding
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:$PORT/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                Write-ColorOutput "Health:     Healthy ✓" "Green"
                
                # Get version info
                $healthData = $response.Content | ConvertFrom-Json
                if ($healthData.version) {
                    Write-ColorOutput "Version:    $($healthData.version)" "Blue"
                }
            }
        } catch {
            Write-ColorOutput "Health:     Starting..." "Yellow"
        }
        
        Write-Host ""
        Write-ColorOutput "📍 URLs:" "Blue"
        Write-Host "   Main:   http://localhost:$PORT"
        Write-Host "   Local:  http://localhost:$PORT/local"
        Write-Host "   Health: http://localhost:$PORT/health"
        
        if (Test-Path $LOG_FILE) {
            Write-Host ""
            Write-ColorOutput "📝 Logs: $LOG_FILE" "Blue"
            Write-ColorOutput "   Last 5 lines:" "Blue"
            Get-Content $LOG_FILE -Tail 5 | ForEach-Object {
                Write-ColorOutput "   │ $_" "Cyan"
            }
        }
    } else {
        Write-ColorOutput "❌ Status: STOPPED" "Red"
        Write-Host ""
        Write-Host "To start: " -NoNewline
        Write-ColorOutput ".\dualmind.ps1 start" "Green"
    }
    
    Write-Host ""
    Write-Host "============================================================"
}

# Show logs
function Show-Logs {
    if (-not (Test-Path $LOG_FILE)) {
        Write-ColorOutput "⚠️  No logs found." "Yellow"
        return $false
    }
    
    Write-ColorOutput "📝 Showing logs (press Ctrl+C to exit):" "Cyan"
    Write-Host "============================================================"
    Get-Content $LOG_FILE -Wait -Tail 50
}

# Run all tests
function Run-Tests {
    Print-Banner
    Write-ColorOutput "🧪 Running DualMind Test Suite..." "Cyan"
    Write-Host ""
    
    # Check if test runner exists
    $testRunner = Join-Path $SCRIPT_DIR "tests\run_all_tests.py"
    if (-not (Test-Path $testRunner)) {
        Write-ColorOutput "❌ Test runner not found: $testRunner" "Red"
        return $false
    }
    
    # Run the tests
    python $testRunner
    $exitCode = $LASTEXITCODE
    
    Write-Host ""
    if ($exitCode -eq 0) {
        Write-ColorOutput "✅ All tests completed successfully!" "Green"
        return $true
    } else {
        Write-ColorOutput "❌ Some tests failed. Review output above." "Red"
        return $false
    }
}

# Show help
function Show-Help {
    Print-Banner
    Write-ColorOutput "Usage:" "Blue"
    Write-Host "  .\dualmind.ps1 [command]"
    Write-Host ""
    Write-ColorOutput "Commands:" "Blue"
    Write-ColorOutput "  start      " "Green" -NoNewline
    Write-Host "Start the chatbot server"
    Write-ColorOutput "  stop       " "Green" -NoNewline
    Write-Host "Stop the chatbot server"
    Write-ColorOutput "  restart    " "Green" -NoNewline
    Write-Host "Restart the chatbot server"
    Write-ColorOutput "  status     " "Green" -NoNewline
    Write-Host "Show server status and info"
    Write-ColorOutput "  logs       " "Green" -NoNewline
    Write-Host "Show server logs (live tail)"
    Write-ColorOutput "  test       " "Green" -NoNewline
    Write-Host "Run all automated tests"
    Write-ColorOutput "  help       " "Green" -NoNewline
    Write-Host "Show this help message"
    Write-Host ""
    Write-ColorOutput "Examples:" "Blue"
    Write-Host "  .\dualmind.ps1 start     " -NoNewline
    Write-ColorOutput "# Start the server" "Cyan"
    Write-Host "  .\dualmind.ps1 status    " -NoNewline
    Write-ColorOutput "# Check if running" "Cyan"
    Write-Host "  .\dualmind.ps1 restart   " -NoNewline
    Write-ColorOutput "# Restart the server" "Cyan"
    Write-Host "  .\dualmind.ps1 logs      " -NoNewline
    Write-ColorOutput "# Watch logs in real-time" "Cyan"
    Write-Host "  .\dualmind.ps1 test      " -NoNewline
    Write-ColorOutput "# Run all tests" "Cyan"
    Write-Host ""
    Write-ColorOutput "Quick Access:" "Blue"
    Write-Host "  After starting, open: " -NoNewline
    Write-ColorOutput "http://localhost:$PORT" "Cyan"
    Write-Host ""
    Write-ColorOutput "Customization:" "Blue"
    Write-Host "  Edit " -NoNewline
    Write-ColorOutput "branding_config.py" "Green" -NoNewline
    Write-Host " to customize names, colors, and text"
    Write-Host ""
    Write-Host "============================================================"
}

# Main script logic
switch ($Command.ToLower()) {
    "start" {
        Print-Banner
        Start-Server
    }
    "stop" {
        Print-Banner
        Stop-Server
    }
    "restart" {
        Print-Banner
        Restart-Server
    }
    "status" {
        Show-Status
    }
    "logs" {
        Show-Logs
    }
    "test" {
        Run-Tests
    }
    "help" {
        Show-Help
    }
    default {
        if ($Command -ne "") {
            Write-ColorOutput "❌ Unknown command: $Command" "Red"
            Write-Host ""
        }
        Show-Help
    }
}

