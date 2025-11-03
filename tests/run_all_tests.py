#!/usr/bin/env python3
"""
Master Test Runner for DualMind
Runs all test suites and provides consolidated summary
"""

import subprocess
import sys
import time
from datetime import datetime

class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color

def print_banner():
    print("\n" + "="*70)
    print(f"{Colors.PURPLE}🧪 DUALMIND COMPREHENSIVE TEST SUITE{Colors.NC}")
    print("="*70 + "\n")

def print_section(title):
    print(f"\n{Colors.CYAN}{'─'*70}")
    print(f"  {title}")
    print(f"{'─'*70}{Colors.NC}\n")

def run_test_suite(name, command, description):
    """Run a test suite and return results"""
    print(f"{Colors.BLUE}▶ {name}{Colors.NC}")
    print(f"  {description}")
    print(f"  Command: {command}\n")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        elapsed_time = time.time() - start_time
        
        if result.returncode == 0:
            print(f"{Colors.GREEN}✅ PASSED{Colors.NC} ({elapsed_time:.2f}s)\n")
            return {
                'name': name,
                'status': 'PASSED',
                'time': elapsed_time,
                'output': result.stdout,
                'error': None
            }
        else:
            print(f"{Colors.RED}❌ FAILED{Colors.NC} ({elapsed_time:.2f}s)")
            print(f"{Colors.RED}Error: {result.stderr[:200]}{Colors.NC}\n")
            return {
                'name': name,
                'status': 'FAILED',
                'time': elapsed_time,
                'output': result.stdout,
                'error': result.stderr
            }
    
    except subprocess.TimeoutExpired:
        print(f"{Colors.RED}❌ TIMEOUT{Colors.NC} (exceeded 60s)\n")
        return {
            'name': name,
            'status': 'TIMEOUT',
            'time': 60.0,
            'output': '',
            'error': 'Test suite exceeded 60 second timeout'
        }
    
    except Exception as e:
        print(f"{Colors.RED}❌ ERROR: {str(e)}{Colors.NC}\n")
        return {
            'name': name,
            'status': 'ERROR',
            'time': 0.0,
            'output': '',
            'error': str(e)
        }

def print_summary(results, total_time):
    """Print consolidated test summary"""
    print("\n" + "="*70)
    print(f"{Colors.PURPLE}📊 TEST EXECUTION SUMMARY{Colors.NC}")
    print("="*70 + "\n")
    
    passed = sum(1 for r in results if r['status'] == 'PASSED')
    failed = sum(1 for r in results if r['status'] == 'FAILED')
    errors = sum(1 for r in results if r['status'] in ['ERROR', 'TIMEOUT'])
    total = len(results)
    
    # Individual results
    print(f"{Colors.CYAN}Test Suite Results:{Colors.NC}\n")
    for result in results:
        status_color = Colors.GREEN if result['status'] == 'PASSED' else Colors.RED
        status_icon = "✅" if result['status'] == 'PASSED' else "❌"
        
        print(f"  {status_icon} {result['name']:<40} {status_color}{result['status']:<8}{Colors.NC} ({result['time']:.2f}s)")
    
    # Overall statistics
    print(f"\n{Colors.CYAN}Overall Statistics:{Colors.NC}\n")
    print(f"  Total Test Suites:  {total}")
    print(f"  {Colors.GREEN}Passed:{Colors.NC}             {passed}")
    print(f"  {Colors.RED}Failed:{Colors.NC}             {failed}")
    print(f"  {Colors.YELLOW}Errors/Timeouts:{Colors.NC}    {errors}")
    print(f"  Total Time:         {total_time:.2f}s")
    
    # Pass rate
    pass_rate = (passed / total * 100) if total > 0 else 0
    rate_color = Colors.GREEN if pass_rate == 100 else Colors.YELLOW if pass_rate >= 50 else Colors.RED
    print(f"  {rate_color}Pass Rate:{Colors.NC}          {pass_rate:.1f}%")
    
    print("\n" + "="*70)
    
    # Final status
    if passed == total:
        print(f"{Colors.GREEN}✅ ALL TESTS PASSED! 🎉{Colors.NC}")
        print("="*70 + "\n")
        return 0
    else:
        print(f"{Colors.RED}❌ SOME TESTS FAILED{Colors.NC}")
        print("="*70 + "\n")
        
        # Show failed tests details
        failed_tests = [r for r in results if r['status'] != 'PASSED']
        if failed_tests:
            print(f"{Colors.RED}Failed Test Details:{Colors.NC}\n")
            for result in failed_tests:
                print(f"  {result['name']}:")
                if result['error']:
                    print(f"    Error: {result['error'][:200]}")
                print()
        
        return 1

