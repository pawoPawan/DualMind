/**
 * StorageManager - Handles all storage operations
 * Uses chrome.storage.sync for settings and chrome.storage.local for chats
 */

export class StorageManager {
  constructor() {
    this.KEYS = {
      SETTINGS: 'dualmind_settings',
      CHATS: 'dualmind_chats',
      CURRENT_CHAT: 'dualmind_current_chat'
    };
  }
  
  // Settings Management
  async getSettings() {
    const result = await chrome.storage.sync.get(this.KEYS.SETTINGS);
    return result[this.KEYS.SETTINGS] || {
      selectedMode: null,
      theme: 'dark',
      apiKeys: {},
      defaultModel: {},
      autoSend: false
    };
  }
  
  async setSetting(key, value) {
    const settings = await this.getSettings();
    settings[key] = value;
    await chrome.storage.sync.set({ [this.KEYS.SETTINGS]: settings });
  }
  
  async saveSettings(settings) {
    await chrome.storage.sync.set({ [this.KEYS.SETTINGS]: settings });
  }
  
  // API Keys
  async getApiKey(provider) {
    const settings = await this.getSettings();
    return settings.apiKeys?.[provider] || null;
  }
  
  async saveApiKey(provider, key) {
    const settings = await this.getSettings();
    if (!settings.apiKeys) settings.apiKeys = {};
    settings.apiKeys[provider] = key;
    await this.saveSettings(settings);
  }
  
  // Chat History
  async getAllChats() {
    const result = await chrome.storage.local.get(this.KEYS.CHATS);
    return result[this.KEYS.CHATS] || [];
  }
  
  async getCurrentChat() {
    const result = await chrome.storage.local.get(this.KEYS.CURRENT_CHAT);
    return result[this.KEYS.CURRENT_CHAT] || null;
  }
  
  async saveChat(chat) {
    const chats = await this.getAllChats();
    const existingIndex = chats.findIndex(c => c.id === chat.id);
    
    if (existingIndex >= 0) {
      chats[existingIndex] = chat;
    } else {
      chats.unshift(chat);
    }
    
    // Keep only last 50 chats
    if (chats.length > 50) {
      chats.splice(50);
    }
    
    await chrome.storage.local.set({ [this.KEYS.CHATS]: chats });
  }
  
  async setCurrentChat(chat) {
    await chrome.storage.local.set({ [this.KEYS.CURRENT_CHAT]: chat });
  }
  
  async deleteChat(chatId) {
    const chats = await this.getAllChats();
    const filtered = chats.filter(c => c.id !== chatId);
    await chrome.storage.local.set({ [this.KEYS.CHATS]: filtered });
  }
  
  async clearAllChats() {
    await chrome.storage.local.set({ [this.KEYS.CHATS]: [] });
    await chrome.storage.local.set({ [this.KEYS.CURRENT_CHAT]: null });
  }
  
  // Model Selection
  async getSelectedModel(mode) {
    const settings = await this.getSettings();
    return settings.defaultModel?.[mode] || null;
  }
  
  async saveSelectedModel(mode, model) {
    const settings = await this.getSettings();
    if (!settings.defaultModel) settings.defaultModel = {};
    settings.defaultModel[mode] = model;
    await this.saveSettings(settings);
  }
}

