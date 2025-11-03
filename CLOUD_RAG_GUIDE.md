# Cloud RAG Guide - DualMind AI

## Overview

DualMind AI now supports **RAG (Retrieval-Augmented Generation) in Cloud Mode** with multiple embedding provider options! This feature allows you to upload documents and have AI answer questions based on your document content while using powerful cloud AI models.

## 🌟 Key Features

### ✅ What's Included

1. **Multiple Embedding Providers**
   - OpenAI (text-embedding-3-small, text-embedding-3-large)
   - Google AI (embedding-001, text-embedding-004) 
   - Cohere (embed-english-v3.0, multilingual)
   - Voyage AI (voyage-2, voyage-large-2, voyage-code-2)
   - Hugging Face (Free, self-hosted options)

2. **Document Processing**
   - Support for TXT, MD, PDF, DOC, DOCX files
   - Automatic text extraction and chunking
   - Server-side document storage per session

3. **Flexible API Keys**
   - Separate API keys for AI and embeddings
   - Or use same API key for both
   - Support for free embedding options (Hugging Face)

4. **Semantic Search**
   - Cosine similarity matching
   - Configurable top-K retrieval
   - Similarity threshold filtering

5. **Cloud AI Integration**
   - Works with all cloud providers (Google, OpenAI, Anthropic, NVIDIA, Azure)
   - Streaming responses with RAG context
   - Source citation in responses

## 🚀 Getting Started

### Option 1: Use the Example Interface

1. Start the DualMind server:
```bash
./dualmind.sh start
```

2. Open the Cloud RAG example:
```
http://localhost:8000/examples/cloud_rag_example.html
```

3. Configure your settings:
   - Enter AI API key
   - Select AI provider and model
   - Select embedding provider and model
   - Optionally enter separate embedding API key

4. Upload documents and start chatting!

### Option 2: API Integration

Integrate RAG into your own application using our API endpoints.

## 📡 API Endpoints

### 1. Get Embedding Providers

```http
GET /api/rag/embedding-providers
```

**Response:**
```json
{
  "providers": {
    "openai": {
      "name": "OpenAI Embeddings",
      "models": [...],
      "requires_api_key": true
    },
    ...
  }
}
```

### 2. Upload Document

```http
POST /api/rag/upload
```

**Request Body:**
```json
{
  "filename": "document.pdf",
  "content": "base64_encoded_content",
  "session_id": "your_session_id",
  "embedding_provider": "openai",
  "embedding_model": "text-embedding-3-small",
  "embedding_api_key": "your_embedding_api_key"
}
```

**Response:**
```json
{
  "success": true,
  "doc_id": "abc123",
  "filename": "document.pdf",
  "chunks": 45,
  "message": "Document processed successfully with 45 chunks"
}
```

### 3. List Documents

```http
GET /api/rag/documents/{session_id}
```

**Response:**
```json
{
  "documents": [
    {
      "id": "abc123",
      "filename": "document.pdf",
      "chunk_count": 45,
      "upload_time": "2024-01-15T10:30:00",
      "size": 15000
    }
  ],
  "total": 1
}
```

### 4. Delete Document

```http
DELETE /api/rag/document
```

**Request Body:**
```json
{
  "session_id": "your_session_id",
  "doc_id": "abc123"
}
```

### 5. Clear All Documents

```http
DELETE /api/rag/documents/{session_id}
```

### 6. RAG-Enhanced Chat (Streaming)

```http
POST /api/rag/chat/stream
```

**Request Body:**
```json
{
  "message": "What does the document say about AI?",
  "api_key": "your_ai_api_key",
  "provider": "nvidia",
  "model": "meta/llama-3.1-8b-instruct",
  "session_id": "your_session_id",
  "embedding_provider": "openai",
  "embedding_model": "text-embedding-3-small",
  "embedding_api_key": "your_embedding_api_key",
  "use_rag": true,
  "top_k": 3
}
```

**Response (Server-Sent Events):**
```
data: {"type": "rag_info", "chunks_used": 3, "sources": ["document.pdf"]}

data: {"type": "chunk", "content": "According "}

data: {"type": "chunk", "content": "to "}

data: {"type": "done", "full_response": "...", "rag_used": true, "sources": ["document.pdf"]}
```

## 💡 Embedding Provider Comparison

| Provider | Best For | Cost | API Key Required | Notes |
|----------|----------|------|------------------|-------|
| **OpenAI** | General purpose | Low | Yes | Fast, reliable, good quality |
| **Google AI** | Integration with Gemini | Free | Yes | Free tier available |
| **Cohere** | Multilingual | Low | Yes | Excellent for non-English |
| **Voyage AI** | Specialized tasks | Medium | Yes | Code-optimized models available |
| **Hugging Face** | No-cost solution | Free | No | Self-hosted, requires server resources |

## 🔧 Configuration

### Recommended Combinations

**For Best Quality:**
- AI: OpenAI GPT-4o or Anthropic Claude 3.5
- Embeddings: OpenAI text-embedding-3-large
- Cost: Medium

**For Best Value:**
- AI: NVIDIA (Free tier)
- Embeddings: Google AI embedding-001 (Free)
- Cost: Free

**For Privacy:**
- AI: Any cloud provider
- Embeddings: Hugging Face (self-hosted)
- Cost: Infrastructure only

**For Multilingual:**
- AI: Google Gemini or Anthropic Claude
- Embeddings: Cohere embed-multilingual-v3.0
- Cost: Medium

## 📝 Usage Examples

### JavaScript Example

