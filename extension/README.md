# 🧠 DualMind Browser Extension

AI assistant browser extension with Local Mode (WebLLM) and Cloud Mode (Google, OpenAI, Anthropic, NVIDIA, Azure).

## ✨ Features

### 🎯 Core Features
- **One-Click Access**: Click extension icon or press `Ctrl/Cmd + Shift + D`
- **Dual Mode Support**: 
  - 💻 **Local Mode**: Run AI in browser (experimental in extensions)
  - ☁️ **Cloud Mode**: Use cloud AI providers
- **Context Menu Integration**: Right-click selected text → Ask DualMind
- **Keyboard Shortcuts**: Quick access with customizable shortcuts
- **Chat History**: Persistent conversations across sessions
- **Privacy First**: All data stored locally in your browser

### ☁️ Cloud Providers
- Google AI (Gemini)
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- NVIDIA
- Azure OpenAI

## 📦 Installation

### Chrome/Edge (Chromium)

#### From Source:
1. Clone the repository:
   ```bash
   cd DualMind/extension/chrome
   ```

2. Open Chrome/Edge and go to `chrome://extensions/`

3. Enable "Developer mode" (toggle in top-right)

4. Click "Load unpacked"

5. Select the `extension/chrome` directory

6. Done! The extension icon should appear in your toolbar

### Safari

Safari extension is coming soon! See `extension/safari/` directory.

## 🚀 Quick Start

### First Time Setup

1. **Click the extension icon** in your browser toolbar

2. **Choose your mode**:
   - **Local Mode**: Works immediately, no setup needed (experimental)
   - **Cloud Mode**: Requires API key (see below)

3. **Start chatting!**

### Cloud Mode Setup

1. Click the extension icon

2. Click **Settings** (⚙️ icon)

3. Select your preferred provider

4. Enter your API key:
   - **Google AI**: [Get Key](https://makersuite.google.com/app/apikey)
   - **OpenAI**: [Get Key](https://platform.openai.com/api-keys)
   - **Anthropic**: [Get Key](https://console.anthropic.com/)

5. Click "Save"

## ⌨️ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Open DualMind | `Ctrl/Cmd + Shift + D` |
| Quick Ask | `Ctrl/Cmd + Shift + A` |
| Send Message | `Ctrl/Cmd + Enter` |

To customize shortcuts: `chrome://extensions/shortcuts`

## 📖 Usage

### Basic Chat
1. Click extension icon
2. Type your message
3. Press `Ctrl/Cmd + Enter` or click send

### Context Menu
1. Select text on any webpage
2. Right-click → "Ask DualMind"
3. Extension opens with your question

### Quick Actions
- Explain this page
- Summarize article
- Help write email
- And more!

## 🏗️ Architecture

### Modular Structure
```
extension/chrome/
├── manifest.json           # Extension configuration
├── background.js           # Service worker
├── popup.html              # Main UI
├── options.html            # Settings page
├── welcome.html            # Welcome screen
├── content/
│   └── content.js          # Content script
├── js/
│   ├── popup.js            # Popup controller
│   ├── options.js          # Options controller
│   └── modules/
│       ├── storage.js      # Storage manager
│       ├── ui.js           # UI manager
│       ├── chat.js         # Chat manager
│       ├── local-mode.js   # Local mode
│       └── cloud-mode.js   # Cloud mode
└── css/
    ├── popup.css           # Popup styles
    └── options.css         # Options styles
```

### Key Components

**Background Service Worker** (`background.js`)
- Handles extension lifecycle
- Manages context menus
- Processes keyboard shortcuts

**Popup** (`popup.html`, `popup.js`)
- Main chat interface
- Mode selection
- Message handling

**Content Script** (`content/content.js`)
- Runs on all web pages
- Enables text selection
- Page interaction

**Modules** (`js/modules/`)
- Modular, reusable components
- Clean separation of concerns
- Easy to maintain and test

## 🔧 Development

### Prerequisites
- Node.js 16+ (for building)
- Chrome/Edge browser
- Git

### Local Development

1. Make changes to files in `extension/chrome/`

2. Reload extension:
   - Go to `chrome://extensions/`
   - Click reload icon on DualMind card

3. Test changes

### Building

```bash
# Install dependencies
cd extension/chrome
npm install

# Build for production
npm run build

# Package extension
npm run package
```

## 🎨 Icons

Extension icons are required in the following sizes:
- `icon16.png` - 16x16px (toolbar)
- `icon48.png` - 48x48px (extensions page)
- `icon128.png` - 128x128px (Web Store)

Place icons in `extension/chrome/icons/` directory.

## 🔒 Privacy & Security

- **Local Storage**: All data stored in your browser
- **No Tracking**: We don't track your usage
- **API Keys**: Stored securely in Chrome's sync storage
- **No Server**: Extension works entirely client-side (Cloud Mode calls APIs directly)

## 🐛 Troubleshooting

### Extension Not Working

**Check permissions:**
- Go to `chrome://extensions/`
- Click "Details" on DualMind
- Ensure all permissions are enabled

**Clear extension data:**
1. Open Settings
2. Click "Clear All Data"
3. Reload extension

### API Errors

**Invalid API Key:**
- Verify key is correct
- Check key has quota/credits
- Ensure key is for correct provider

**Rate Limits:**
- Wait a few minutes
- Try again
- Consider upgrading API plan

### Local Mode Issues

**Note**: Local Mode in browser extensions has limitations:
- WebGPU may not be available in extension context
- WASM modules have size restrictions
- Recommended to use Cloud Mode for best experience

For full Local Mode capabilities, use the **DualMind Web Application**.

## 📝 Changelog

### v1.0.0 (2025-11-03)
- ✅ Initial release
- ✅ Chrome/Edge support
- ✅ Local & Cloud modes
- ✅ Context menu integration
- ✅ Keyboard shortcuts
- ✅ Chat history
- ✅ 5 cloud providers

## 🛣️ Roadmap

- [ ] Safari extension
- [ ] Firefox extension
- [ ] Full WebLLM integration
- [ ] RAG document support
- [ ] Voice input
- [ ] Multi-language support
- [ ] Export conversations
- [ ] Custom themes

## 📄 License

Same as DualMind main project.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/dualmind/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/dualmind/discussions)
- **Email**: support@dualmind.ai

---

**Built with ❤️ by the DualMind Team**

