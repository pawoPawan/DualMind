# Chrome Web Store - Required Assets

## 📦 What You Need Before Submitting

### 1. Developer Account
- **Cost**: $5 USD one-time registration fee
- **URL**: https://chrome.google.com/webstore/devconsole
- **Required**: Google account

### 2. Extension Package
- ✅ All files in `extension/chrome/` directory
- ✅ Will be zipped automatically

### 3. Store Listing Images

#### Required Screenshots (1280x800 or 640x400 pixels)
You need **at least 1** screenshot, but **3-5 recommended**:

**Suggested screenshots:**
1. **Mode Selection Screen** - Show Local vs Cloud mode choice
2. **Chat Interface** - Show a conversation in progress
3. **Settings Panel** - Show API key configuration
4. **Context Menu** - Show right-click "Ask DualMind" feature
5. **Chat History** - Show multiple chats in sidebar

**How to create:**
- Take screenshots of the extension in action
- Resize to 1280x800 pixels
- Save as PNG or JPEG
- Show the best features!

#### Promotional Images (Optional but Recommended)

**Small Promotional Tile** - 440x280 pixels
- Shows in search results
- Eye-catching design with logo and tagline

**Large Promotional Tile** - 920x680 pixels  
- Featured placements
- More detailed promotional image

**Marquee Promotional Tile** - 1400x560 pixels
- Premium placement (if selected by Chrome team)
- High-quality banner

### 4. Store Listing Information

#### Category
Select: **Productivity**

#### Language
Select: **English (United States)**

#### Short Description (132 characters max)
```
AI chat assistant with Local Mode (WebLLM) and Cloud Mode. Works on any webpage with context menus and keyboard shortcuts.
```

#### Detailed Description (Max 16,000 characters)
```
🧠 DualMind - Your Intelligent AI Assistant

DualMind is a powerful browser extension that brings AI assistance directly to your browser. Choose between Local Mode (privacy-focused, runs in your browser) or Cloud Mode (leveraging powerful cloud AI providers).

✨ KEY FEATURES

🎯 One-Click Access
• Click the toolbar icon or press Ctrl/Cmd + Shift + D
• Access AI assistance from any webpage
• No context switching needed

🖱️ Context Menu Integration
• Select text on any page → Right-click → "Ask DualMind"
• "Explain this with DualMind" for detailed explanations
• "Summarize this page" for quick content overview

💻 Local Mode (Privacy First)
• Run AI models directly in your browser
• No API keys required
• Your data never leaves your device
• Perfect for sensitive information

☁️ Cloud Mode (Power & Speed)
• Access to leading AI providers:
  - Google AI (Gemini)
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic (Claude)
  - NVIDIA AI
  - Azure OpenAI
• Fast responses
• Latest AI capabilities

💬 Smart Chat Management
• Multiple conversation threads
• Rename and organize chats
• Full conversation history
• Search through past chats

🎨 Modern Interface
• Beautiful, responsive design
• Dark and light mode support
• Smooth animations
• Intuitive navigation

⚡ Keyboard Shortcuts
• Ctrl/Cmd + Shift + D - Open DualMind
• Ctrl/Cmd + Shift + A - Quick Ask with selected text
• Fast, keyboard-driven workflow

🔒 Privacy & Security
• API keys stored securely in browser
• No data collection by extension
• Open source (GitHub available)
• Full control over your data

📱 Perfect For
• Developers seeking code help
• Students researching topics
• Writers needing inspiration
• Anyone wanting AI assistance while browsing

🚀 Getting Started
1. Install the extension
2. Choose your preferred mode (Local or Cloud)
3. For Cloud Mode: Add your API keys in Settings
4. Start chatting!

🔗 Support & Documentation
Visit our GitHub repository for:
• Detailed documentation
• Troubleshooting guides
• Feature requests
• Bug reports

Transform your browsing experience with intelligent AI assistance - install DualMind today!
```

#### Privacy Policy (Required)
You'll need to create a privacy policy. I'll help you with this below.

### 5. Additional Information

**Homepage URL** (Optional):
```
https://github.com/pawoPawan/DualMind
```

**Support Email** (Required):
```
your-email@example.com
```

**Single Purpose Description**:
```
DualMind provides AI-powered chat assistance directly in the browser, allowing users to interact with AI models through a popup interface, context menus, and keyboard shortcuts.
```

**Permissions Justification**:
- **storage**: Required to save user settings, API keys, and chat history locally
- **activeTab**: Required to get selected text from the current page for context menu features
- **contextMenus**: Required to add "Ask DualMind" options to the right-click menu

## 📸 Creating Screenshots

### Using Chrome's Developer Tools:
1. Load your extension in Chrome
2. Open the popup (click icon)
3. Press Ctrl/Cmd + Shift + C (Inspect)
4. Click the device toggle icon (top-left)
5. Set viewport to 1280x800
6. Take screenshot: Ctrl/Cmd + Shift + P → "Capture screenshot"

### Recommended Tools:
- **Mac**: Built-in Screenshot tool (Cmd + Shift + 5)
- **Windows**: Snipping Tool or Snip & Sketch
- **Online**: Canva, Figma (for promotional tiles)

## 🔐 Privacy Policy Template

Create a file named `PRIVACY_POLICY.md` and host it on GitHub Pages or your website:

```markdown
# DualMind Extension - Privacy Policy

Last Updated: [Current Date]

## Overview
DualMind is committed to protecting your privacy. This extension operates with minimal data collection.

## Data Collection
DualMind does NOT collect, transmit, or sell any personal data. All data is stored locally in your browser.

## Local Storage
The extension stores the following locally:
- Chat history
- User preferences (theme, mode selection)
- API keys (encrypted in Chrome storage)
- Settings

## Third-Party Services
When using Cloud Mode, you connect directly to your chosen AI provider:
- Google AI
- OpenAI  
- Anthropic
- NVIDIA
- Azure

Your API keys and conversations are sent directly to these providers. Please review their privacy policies.

## Permissions
- **storage**: Save settings and chat history locally
- **activeTab**: Read selected text for context menu features
- **contextMenus**: Add right-click menu options

## Data Security
API keys are stored securely using Chrome's encrypted storage API.

## Changes to Privacy Policy
We may update this policy. Check this page for the latest version.

## Contact
Questions? Contact: your-email@example.com
```

## 📋 Pre-Submission Checklist

Before uploading:
- [ ] All required files present
- [ ] Icons created (16, 48, 128)
- [ ] No Python files in package
- [ ] No __pycache__ directories
- [ ] Extension tested in Chrome
- [ ] Screenshots prepared (3-5 images, 1280x800)
- [ ] Privacy policy published online
- [ ] Support email ready
- [ ] Developer account created ($5 fee paid)

## 💰 Pricing

**Free** - The extension will be free to install

**In-app Purchases**: None

**Ads**: None

## 🚀 Ready to Submit?

Once you have everything ready, I'll help you:
1. Create the ZIP package
2. Fill out the submission form
3. Submit for review

Chrome Web Store review typically takes 1-3 business days.

