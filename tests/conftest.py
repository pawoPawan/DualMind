"""
Pytest configuration and fixtures for DualMind tests
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def test_session_id():
    """Provide a test session ID"""
    return "test_session_12345"


@pytest.fixture
def sample_document():
    """Provide sample document content"""
    return {
        "filename": "test_document.txt",
        "content": "This is a test document. It contains sample text for testing purposes."
    }


@pytest.fixture
def sample_chunks():
    """Provide sample text chunks"""
    return [
        "This is the first chunk of text.",
        "This is the second chunk of text.",
        "This is the third chunk of text."
    ]


@pytest.fixture
def sample_embeddings():
    """Provide sample embeddings"""
    return [
        [0.1, 0.2, 0.3, 0.4, 0.5],
        [0.2, 0.3, 0.4, 0.5, 0.6],
        [0.3, 0.4, 0.5, 0.6, 0.7]
    ]


@pytest.fixture
def mock_api_key():
    """Provide a mock API key for testing"""
    return "test_api_key_12345"