def check_server_running():
    """Check if DualMind server is running"""
    print(f"{Colors.CYAN}Checking server status...{Colors.NC}")
    result = subprocess.run(
        "curl -s http://localhost:8000/health",
        shell=True,
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if result.returncode == 0 and 'healthy' in result.stdout.lower():
        print(f"{Colors.GREEN}✅ Server is running{Colors.NC}\n")
        return True
    else:
        print(f"{Colors.YELLOW}⚠️  Server not running (some tests may be skipped){Colors.NC}\n")
        return False

def main():
    print_banner()
    
    # Check environment
    print_section("ENVIRONMENT CHECK")
    server_running = check_server_running()
    
    # Define test suites
    test_suites = [
        {
            'name': 'RAG Integration Tests',
            'command': 'cd /Users/pawkumar/Documents/pawan/DualMind && python3 tests/run_rag_tests.py',
            'description': 'Per-chat RAG document isolation and management tests'
        },
        {
            'name': 'Python Syntax Check',
            'command': 'cd /Users/pawkumar/Documents/pawan/DualMind && find src/ -name "*.py" -exec python3 -m py_compile {} +',
            'description': 'Verify all Python files have valid syntax'
        },
        {
            'name': 'Server Health Check',
            'command': 'cd /Users/pawkumar/Documents/pawan/DualMind && curl -sf http://localhost:8000/health > /dev/null && echo "Server healthy"',
            'description': 'Verify server is running and healthy',
            'skip_if_no_server': True
        },
        {
            'name': 'API Endpoints Check',
            'command': 'cd /Users/pawkumar/Documents/pawan/DualMind && curl -sf http://localhost:8000/api/providers > /dev/null && echo "API endpoints working"',
            'description': 'Verify core API endpoints are accessible',
            'skip_if_no_server': True
        }
    ]
    
    # Add pytest tests if pytest is available
    try:
        subprocess.run(['pytest', '--version'], capture_output=True, check=True)
        test_suites.append({
            'name': 'Pytest Integration Tests',
            'command': 'cd /Users/pawkumar/Documents/pawan/DualMind && pytest tests/integration/ -v --tb=short',
            'description': 'Run pytest integration test suite'
        })
    except:
        print(f"{Colors.YELLOW}ℹ️  Pytest not installed, skipping pytest tests{Colors.NC}\n")
    
    # Run all test suites
    print_section("RUNNING TEST SUITES")
    
    results = []
    start_time = time.time()
    
    for suite in test_suites:
        # Skip server-dependent tests if server not running
        if suite.get('skip_if_no_server') and not server_running:
            print(f"{Colors.YELLOW}⊘ {suite['name']} (skipped - server not running){Colors.NC}\n")
            continue
        
        result = run_test_suite(
            suite['name'],
            suite['command'],
            suite['description']
        )
        results.append(result)
    
    total_time = time.time() - start_time
    
    # Print summary
    exit_code = print_summary(results, total_time)
    
    # Additional info
    print(f"{Colors.CYAN}Test Execution Details:{Colors.NC}")
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Platform:  {sys.platform}")
    print(f"  Python:    {sys.version.split()[0]}")
    print()
    
    # Instructions for manual UI tests
    print(f"{Colors.CYAN}Manual UI Tests:{Colors.NC}")
    print(f"  To run manual UI tests, see: tests/ui/test_per_chat_rag_ui.py")
    print(f"  Server must be running: ./dualmind.sh start")
    print(f"  Then open: http://localhost:8000/local or /cloud")
    print()
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()

