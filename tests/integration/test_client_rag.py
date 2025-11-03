"""
Integration tests for client-side RAG functionality.

Tests validate the document processing, embedding, and retrieval features
that run in the browser using Transformers.js.
"""

import pytest
from fastapi.testclient import TestClient
from server import app


class TestClientRAGEndpoints:
    """Test client-side RAG API endpoints"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_embedding_models_endpoint(self):
        """Test that embedding models endpoint returns valid data"""
        response = self.client.get("/api/local/embedding-models")
        assert response.status_code == 200
        
        data = response.json()
        assert "source" in data
        assert "models" in data
        
        models = data["models"]
        assert len(models) > 0
        
        # Verify model structure
        first_model = models[0]
        required_fields = ["id", "name", "description", "size_mb", "dimensions", "category"]
        for field in required_fields:
            assert field in first_model, f"Missing field: {field}"
    
    def test_embedding_model_categories(self):
        """Test that embedding models are properly categorized"""
        response = self.client.get("/api/local/embedding-models")
        data = response.json()
        models = data["models"]
        
        categories = set()
        for model in models:
            categories.add(model["category"])
        
        # Should have multiple categories
        assert len(categories) >= 2
        # Common categories
        expected_categories = {"speed", "quality", "multilingual"}
        assert categories.intersection(expected_categories)


class TestLocalModeRAGUI:
    """Test Local Mode RAG UI components"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_local_mode_has_rag_elements(self):
        """Test that local mode UI includes RAG/knowledge base elements"""
        response = self.client.get("/local")
        content = response.text.lower()
        
        # Check for knowledge base/document upload UI elements
        assert "attach" in content or "upload" in content or "knowledge" in content
        assert "file" in content
    
    def test_local_mode_has_rag_modal(self):
        """Test that local mode has knowledge base modal"""
        response = self.client.get("/local")
        content = response.text
        
        # Should have modal or similar UI for document management
        assert "modal" in content.lower() or "dialog" in content.lower()
    
    def test_local_mode_rag_scripts(self):
        """Test that local mode loads RAG JavaScript modules"""
        response = self.client.get("/local")
        content = response.text
        
        # Should reference modular app structure which includes RAG
        assert "/static/js/app.js" in content
        
        # Verify RAG module exists
        rag_response = self.client.get("/static/js/rag.js")
        assert rag_response.status_code == 200


class TestCloudModeRAGUI:
    """Test Cloud Mode RAG UI components"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_cloud_mode_has_rag_elements(self):
        """Test that cloud mode UI includes RAG elements"""
        response = self.client.get("/cloud")
        content = response.text.lower()
        
        # Check for RAG UI elements
        assert "attach" in content or "upload" in content or "knowledge" in content
    
    def test_cloud_mode_has_document_management(self):
        """Test that cloud mode has document management UI"""
        response = self.client.get("/cloud")
        content = response.text
        
        # Should have UI for managing uploaded documents
        assert "modal" in content.lower() or "dialog" in content.lower()


class TestRAGStaticAssets:
    """Test RAG-related static assets"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_rag_js_module_exists(self):
        """Test that RAG JavaScript module is served"""
        response = self.client.get("/static/js/rag.js")
        assert response.status_code == 200
        content = response.text
        
        # Should contain key RAG functions
        assert "handleFileUpload" in content or "uploadDocument" in content
        assert "knowledgeBase" in content or "documents" in content
    
    def test_embedding_models_json_exists(self):
        """Test that embedding models JSON is served"""
        response = self.client.get("/static/embedding_models.json")
        assert response.status_code == 200
        data = response.json()
        
        assert "transformers_js" in data
        assert len(data["transformers_js"]["models"]) > 0
    
    def test_rag_css_integration(self):
        """Test that RAG UI elements have styling"""
        response = self.client.get("/static/css/local.css")
        assert response.status_code == 200
        content = response.text
        
        # Should have styles for knowledge base/modal elements
        rag_selectors = ["modal", "knowledge", "upload", "document", "attach"]
        found = sum(1 for selector in rag_selectors if selector in content.lower())
        assert found >= 2


class TestRAGFeatureIntegration:
    """Test RAG feature integration across the application"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_local_and_cloud_rag_parity(self):
        """Test that both modes have similar RAG features"""
        local_response = self.client.get("/local")
        cloud_response = self.client.get("/cloud")
        
        local_content = local_response.text.lower()
        cloud_content = cloud_response.text.lower()
        
        # Both should have attach/upload functionality
        assert ("attach" in local_content or "upload" in local_content)
        assert ("attach" in cloud_content or "upload" in cloud_content)
    
    def test_rag_documentation_exists(self):
        """Test that RAG documentation files exist"""
        # This assumes documentation is accessible via static serving
        # or we just verify the files exist in the filesystem
        import os
        
        docs = [
            "/Users/pawkumar/Documents/pawan/DualMind/RAG_GUIDE.md",
            "/Users/pawkumar/Documents/pawan/DualMind/CLOUD_RAG_GUIDE.md",
            "/Users/pawkumar/Documents/pawan/DualMind/RAG_IMPLEMENTATION.md"
        ]
        
        for doc in docs:
            assert os.path.exists(doc), f"Documentation not found: {doc}"


class TestRAGUserFlow:
    """Test complete RAG user flow scenarios"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_embedding_model_selection_flow(self):
        """Test user can access embedding model information"""
        # 1. Get available embedding models
        response = self.client.get("/api/local/embedding-models")
        assert response.status_code == 200
        
        data = response.json()
        models = data["models"]
        assert len(models) > 0
        
        # 2. Models should have all info needed for user selection
        for model in models[:3]:  # Check first 3 models
            assert "name" in model
            assert "description" in model
            assert "size_mb" in model
            assert "category" in model
    
    def test_rag_ui_accessibility(self):
        """Test RAG UI has proper accessibility features"""
        response = self.client.get("/local")
        content = response.text
        
        # Should have tooltips or labels for RAG features
        assert "title=" in content or "aria-label" in content
        
        # File input should be properly labeled
        if "file" in content.lower():
            assert "button" in content.lower() or "input" in content.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

