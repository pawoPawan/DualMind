/**
 * DualMind Extension - Options Page Controller
 */

class OptionsController {
  constructor() {
    this.init();
  }
  
  async init() {
    console.log('🎛️ Initializing options page...');
    
    // Load current settings
    await this.loadSettings();
    
    // Setup event listeners
    this.setupEventListeners();
    
    console.log('✅ Options page initialized');
  }
  
  async loadSettings() {
    const result = await chrome.storage.sync.get('dualmind_settings');
    const settings = result.dualmind_settings || {};
    
    // Theme
    const themeSelect = document.getElementById('theme-select');
    if (themeSelect) {
      themeSelect.value = settings.theme || 'dark';
    }
    
    // Default mode
    const defaultMode = document.getElementById('default-mode');
    if (defaultMode) {
      defaultMode.value = settings.selectedMode || '';
    }
    
    // Cloud provider
    const cloudProvider = document.getElementById('cloud-provider');
    if (cloudProvider) {
      cloudProvider.value = settings.cloudProvider || 'google';
    }
    
    // Load API keys
    await this.loadApiKeys(settings.apiKeys || {});
  }
  
  async loadApiKeys(apiKeys) {
    const items = document.querySelectorAll('.api-key-item');
    items.forEach(item => {
      const provider = item.dataset.provider;
      const input = item.querySelector('.api-key-input');
      if (input && apiKeys[provider]) {
        input.value = apiKeys[provider];
      }
    });
  }
  
  setupEventListeners() {
    // Save all settings
    document.getElementById('save-settings-btn')?.addEventListener('click', () => {
      this.saveAllSettings();
    });
    
    // Individual API key save buttons
    document.querySelectorAll('.save-key-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const item = e.target.closest('.api-key-item');
        this.saveApiKey(item);
      });
    });
    
    // Show/hide API key buttons
    document.querySelectorAll('.show-key-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const item = e.target.closest('.api-key-item');
        const input = item.querySelector('.api-key-input');
        if (input.type === 'password') {
          input.type = 'text';
          e.target.textContent = 'Hide';
        } else {
          input.type = 'password';
          e.target.textContent = 'Show';
        }
      });
    });
    
    // Clear chats
    document.getElementById('clear-chats-btn')?.addEventListener('click', () => {
      this.clearChats();
    });
    
    // Clear all data
    document.getElementById('clear-all-btn')?.addEventListener('click', () => {
      this.clearAllData();
    });
  }
  
  async saveAllSettings() {
    try {
      const settings = await this.getSettings();
      
      const data = {
        theme: document.getElementById('theme-select').value,
        selectedMode: document.getElementById('default-mode').value,
        cloudProvider: document.getElementById('cloud-provider').value,
        apiKeys: settings.apiKeys || {}
      };
      
      await chrome.storage.sync.set({ dualmind_settings: data });
      
      this.showStatus('Settings saved successfully!', 'success');
    } catch (error) {
      console.error('Failed to save settings:', error);
      this.showStatus('Failed to save settings', 'error');
    }
  }
  
  async saveApiKey(item) {
    const provider = item.dataset.provider;
    const input = item.querySelector('.api-key-input');
    const key = input.value.trim();
    
    if (!key) {
      this.showStatus('Please enter an API key', 'error');
      return;
    }
    
    try {
      const settings = await this.getSettings();
      if (!settings.apiKeys) settings.apiKeys = {};
      settings.apiKeys[provider] = key;
      
      await chrome.storage.sync.set({ dualmind_settings: settings });
      
      this.showStatus(`${provider} API key saved!`, 'success');
    } catch (error) {
      console.error('Failed to save API key:', error);
      this.showStatus('Failed to save API key', 'error');
    }
  }
  
  async clearChats() {
    if (!confirm('Are you sure you want to clear all chat history?')) {
      return;
    }
    
    try {
      await chrome.storage.local.set({
        dualmind_chats: [],
        dualmind_current_chat: null
      });
      
      this.showStatus('Chat history cleared', 'success');
    } catch (error) {
      console.error('Failed to clear chats:', error);
      this.showStatus('Failed to clear chats', 'error');
    }
  }
  
  async clearAllData() {
    if (!confirm('Are you sure you want to reset all data? This cannot be undone.')) {
      return;
    }
    
    try {
      await chrome.storage.sync.clear();
      await chrome.storage.local.clear();
      
      this.showStatus('All data cleared! Reloading...', 'success');
      
      setTimeout(() => {
        location.reload();
      }, 1500);
    } catch (error) {
      console.error('Failed to clear data:', error);
      this.showStatus('Failed to clear data', 'error');
    }
  }
  
  async getSettings() {
    const result = await chrome.storage.sync.get('dualmind_settings');
    return result.dualmind_settings || {};
  }
  
  showStatus(message, type = 'success') {
    const statusEl = document.getElementById('status-message');
    if (statusEl) {
      statusEl.textContent = message;
      statusEl.className = `status-message ${type}`;
      
      setTimeout(() => {
        statusEl.textContent = '';
        statusEl.className = 'status-message';
      }, 3000);
    }
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => new OptionsController());
} else {
  new OptionsController();
}

