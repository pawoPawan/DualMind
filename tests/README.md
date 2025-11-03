# DualMind Test Suite

Comprehensive test suite for DualMind AI Chatbot covering unit tests, integration tests, and UI tests.

## 📁 Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Pytest configuration and fixtures
├── requirements-test.txt    # Test dependencies
├── unit/                    # Unit tests
│   ├── __init__.py
│   └── test_server.py       # Server endpoint tests
├── integration/             # Integration tests
│   ├── __init__.py
│   └── test_rag.py          # RAG functionality tests
└── ui/                      # UI tests
    ├── __init__.py
    └── test_ui.py           # UI component tests
```

## 🚀 Quick Start

### 1. Install Test Dependencies

```bash
pip install -r tests/requirements-test.txt
```

Or install with main dependencies:

```bash
pip install -r requirements.txt
pip install pytest pytest-cov pytest-asyncio
```

### 2. Run All Tests

```bash
# From project root
pytest

# With coverage report
pytest --cov=. --cov-report=html

# Verbose output
pytest -v
```

### 3. Run Specific Test Categories

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# UI tests only
pytest tests/ui/

# Run specific test file
pytest tests/unit/test_server.py

# Run specific test class
pytest tests/unit/test_server.py::TestHealthEndpoint

# Run specific test method
pytest tests/unit/test_server.py::TestHealthEndpoint::test_health_check_status
```

## 📊 Test Coverage

### Unit Tests (`tests/unit/`)

Tests individual components and functions in isolation.

**Coverage:**
- ✅ Health check endpoint
- ✅ Cloud provider endpoints (Google, OpenAI, Anthropic, NVIDIA, Azure)
- ✅ Provider model listing
- ✅ Embedding provider endpoints
- ✅ Embedding model listing (Cloud & Local)
- ✅ RAG document management (upload, list, delete)
- ✅ UI serving endpoints
- ✅ Static file serving
- ✅ Chat endpoint structure

**Example:**
```bash
pytest tests/unit/test_server.py -v
```

### Integration Tests (`tests/integration/`)

Tests interactions between multiple components.

**Coverage:**
- ✅ Document processing (TXT, MD, PDF, DOCX)
- ✅ Document chunking with overlap
- ✅ Document storage and retrieval
- ✅ Semantic search functionality
- ✅ Embedding service integration
- ✅ Multi-session handling
- ✅ End-to-end RAG workflow

**Example:**
```bash
pytest tests/integration/test_rag.py -v
```

### UI Tests (`tests/ui/`)

Tests user interface components and interactions.

**Coverage:**
- ✅ Landing page rendering
- ✅ Local mode UI loading
- ✅ Cloud mode UI loading
- ✅ Enhanced UI with modern design
- ✅ Sidebar and chat history
- ✅ Model selector functionality
- ✅ Markdown and code highlighting
- ✅ Responsive design
- ✅ Accessibility features
- ✅ Dark mode styling
- ✅ Static asset serving

**Example:**
```bash
pytest tests/ui/test_ui.py -v
```

## 📝 Writing New Tests

### Test File Naming

- Unit tests: `test_<module_name>.py`
- Integration tests: `test_<feature_name>.py`
- UI tests: `test_<component_name>.py`

### Test Class Naming

```python
class TestFeatureName:
    """Test feature description"""
    
    def setup_method(self):
        """Setup before each test"""
        pass
    
    def test_specific_behavior(self):
        """Test specific behavior"""
        assert True
```

### Using Fixtures

```python
def test_with_fixture(test_session_id, sample_document):
    """Test using fixtures from conftest.py"""
    assert test_session_id is not None
    assert sample_document["filename"] == "test_document.txt"
```

### Test Markers

```python
import pytest

@pytest.mark.unit
def test_unit_functionality():
    """Mark as unit test"""
    pass

@pytest.mark.integration
def test_integration_functionality():
    """Mark as integration test"""
    pass

@pytest.mark.slow
def test_slow_operation():
    """Mark as slow test"""
    pass

@pytest.mark.requires_api_key
def test_with_api_key():
    """Mark as requiring API key"""
    pass
```

Run specific markers:
```bash
pytest -m unit        # Run only unit tests
pytest -m integration # Run only integration tests
pytest -m "not slow"  # Skip slow tests
```

## 🔍 Test Examples

### Testing API Endpoints

```python
from fastapi.testclient import TestClient
from server import app

def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### Testing Document Processing

```python
from document_processor import DocumentProcessor

def test_process_document():
    processor = DocumentProcessor()
    result = processor.process("Test content", "test.txt")
    assert result is not None
    assert "test" in result.lower()
```

### Testing RAG Workflow

```python
def test_rag_workflow(test_session_id):
    from document_processor import DocumentProcessor, DocumentChunker, DocumentStore
    
    processor = DocumentProcessor()
    chunker = DocumentChunker()
    store = DocumentStore()
    
    # Process
    content = processor.process("Test document", "test.txt")
    
    # Chunk
    chunks = chunker.chunk(content)
    
    # Store
    doc_id = store.add_document(test_session_id, "test.txt", content)
    
    assert doc_id is not None
    assert len(chunks) > 0
```

## 📈 Coverage Reports

### Generate HTML Coverage Report

```bash
pytest --cov=. --cov-report=html
```

View report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Coverage Summary

```bash
pytest --cov=. --cov-report=term-missing
```

## 🐛 Debugging Tests

### Run with Print Statements

```bash
pytest -s tests/unit/test_server.py
```

### Run with PDB Debugger

```python
def test_with_debugger():
    import pdb; pdb.set_trace()
    assert True
```

### Show Local Variables on Failure

```bash
pytest -l tests/unit/test_server.py
```

### Stop on First Failure

```bash
pytest -x
```

### Run Last Failed Tests

```bash
pytest --lf
```

## 🎯 Best Practices

1. **Write descriptive test names**
   - ✅ `test_health_endpoint_returns_200`
   - ❌ `test_health`

2. **One assertion concept per test**
   - Test one thing at a time
   - Makes debugging easier

3. **Use fixtures for common setup**
   - Defined in `conftest.py`
   - Reusable across tests

4. **Mock external dependencies**
   - Don't make real API calls in tests
   - Use `pytest-mock` or `unittest.mock`

5. **Test edge cases**
   - Empty inputs
   - Invalid data
   - Boundary conditions

6. **Keep tests fast**
   - Unit tests should run in milliseconds
   - Mark slow tests with `@pytest.mark.slow`

7. **Test both success and failure cases**
   - Happy path
   - Error conditions

## 🔧 Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r tests/requirements-test.txt
    
    - name: Run tests
      run: pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)

## 🤝 Contributing

When adding new features:

1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Maintain > 80% coverage
4. Document test purpose clearly

## 📞 Support

If you encounter test failures:

1. Check error messages carefully
2. Run with `-v` for verbose output
3. Use `-s` to see print statements
4. Check if you need API keys (some tests may need them)

## 📊 Test Statistics

Run this command to see test statistics:

```bash
pytest --collect-only
```

Current test count:
- **Unit tests:** 40+ tests
- **Integration tests:** 30+ tests
- **UI tests:** 30+ tests
- **Total:** 100+ tests

---

**Happy Testing! 🧪**

