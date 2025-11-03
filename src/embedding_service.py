"""
Embedding Service for RAG Support
===================================
Unified interface for different embedding providers in cloud mode
"""

import os
from typing import List, Dict, Any, Optional
import numpy as np


# Embedding provider configurations
EMBEDDING_PROVIDERS = {
    "openai": {
        "name": "OpenAI Embeddings",
        "models": [
            {"id": "text-embedding-3-small", "name": "text-embedding-3-small (Recommended)", "dimensions": 1536, "cost": "Lowest"},
            {"id": "text-embedding-3-large", "name": "text-embedding-3-large", "dimensions": 3072, "cost": "Medium"},
            {"id": "text-embedding-ada-002", "name": "text-embedding-ada-002 (Legacy)", "dimensions": 1536, "cost": "Low"}
        ],
        "description": "OpenAI's powerful embedding models",
        "requires_api_key": True
    },
    "cohere": {
        "name": "Cohere Embeddings",
        "models": [
            {"id": "embed-english-v3.0", "name": "embed-english-v3.0 (Recommended)", "dimensions": 1024, "cost": "Low"},
            {"id": "embed-english-light-v3.0", "name": "embed-english-light-v3.0", "dimensions": 384, "cost": "Lowest"},
            {"id": "embed-multilingual-v3.0", "name": "embed-multilingual-v3.0", "dimensions": 1024, "cost": "Low"}
        ],
        "description": "Cohere's multilingual embeddings",
        "requires_api_key": True
    },
    "google": {
        "name": "Google AI Embeddings",
        "models": [
            {"id": "models/embedding-001", "name": "embedding-001 (Recommended)", "dimensions": 768, "cost": "Free"},
            {"id": "models/text-embedding-004", "name": "text-embedding-004", "dimensions": 768, "cost": "Free"}
        ],
        "description": "Google's Gemini embedding models",
        "requires_api_key": True
    },
    "voyage": {
        "name": "Voyage AI",
        "models": [
            {"id": "voyage-2", "name": "voyage-2 (Recommended)", "dimensions": 1024, "cost": "Low"},
            {"id": "voyage-large-2", "name": "voyage-large-2", "dimensions": 1536, "cost": "Medium"},
            {"id": "voyage-code-2", "name": "voyage-code-2 (Code specialized)", "dimensions": 1536, "cost": "Low"}
        ],
        "description": "Voyage AI specialized embeddings",
        "requires_api_key": True
    },
    "huggingface": {
        "name": "Hugging Face (Free, Self-hosted)",
        "models": [
            {"id": "sentence-transformers/all-MiniLM-L6-v2", "name": "all-MiniLM-L6-v2 (Fast)", "dimensions": 384, "cost": "Free"},
            {"id": "sentence-transformers/all-mpnet-base-v2", "name": "all-mpnet-base-v2 (Quality)", "dimensions": 768, "cost": "Free"},
            {"id": "BAAI/bge-small-en-v1.5", "name": "bge-small-en-v1.5", "dimensions": 384, "cost": "Free"},
            {"id": "BAAI/bge-base-en-v1.5", "name": "bge-base-en-v1.5 (Recommended)", "dimensions": 768, "cost": "Free"}
        ],
        "description": "Free, open-source models (runs on your server)",
        "requires_api_key": False
    }
}