```javascript
// Upload a document
async function uploadDocument(file) {
  const reader = new FileReader();
  reader.onload = async (e) => {
    const base64Content = btoa(e.target.result);
    
    const response = await fetch('/api/rag/upload', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        filename: file.name,
        content: base64Content,
        session_id: 'my_session',
        embedding_provider: 'openai',
        embedding_model: 'text-embedding-3-small',
        embedding_api_key: 'sk-...'
      })
    });
    
    const result = await response.json();
    console.log(result);
  };
  reader.readAsBinaryString(file);
}

// Chat with RAG
async function chatWithRAG(message) {
  const response = await fetch('/api/rag/chat/stream', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      message: message,
      api_key: 'your_ai_key',
      provider: 'nvidia',
      model: 'meta/llama-3.1-8b-instruct',
      session_id: 'my_session',
      embedding_provider: 'openai',
      embedding_model: 'text-embedding-3-small',
      embedding_api_key: 'your_embedding_key',
      use_rag: true,
      top_k: 3
    })
  });
  
  // Handle streaming response
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  
  while (true) {
    const {done, value} = await reader.read();
    if (done) break;
    
    const chunk = decoder.decode(value);
    // Process SSE events
    console.log(chunk);
  }
}
```

### Python Example

```python
import requests
import base64

# Upload document
def upload_document(filename, filepath):
    with open(filepath, 'rb') as f:
        content = base64.b64encode(f.read()).decode()
    
    response = requests.post('http://localhost:8000/api/rag/upload', json={
        'filename': filename,
        'content': content,
        'session_id': 'my_session',
        'embedding_provider': 'openai',
        'embedding_model': 'text-embedding-3-small',
        'embedding_api_key': 'sk-...'
    })
    
    return response.json()

# Chat with RAG
def chat_with_rag(message):
    response = requests.post('http://localhost:8000/api/rag/chat/stream', 
        json={
            'message': message,
            'api_key': 'your_ai_key',
            'provider': 'nvidia',
            'model': 'meta/llama-3.1-8b-instruct',
            'session_id': 'my_session',
            'embedding_provider': 'openai',
            'embedding_model': 'text-embedding-3-small',
            'embedding_api_key': 'your_embedding_key',
            'use_rag': True,
            'top_k': 3
        },
        stream=True
    )
    
    for line in response.iter_lines():
        if line.startswith(b'data: '):
            data = json.loads(line[6:])
            print(data)
```

## 🔍 How It Works

### Document Processing Flow

1. **Upload**: Client sends file with base64 encoding
2. **Extract**: Server extracts text (supports PDF, DOCX, TXT, MD)
3. **Chunk**: Text split into ~500 character chunks with overlap
4. **Embed**: Each chunk embedded using selected provider
5. **Store**: Document stored with chunks and embeddings

### Query Flow

1. **Question**: User asks a question
2. **Embed**: Question embedded using same embedding model
3. **Search**: Cosine similarity calculated with all chunks
4. **Retrieve**: Top-K most similar chunks retrieved
5. **Augment**: Chunks added as context to AI prompt
6. **Generate**: AI generates answer based on context
7. **Stream**: Response streamed back to client with sources

## 🛠️ Advanced Configuration

### Chunking Parameters

Modify in `document_processor.py`:
```python
chunker = DocumentChunker(
    chunk_size=500,      # Characters per chunk
    chunk_overlap=50     # Overlap between chunks
)
```

### Search Parameters

Adjust in API request:
```json
{
  "top_k": 5,              // Number of chunks to retrieve
  "similarity_threshold": 0.3  // Minimum similarity score
}
```

### Storage

Documents stored in `./rag_storage/` directory:
- One JSON file per session
- Includes chunks and embeddings
- Persistent across server restarts

## 🐛 Troubleshooting

### Document Upload Fails
- Check file size (recommend < 10MB)
- Verify file format is supported
- Ensure embedding API key is valid

### No RAG Context Retrieved
- Upload at least one document first
- Check if question relates to document content
- Lower similarity_threshold if needed

### Embedding Errors
- Verify API key is correct for embedding provider
- Check API rate limits
- Try a different embedding provider

### Slow Response
- Reduce top_k parameter
- Use faster embedding model (e.g., text-embedding-3-small)
- Use smaller documents or fewer chunks

## 💰 Cost Considerations

### OpenAI Embeddings
- text-embedding-3-small: $0.02 per 1M tokens
- text-embedding-3-large: $0.13 per 1M tokens

### Cohere Embeddings
- embed-english-v3.0: $0.10 per 1M tokens
- embed-multilingual-v3.0: $0.10 per 1M tokens

### Free Options
- Google AI: Free tier available
- Hugging Face: Self-hosted (infrastructure cost only)

**Tip**: For cost savings, use free embedding providers (Google or Hugging Face) with any AI provider.

## 🎯 Best Practices

1. **Document Size**: Keep documents under 10MB for best performance
2. **Chunk Size**: Default 500 characters works well for most cases
3. **Top-K**: Start with 3-5 chunks, adjust based on results
4. **API Keys**: Use separate keys for better tracking and limits
5. **Sessions**: Use consistent session IDs for persistent document access
6. **Cleanup**: Clear documents when done to save storage

## 📚 Additional Resources

- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [Cohere Embeddings](https://docs.cohere.com/docs/embeddings)
- [Google AI Embeddings](https://ai.google.dev/docs/embeddings_guide)
- [Voyage AI Documentation](https://docs.voyageai.com/)
- [Sentence Transformers](https://www.sbert.net/)

## 🔮 Future Enhancements

- [ ] Support for images in documents (OCR)
- [ ] Advanced chunking strategies (semantic chunking)
- [ ] Vector database integration (Pinecone, Weaviate)
- [ ] Multi-document cross-referencing
- [ ] Document summarization
- [ ] Metadata filtering
- [ ] Hybrid search (keyword + semantic)

---

**Questions or issues?** Open an issue on GitHub or consult the main [README.md](README.md) for general DualMind documentation.

