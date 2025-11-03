# 🚀 DualMind Extension - Quick Installation Guide

## Chrome / Edge / Brave / Opera

### Step 1: Prepare Icons (Required)

Before installing, you need to add extension icons:

```bash
cd extension/chrome/icons

# Option A: Use ImageMagick to create placeholder icons
convert -size 16x16 xc:#6366f1 -pointsize 12 -fill white -gravity center -annotate +0+0 "D" icon16.png
convert -size 48x48 xc:#6366f1 -pointsize 32 -fill white -gravity center -annotate +0+0 "D" icon48.png
convert -size 128x128 xc:#6366f1 -pointsize 96 -fill white -gravity center -annotate +0+0 "D" icon128.png

# Option B: Copy icon files you've created
# cp /path/to/your/icon16.png icon16.png
# cp /path/to/your/icon48.png icon48.png
# cp /path/to/your/icon128.png icon128.png
```

Or download brain emoji icons and rename them.

### Step 2: Load Extension

1. **Open Extensions Page**
   - Chrome: Navigate to `chrome://extensions/`
   - Edge: Navigate to `edge://extensions/`
   - Brave: Navigate to `brave://extensions/`
   - Opera: Navigate to `opera://extensions/`

2. **Enable Developer Mode**
   - Look for "Developer mode" toggle in the top-right corner
   - Turn it ON

3. **Load Unpacked Extension**
   - Click "Load unpacked" button
   - Navigate to your `DualMind/extension/chrome` directory
   - Select the folder and click "Select Folder" / "Open"

4. **Verify Installation**
   - Extension should appear in your extensions list
   - You should see "DualMind AI Assistant" with the icon
   - Click the extension icon in your toolbar to open

### Step 3: First Use

1. **Click Extension Icon** in toolbar
   - Or press `Ctrl/Cmd + Shift + D`

2. **Choose Mode**
   - **Local Mode**: Experimental, works immediately
   - **Cloud Mode**: Requires API key (recommended)

3. **For Cloud Mode**:
   - Click Settings (⚙️)
   - Choose provider (Google, OpenAI, Anthropic, etc.)
   - Enter your API key
   - Save

4. **Start Chatting!**

## Safari (macOS)

Coming soon! Safari extension requires Xcode and different packaging.

## Firefox

Coming soon! Firefox uses Manifest V2 and requires modifications.

## Troubleshooting

### "Invalid manifest"
- Make sure you selected the `chrome` directory, not `extension`
- Check that `manifest.json` exists
- Verify JSON syntax is valid

### "Icons missing"
- Add icon files to `icons/` directory
- See `icons/ICONS_README.md` for instructions

### Extension doesn't appear in toolbar
- Click the puzzle piece icon (Extensions menu)
- Find "DualMind AI Assistant"
- Click the pin icon to pin to toolbar

### Can't load extension
- Make sure Developer Mode is enabled
- Check browser console for errors
- Verify all required files exist

## Permissions Explanation

The extension requests these permissions:

- **storage**: Save your settings and chat history locally
- **activeTab**: Access current page for context-aware features
- **contextMenus**: Add "Ask DualMind" to right-click menu
- **host_permissions**: Make API calls to cloud providers (Cloud Mode only)

## Next Steps

1. **Configure Settings**
   - Right-click extension icon → Options
   - Or click Settings in popup

2. **Add API Keys** (for Cloud Mode)
   - Google AI: https://makersuite.google.com/app/apikey
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/

3. **Customize Shortcuts**
   - Go to `chrome://extensions/shortcuts`
   - Find "DualMind AI Assistant"
   - Click edit icons to customize

4. **Try Features**
   - Select text on any webpage → right-click → "Ask DualMind"
   - Press `Ctrl/Cmd + Shift + A` for quick ask
   - Use quick action buttons in popup

## Building for Distribution

To package for Chrome Web Store:

```bash
cd extension/chrome
npm run package
```

This creates `dualmind-extension.zip` ready for upload.

## Support

- **GitHub Issues**: Report bugs and request features
- **Documentation**: See `extension/README.md`
- **Main App**: For full features, use the web application

---

**Enjoy using DualMind! 🧠**

