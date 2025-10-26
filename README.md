# Dual Mind Chatbot

A beautiful AI-powered chatbot with **dual modes**: Cloud-based (Google ADK) and Local browser-based inference.

🎉 **Two Ways to Chat:**
- ☁️ **Cloud Mode**: Fast responses with Google's Gemini (requires API key)
- 🔒 **Local Mode**: 100% private, runs in your browser (no API key needed!)

Reference: [Google ADK Documentation](https://google.github.io/adk-docs/)

## 🚀 Quick Start

### Option 1: Using Management Script (Recommended) ⭐

```bash
# Start the chatbot
./gauraai.sh start

# Check status
./gauraai.sh status

# Stop when done
./gauraai.sh stop
```

### Option 2: Manual Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server
python3 server.py
```

### 3. Open Your Browser

Visit: **http://localhost:8000**

📖 **Management Commands**: See [MANAGEMENT_GUIDE.md](MANAGEMENT_GUIDE.md) for complete documentation.

### 4. Choose Your Mode

You'll see two options:

**Option A: ☁️ Cloud Mode** (Faster)
- Click "Cloud Mode"
- Select your AI provider (Google, OpenAI, Anthropic, NVIDIA, or Azure)
- Choose your preferred AI model from the list
- Enter your Model access API key (most providers offer FREE tiers!)
- Start chatting with your chosen model!

**Option B: 🔒 Local Mode** (Private, No API Key!)
- Click "Local Mode"
- Choose a model to download (600MB - 2GB)
- Model downloads once and runs in your browser
- 100% private - data never leaves your device
- No API key required!

That's it! Start chatting! 🎉

## ✨ Features

### Cloud Mode (☁️)
- ✅ **Multi-Cloud Providers** - Choose from Google, OpenAI, Anthropic, NVIDIA, Azure
- ✅ **🤖 Dynamic Model Selection** - Select from multiple AI models per provider
- ✅ **Fast Responses** - Powered by cutting-edge AI models
- ✅ **No Downloads** - Start chatting immediately
- ✅ **Model access API Key** - Secure storage in browser localStorage
- ✅ **Recommended Models** - Auto-selection with visual indicators

### Local Mode (🔒) - NEW!
- ✅ **100% Privacy** - Runs entirely in your browser
- ✅ **No API Key Required** - No registration needed
- ✅ **Offline Capable** - Works without internet after download
- ✅ **GGUF Models** - Uses WebLLM with efficient models
- ✅ **Multiple Models** - Choose from TinyLlama, Phi-3, Llama 3.2
- ✅ **📚 RAG Support** - Upload documents and chat with your files! (NEW!)
- ✅ **Local Embeddings** - Semantic search using Transformers.js
- ✅ **Document Management** - Upload, view, delete documents in browser

### Common Features
- ✅ **Modern Web UI** - Beautiful, responsive chat interface
- ✅ **Session Management** - Maintains conversation context
- ✅ **Real-time Chat** - Instant responses with typing indicators
- ✅ **🔄 Enhanced Mode Switching** - Smart dialogs, info banners, smooth transitions
- ✅ **🎨 Fully Customizable** - Change name, colors, text in one file!

## 📁 Project Structure

```
learn/
├── server.py                  # FastAPI server with dual-mode support
├── gauraai.sh                 # 🎯 MANAGEMENT SCRIPT (start/stop/status)
├── branding_config.py         # 🎨 CUSTOMIZE ALL NAMES & COLORS HERE
├── model_manager.py           # Model download manager (optional)
├── agent.py                   # Legacy - not used
├── static/
│   └── index_local.html       # Local mode UI with WebLLM
├── requirements.txt           # Python dependencies
├── .env                       # Optional configuration
├── README.md                  # This file
├── MANAGEMENT_GUIDE.md        # 🎯 Management script documentation
├── CUSTOMIZATION_GUIDE.md     # How to customize everything
├── FEATURES.md                # Detailed feature documentation
├── MODE_SWITCHING_GUIDE.md    # 🔄 Enhanced mode switching guide
├── MODEL_SELECTION_GUIDE.md   # 🤖 Model selection documentation
└── MULTI_CLOUD_GUIDE.md       # ☁️ Multi-cloud provider guide
```

## 🎮 How It Works

### Cloud Mode (☁️):
**First Time:**
1. Open http://localhost:8000
2. Choose "Cloud Mode"
3. Enter your Model access API key
4. Start chatting!

**Next Time:**
- Automatically loads with saved API key
- Switch to Local Mode anytime via header button

### Local Mode (🔒):
**First Time:**
1. Open http://localhost:8000
2. Choose "Local Mode" (or visit http://localhost:8000/local)
3. Select a model (TinyLlama recommended for speed)
4. Model downloads to browser (one-time, ~600MB-2GB)
5. Chat privately - all processing in your browser!

**Next Time:**
- Model is cached in browser
- Loads instantly
- Works offline!

**Available Models:**
- **TinyLlama 1.1B** - Fastest, ~600MB, great for quick responses
- **Phi-3 Mini** - Balanced, ~2GB, Microsoft's powerful model
- **Llama 3.2 1B** - Meta's latest, ~800MB, good quality

## 🤖 Model Selection (NEW!)

**Choose the perfect AI model for your needs!**

### How It Works:
1. **Select Provider** → Choose from 5 cloud providers
2. **View Models** → Models load automatically
3. **Pick Your Model** → Click on any model card
4. **Enter API Key** → Start chatting!

### Available Models by Provider:

#### 🔷 Google AI (Gemini)
- **Gemini 1.5 Flash** ⭐ - Fast and versatile (Recommended)
- Gemini 1.5 Flash-8B - Ultra fast and compact
- Gemini 1.5 Pro - Most capable model
- Gemini 2.0 Flash (Experimental) - Latest experimental
- Gemini Experimental 1206 - Cutting-edge

#### 🟢 OpenAI (GPT)
- **GPT-4o** ⭐ - Most capable GPT-4 model (Recommended)
- GPT-4o Mini - Affordable and fast
- GPT-4 Turbo - Previous flagship
- GPT-3.5 Turbo - Fast and affordable
- o1 Preview & o1 Mini - Advanced reasoning

#### 🟣 Anthropic (Claude)
- **Claude 3.5 Sonnet** ⭐ - Most intelligent (Recommended)
- Claude 3.5 Haiku - Fastest model
- Claude 3 Opus - Powerful reasoning
- Claude 3 Sonnet - Balanced performance
- Claude 3 Haiku - Fast and affordable

#### 🟩 NVIDIA AI
- **Llama 3.1 Nemotron 70B** ⭐ - NVIDIA's flagship (Recommended)
- Llama 3.1 Nemotron 51B - Balanced
- Llama 3.1 405B - Most powerful
- Llama 3.1 70B & 8B - Various sizes

#### 🔵 Microsoft Azure OpenAI
- **GPT-4o (Azure)** ⭐ - Most capable on Azure (Recommended)
- GPT-4 Turbo (Azure) - Azure-hosted GPT-4
- GPT-3.5 Turbo (Azure) - Fast and affordable

### Features:
- ⭐ **Recommended Models** - Auto-selected for easy start
- 🎨 **Beautiful Model Cards** - Interactive selection UI
- 🔄 **Dynamic Loading** - Models fetched on-the-fly
- 📊 **Clear Descriptions** - Know what each model does
- 💡 **Smart Selection** - First recommended model auto-selected

📖 See [MODEL_SELECTION_GUIDE.md](MODEL_SELECTION_GUIDE.md) for complete documentation.

## 🎨 Customization (NEW!)

**Want to change the name, colors, or text?**

All branding is in ONE file: `branding_config.py`

```python
# Change chatbot name
CHATBOT_NAME = "YourBotName"  # Change from "Gaura AI"

# Change colors
COLOR_PRIMARY_START = "#4299e1"  # Your brand color

# Change any text
WELCOME_MESSAGE_CLOUD = "Your custom welcome message!"
```

**100+ customizable variables!**

📖 See [CUSTOMIZATION_GUIDE.md](CUSTOMIZATION_GUIDE.md) for complete guide.

---

## 🔄 Enhanced Mode Switching (NEW!)

**Seamless switching between Cloud and Local modes!**

### Features:
- 📊 **Informative Dialogs** - Detailed comparison before switching
- 💡 **Smart Banners** - Helpful tips (dismissible, remembered)
- 🎨 **Smooth Animations** - Professional slide transitions
- 🔘 **Enhanced Buttons** - Icons and helpful tooltips
- 💾 **Persistent Settings** - Remembers your preferences

### From Cloud Mode:
Click "🔒 Switch to Local Mode" → See comparison → Confirm → Done!

### From Local Mode:
Click "☁️ Switch to Cloud Mode" → See comparison → Confirm → Done!

📖 See [MODE_SWITCHING_GUIDE.md](MODE_SWITCHING_GUIDE.md) for complete details.

---

## 🔑 Getting Your FREE Model Access API Key

### Step-by-Step:

1. **Visit**: https://aistudio.google.com/apikey
2. **Sign in** with your Google account
3. **Click** "Create API Key" (this is your Model access API key)
4. **Copy** your key (starts with `AIza...`)
5. **Paste** into the chatbot popup
6. **Start** chatting!

### FREE Tier Includes:
- ✅ 60 requests per minute
- ✅ 1,500 requests per day
- ✅ No credit card required
- ✅ Access to Gemini 2.0 Flash

## 🎨 UI Features

- 💬 Real-time chat interface
- 🎨 Beautiful gradient design
- 📱 Responsive (works on mobile)
- ⌨️ Keyboard shortcuts (Enter to send)
- 💭 Typing indicators
- 🎭 Smooth animations
- 🔐 Secure API key modal
- 🔄 Easy key management

## 📊 API Endpoints

### Chat
```bash
POST /api/chat
{
  "message": "Hello!",
  "api_key": "your_api_key",
  "provider": "google",           # Cloud provider (google, openai, anthropic, nvidia, azure)
  "model": "gemini-1.5-flash",    # Selected model ID
  "session_id": "optional"
}
```

### Get Providers
```bash
GET /api/providers
# Returns list of available cloud providers
```

### Get Models for Provider
```bash
GET /api/providers/{provider_id}/models
# Returns available models for a specific provider
```

### Get History
```bash
GET /api/history/{session_id}
```

### Clear Session
```bash
DELETE /api/session/{session_id}
```

### Health Check
```bash
GET /health
```

## 🔧 Configuration

No configuration needed! Just run and use.

Optional: Set default port in `.env`:
```env
PORT=8000
```

## 🚀 Deployment

### Local
```bash
python3 server.py
```

### Production (with Gunicorn)
```bash
pip install gunicorn
gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY server.py .
CMD ["python", "server.py"]
```

```bash
docker build -t adk-chatbot .
docker run -p 8000:8000 adk-chatbot
```

## 🔒 Security

- ✅ Model access API keys stored in browser's localStorage (client-side only)
- ✅ Keys never stored on server
- ✅ Each user uses their own Model access API key
- ✅ Keys transmitted securely via HTTPS (in production)
- ✅ Easy to change/revoke keys anytime

## 💡 Tips

1. **Model Access API Key Format**: Should start with `AIza`
2. **Storage**: Key is saved in your browser
3. **Privacy**: Use incognito mode for temporary sessions
4. **Multiple Keys**: Clear browser data to switch accounts
5. **Quota**: Free tier has limits - check Google AI Studio

## 📖 Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Get API Key](https://aistudio.google.com/apikey)
- [ADK Quickstart](https://google.github.io/adk-docs/get-started/quickstart/)
- [Gemini API Docs](https://ai.google.dev/docs)

## 🎯 What's Next?

- Add function calling/tools
- Implement multi-agent systems
- Add voice input/output
- Export conversations
- Add authentication for team use
- Deploy to cloud (Cloud Run, GKE)

## 🐛 Troubleshooting

### "Invalid Model access API key" error:
- Make sure key starts with `AIza`
- Get new Model access API key from https://aistudio.google.com/apikey
- Check if key is active in Google AI Studio

### Can't connect to server:
- Make sure server is running: `python3 server.py`
- Check if port 8000 is available
- Try different port: `PORT=8001 python3 server.py`

### Browser not saving Model access API key:
- Check if cookies/localStorage enabled
- Try different browser
- Clear browser cache and retry

## 📝 License

Open source - use freely!

---

**GauraAI - Your Intelligent AI Assistant 🤖**

Powered by Google's Agent Development Kit

**No setup, no configuration files, just run and chat!** 🚀
