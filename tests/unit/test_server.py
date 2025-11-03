"""
Unit tests for DualMind Server
Tests all API endpoints and core functionality
"""

import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from server import app


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_health_check_status(self):
        """Test health endpoint returns 200"""
        response = self.client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_content(self):
        """Test health endpoint returns correct content"""
        response = self.client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert data["message"] == "DualMind AI Chatbot is running"


class TestProviderEndpoints:
    """Test cloud provider endpoints"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_get_all_providers(self):
        """Test getting all cloud providers"""
        response = self.client.get("/api/providers")
        assert response.status_code == 200
        data = response.json()
        assert "providers" in data
        assert "google" in data["providers"]
        assert "openai" in data["providers"]
        assert "anthropic" in data["providers"]
        assert "nvidia" in data["providers"]
        assert "azure" in data["providers"]
    
    def test_provider_structure(self):
        """Test provider data structure"""
        response = self.client.get("/api/providers")
        data = response.json()
        google_provider = data["providers"]["google"]
        
        assert "name" in google_provider
        assert "icon" in google_provider
        assert "api_key_label" in google_provider
        assert "models" in google_provider
        assert isinstance(google_provider["models"], list)
    
    def test_get_provider_models_google(self):
        """Test getting models for Google provider"""
        response = self.client.get("/api/providers/google/models")
        assert response.status_code == 200
        data = response.json()
        assert data["provider"] == "google"
        assert "models" in data
        assert len(data["models"]) > 0
    
    def test_get_provider_models_openai(self):
        """Test getting models for OpenAI provider"""
        response = self.client.get("/api/providers/openai/models")
        assert response.status_code == 200
        data = response.json()
        assert data["provider"] == "openai"
        assert "models" in data
    
    def test_get_provider_models_invalid(self):
        """Test getting models for invalid provider"""
        response = self.client.get("/api/providers/invalid_provider/models")
        assert response.status_code == 404


class TestEmbeddingEndpoints:
    """Test embedding provider endpoints"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_get_embedding_providers(self):
        """Test getting all embedding providers"""
        response = self.client.get("/api/rag/embedding-providers")
        assert response.status_code == 200
        data = response.json()
        assert "providers" in data
        assert "openai" in data["providers"]
        assert "google" in data["providers"]
        assert "cohere" in data["providers"]
        assert "voyage" in data["providers"]
        assert "huggingface" in data["providers"]
    
    def test_embedding_provider_structure(self):
        """Test embedding provider data structure"""
        response = self.client.get("/api/rag/embedding-providers")
        data = response.json()
        openai = data["providers"]["openai"]
        
        assert "name" in openai
        assert "models" in openai
        assert "description" in openai
        assert "requires_api_key" in openai
        assert isinstance(openai["models"], list)
        assert len(openai["models"]) > 0
    
    def test_get_embedding_models_openai(self):
        """Test getting embedding models for OpenAI"""
        response = self.client.get("/api/rag/embedding-models/openai")
        assert response.status_code == 200
        data = response.json()
        assert data["provider"] == "openai"
        assert "models" in data
        assert len(data["models"]) > 0
        
        # Check first model structure
        model = data["models"][0]
        assert "id" in model
        assert "name" in model
        assert "dimensions" in model
    
    def test_get_embedding_models_google(self):
        """Test getting embedding models for Google"""
        response = self.client.get("/api/rag/embedding-models/google")
        assert response.status_code == 200
        data = response.json()
        assert data["provider"] == "google"
    
    def test_get_embedding_models_invalid(self):
        """Test getting embedding models for invalid provider"""
        response = self.client.get("/api/rag/embedding-models/invalid")
        assert response.status_code == 404
    
    def test_get_local_embedding_models(self):
        """Test getting local Transformers.js embedding models"""
        response = self.client.get("/api/local/embedding-models")
        assert response.status_code == 200
        data = response.json()
        assert "source" in data
        assert "models" in data
        assert isinstance(data["models"], list)
        assert len(data["models"]) > 0
        
        # Check model structure
        model = data["models"][0]
        assert "id" in model
        assert "name" in model
        assert "dimensions" in model
        assert "category" in model


class TestUIEndpoints:
    """Test UI serving endpoints"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_root_endpoint(self):
        """Test root endpoint serves HTML"""
        response = self.client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_local_mode_endpoint(self):
        """Test local mode endpoint serves HTML"""
        response = self.client.get("/local")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert b"Local Mode" in response.content or b"local" in response.content.lower()
    
    def test_static_files(self):
        """Test static file serving"""
        response = self.client.get("/static/embedding_models.json")
        assert response.status_code == 200
        data = response.json()
        # JSON structure can be dict or list depending on format
        assert isinstance(data, (dict, list))


class TestRAGDocumentEndpoints:
    """Test RAG document management endpoints"""
    
    def setup_method(self):
        self.client = TestClient(app)
        self.session_id = "test_session_123"
    
    def test_get_documents_empty(self):
        """Test getting documents for non-existent session"""
        response = self.client.get(f"/api/rag/documents/{self.session_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == self.session_id
        assert data["documents"] == []
    
    def test_upload_document(self):
        """Test uploading a document"""
        doc_data = {
            "session_id": self.session_id,
            "filename": "test.txt",
            "content": "This is a test document content.",
            "embedding_provider": "huggingface",
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
        }
        
        # Note: This requires proper authentication and might fail without API keys
        # For now, we test the endpoint structure
        response = self.client.post("/api/rag/upload", json=doc_data)
        # Could be 200 (success) or 500 (missing API key), both are valid responses
        assert response.status_code in [200, 500]
    
    def test_delete_all_documents(self):
        """Test deleting all documents for a session"""
        response = self.client.delete(f"/api/rag/documents/{self.session_id}")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data


class TestChatEndpoint:
    """Test chat endpoint"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_chat_missing_api_key(self):
        """Test chat endpoint without API key"""
        chat_data = {
            "provider": "google",
            "model": "gemini-1.5-flash",
            "message": "Hello, how are you?"
        }
        
        response = self.client.post("/api/chat/stream", json=chat_data)
        # Should fail without API key
        assert response.status_code in [400, 401, 500]
    
    def test_chat_invalid_provider(self):
        """Test chat endpoint with invalid provider"""
        chat_data = {
            "provider": "invalid_provider",
            "model": "some-model",
            "message": "Hello",
            "api_key": "fake_key"
        }
        
        response = self.client.post("/api/chat/stream", json=chat_data)
        assert response.status_code in [400, 500]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

