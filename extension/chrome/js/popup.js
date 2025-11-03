/**
 * DualMind Extension - Popup Controller
 * Main entry point for the extension popup
 */

import { StorageManager } from './modules/storage.js';
import { ChatManager } from './modules/chat.js';
import { UIManager } from './modules/ui.js';
import { LocalModeManager } from './modules/local-mode.js';
import { CloudModeManager } from './modules/cloud-mode.js';

class DualMindPopup {
  constructor() {
    this.storage = new StorageManager();
    this.ui = new UIManager();
    this.chat = null;
    this.currentMode = null;
    
    this.init();
  }
  
  async init() {
    console.log('🚀 Initializing DualMind Extension Popup...');
    
    // Get stored mode preference
    const settings = await this.storage.getSettings();
    
    if (settings.selectedMode) {
      // User has already selected a mode
      await this.loadMode(settings.selectedMode);
    } else {
      // Show mode selector
      this.showModeSelector();
    }
    
    // Setup event listeners
    this.setupEventListeners();
    
    // Check for pending query from context menu
    await this.checkPendingQuery();
    
    console.log('✅ DualMind Extension Popup initialized');
  }
  
  setupEventListeners() {
    // Mode selection
    document.querySelectorAll('.mode-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const mode = e.currentTarget.dataset.mode;
        this.selectMode(mode);
      });
    });
    
    // Switch mode button
    document.getElementById('switch-mode-btn')?.addEventListener('click', () => {
      this.showModeSelector();
    });
    
    // New chat button
    document.getElementById('new-chat-btn')?.addEventListener('click', () => {
      this.chat?.startNewChat();
    });
    
    // Settings button
    document.getElementById('settings-btn')?.addEventListener('click', () => {
      chrome.runtime.sendMessage({ action: 'openOptions' });
    });
    
    // Open options link
    document.getElementById('open-options')?.addEventListener('click', (e) => {
      e.preventDefault();
      chrome.runtime.sendMessage({ action: 'openOptions' });
    });
    
    // Send message button
    document.getElementById('send-btn')?.addEventListener('click', () => {
      this.sendMessage();
    });
    
    // Message input
    const messageInput = document.getElementById('message-input');
    if (messageInput) {
      messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
          e.preventDefault();
          this.sendMessage();
        }
      });
      
      messageInput.addEventListener('input', (e) => {
        this.updateCharCount(e.target.value.length);
        this.autoResize(e.target);
      });
    }
    
    // Quick action buttons
    document.querySelectorAll('.quick-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const action = e.currentTarget.dataset.action;
        this.handleQuickAction(action);
      });
    });
  }
  
  showModeSelector() {
    document.getElementById('mode-selector')?.classList.remove('hidden');
    document.getElementById('chat-container')?.classList.remove('active');
  }
  
  async selectMode(mode) {
    console.log(`📌 Selected mode: ${mode}`);
    
    // Save mode preference
    await this.storage.setSetting('selectedMode', mode);
    
    // Load the selected mode
    await this.loadMode(mode);
  }
  
  async loadMode(mode) {
    this.currentMode = mode;
    
    // Hide mode selector
    document.getElementById('mode-selector')?.classList.add('hidden');
    
    // Show loading
    this.ui.showLoading(`Loading ${mode} mode...`);
    
    try {
      // Initialize appropriate manager
      if (mode === 'local') {
        this.chat = new LocalModeManager(this.storage, this.ui);
        await this.chat.init();
      } else {
        this.chat = new CloudModeManager(this.storage, this.ui);
        await this.chat.init();
      }
      
      // Show chat container
      document.getElementById('chat-container')?.classList.add('active');
      
      // Update mode badge
      const badge = document.getElementById('current-mode-badge');
      if (badge) {
        badge.textContent = mode === 'local' ? '💻 Local' : '☁️ Cloud';
      }
      
      this.ui.hideLoading();
      
    } catch (error) {
      console.error('Failed to load mode:', error);
      this.ui.hideLoading();
      this.ui.showError(`Failed to load ${mode} mode: ${error.message}`);
    }
  }
  
  async checkPendingQuery() {
    const result = await chrome.storage.local.get('pendingQuery');
    if (result.pendingQuery) {
      // Clear the pending query
      await chrome.storage.local.remove('pendingQuery');
      
      // Set the query in input
      const input = document.getElementById('message-input');
      if (input) {
        input.value = result.pendingQuery;
        this.updateCharCount(result.pendingQuery.length);
        
        // Auto-send after a short delay
        setTimeout(() => {
          this.sendMessage();
        }, 500);
      }
    }
  }
  
  async sendMessage() {
    const input = document.getElementById('message-input');
    const message = input?.value.trim();
    
    if (!message || !this.chat) return;
    
    // Clear input
    input.value = '';
    this.updateCharCount(0);
    this.autoResize(input);
    
    // Send message via chat manager
    await this.chat.sendMessage(message);
  }
  
  handleQuickAction(action) {
    const input = document.getElementById('message-input');
    if (input) {
      input.value = action;
      this.updateCharCount(action.length);
      input.focus();
    }
  }
  
  updateCharCount(count) {
    const charCount = document.getElementById('char-count');
    if (charCount) {
      charCount.textContent = `${count} / 2000`;
      if (count > 2000) {
        charCount.style.color = 'var(--error)';
      } else {
        charCount.style.color = 'var(--text-secondary)';
      }
    }
  }
  
  autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 100) + 'px';
  }
}

// Initialize popup when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => new DualMindPopup());
} else {
  new DualMindPopup();
}

