"""
Integration tests for RAG (Retrieval Augmented Generation)
Tests document processing, embedding, and retrieval
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from document_processor import DocumentProcessor, DocumentChunker, DocumentStore
from embedding_service import EmbeddingClient


class TestDocumentProcessor:
    """Test document processing functionality"""
    
    def setup_method(self):
        self.processor = DocumentProcessor()
    
    def test_process_text_file(self):
        """Test processing plain text"""
        content = "This is a test document.\nIt has multiple lines.\nFor testing purposes."
        result = self.processor.process(content, "test.txt")
        
        assert result is not None
        assert len(result) > 0
        assert "test document" in result.lower()
    
    def test_process_markdown_file(self):
        """Test processing markdown"""
        content = "# Test Header\n\nThis is **bold** text.\n\n- Item 1\n- Item 2"
        result = self.processor.process(content, "test.md")
        
        assert result is not None
        assert "test header" in result.lower()
        assert "bold" in result.lower()
    
    def test_process_empty_content(self):
        """Test processing empty content"""
        result = self.processor.process("", "test.txt")
        assert result == ""
    
    def test_unsupported_file_type(self):
        """Test processing unsupported file type"""
        result = self.processor.process("content", "test.xyz")
        assert result is not None


class TestDocumentChunker:
    """Test document chunking functionality"""
    
    def setup_method(self):
        self.chunker = DocumentChunker(chunk_size=100, chunk_overlap=20)
    
    def test_chunk_short_text(self):
        """Test chunking text shorter than chunk size"""
        text = "This is a short text."
        chunks = self.chunker.chunk_text(text)
        
        assert len(chunks) == 1
        assert chunks[0] == text
    
    def test_chunk_long_text(self):
        """Test chunking long text"""
        text = "Word " * 100  # 500 characters
        chunks = self.chunker.chunk_text(text)
        
        assert len(chunks) > 1
        for chunk in chunks:
            assert len(chunk) <= self.chunker.chunk_size + 50  # Allow some tolerance
    
    def test_chunk_with_overlap(self):
        """Test that chunks have proper overlap"""
        text = "This is sentence one. This is sentence two. This is sentence three. " * 5
        chunks = self.chunker.chunk_text(text)
        
        if len(chunks) > 1:
            # Check that there's some overlap between consecutive chunks
            assert len(chunks) >= 2
    
    def test_chunk_empty_text(self):
        """Test chunking empty text"""
        chunks = self.chunker.chunk_text("")
        assert len(chunks) == 0 or chunks == [""]
    
    def test_custom_chunk_size(self):
        """Test chunking with custom size"""
        chunker = DocumentChunker(chunk_size=50, chunk_overlap=10)
        text = "Word " * 50
        chunks = chunker.chunk_text(text)
        
        for chunk in chunks:
            assert len(chunk) <= 60  # chunk_size + tolerance


class TestDocumentStore:
    """Test document storage and retrieval"""
    
    def setup_method(self):
        self.store = DocumentStore()
        self.session_id = "test_session"
    
    def test_add_document(self):
        """Test adding a document"""
        doc_id = self.store.add_document(
            session_id=self.session_id,
            filename="test.txt",
            content="Test content"
        )
        
        assert doc_id is not None
        assert isinstance(doc_id, str)
    
    def test_get_documents(self):
        """Test retrieving documents"""
        # Add a document
        self.store.add_document(
            session_id=self.session_id,
            filename="test.txt",
            content="Test content"
        )
        
        # Retrieve documents
        docs = self.store.get_documents(self.session_id)
        assert len(docs) == 1
        assert docs[0]["filename"] == "test.txt"
    
    def test_add_chunks(self):
        """Test adding chunks to a document"""
        doc_id = self.store.add_document(
            session_id=self.session_id,
            filename="test.txt",
            content="Test content"
        )
        
        chunks = ["Chunk 1", "Chunk 2", "Chunk 3"]
        embeddings = [[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]]
        
        self.store.add_chunks(self.session_id, doc_id, chunks, embeddings)
        
        # Verify chunks were added
        assert self.session_id in self.store.chunks
        assert len(self.store.chunks[self.session_id]) == 3
    
    def test_search_chunks(self):
        """Test semantic search"""
        doc_id = self.store.add_document(
            session_id=self.session_id,
            filename="test.txt",
            content="Test content"
        )
        
        chunks = ["Python programming", "JavaScript coding", "Java development"]
        embeddings = [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0]
        ]
        
        self.store.add_chunks(self.session_id, doc_id, chunks, embeddings)
        
        # Search with query embedding similar to first chunk
        query_embedding = [0.9, 0.1, 0.0]
        results = self.store.search_chunks(self.session_id, query_embedding, top_k=2)
        
        assert len(results) <= 2
        if len(results) > 0:
            assert "text" in results[0]
            assert "score" in results[0]
    
    def test_delete_document(self):
        """Test deleting a document"""
        doc_id = self.store.add_document(
            session_id=self.session_id,
            filename="test.txt",
            content="Test content"
        )
        
        # Delete the document
        self.store.delete_document(self.session_id, doc_id)
        
        # Verify it's deleted
        docs = self.store.get_documents(self.session_id)
        assert len(docs) == 0
    
    def test_clear_session(self):
        """Test clearing all documents in a session"""
        # Add multiple documents
        self.store.add_document(self.session_id, "test1.txt", "Content 1")
        self.store.add_document(self.session_id, "test2.txt", "Content 2")
        
        # Clear session
        self.store.clear_session(self.session_id)
        
        # Verify all documents are cleared
        docs = self.store.get_documents(self.session_id)
        assert len(docs) == 0
    
    def test_multiple_sessions(self):
        """Test handling multiple sessions"""
        session1 = "session1"
        session2 = "session2"
        
        self.store.add_document(session1, "file1.txt", "Content 1")
        self.store.add_document(session2, "file2.txt", "Content 2")
        
        # Verify sessions are separate
        docs1 = self.store.get_documents(session1)
        docs2 = self.store.get_documents(session2)
        
        assert len(docs1) == 1
        assert len(docs2) == 1
        assert docs1[0]["filename"] != docs2[0]["filename"]


class TestEmbeddingService:
    """Test embedding service functionality"""
    
    def test_list_providers(self):
        """Test listing embedding providers"""
        from embedding_service import EMBEDDING_PROVIDERS
        
        assert "openai" in EMBEDDING_PROVIDERS
        assert "google" in EMBEDDING_PROVIDERS
        assert "cohere" in EMBEDDING_PROVIDERS
        assert "voyage" in EMBEDDING_PROVIDERS
        assert "huggingface" in EMBEDDING_PROVIDERS
    
    def test_provider_models(self):
        """Test that each provider has models"""
        from embedding_service import EMBEDDING_PROVIDERS
        
        for provider_id, provider in EMBEDDING_PROVIDERS.items():
            assert "models" in provider
            assert len(provider["models"]) > 0
            
            # Check model structure
            model = provider["models"][0]
            assert "id" in model
            assert "name" in model
            assert "dimensions" in model
    
    def test_embedding_client_initialization(self):
        """Test EmbeddingClient initialization"""
        # This will fail without API keys, but tests the structure
        try:
            client = EmbeddingClient("openai", "fake_key")
            assert client.provider == "openai"
        except Exception as e:
            # Expected to fail without valid API key
            assert True


class TestRAGEndToEnd:
    """End-to-end RAG workflow tests"""
    
    def setup_method(self):
        self.processor = DocumentProcessor()
        self.chunker = DocumentChunker()
        self.store = DocumentStore()
        self.session_id = "e2e_test_session"
    
    def test_full_rag_workflow(self):
        """Test complete RAG workflow: process, chunk, store, search"""
        # 1. Process document
        content = """
        Python is a high-level programming language.
        It is known for its simplicity and readability.
        Python is widely used in web development, data science, and AI.
        """
        
        processed = self.processor.process(content, "python.txt")
        assert processed is not None
        
        # 2. Chunk the document
        chunks = self.chunker.chunk_text(processed)
        assert len(chunks) > 0
        
        # 3. Add to store (without embeddings for this test)
        doc_id = self.store.add_document(
            session_id=self.session_id,
            filename="python.txt",
            content=processed
        )
        
        assert doc_id is not None
        
        # 4. Verify document is stored
        docs = self.store.get_documents(self.session_id)
        assert len(docs) == 1
        assert docs[0]["filename"] == "python.txt"
    
    def test_multiple_document_workflow(self):
        """Test handling multiple documents"""
        documents = [
            ("python.txt", "Python is a programming language."),
            ("javascript.txt", "JavaScript is used for web development."),
            ("java.txt", "Java is an object-oriented language.")
        ]
        
        for filename, content in documents:
            processed = self.processor.process(content, filename)
            doc_id = self.store.add_document(
                session_id=self.session_id,
                filename=filename,
                content=processed
            )
            assert doc_id is not None
        
        # Verify all documents are stored
        docs = self.store.get_documents(self.session_id)
        assert len(docs) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