class EmbeddingClient:
    """Unified client for multiple embedding providers"""
    
    def __init__(self, provider: str, api_key: Optional[str] = None, model: Optional[str] = None):
        self.provider = provider
        self.api_key = api_key
        
        if provider not in EMBEDDING_PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}. Available: {list(EMBEDDING_PROVIDERS.keys())}")
        
        self.config = EMBEDDING_PROVIDERS[provider]
        
        # Use provided model or default (first model in list)
        if model:
            self.model = model
        else:
            self.model = self.config["models"][0]["id"]
        
        # Initialize provider-specific client
        self._init_client()
    
    def _init_client(self):
        """Initialize the provider-specific client"""
        if self.provider == "huggingface" and self.api_key is None:
            # For self-hosted HF models, we'll use sentence-transformers
            try:
                from sentence_transformers import SentenceTransformer
                self.client = SentenceTransformer(self.model)
            except ImportError:
                raise ImportError("sentence-transformers not installed. Install with: pip install sentence-transformers")
    
    def embed_text(self, text: str) -> List[float]:
        """
        Embed a single text string
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding
        """
        return self.embed_texts([text])[0]
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple text strings
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embeddings
        """
        if self.provider == "openai":
            return self._embed_openai(texts)
        elif self.provider == "cohere":
            return self._embed_cohere(texts)
        elif self.provider == "google":
            return self._embed_google(texts)
        elif self.provider == "voyage":
            return self._embed_voyage(texts)
        elif self.provider == "huggingface":
            return self._embed_huggingface(texts)
        else:
            raise NotImplementedError(f"Provider {self.provider} not yet implemented")
    
    def _embed_openai(self, texts: List[str]) -> List[List[float]]:
        """OpenAI embeddings"""
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.api_key)
            
            response = client.embeddings.create(
                model=self.model,
                input=texts
            )
            
            return [item.embedding for item in response.data]
            
        except Exception as e:
            raise Exception(f"OpenAI embedding error: {str(e)}")
    
    def _embed_cohere(self, texts: List[str]) -> List[List[float]]:
        """Cohere embeddings"""
        try:
            import cohere
            
            client = cohere.Client(api_key=self.api_key)
            
            response = client.embed(
                texts=texts,
                model=self.model,
                input_type="search_document"  # For indexing documents
            )
            
            return response.embeddings
            
        except Exception as e:
            raise Exception(f"Cohere embedding error: {str(e)}")
    
    def _embed_google(self, texts: List[str]) -> List[List[float]]:
        """Google AI embeddings"""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            
            embeddings = []
            for text in texts:
                result = genai.embed_content(
                    model=self.model,
                    content=text,
                    task_type="retrieval_document"
                )
                embeddings.append(result['embedding'])
            
            return embeddings
            
        except Exception as e:
            raise Exception(f"Google AI embedding error: {str(e)}")
    
    def _embed_voyage(self, texts: List[str]) -> List[List[float]]:
        """Voyage AI embeddings"""
        try:
            import voyageai
            
            client = voyageai.Client(api_key=self.api_key)
            
            response = client.embed(
                texts=texts,
                model=self.model,
                input_type="document"
            )
            
            return response.embeddings
            
        except Exception as e:
            raise Exception(f"Voyage AI embedding error: {str(e)}")
    
    def _embed_huggingface(self, texts: List[str]) -> List[List[float]]:
        """Hugging Face embeddings (self-hosted)"""
        try:
            embeddings = self.client.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
            
        except Exception as e:
            raise Exception(f"Hugging Face embedding error: {str(e)}")
    
    def embed_query(self, query: str) -> List[float]:
        """
        Embed a search query (may use different parameters than documents)
        
        Args:
            query: Search query text
            
        Returns:
            Query embedding
        """
        # For Cohere, we use search_query type
        if self.provider == "cohere":
            try:
                import cohere
                client = cohere.Client(api_key=self.api_key)
                response = client.embed(
                    texts=[query],
                    model=self.model,
                    input_type="search_query"
                )
                return response.embeddings[0]
            except Exception as e:
                raise Exception(f"Cohere query embedding error: {str(e)}")
        
        # For Google, use retrieval_query task type
        elif self.provider == "google":
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                result = genai.embed_content(
                    model=self.model,
                    content=query,
                    task_type="retrieval_query"
                )
                return result['embedding']
            except Exception as e:
                raise Exception(f"Google AI query embedding error: {str(e)}")
        
        # For others, use regular embedding
        else:
            return self.embed_text(query)


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    vec1_np = np.array(vec1)
    vec2_np = np.array(vec2)
    
    dot_product = np.dot(vec1_np, vec2_np)
    norm1 = np.linalg.norm(vec1_np)
    norm2 = np.linalg.norm(vec2_np)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return float(dot_product / (norm1 * norm2))


def get_provider_info(provider: str) -> Dict[str, Any]:
    """Get information about an embedding provider"""
    if provider not in EMBEDDING_PROVIDERS:
        return None
    return EMBEDDING_PROVIDERS[provider]


def list_providers() -> Dict[str, Dict[str, Any]]:
    """List all available embedding providers"""
    return EMBEDDING_PROVIDERS


if __name__ == "__main__":
    # Test/demo
    print("Available Embedding Providers:")
    print("=" * 80)
    for key, provider in EMBEDDING_PROVIDERS.items():
        print(f"\n📊 {provider['name']}")
        print(f"   {provider['description']}")
        print(f"   API Key Required: {provider['requires_api_key']}")
        print(f"   Models:")
        for model in provider['models']:
            print(f"      - {model['name']} ({model['dimensions']} dims, {model['cost']} cost)")
    print("\n" + "=" * 80)

