# Extension Icons

This directory should contain the extension icons in the following sizes:

## Required Icons

- **icon16.png** (16x16px) - Displayed in browser toolbar
- **icon48.png** (48x48px) - Displayed in extensions management page
- **icon128.png** (128x128px) - Displayed in Chrome Web Store

## Design Guidelines

### Style
- Use the DualMind brain icon (🧠) as inspiration
- Clean, modern design
- Works well at small sizes
- Clear on both light and dark backgrounds

### Colors
- Primary: #6366f1 (indigo)
- Secondary: #764ba2 (purple)
- Or use gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%)

## Creating Icons

### Option 1: Use a Design Tool
1. Create icons in Figma, Sketch, or Adobe Illustrator
2. Export as PNG at exact sizes
3. Place in this directory

### Option 2: Use an Icon Generator
1. Visit [favicon.io](https://favicon.io/) or similar
2. Upload your logo or use text
3. Generate and download icons
4. Rename to match requirements

### Option 3: Use Emoji
For quick testing, you can use an emoji-to-icon converter:
1. Visit [emojipng.com](https://www.emojipng.com/)
2. Download brain emoji 🧠 in various sizes
3. Use as placeholder icons

## Placeholder Icons

For development, you can use simple colored squares:

```bash
# Install ImageMagick (if not already installed)
# macOS: brew install imagemagick
# Ubuntu: sudo apt-get install imagemagick

# Create placeholder icons
convert -size 16x16 xc:#6366f1 icon16.png
convert -size 48x48 xc:#6366f1 icon48.png
convert -size 128x128 xc:#6366f1 icon128.png
```

Or add text:

```bash
convert -size 16x16 xc:#6366f1 -pointsize 12 -fill white -gravity center -annotate +0+0 "D" icon16.png
convert -size 48x48 xc:#6366f1 -pointsize 32 -fill white -gravity center -annotate +0+0 "D" icon48.png
convert -size 128x128 xc:#6366f1 -pointsize 96 -fill white -gravity center -annotate +0+0 "D" icon128.png
```

## Testing Icons

After adding icons:
1. Reload extension in `chrome://extensions/`
2. Check toolbar icon (icon16.png)
3. Check extensions page (icon48.png)
4. Icons should be crisp and clear

## Notes

- PNG format required
- Transparent background recommended
- Optimize file size (keep under 10KB each)
- Test on both light and dark themes

