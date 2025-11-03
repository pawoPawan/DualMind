"""
UI Tests for DualMind
Tests user interface functionality and interactions
"""

import pytest
import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from server import app


class TestLandingPage:
    """Test main landing page UI"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_landing_page_loads(self):
        """Test that landing page loads successfully"""
        response = self.client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_landing_page_contains_branding(self):
        """Test that landing page contains branding elements"""
        response = self.client.get("/")
        content = response.text.lower()
        assert "dualmind" in content or "chatbot" in content
    
    def test_landing_page_has_mode_selection(self):
        """Test that landing page has mode selection"""
        response = self.client.get("/")
        content = response.text.lower()
        # Should have references to local and cloud modes
        assert "local" in content or "cloud" in content


class TestLocalModeUI:
    """Test Local Mode UI"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_local_mode_loads(self):
        """Test that local mode page loads"""
        response = self.client.get("/local")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_local_mode_has_chat_elements(self):
        """Test that local mode has required chat elements"""
        response = self.client.get("/local")
        content = response.text.lower()
        
        # Check for essential UI elements
        assert "input" in content or "textarea" in content
        assert "message" in content or "chat" in content
    
    def test_local_mode_has_webllm_import(self):
        """Test that local mode imports WebLLM"""
        response = self.client.get("/local")
        content = response.text
        
        assert "@mlc-ai/web-llm" in content or "CreateMLCEngine" in content
    
    def test_local_mode_has_transformers(self):
        """Test that local mode imports Transformers.js"""
        response = self.client.get("/local")
        content = response.text
        
        assert "@xenova/transformers" in content or "transformers" in content.lower()
    
    def test_local_mode_has_markdown_support(self):
        """Test that local mode has markdown rendering"""
        response = self.client.get("/local")
        content = response.text
        
        assert "marked" in content.lower()
    
    def test_local_mode_has_code_highlighting(self):
        """Test that local mode has code highlighting"""
        response = self.client.get("/local")
        content = response.text
        
        assert "highlight" in content.lower() or "hljs" in content


class TestCloudModeUI:
    """Test Cloud Mode UI"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_cloud_mode_loads(self):
        """Test that cloud mode page loads"""
        response = self.client.get("/cloud")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_cloud_mode_has_provider_selection(self):
        """Test that cloud mode has provider selection"""
        response = self.client.get("/cloud")
        content = response.text.lower()
        
        # Should have provider-related elements
        assert "provider" in content or "api" in content
    
    def test_cloud_mode_has_chat_elements(self):
        """Test that cloud mode has chat elements"""
        response = self.client.get("/cloud")
        content = response.text.lower()
        
        assert "message" in content or "chat" in content
        assert "send" in content or "submit" in content


class TestEnhancedLocalUI:
    """Test Enhanced Local Mode UI"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_enhanced_local_loads(self):
        """Test that enhanced local mode loads"""
        response = self.client.get("/static/local_enhanced.html")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_enhanced_ui_has_sidebar(self):
        """Test that enhanced UI has sidebar"""
        response = self.client.get("/static/local_enhanced.html")
        content = response.text.lower()
        
        assert "sidebar" in content
    
    def test_enhanced_ui_has_chat_history(self):
        """Test that enhanced UI has chat history"""
        response = self.client.get("/static/local_enhanced.html")
        content = response.text.lower()
        
        assert "chat" in content and "history" in content
    
    def test_enhanced_ui_has_model_selector(self):
        """Test that enhanced UI has model selector"""
        response = self.client.get("/static/local_enhanced.html")
        content = response.text.lower()
        
        assert "model" in content and ("select" in content or "selector" in content)
    
    def test_enhanced_ui_has_modern_styling(self):
        """Test that enhanced UI has modern CSS"""
        response = self.client.get("/static/local_enhanced.html")
        content = response.text
        
        # Check for modern CSS features
        assert "flex" in content.lower() or "grid" in content.lower()
        assert "border-radius" in content.lower()
        assert "transition" in content.lower()


class TestStaticAssets:
    """Test static asset serving"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_embedding_models_json(self):
        """Test that embedding models JSON is accessible"""
        response = self.client.get("/static/embedding_models.json")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_embedding_models_structure(self):
        """Test embedding models JSON structure"""
        response = self.client.get("/static/embedding_models.json")
        data = response.json()
        
        # Check first model structure
        model = data[0]
        assert "id" in model
        assert "name" in model
        assert "dimensions" in model
        assert "category" in model
    
    def test_local_enhanced_html(self):
        """Test that enhanced local HTML is accessible"""
        response = self.client.get("/static/local_enhanced.html")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestResponsiveDesign:
    """Test responsive design elements"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_local_mode_has_viewport_meta(self):
        """Test that local mode has viewport meta tag"""
        response = self.client.get("/local")
        content = response.text
        
        assert "viewport" in content.lower()
        assert "width=device-width" in content.lower()
    
    def test_enhanced_ui_has_media_queries(self):
        """Test that enhanced UI has responsive media queries"""
        response = self.client.get("/static/local_enhanced.html")
        content = response.text
        
        assert "@media" in content
        assert "max-width" in content or "min-width" in content


class TestAccessibility:
    """Test accessibility features"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_ui_has_semantic_html(self):
        """Test that UI uses semantic HTML"""
        response = self.client.get("/static/local_enhanced.html")
        content = response.text.lower()
        
        # Check for semantic elements
        semantic_elements = ["header", "main", "footer", "nav", "button"]
        found = sum(1 for element in semantic_elements if element in content)
        assert found >= 3
    
    def test_buttons_have_labels(self):
        """Test that buttons have proper labels"""
        response = self.client.get("/static/local_enhanced.html")
        content = response.text
        
        # Buttons should have text or title attributes
        assert "button" in content.lower()
        # Should have either text content or title/aria-label
        assert "title=" in content or "aria-label" in content or ">Send<" in content


class TestJavaScriptFunctionality:
    """Test JavaScript functionality presence"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_local_mode_has_send_function(self):
        """Test that local mode has sendMessage function"""
        response = self.client.get("/local")
        content = response.text
        
        assert "sendMessage" in content or "send" in content.lower()
    
    def test_enhanced_ui_has_essential_functions(self):
        """Test that enhanced UI has essential functions"""
        response = self.client.get("/static/local_enhanced.html")
        content = response.text
        
        essential_functions = [
            "sendMessage",
            "addMessage",
            "openModelSelector",
        ]
        
        found = sum(1 for func in essential_functions if func in content)
        assert found >= 2
    
    def test_ui_has_event_handlers(self):
        """Test that UI has event handlers"""
        response = self.client.get("/static/local_enhanced.html")
        content = response.text
        
        # Check for common event handlers
        assert "onclick" in content.lower() or "addEventListener" in content


class TestDarkMode:
    """Test dark mode functionality"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_enhanced_ui_has_dark_mode_styling(self):
        """Test that enhanced UI has dark mode CSS"""
        response = self.client.get("/static/local_enhanced.html")
        content = response.text
        
        # Check for dark color schemes
        assert "#1e1e1e" in content or "#2d2d2d" in content
        assert "background" in content.lower()


class TestErrorHandling:
    """Test error handling in UI"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_404_handling(self):
        """Test that 404 errors are handled"""
        response = self.client.get("/nonexistent-page")
        assert response.status_code == 404
    
    def test_invalid_static_file(self):
        """Test handling of invalid static files"""
        response = self.client.get("/static/nonexistent.html")
        assert response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

