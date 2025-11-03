# DualMind AI

> **Intelligent AI Assistant with Dual Modes: Cloud & Local**  
> Available on Web and Mobile platforms with advanced RAG capabilities.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React Native](https://img.shields.io/badge/React_Native-Expo-blue.svg)](https://expo.dev/)

---

## 🚀 Quick Start

### Web Application

```bash
# Start the server
./dualmind.sh start

# Open browser
open http://localhost:8000
```

That's it! Choose **Cloud Mode** (with API key) or **Local Mode** (no API key required).

### Mobile Application

```bash
# Setup (one-time)
./setup_mobile.sh

# Start backend
./dualmind.sh start

# Start mobile app (in new terminal)
cd mobile && npm start
```

Scan QR code with **Expo Go** app ([iOS](https://apps.apple.com/app/expo-go/id982107779) | [Android](https://play.google.com/store/apps/details?id=host.exp.exponent))

---

## ✨ Features

### 🌐 Web Platform

#### Cloud Mode (☁️)
- **Multi-Provider Support**: Google AI, OpenAI, Anthropic, NVIDIA, Azure
- **30+ AI Models**: GPT-4o, Claude 3.5 Sonnet, Gemini 2.0, Llama 3.1, and more
- **RAG Support**: Upload documents, 5 embedding providers (OpenAI, Google, Cohere, Voyage AI, Hugging Face)
- **Dynamic Model Selection**: Choose optimal models for your task
- **Streaming Responses**: Real-time token streaming
- **Secure Storage**: API keys encrypted in localStorage

#### Local Mode (🔒)
- **100% Privacy**: Runs entirely in your browser via WebGPU
- **No API Key Required**: Zero registration, zero tracking
- **Offline Capable**: Works after initial model download
- **Multiple Models**: TinyLlama, Phi-3, Llama 3.2, Qwen2.5, SmolLM2
- **Local RAG**: Document Q&A with 6 Transformers.js embedding models
- **Custom Memory**: Set personalized AI instructions

#### User Experience
- **📝 Markdown & Code Highlighting**: Beautiful syntax rendering
- **💾 Export Conversations**: JSON & Markdown formats
- **🎤 Voice Input**: Web Speech API integration
- **🔄 Regenerate Responses**: Get alternative answers
- **🌙 Dark Mode**: Persistent theme with smooth animations
- **📁 Chat History**: Save, load, and manage conversations

### 📱 Mobile Platform

- **Native iOS & Android**: Built with React Native/Expo
- **Cloud Mode Integration**: All cloud providers accessible
- **Secure Storage**: Biometric authentication & encrypted keys
- **Offline Support**: Local conversations cached
- **Touch-Optimized UI**: Native mobile components
- **Cross-Platform**: Single codebase for both platforms

---

## 📁 Project Structure

```
DualMind/
├── 🌐 WEB APPLICATION
│   ├── server.py                    # FastAPI backend
│   ├── dualmind.sh                  # Server manager (start/stop/status)
│   ├── branding_config.py           # Customization config
│   ├── cloud_providers.py           # Multi-cloud integration
│   ├── model_fetcher.py             # Dynamic model loading
│   ├── embedding_service.py         # RAG embedding service
│   ├── document_processor.py        # Document processing for RAG
│   ├── requirements.txt             # Python dependencies
│   └── static/
│       ├── css/local.css            # Modular CSS
│       ├── js/                      # Modular JavaScript
│       │   ├── app.js               # Main coordinator
│       │   ├── config.js            # Configuration
│       │   ├── storage.js           # Storage manager
│       │   ├── ui.js                # UI manager
│       │   ├── chat.js              # Chat manager
│       │   ├── models.js            # Model manager
│       │   └── rag.js               # RAG manager
│       ├── local.html               # Local mode UI
│       └── embedding_models.json    # Embedding config
│
├── 📱 MOBILE APPLICATION
│   ├── mobile/
│   │   ├── App.js                   # Main entry point
│   │   ├── app.json                 # Expo configuration
│   │   ├── package.json             # Dependencies
│   │   └── src/
│   │       ├── config/              # API & branding config
│   │       ├── services/            # API client
│   │       ├── screens/             # Mobile screens
│   │       └── components/          # React Native components
│   └── setup_mobile.sh              # Setup script
│
├── 🧪 TESTS
│   ├── tests/
│   │   ├── unit/                    # Unit tests
│   │   ├── integration/             # Integration tests
│   │   ├── ui/                      # UI tests
│   │   └── README.md                # Testing documentation
│   └── pytest.ini                   # Pytest configuration
│
├── 📚 DOCUMENTATION
│   ├── README.md                    # This file
│   ├── ADVANCED_FEATURES.md         # Feature documentation
│   ├── RAG_GUIDE.md                 # Local RAG guide
│   ├── CLOUD_RAG_GUIDE.md           # Cloud RAG guide
│   └── EXPO_CONNECTION_GUIDE.md     # Mobile setup guide
│
└── 📦 EXAMPLES
    ├── examples/
    │   ├── cloud_rag_example.html   # Cloud RAG demo
    │   └── README.md                # Examples documentation
```

---

## 🎯 How It Works

### Cloud Mode (☁️)

1. **Select Provider** → Choose from Google, OpenAI, Anthropic, NVIDIA, or Azure
2. **Choose Model** → Browse 30+ models with recommendations
3. **Enter API Key** → Your key, your control (stored locally)
4. **Start Chatting** → Fast, powerful AI responses

**Optional RAG**: Upload documents → Select embedding provider → Ask questions about your files

### Local Mode (🔒)

1. **Choose Model** → TinyLlama (600MB), Phi-3 (2GB), or others
2. **Download Once** → Model cached in browser
3. **Chat Privately** → Everything runs in your browser
4. **Work Offline** → No internet needed after download

**Optional RAG**: Upload documents → Select embedding model → Semantic search powered by Transformers.js

---

## 🔑 Getting API Keys (Cloud Mode Only)

DualMind supports multiple AI providers. Choose based on your needs:

| Provider | Free Tier | Get API Key |
|----------|-----------|-------------|
| **Google AI** | ✅ 60 req/min | [Get Key](https://aistudio.google.com/apikey) |
| **OpenAI** | ❌ Credit card required | [Get Key](https://platform.openai.com/api-keys) |
| **Anthropic** | ❌ Credit card required | [Get Key](https://console.anthropic.com/) |
| **NVIDIA** | ✅ Free endpoints | [Get Key](https://build.nvidia.com/) |
| **Azure OpenAI** | ❌ Azure subscription | [Get Access](https://azure.microsoft.com/products/ai-services/openai-service) |

**Recommended for Beginners**: Start with **Google AI** (Gemini) - generous free tier, no credit card needed.

---

## 📊 API Endpoints

### Core Endpoints

```bash
# Chat with streaming
POST /api/chat
{
  "message": "Hello!",
  "api_key": "your_key",
  "provider": "google",
  "model": "gemini-2.0-flash-exp",
  "session_id": "optional"
}

# Get available providers
GET /api/providers

# Get models for provider
GET /api/providers/{provider_id}/models

# Health check
GET /health
```

### RAG Endpoints

```bash
# Upload document for RAG
POST /api/rag/upload

# List documents
GET /api/rag/documents/{session_id}

# Chat with RAG context
POST /api/rag/chat/stream

# Get embedding providers
GET /api/rag/embedding-providers

# Get embedding models
GET /api/rag/embedding-models/{provider}
GET /api/local/embedding-models
```

---

## 🎨 Customization

Want to rebrand DualMind? Everything is configurable in `branding_config.py`:

```python
# Change name and icon
CHATBOT_NAME = "MyAI Assistant"
CHATBOT_ICON = "🤖"

# Customize colors
COLOR_PRIMARY_START = "#667eea"
COLOR_PRIMARY_END = "#764ba2"

# Update messages
WELCOME_MESSAGE_CLOUD = "Welcome to MyAI!"
WELCOME_MESSAGE_LOCAL = "Your private AI assistant"
```

Over 100+ customizable variables for complete branding control.

---

## 🚀 Deployment

### Web Application

**Development**:
```bash
python3 server.py
```

**Production (Gunicorn)**:
```bash
pip install gunicorn
gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Docker**:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "server.py"]
```

**Cloud Platforms**:
- **Google Cloud Run**: `gcloud run deploy --source .`
- **Railway**: Connect GitHub repository
- **Heroku**: `git push heroku main`
- **AWS ECS**: Deploy with Docker image

### Mobile Application

**Development**:
```bash
cd mobile && npm start
```

**Production Builds**:
```bash
# Android APK
eas build --platform android

# iOS IPA (requires Apple Developer account)
eas build --platform ios
```

**Over-The-Air Updates**:
```bash
eas update --branch production
```

---

## 🔒 Security

### Web Platform
- ✅ API keys stored client-side only (localStorage)
- ✅ Keys never transmitted to our servers
- ✅ HTTPS required for production
- ✅ Local mode: Zero data transmission
- ✅ No tracking, no analytics, no telemetry

### Mobile Platform
- ✅ Encrypted storage (React Native SecureStore)
- ✅ Biometric authentication (Face ID, Touch ID, Fingerprint)
- ✅ SSL certificate pinning (optional)
- ✅ App sandboxing for data isolation
- ✅ Auto-lock for sensitive sessions

---

## 🧪 Testing

```bash
# Install test dependencies
pip install -r tests/requirements-test.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test suite
pytest tests/unit/
pytest tests/integration/
pytest tests/ui/
```

See `tests/README.md` for comprehensive testing documentation.

---

## 💡 Tips & Best Practices

### Web Application
- **Model Selection**: Start with recommended models (marked with ⭐)
- **Local Mode**: Download models on fast WiFi (600MB - 2GB)
- **Browser**: Use Chrome 113+ or Edge for WebGPU support
- **Storage**: Clear browser data to reset settings
- **Performance**: Local mode works best with dedicated GPU

### Mobile Application
- **Setup**: Run `./setup_mobile.sh` before first use
- **Network**: Ensure phone and computer on same WiFi for testing
- **IP Address**: Update API URL in `mobile/src/config/api.js` for real devices
- **Caching**: Run `expo start -c` if you encounter issues
- **Testing**: Use physical device for biometric features

### RAG (Document Q&A)
- **Cloud RAG**: Best for production, supports multiple embedding providers
- **Local RAG**: Best for privacy, uses Transformers.js (browser-based)
- **Document Size**: Keep documents under 10MB for optimal performance
- **Chunking**: System automatically chunks documents for better retrieval

---

## 🐛 Troubleshooting

### Server Issues

**Port already in use**:
```bash
lsof -ti:8000 | xargs kill
# Or use different port
PORT=8001 python3 server.py
```

**Server won't start**:
```bash
# Check status
./dualmind.sh status

# View logs
./dualmind.sh logs

# Restart
./dualmind.sh restart
```

### Mobile Issues

**Cannot connect to backend**:
1. Check backend is running: `./dualmind.sh status`
2. Verify IP address in `mobile/src/config/api.js`
3. Ensure same WiFi network
4. Check firewall allows port 8000

**QR code not showing**:
```bash
cd mobile
npx expo start -c  # Clear cache
```

**Module errors**:
```bash
cd mobile
rm -rf node_modules
npm install
npx expo start
```

### Browser Issues

**Local mode not loading**:
- Update to Chrome 113+ or Edge 113+
- Enable WebGPU (check `chrome://flags/#enable-webgpu`)
- Clear browser cache
- Verify sufficient disk space

**API key not saving**:
- Enable cookies/localStorage
- Disable blocking extensions
- Try incognito mode
- Use different browser

---

## 📖 Documentation

- **[ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)** - Markdown, voice input, dark mode, export, chat history
- **[RAG_GUIDE.md](RAG_GUIDE.md)** - Local RAG implementation with Transformers.js
- **[CLOUD_RAG_GUIDE.md](CLOUD_RAG_GUIDE.md)** - Cloud RAG with multiple embedding providers
- **[EXPO_CONNECTION_GUIDE.md](EXPO_CONNECTION_GUIDE.md)** - Mobile connection troubleshooting
- **[tests/README.md](tests/README.md)** - Testing documentation

---

## 🛠️ Technology Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI server
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation

### Frontend (Web)
- **[WebLLM](https://webllm.mlc.ai/)** - Browser-based LLM inference
- **[Transformers.js](https://huggingface.co/docs/transformers.js)** - Local embeddings
- **Vanilla JavaScript** - Modular, no framework overhead
- **Modern CSS** - Responsive, animations, dark mode

### Mobile
- **[React Native](https://reactnative.dev/)** - Cross-platform framework
- **[Expo](https://expo.dev/)** - Development & deployment platform
- **SecureStore** - Encrypted storage
- **Biometrics** - Authentication

### AI Integrations
- **Google AI (Gemini)** - Generative AI
- **OpenAI (GPT)** - Language models
- **Anthropic (Claude)** - Conversational AI
- **NVIDIA AI** - Inference endpoints
- **Azure OpenAI** - Enterprise AI

---

## 🎯 What's Next?

### Planned Features
- [ ] Function calling & tools integration
- [ ] Multi-agent systems
- [ ] Conversation search & filtering
- [ ] Image understanding (multimodal)
- [ ] Multi-language voice support
- [ ] Team collaboration features
- [ ] Enterprise authentication
- [ ] Usage analytics dashboard

### Mobile Enhancements
- [ ] Feature parity with web
- [ ] Local Mode via WebView
- [ ] Push notifications
- [ ] Image/camera integration
- [ ] Widget support
- [ ] Apple Watch / Wear OS apps

---

## 📝 License

MIT License - Open source, free to use and modify.

---

## 🌟 About

**DualMind AI** is a comprehensive, cross-platform AI assistant that prioritizes user control and privacy.

### Why DualMind?

✨ **Choice**: Cloud (fast) or Local (private)  
🌐 **Cross-Platform**: Web and mobile  
🔒 **Privacy**: Your data, your device  
🎨 **Customizable**: Rebrand in minutes  
🚀 **Easy**: One command to start  
📚 **RAG**: Chat with your documents  

### Perfect For

- 👨‍💻 **Developers**: Learn AI integration, customize everything
- 🏢 **Enterprises**: Self-host, maintain privacy, enterprise features
- 🎓 **Students**: Experiment with 30+ AI models
- 🔐 **Privacy-Conscious**: Local mode for sensitive data
- 📱 **Mobile Users**: Native iOS/Android experience

---

**Made with ❤️ for the AI community**

[![GitHub stars](https://img.shields.io/github/stars/pawoPawan/DualMind?style=social)](https://github.com/pawoPawan/DualMind)
[![GitHub forks](https://img.shields.io/github/forks/pawoPawan/DualMind?style=social)](https://github.com/pawoPawan/DualMind/fork)

**Star ⭐ this project if you find it useful!**

---

### Quick Reference

```bash
# Web: Start server
./dualmind.sh start

# Web: Check status  
./dualmind.sh status

# Web: Stop server
./dualmind.sh stop

# Mobile: Setup
./setup_mobile.sh

# Mobile: Start
cd mobile && npm start

# Tests: Run all
pytest
```

**Documentation**: Browse `/docs` endpoint when server is running: `http://localhost:8000/docs`
