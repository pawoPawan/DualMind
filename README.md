# DualMind AI Chatbot

A beautiful AI-powered chatbot with **dual modes**: Cloud-based and Local browser-based inference, available on **Web** and **Mobile** platforms.

🎉 **Two Ways to Chat:**
- ☁️ **Cloud Mode**: Fast responses with multiple AI providers (Google, OpenAI, Anthropic, NVIDIA, Azure)
- 🔒 **Local Mode**: 100% private, runs in your browser (no API key needed!)

📱 **Two Platforms:**
- 🌐 **Web App**: Beautiful responsive web interface
- 📱 **Mobile App**: Native iOS & Android via Expo/React Native

Reference: [Google ADK Documentation](https://google.github.io/adk-docs/)

---

## 📚 Table of Contents

- [🚀 Quick Start](#-quick-start)
  - [🌐 Web Application](#-web-application)
  - [📱 Mobile Application](#-mobile-application)
- [✨ Features](#-features)
  - [Web Platform Features](#-web-platform-features)
  - [Mobile Platform Features](#-mobile-platform-features)
- [📁 Project Structure](#-project-structure)
- [🎮 How It Works](#-how-it-works)
- [🤖 Model Selection](#-model-selection-new)
- [🎨 Customization](#-customization-new)
- [🔄 Enhanced Mode Switching](#-enhanced-mode-switching-new)
- [🔑 Getting Your FREE API Key](#-getting-your-free-model-access-api-key)
- [🎨 UI Features](#-ui-features)
- [📊 API Endpoints](#-api-endpoints)
- [🔧 Configuration](#-configuration)
- [🚀 Deployment](#-deployment)
  - [Web Application Deployment](#-web-application-deployment)
  - [Mobile App Deployment](#-mobile-app-deployment)
- [🔒 Security](#-security)
- [💡 Tips](#-tips)
- [📖 Resources](#-resources)
- [🎯 What's Next?](#-whats-next)
- [🐛 Troubleshooting](#-troubleshooting)
- [📝 License](#-license)

---

## 🚀 Quick Start

---

### 🌐 Web Application

#### Option 1: Using Management Script (Recommended) ⭐

```bash
# Start the chatbot
./dualmind.sh start

# Check status
./dualmind.sh status

# Stop when done
./dualmind.sh stop
```

#### Option 2: Manual Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server
python3 server.py
```

#### 3. Open Your Browser

Visit: **http://localhost:8000**

#### 4. Choose Your Mode

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

---

### 📱 Mobile Application

#### 1. Prerequisites

Make sure you have Node.js installed:
```bash
node --version  # Should be v16 or higher
npm --version
```

#### 2. Setup Mobile App (One-Time)

```bash
# Run the setup script
./setup_mobile.sh
```

This will:
- Install Expo CLI
- Create React Native project
- Install all dependencies
- Setup project structure

#### 3. Start the Backend Server

```bash
# Terminal 1: Start backend server
./dualmind.sh start
```

#### 4. Start Mobile App

```bash
# Terminal 2: Start mobile app
cd mobile
npm start
```

#### 5. Run on Your Device

**Option A: Physical Device** (Recommended for testing)
1. Install **Expo Go** app:
   - [Android Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)
   - [iOS App Store](https://apps.apple.com/app/expo-go/id982107779)
2. Scan QR code from terminal
3. App loads on your phone! 🎉

**Option B: iOS Simulator** (Mac only)
```bash
npm run ios
# Or press 'i' in the Expo terminal
```

**Option C: Android Emulator**
```bash
npm run android
# Or press 'a' in the Expo terminal
```

#### 6. Connect to Backend

For testing on a **real device**, update the API URL:

```bash
# 1. Find your computer's IP address
ifconfig | grep "inet " | grep -v 127.0.0.1

# 2. Edit mobile/src/config/api.js
# Change: http://localhost:8000
# To: http://YOUR_IP:8000 (e.g., http://192.168.1.100:8000)
```

Make sure your phone and computer are on the **same WiFi network**.

📖 **Detailed Guides**: 
- [MOBILE_QUICK_START.md](MOBILE_QUICK_START.md) - Complete mobile setup
- [EXPO_CONNECTION_GUIDE.md](EXPO_CONNECTION_GUIDE.md) - Connection troubleshooting
- [MOBILE_APP_PLAN.md](MOBILE_APP_PLAN.md) - Architecture & features
- [MOBILE_TESTING_GUIDE.md](MOBILE_TESTING_GUIDE.md) - Testing guide

---

## ✨ Features

### 🌐 Web Platform Features

#### Cloud Mode (☁️)
- ✅ **Multi-Cloud Providers** - Google, OpenAI, Anthropic, NVIDIA, Azure
- ✅ **30+ AI Models** - GPT-4o, Claude 3.5, Gemini, Llama 3.1, and more
- ✅ **📚 RAG Support (NEW!)** - Document Q&A with embedding model selection
- ✅ **5 Embedding Providers** - OpenAI, Google, Cohere, Voyage, Hugging Face (free!)
- ✅ **Dynamic Model Selection** - Choose optimal model per task
- ✅ **Fast Responses** - Powered by cutting-edge AI infrastructure
- ✅ **Secure API Keys** - Encrypted storage in browser localStorage
- ✅ **Smart Defaults** - Recommended models with visual indicators

#### Local Mode (🔒)
**Privacy & Performance:**
- ✅ **100% Privacy** - Runs entirely in your browser
- ✅ **No API Key Required** - No registration needed
- ✅ **Offline Capable** - Works without internet after model download
- ✅ **WebGPU Acceleration** - GPU-powered inference

**AI Capabilities:**
- ✅ **Multiple Models** - TinyLlama, Phi-3, Llama 3.2, Qwen2.5, SmolLM2
- ✅ **📚 RAG Support** - Upload documents and chat with your files
- ✅ **6 Embedding Models** - Choose quality vs speed (all-MiniLM, MPNet, BGE, GTE, E5)
- ✅ **Local Embeddings** - Semantic search using Transformers.js
- ✅ **💭 Custom Memory** - Set personalized AI instructions

**User Experience:**
- ✅ **📝 Markdown & Code Highlighting** - Beautiful syntax highlighting
- ✅ **💾 Export Conversations** - Download as JSON or Markdown
- ✅ **🎤 Voice Input** - Speak your messages using Web Speech API
- ✅ **🔄 Regenerate Responses** - Get alternative answers instantly
- ✅ **🌙 Dark Mode** - Eye-friendly theme with persistence
- ✅ **📁 Chat History** - Save, load, and manage multiple conversations

#### Common Web Features
- ✅ **Modern Web UI** - Beautiful, responsive chat interface
- ✅ **Session Management** - Maintains conversation context
- ✅ **Real-time Chat** - Instant responses with typing indicators
- ✅ **🔄 Enhanced Mode Switching** - Smart dialogs, info banners, smooth transitions
- ✅ **🎨 Fully Customizable** - Change name, colors, text in one file!

### 📱 Mobile Platform Features

#### Mobile App Capabilities
- ✅ **Native iOS & Android** - Built with React Native/Expo
- ✅ **Cloud Mode Support** - Access all cloud providers on mobile
- ✅ **Secure Storage** - Biometric authentication & encrypted storage
- ✅ **Offline Support** - Local Mode via WebView
- ✅ **Push Notifications** - Get notified of responses (planned)
- ✅ **Cross-Platform** - One codebase for iOS & Android
- ✅ **Beautiful UI** - Native mobile components
- ✅ **Easy Deployment** - Build APK/IPA with Expo

#### Mobile-Specific Features
- 📱 **Touch-Optimized** - Designed for mobile interaction
- 🔐 **Biometric Auth** - Face ID / Touch ID / Fingerprint
- 💾 **AsyncStorage** - Conversation caching
- 🎨 **Native Navigation** - Smooth screen transitions
- 📲 **Share Integration** - Share responses with other apps
- 🌙 **Dark Mode** - System-aware theme switching

## 📁 Project Structure

```
learn/
├── 🌐 WEB APPLICATION
│   ├── server.py                    # FastAPI server with dual-mode support
│   ├── dualmind.sh                  # 🎯 MANAGEMENT SCRIPT (start/stop/status)
│   ├── branding_config.py           # 🎨 CUSTOMIZE ALL NAMES & COLORS HERE
│   ├── cloud_providers.py           # Multi-cloud provider implementation
│   ├── model_fetcher.py             # Dynamic model fetching
│   ├── model_manager.py             # Model download manager
│   ├── static/
│   │   └── index_local.html         # Local mode UI with WebLLM
│   └── requirements.txt             # Python dependencies
│
├── 📱 MOBILE APPLICATION
│   ├── mobile/
│   │   ├── App.js                   # Main mobile app entry
│   │   ├── app.json                 # Expo configuration
│   │   ├── package.json             # Node dependencies
│   │   ├── src/
│   │   │   ├── config/
│   │   │   │   ├── api.js           # API configuration
│   │   │   │   └── branding.js      # Mobile branding
│   │   │   ├── services/
│   │   │   │   └── api.js           # API client
│   │   │   ├── screens/             # Mobile screens
│   │   │   ├── components/          # React Native components
│   │   │   └── navigation/          # Navigation setup
│   │   └── assets/                  # Images, icons, splash
│   └── setup_mobile.sh              # Mobile setup script
│
├── 📚 DOCUMENTATION
│   ├── README.md                    # This file (main documentation)
│   ├── FEATURES.md                  # Detailed feature documentation
│   ├── CUSTOMIZATION_GUIDE.md       # Customization guide
│   ├── MODE_SWITCHING_GUIDE.md      # Mode switching guide
│   ├── MODEL_SELECTION_GUIDE.md     # Model selection guide
│   ├── MULTI_CLOUD_GUIDE.md         # Multi-cloud provider guide
│   ├── RAG_GUIDE.md                 # RAG implementation guide
│   │
│   ├── 📱 Mobile Docs:
│   ├── MOBILE_APP_PLAN.md           # Mobile app architecture
│   ├── MOBILE_QUICK_START.md        # Mobile quick start guide
│   ├── MOBILE_TESTING_GUIDE.md      # Mobile testing guide
│   └── EXPO_CONNECTION_GUIDE.md     # Expo connection troubleshooting
│
└── 🔧 CONFIGURATION
    ├── .env                         # Optional environment variables
    └── dualmind.sh                  # Alternative management script
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
CHATBOT_NAME = "YourBotName"  # Change from "DualMind AI"

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

### 🌐 Web Application Deployment

#### Local
```bash
python3 server.py
```

#### Production (with Gunicorn)
```bash
pip install gunicorn
gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY server.py .
CMD ["python", "server.py"]
```

```bash
docker build -t dualmind-ai-chatbot .
docker run -p 8000:8000 dualmind-ai-chatbot
```

#### Cloud Platforms
- **Google Cloud Run**: `gcloud run deploy`
- **Heroku**: `git push heroku main`
- **Railway**: Connect GitHub repo
- **AWS EC2**: Deploy with systemd service

---

### 📱 Mobile App Deployment

#### Development Build (Testing)
```bash
cd mobile

# For testing on physical devices
npx expo start

# For iOS simulator (Mac only)
npx expo start --ios

# For Android emulator
npx expo start --android
```

#### Production Builds

**Android APK** (for sideloading/distribution)
```bash
cd mobile

# Create production build
eas build --platform android --profile production

# Or build locally
expo build:android -t apk
```

**iOS IPA** (requires Apple Developer account)
```bash
cd mobile

# Create production build
eas build --platform ios --profile production

# Or build locally (Mac only)
expo build:ios
```

#### Publishing to App Stores

**Google Play Store:**
1. Build signed APK/AAB:
   ```bash
   eas build --platform android --profile production
   ```
2. Create Google Play Console account
3. Upload AAB file
4. Fill in store listing details
5. Submit for review

**Apple App Store:**
1. Build IPA:
   ```bash
   eas build --platform ios --profile production
   ```
2. Create App Store Connect account
3. Upload via Transporter or Xcode
4. Fill in App Store listing
5. Submit for review

#### Over-The-Air (OTA) Updates

With Expo, you can push updates without app store approval:

```bash
cd mobile
eas update --branch production
```

Updates are downloaded automatically when users open the app!

**Note:** OTA updates work for JavaScript/React changes only, not for native code changes.

## 🔒 Security

### Web Application Security
- ✅ Model access API keys stored in browser's localStorage (client-side only)
- ✅ Keys never stored on server
- ✅ Each user uses their own Model access API key
- ✅ Keys transmitted securely via HTTPS (in production)
- ✅ Easy to change/revoke keys anytime
- ✅ Local mode: 100% client-side processing, zero data transmission

### Mobile Application Security
- ✅ **Encrypted Storage**: API keys stored using React Native's SecureStore
- ✅ **Biometric Authentication**: Face ID, Touch ID, or Fingerprint support
- ✅ **Secure Communication**: All API calls over HTTPS
- ✅ **No Key Logging**: Keys never logged or transmitted to third parties
- ✅ **App Sandboxing**: iOS/Android app sandboxing for data isolation
- ✅ **Certificate Pinning**: Optional SSL pinning for enhanced security
- ✅ **Auto-Lock**: Session timeout for sensitive data

## 💡 Tips

### Web Application Tips
1. **Model Access API Key Format**: Format varies by provider (Google keys start with `AIza`)
2. **Storage**: Keys are saved in your browser localStorage
3. **Privacy**: Use incognito mode for temporary sessions
4. **Multiple Keys**: Clear browser data to switch accounts
5. **Quota**: Free tier has limits - check your provider's documentation
6. **Local Mode**: Download models on fast WiFi (600MB - 2GB)
7. **Performance**: Local mode works best with WebGPU-enabled browsers

### Mobile Application Tips
1. **First Setup**: Run `./setup_mobile.sh` before starting development
2. **Same WiFi**: Ensure phone and computer on same network for testing
3. **IP Address**: Update API URL in `mobile/src/config/api.js` for real devices
4. **Expo Go**: Use Expo Go app for quick testing (no build required)
5. **Cache Clearing**: Run `expo start -c` if you encounter module issues
6. **Backend First**: Always start backend server before testing mobile app
7. **Development**: Use iOS simulator (Mac) or Android emulator for faster testing
8. **Biometric Auth**: Test on real device, simulators may not support biometrics

## 📖 Resources

### 📚 Project Documentation
- **[ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)** - Advanced features guide
- **[RAG_GUIDE.md](RAG_GUIDE.md)** - Document Q&A for Local Mode
- **[CLOUD_RAG_GUIDE.md](CLOUD_RAG_GUIDE.md)** - Document Q&A for Cloud Mode (NEW!)
- **[MOBILE_APP_PLAN.md](MOBILE_APP_PLAN.md)** - Mobile architecture
- **[MOBILE_TESTING_GUIDE.md](MOBILE_TESTING_GUIDE.md)** - Mobile testing
- **[EXPO_CONNECTION_GUIDE.md](EXPO_CONNECTION_GUIDE.md)** - Troubleshooting

### 🔑 Get API Keys (Cloud Mode)
- [Google Gemini](https://aistudio.google.com/apikey) - Free tier available
- [OpenAI](https://platform.openai.com/api-keys) - GPT models
- [Anthropic](https://console.anthropic.com/) - Claude models
- [NVIDIA](https://build.nvidia.com/) - Free AI endpoints
- [Azure OpenAI](https://azure.microsoft.com/products/ai-services/openai-service)

### 🛠️ Technology Stack
- [WebLLM](https://webllm.mlc.ai/) - Browser-based LLM inference
- [Transformers.js](https://huggingface.co/docs/transformers.js) - Local embeddings
- [FastAPI](https://fastapi.tiangolo.com/) - Python backend
- [React Native](https://reactnative.dev/) / [Expo](https://docs.expo.dev/) - Mobile platform

## 🎯 What's Next?

### Planned Features

#### Web Application
- [ ] Function calling/tools integration
- [ ] Multi-agent systems
- [ ] PDF export format
- [ ] Conversation search and filtering
- [ ] Authentication for team/enterprise use
- [ ] More local models (Mistral, Gemma, Qwen)
- [ ] Image understanding (multimodal support)
- [ ] Multi-language voice support

#### Mobile Application
- [ ] Feature parity with web (markdown, dark mode, etc.)
- [ ] Local Mode via WebView + WebLLM
- [ ] Push notifications for long responses
- [ ] Image/camera integration for multimodal chat
- [ ] Offline mode with local caching
- [ ] Share conversations via native sharing
- [ ] Widget support (iOS/Android)
- [ ] Apple Watch / Wear OS companion app

#### Infrastructure
- [ ] Multi-user authentication system
- [ ] Team collaboration features
- [ ] Usage analytics dashboard
- [ ] Rate limiting and quota management
- [ ] Deploy to cloud (Cloud Run, GKE, AWS)
- [ ] CDN integration for faster model downloads
- [ ] Database integration for conversation persistence

## 🐛 Troubleshooting

### Web Application Issues

#### "Invalid API key" error:
- Verify key format (varies by provider - Google keys start with `AIza`)
- Get new API key from your provider's console
- Check if key is active and has proper permissions
- Try a different provider to isolate the issue

#### Can't connect to server:
- Make sure server is running: `python3 server.py` or `./dualmind.sh status`
- Check if port 8000 is available: `lsof -i:8000`
- Try different port: `PORT=8001 python3 server.py`
- Check firewall settings

#### Browser not saving API key:
- Check if cookies/localStorage enabled
- Try different browser
- Clear browser cache and retry
- Disable browser extensions that might block storage

#### Local Mode not loading:
- Ensure WebGPU is supported (Chrome 113+)
- Check browser console for errors
- Try clearing browser cache
- Verify sufficient disk space for model download

---

### Mobile Application Issues

#### Cannot connect to backend:
```bash
# 1. Check backend is running
./dualmind.sh status

# 2. Verify firewall allows port 8000
# 3. For real device: Check IP in mobile/src/config/api.js
# 4. Ensure same WiFi network
```

#### QR code not showing:
- Make terminal window larger (QR needs space)
- Wait 30-60 seconds for Metro to start
- Open web interface: `http://localhost:8081`
- Use manual URL entry in Expo Go

#### Metro bundler won't start:
```bash
cd mobile
npx expo start -c  # Clear cache
```

#### Module not found errors:
```bash
cd mobile
rm -rf node_modules
npm install
npx expo start
```

#### Expo Go not loading app:
1. Ensure phone and computer on same network
2. Try scanning QR code again
3. Manually enter URL shown in terminal
4. Try tunnel mode: `npx expo start --tunnel`

#### App crashes on device:
- Check React Native logs in terminal
- Clear Expo cache: `npx expo start -c`
- Rebuild: `rm -rf node_modules && npm install`
- Check for missing dependencies

#### IP address changed:
```bash
# Find new IP
ifconfig | grep "inet " | grep -v 127.0.0.1

# Update mobile/src/config/api.js
export const API_BASE_URL = 'http://NEW_IP:8000';
```

---

### Common Issues

#### Port already in use:
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill

# Or use different port
PORT=8001 python3 server.py
```

#### Python dependencies issues:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### Node.js/npm issues:
```bash
# Update Node.js (should be v16+)
node --version

# Clear npm cache
npm cache clean --force
```

📖 **More Help**: 
- [EXPO_CONNECTION_GUIDE.md](EXPO_CONNECTION_GUIDE.md) - Detailed mobile troubleshooting
- [MOBILE_TESTING_GUIDE.md](MOBILE_TESTING_GUIDE.md) - Mobile testing guide


## 📝 License

Open source - use freely!

---

## 🌟 About DualMind AI

**DualMind AI Chatbot** is a comprehensive, cross-platform AI assistant that puts you in control.

### Key Highlights:
- 🌐 **Web & Mobile**: Access from any device
- ☁️ **Multi-Cloud**: 5 AI providers, 30+ models
- 🔒 **Privacy First**: Local mode with zero data transmission
- 🎨 **Fully Customizable**: Change branding in minutes
- 📱 **Native Mobile**: React Native for iOS & Android
- 🚀 **Easy Deployment**: One-click setup, multiple deployment options

### Perfect For:
- 👨‍💻 **Developers**: Learn AI integration, customize everything
- 🏢 **Enterprises**: Self-host, maintain privacy, scale as needed
- 🎓 **Students**: Experiment with different AI models
- 🔐 **Privacy-Conscious**: Use local mode for sensitive data
- 📱 **Mobile Users**: Native app experience on iOS/Android

---

**DualMind AI - Your Intelligent AI Assistant, Everywhere** 🤖

Powered by Google ADK, OpenAI, Anthropic, NVIDIA, Azure, and WebLLM

### Quick Start Commands:
```bash
# Web Application
./dualmind.sh start

# Mobile Application
./setup_mobile.sh
cd mobile && npm start
```

**No complex setup, just run and chat!** 🚀

---

**Made with ❤️ for the AI community**

Star ⭐ this project if you find it useful!
