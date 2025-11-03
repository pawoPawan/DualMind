/**
 * LocalModeManager - Handles WebLLM local inference
 * Note: This is a simplified version. Full WebLLM integration requires
 * additional setup and may have size limitations in extensions.
 */

import { ChatManager } from './chat.js';

export class LocalModeManager extends ChatManager {
  constructor(storage, ui) {
    super(storage, ui);
    this.model = null;
    this.isModelLoaded = false;
  }
  
  async init() {
    await super.init();
    
    this.ui.updateModelInfo('⚠️ Local Mode: Limited in extension');
    this.ui.showInfo('🔧 Local Mode is experimental in browser extensions. For full local mode, use the web app. Using fallback mode...');
    
    // Note: WebLLM requires WebGPU and significant resources
    // In a real implementation, you would:
    // 1. Check WebGPU availability
    // 2. Load WebLLM library
    // 3. Initialize model
    // For now, we'll use a simple fallback
  }
  
  getMode() {
    return 'local';
  }
  
  async generateResponse(message) {
    // Fallback response since WebLLM may not work well in extensions
    // In production, you would integrate WebLLM here if feasible
    
    return `🔧 **Local Mode Response** (Fallback)

I received your message: "${message}"

**Note**: Full local mode with WebLLM is best used in the web application due to browser extension limitations (WASM, WebGPU, model size).

**For full local AI capabilities:**
1. Use the DualMind web application
2. Or switch to Cloud Mode in this extension

**Cloud Mode** provides full AI capabilities right in your browser extension!

Would you like to switch to Cloud Mode? Click the switch icon in the header.`;
  }
}

