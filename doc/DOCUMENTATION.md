# DualMind - Complete Documentation

**Version**: 2.0.0  
**Last Updated**: November 3, 2025

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Features Overview](#features-overview)
3. [Local Mode Guide](#local-mode-guide)
4. [Cloud Mode Guide](#cloud-mode-guide)
5. [RAG (Document Q&A)](#rag-document-qa)
6. [Advanced Features](#advanced-features)
7. [Mobile App](#mobile-app)
8. [API Reference](#api-reference)
9. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Installation

```bash
# Clone repository
git clone <your-repo-url>
cd DualMind

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r doc/requirements.txt

# Start server
./dualmind.sh start

# Access application
# Local Mode: http://localhost:8000/local
# Cloud Mode: http://localhost:8000/cloud
```

### Server Management

```bash
./dualmind.sh start      # Start server
./dualmind.sh stop       # Stop server
./dualmind.sh restart    # Restart server
./dualmind.sh status     # Check status
./dualmind.sh logs       # View logs
```

---

## Features Overview

### Core Features

#### 🎨 **Dual Mode Architecture**
- **Local Mode**: Run AI models directly in your browser using WebLLM (no API keys needed)
- **Cloud Mode**: Connect to 5 cloud providers (Google, OpenAI, Anthropic, NVIDIA, Azure)
- Switch seamlessly between modes

#### 💬 **Chat Management**
- Create unlimited chats
- Rename chats
- Delete individual chats
- Switch between chats
- Export conversations (Markdown)
- Chat history with timestamps

#### 🎨 **User Interface**
- Modern, responsive design
- Dark/Light mode toggle
- Markdown rendering with code highlighting
- Real-time typing indicators
- Message actions (copy, regenerate)
- Tooltips on all icons
- Empty states and loading indicators

#### 🗣️ **Voice & Input**
- Voice input support (Web Speech API)
- Enter key to send messages
- Multi-line input support
- Auto-focus on input

#### ⚙️ **Settings Panel**
- Dark mode toggle
- Custom memory (system prompt)
- Per-chat context
- Clear all chats

#### 📚 **RAG (Retrieval Augmented Generation)**
- Upload documents per chat
- Automatic document embedding
- Semantic search
- Real-time progress indicators
- Per-chat document isolation
- Automatic cleanup on deletion
- Knowledge Base statistics

---

## Local Mode Guide

### What is Local Mode?

Local Mode runs AI models entirely in your browser using WebLLM and WebGPU. **No API keys required!** Models run on your GPU for fast inference while maintaining complete privacy.

### System Requirements

- **Browser**: Chrome/Edge 113+ with WebGPU support
- **GPU**: 6GB+ VRAM recommended
- **RAM**: 8GB+ system memory
- **Storage**: ~4GB for model downloads

### Check WebGPU Support

```javascript
// Visit: chrome://gpu
// Look for "WebGPU: Enabled"
```

Or open console in browser:
```javascript
navigator.gpu ? console.log("✅ WebGPU Supported") : console.log("❌ Not Supported");
```

### Getting Started

1. **Open Local Mode**
   ```
   http://localhost:8000/local
   ```

2. **Select a Model**
   - Click the model selector button
   - Choose from available models:
     - **Llama-3.2-3B** (Fast, 3GB) - Best for speed
     - **Llama-3.1-8B** (Balanced, 5GB) - Best balance
     - **Qwen2.5-7B** (Quality, 5GB) - High quality
     - **Gemma-2-9B** (Large, 6GB) - Best results

3. **Wait for Download**
   - First time: Model downloads (progress shown)
   - Future use: Cached in browser

4. **Start Chatting!**
   - Model loads automatically
   - Type your message
   - Press Enter or click send button

### Local Mode Features

#### Model Selection
- Dynamic model loading
- Download progress with percentage
- Model caching for faster subsequent loads
- Input disabled during download

#### RAG in Local Mode
- 6 Transformers.js embedding models:
  - **all-MiniLM-L6-v2** - Fast, good for speed
  - **all-mpnet-base-v2** - Best quality
  - **BGE-small-en-v1.5** - Balanced
  - **BGE-base-en-v1.5** - High quality
  - **GTE-small** - Fast multilingual
  - **E5-small-multilingual** - Multilingual support

#### Upload Documents
1. Click 📎 (attachment) icon
2. Select documents (TXT, MD, PDF, DOC, DOCX)
3. Wait for processing (progress shown):
   - Reading document
   - Chunking text
   - Generating embeddings
   - Indexing chunks
4. Documents linked to current chat
5. Ask questions using uploaded content!

#### Progress Indicators
- "📚 Initializing document processing..."
- "🔄 Loading embedding model..."
- "📄 Reading [filename]..."
- "✂️ Splitting into chunks..."
- "🧮 Indexing: X/Y chunks..."
- "✅ [filename] indexed: N chunks, M words"

---

## Cloud Mode Guide

### What is Cloud Mode?

Cloud Mode connects to cloud AI providers using their APIs. More powerful models with API key authentication.

### Supported Providers

1. **Google AI (Gemini)**
   - Models: gemini-1.5-pro, gemini-1.5-flash
   - Get key: https://makersuite.google.com/app/apikey

2. **OpenAI (GPT)**
   - Models: gpt-4o, gpt-4-turbo, gpt-3.5-turbo
   - Get key: https://platform.openai.com/api-keys

3. **Anthropic (Claude)**
   - Models: claude-3-5-sonnet, claude-3-opus
   - Get key: https://console.anthropic.com/

4. **NVIDIA**
   - Models: Various NVIDIA models
   - Get key: https://build.nvidia.com/

5. **Azure OpenAI**
   - Models: GPT models via Azure
   - Get key: https://portal.azure.com/

### Getting Started

1. **Open Cloud Mode**
   ```
   http://localhost:8000/cloud
   ```

2. **Select Provider & Model**
   - Click model selector
   - Choose provider (e.g., Google)
   - Select model (e.g., gemini-1.5-pro)

3. **Enter API Key**
   - Click "Change API Key"
   - Paste your API key
   - Key stored in browser localStorage

4. **Start Chatting!**
   - Type your message
   - API processes request
   - Streaming response displayed

### Cloud RAG

#### Embedding Providers
- **OpenAI** - text-embedding-3-small/large
- **Google AI** - text-embedding-004
- **Cohere** - embed-english-v3.0
- **Voyage AI** - voyage-2, voyage-large-2
- **Hugging Face** - sentence-transformers models

#### Upload Documents
1. Click 📎 icon
2. Select embedding provider
3. Upload documents
4. Server processes and embeds
5. Ask questions using content!

#### RAG API Endpoints

**Upload Document:**
```bash
POST /api/rag/upload
{
  "filename": "pricing.txt",
  "content": "base64_encoded_content",
  "session_id": "abc123",
  "embedding_provider": "openai",
  "embedding_api_key": "sk-..."
}
```

**List Documents:**
```bash
GET /api/rag/documents/{session_id}
```

**Delete Document:**
```bash
DELETE /api/rag/document
{
  "session_id": "abc123",
  "doc_id": "doc_id_here"
}
```

**RAG Chat:**
```bash
POST /api/rag/chat/stream
{
  "message": "What are your prices?",
  "api_key": "your_key",
  "provider": "google",
  "session_id": "abc123",
  "use_rag": true,
  "top_k": 3
}
```

---

## RAG (Document Q&A)

### What is RAG?

RAG (Retrieval Augmented Generation) allows the AI to answer questions based on your uploaded documents. It combines:
1. **Document Upload** - Upload your files
2. **Chunking** - Split into manageable pieces
3. **Embedding** - Convert to vectors
4. **Search** - Find relevant chunks
5. **Generation** - AI answers using found content

### Per-Chat Document Management

**Key Features:**
- ✅ Each chat has its own documents
- ✅ Documents isolated per chat
- ✅ Switch chats = switch documents
- ✅ New chats start with 0 documents
- ✅ Delete chat = delete documents
- ✅ Clear all chats = clear all documents

### Usage Example

**Scenario: Support Documentation**

1. **Create Chat: "Product Support"**
   - Upload: `pricing.pdf`, `features.md`, `faq.txt`
   - Ask: "What's the pricing for enterprise?"
   - AI uses pricing.pdf to answer

2. **Create Chat: "Development Docs"**
   - Upload: `api-reference.md`, `setup-guide.md`
   - Ask: "How do I authenticate?"
   - AI uses api-reference.md to answer
   - Does NOT see pricing.pdf from other chat

3. **Switch to "Product Support"**
   - Still has pricing.pdf, features.md, faq.txt
   - Ask follow-up questions
   - Documents persisted

4. **Delete "Product Support"**
   - Chat deleted
   - All 3 documents deleted
   - "Development Docs" unaffected

### Document Processing Flow

```
1. User uploads document
   ↓
2. Extract text (PDF, DOC, etc.)
   ↓
3. Split into chunks (500 chars, 50 overlap)
   ↓
4. Generate embeddings (vector representations)
   ↓
5. Store with chat ID
   ↓
6. User asks question
   ↓
7. Embed question
   ↓
8. Search chunks (cosine similarity)
   ↓
9. Retrieve top K chunks
   ↓
10. Inject into prompt
   ↓
11. AI generates answer
```

### Progress Indicators

When uploading documents, you'll see:
- 📚 **Initializing document processing...**
- 🔄 **Loading embedding model...**
- 📄 **Reading [filename]...**
- ✂️ **Splitting into chunks...**
- 🧮 **Indexing: 1/15 chunks...**
- 🧮 **Indexing: 15/15 chunks...**
- ✅ **pricing.txt indexed: 15 chunks, 245 words**

When using RAG:
- 🔍 **Searching knowledge base...**
- 📚 **Found relevant information, generating answer...**

Console shows:
```
📚 RAG: Using 3 relevant chunks:
  1. pricing.txt (similarity: 0.872)
  2. features.md (similarity: 0.745)
  3. faq.txt (similarity: 0.623)
```

### Knowledge Base Modal

View your documents:
- **Summary**: `📊 2 document(s) | 🧩 30 chunks | 📝 487 words`
- **Per Document**:
  - Filename
  - Chunk count
  - Word count
  - Timestamp
  - Remove button

---

## Advanced Features

### 1. Custom Memory (System Prompt)

Set persistent instructions for the AI:

**Settings → Custom Memory**
```
You are a helpful assistant specialized in software development.
Always provide code examples and explain technical concepts clearly.
```

This is included in every message to the AI.

### 2. Per-Chat Context

Set context for specific chat:

**Settings → Chat Context**
```
This chat is about the Q4 marketing campaign.
Budget: $50k, Target: Young professionals
```

Only applies to current chat.

### 3. Dark Mode

Toggle between light and dark themes:
- **Settings → Dark Mode Toggle**
- Persisted in localStorage
- Smooth transition animations

### 4. Export Conversations

Export chat as Markdown:
1. Click export button
2. Choose location
3. Saves as `dualmind-chat-[timestamp].md`

Format:
```markdown
# DualMind Conversation

**Date**: 2025-11-03

## Message 1
**User**: Hello!

**Assistant**: Hi! How can I help?
```

### 5. Voice Input

Speak your messages:
1. Click microphone icon
2. Allow microphone access
3. Speak your message
4. Text appears in input
5. Click send or continue editing

### 6. Message Actions

**Copy Message**: Click copy icon
**Regenerate Response**: Click regenerate icon (re-asks last question)

### 7. Code Highlighting

Code blocks automatically highlighted:

```python
def hello():
    print("Hello, DualMind!")
```

Supports: Python, JavaScript, Java, C++, HTML, CSS, JSON, and more.

### 8. Markdown Rendering

Full Markdown support:
- **Bold**, *italic*, `code`
- Lists (bullet, numbered)
- Links: [DualMind](https://example.com)
- Headers, blockquotes, tables
- Images

---

## Mobile App

### Overview

DualMind includes a React Native/Expo mobile app for iOS and Android.

**Location**: `learn/mobile/`

### Features

- Chat with AI on mobile
- Cloud Mode support
- Voice input
- Dark mode
- Chat history sync

### Setup

```bash
cd learn/mobile
npm install
npx expo start
```

### Connection Guide

**Quick Setup:**
1. Ensure backend is running: `./dualmind.sh start`
2. Start mobile app: `cd mobile && npm start`
3. Scan QR code with Expo Go app
4. If QR doesn't appear, open: `http://localhost:8081`

---

## API Reference

### Health Check

```bash
GET /health

Response:
{
  "status": "healthy",
  "version": "2.0.0"
}
```

### List Providers

```bash
GET /api/providers

Response:
{
  "providers": ["google", "openai", "anthropic", "nvidia", "azure"]
}
```

### Get Provider Models

```bash
GET /api/models/{provider}

Response:
{
  "models": [
    {
      "id": "gemini-1.5-pro",
      "name": "Gemini 1.5 Pro",
      "description": "Most capable model"
    }
  ]
}
```

### Chat (Streaming)

```bash
POST /api/chat

Body:
{
  "message": "Hello!",
  "api_key": "your_key",
  "provider": "google",
  "model": "gemini-1.5-pro",
  "session_id": "abc123"
}

Response: Server-Sent Events (streaming)
```

### Embedding Providers

```bash
GET /api/rag/embedding-providers

Response:
{
  "providers": {
    "openai": {
      "models": ["text-embedding-3-small", "text-embedding-3-large"]
    },
    "google": {
      "models": ["text-embedding-004"]
    }
  }
}
```

### Local Embedding Models

```bash
GET /api/local/embedding-models

Response:
{
  "transformers_js": {
    "source": "Hugging Face Transformers.js",
    "models": [...]
  }
}
```

---

## Troubleshooting

### Local Mode Issues

**Problem**: WebGPU not supported
- **Solution**: Update browser to Chrome/Edge 113+
- Enable: `chrome://flags/#enable-webgpu`

**Problem**: Model download stuck
- **Solution**: Clear browser cache, retry
- Check internet connection
- Try smaller model

**Problem**: Model loading slow
- **Solution**: Normal on first load (downloads ~4GB)
- Subsequent loads are fast (cached)

**Problem**: Out of memory
- **Solution**: Close other tabs
- Try smaller model
- Increase browser memory limit

### Cloud Mode Issues

**Problem**: "Invalid API key"
- **Solution**: Verify key is correct
- Check key has credits/quota
- Ensure key is for correct provider

**Problem**: Rate limit exceeded
- **Solution**: Wait and retry
- Upgrade API plan
- Use different provider

**Problem**: Model not responding
- **Solution**: Check provider status
- Verify model ID is correct
- Try different model

### RAG Issues

**Problem**: Documents not uploading
- **Solution**: Check file size (<10MB recommended)
- Verify file format (TXT, MD, PDF, DOC, DOCX)
- Check console for errors

**Problem**: RAG not finding relevant info
- **Solution**: Use more specific questions
- Upload more relevant documents
- Try different embedding model

**Problem**: "Knowledge Base empty"
- **Solution**: Upload documents for current chat
- Switch to chat with documents
- Re-upload if documents missing

### General Issues

**Problem**: Server won't start
- **Solution**: Check port 8000 available
- Activate virtual environment
- Install dependencies: `pip install -r doc/requirements.txt`

**Problem**: UI not loading
- **Solution**: Verify server running: `./dualmind.sh status`
- Clear browser cache
- Check console for errors

**Problem**: Chat not appearing in sidebar
- **Solution**: Send first message (auto-names chat)
- Refresh page
- Check localStorage not full

---

## Performance Tips

### Local Mode
- Use smaller models on systems with <8GB VRAM
- Close unused browser tabs
- Use Chrome/Edge for best WebGPU performance

### Cloud Mode
- Choose appropriate model for task
- Use streaming for better UX
- Cache API keys securely

### RAG
- Keep documents under 10MB
- Use TXT/MD for fastest processing
- Upload relevant documents only
- Use appropriate embedding model

---

## Security Best Practices

1. **API Keys**: Never share or commit to git
2. **localStorage**: Keys stored client-side only
3. **Documents**: Processed client-side (Local Mode)
4. **Server**: Run behind reverse proxy in production
5. **CORS**: Configure allowed origins appropriately

---

## Development

### Project Structure

```
DualMind/
├── src/                 # Backend source
│   ├── server.py        # FastAPI backend
│   ├── document_processor.py
│   ├── embedding_service.py
│   └── ...
├── static/              # Frontend assets
│   ├── js/              # JavaScript modules
│   ├── css/             # Styling
│   ├── local.html       # Local Mode UI
│   └── cloud.html       # Cloud Mode UI
├── doc/                 # Documentation
│   ├── DOCUMENTATION.md
│   ├── PRODUCTION_READINESS_REPORT.md
│   └── requirements.txt # Python dependencies
├── tests/               # Test suite
└── dualmind.sh          # Management script
```

### Running Tests

```bash
# Quick test
python3 run_rag_tests.py

# Full test suite
pytest tests/ -v

# UI tests (manual)
python3 tests/ui/test_per_chat_rag_ui.py
```

---

## Support & Contributing

### Getting Help
- Check this documentation
- Review `PRODUCTION_READINESS_REPORT.md`
- Check issues on GitHub
- Read source code (well-commented!)

### Contributing
- Fork repository
- Create feature branch
- Make changes
- Add tests
- Submit pull request

---

## License

[Your License Here]

---

## Changelog

### v2.0.0 (2025-11-03)
- ✅ Per-chat document management
- ✅ RAG progress indicators
- ✅ Automatic document cleanup
- ✅ Feature parity (Local/Cloud)
- ✅ Comprehensive testing
- ✅ Production ready

### v1.0.0
- Initial release

---

**DualMind** - AI Chat with Dual Mode Architecture  
Built with ❤️ using FastAPI, WebLLM, and Modern Web Technologies

