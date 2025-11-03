"""
Document Processing for RAG
============================
Handle document upload, text extraction, chunking, and storage
"""

import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib


class DocumentChunker:
    """Split documents into chunks for embedding"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Text to split
            
        Returns:
            List of text chunks
        """
        if not text or len(text) == 0:
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            
            # If this is not the last chunk, try to break at a sentence or word boundary
            if end < text_length:
                # Look for sentence boundary (. ! ?)
                for i in range(end, start + self.chunk_size // 2, -1):
                    if text[i] in '.!?\n':
                        end = i + 1
                        break
                else:
                    # If no sentence boundary, look for word boundary
                    for i in range(end, start + self.chunk_size // 2, -1):
                        if text[i].isspace():
                            end = i
                            break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            
            # Prevent infinite loop
            if start <= end - self.chunk_size + self.chunk_overlap:
                start = end
        
        return chunks


class DocumentProcessor:
    """Process documents for RAG"""
    
    @staticmethod
    def extract_text_from_file(file_content: bytes, filename: str) -> str:
        """
        Extract text from various file formats
        
        Args:
            file_content: File content as bytes
            filename: Original filename
            
        Returns:
            Extracted text
        """
        file_ext = Path(filename).suffix.lower()
        
        try:
            if file_ext in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml']:
                # Plain text files
                return file_content.decode('utf-8', errors='ignore')
            
            elif file_ext == '.pdf':
                # PDF files
                return DocumentProcessor._extract_from_pdf(file_content)
            
            elif file_ext in ['.doc', '.docx']:
                # Word documents
                return DocumentProcessor._extract_from_docx(file_content)
            
            else:
                # Try to decode as text
                return file_content.decode('utf-8', errors='ignore')
        
        except Exception as e:
            raise Exception(f"Error extracting text from {filename}: {str(e)}")
    
    @staticmethod
    def _extract_from_pdf(file_content: bytes) -> str:
        """Extract text from PDF"""
        try:
            from PyPDF2 import PdfReader
            from io import BytesIO
            
            pdf_file = BytesIO(file_content)
            pdf_reader = PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        
        except ImportError:
            raise ImportError("PyPDF2 not installed. Install with: pip install PyPDF2")
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    @staticmethod
    def _extract_from_docx(file_content: bytes) -> str:
        """Extract text from DOCX"""
        try:
            from docx import Document
            from io import BytesIO
            
            docx_file = BytesIO(file_content)
            doc = Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        
        except ImportError:
            raise ImportError("python-docx not installed. Install with: pip install python-docx")
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    @staticmethod
    def generate_document_id(filename: str, content: str) -> str:
        """Generate unique document ID based on filename and content"""
        hash_input = f"{filename}:{content[:1000]}"  # Use first 1000 chars for hash
        return hashlib.md5(hash_input.encode()).hexdigest()


class DocumentStore:
    """In-memory document store for RAG"""
    
    def __init__(self, storage_dir: str = "./rag_storage"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.documents = {}  # {session_id: {doc_id: document}}
        self._load_from_disk()
    
    def _get_session_file(self, session_id: str) -> Path:
        """Get storage file path for a session"""
        return self.storage_dir / f"{session_id}.json"
    
    def _load_from_disk(self):
        """Load documents from disk"""
        try:
            for file_path in self.storage_dir.glob("*.json"):
                session_id = file_path.stem
                with open(file_path, 'r') as f:
                    self.documents[session_id] = json.load(f)
        except Exception as e:
            print(f"Error loading documents from disk: {e}")
    
    def _save_session(self, session_id: str):
        """Save session documents to disk"""
        try:
            if session_id in self.documents:
                with open(self._get_session_file(session_id), 'w') as f:
                    json.dump(self.documents[session_id], f)
        except Exception as e:
            print(f"Error saving session to disk: {e}")
    
    def add_document(self, session_id: str, document: Dict[str, Any]):
        """Add a document to the store"""
        if session_id not in self.documents:
            self.documents[session_id] = {}
        
        doc_id = document.get("id")
        self.documents[session_id][doc_id] = document
        self._save_session(session_id)
    
    def get_document(self, session_id: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific document"""
        return self.documents.get(session_id, {}).get(doc_id)
    
    def list_documents(self, session_id: str) -> List[Dict[str, Any]]:
        """List all documents for a session"""
        if session_id not in self.documents:
            return []
        
        # Return simplified document list (without embeddings)
        docs = []
        for doc_id, doc in self.documents[session_id].items():
            docs.append({
                "id": doc["id"],
                "filename": doc["filename"],
                "chunk_count": len(doc["chunks"]),
                "upload_time": doc.get("upload_time", ""),
                "size": len(doc.get("text", ""))
            })
        return docs
    
    def delete_document(self, session_id: str, doc_id: str) -> bool:
        """Delete a document"""
        if session_id in self.documents and doc_id in self.documents[session_id]:
            del self.documents[session_id][doc_id]
            self._save_session(session_id)
            return True
        return False
    
    def clear_session(self, session_id: str):
        """Clear all documents for a session"""
        if session_id in self.documents:
            del self.documents[session_id]
            file_path = self._get_session_file(session_id)
            if file_path.exists():
                file_path.unlink()
    
    def search_chunks(self, session_id: str, query_embedding: List[float], 
                     top_k: int = 3, similarity_threshold: float = 0.3) -> List[Dict[str, Any]]:
        """
        Search for relevant chunks using cosine similarity
        
        Args:
            session_id: Session identifier
            query_embedding: Query embedding vector
            top_k: Number of top results to return
            similarity_threshold: Minimum similarity score
            
        Returns:
            List of relevant chunks with metadata
        """
        if session_id not in self.documents:
            return []
        
        from embedding_service import cosine_similarity
        
        results = []
        
        # Search through all documents in the session
        for doc_id, doc in self.documents[session_id].items():
            chunks = doc.get("chunks", [])
            embeddings = doc.get("embeddings", [])
            
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                similarity = cosine_similarity(query_embedding, embedding)
                
                if similarity >= similarity_threshold:
                    results.append({
                        "chunk": chunk,
                        "similarity": similarity,
                        "document": doc["filename"],
                        "doc_id": doc_id,
                        "chunk_index": i
                    })
        
        # Sort by similarity and return top_k
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]


# Global document store instance
document_store = DocumentStore()


if __name__ == "__main__":
    # Test chunking
    chunker = DocumentChunker(chunk_size=100, chunk_overlap=20)
    test_text = "This is a test document. " * 50
    chunks = chunker.chunk_text(test_text)
    print(f"Created {len(chunks)} chunks from test text")
    print(f"First chunk: {chunks[0][:50]}...")

