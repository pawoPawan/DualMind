/**
 * DualMind Main Application
 * Coordinates all modules and provides global interface
 */

import { config } from './config.js';
import { ui } from './ui.js';
import { chat } from './chat.js';
import { models } from './models.js';
import { rag } from './rag.js';
import { storage } from './storage.js';

class DualMindApp {
    constructor() {
        this.config = config;
        this.ui = ui;
        this.chat = chat;
        this.models = models;
        this.rag = rag;
        this.storage = storage;
    }
    
    async initialize() {
        console.log('🧠 Initializing DualMind...');
        
        // Initialize all modules
        await this.config.initialize();
        this.ui.initialize();
        await this.models.initialize();
        await this.rag.initialize();
        
        // Load chat history
        this.chat.updateChatHistoryUI();
        
        // Setup global event handlers
        this.setupGlobalEvents();
        
        console.log('✅ DualMind ready!');
    }
    
    setupGlobalEvents() {
        // Handle Enter key for sending messages
        const input = document.getElementById('userInput');
        if (input) {
            input.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
        }
    }
    
    // Public API methods (called from HTML)
    async sendMessage() {
        const input = document.getElementById('userInput');
        if (input) {
            const message = input.value.trim();
            if (message) {
                await this.chat.sendMessage(message);
            }
        }
    }
    
    startNewChat() {
        this.chat.startNewChat();
    }
    
    regenerateResponse() {
        this.chat.regenerateLastResponse();
    }
    
    copyMessage(messageId) {
        this.chat.copyMessage(messageId);
    }
    
    loadConversation(id) {
        this.chat.loadConversation(id);
    }
    
    exportChat() {
        this.chat.exportChat();
    }
    
    openModelSelector() {
        this.models.openModelSelector();
    }
    
    closeModelSelector() {
        this.models.closeModelSelector();
    }
    
    openKnowledgeBase() {
        this.rag.openKnowledgeBase();
    }
    
    closeKnowledgeBase() {
        this.rag.closeKnowledgeBase();
    }
    
    handleFileUpload(event) {
        this.rag.handleFileUpload(event);
    }
    
    removeDocument(index) {
        this.rag.removeDocument(index);
    }
    
    toggleVoice() {
        if ('webkitSpeechRecognition' in window) {
            const recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                const input = document.getElementById('userInput');
                if (input) {
                    input.value = transcript;
                    this.ui.updateSendButton();
                }
            };
            
            recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.ui.showNotification('Voice input failed. Please try again.');
            };
            
            recognition.start();
        } else {
            this.ui.showNotification('Voice input is not supported in your browser.');
        }
    }
    
    openSettings() {
        // Load current settings
        const darkMode = this.storage.getDarkMode();
        const customMemory = this.storage.getCustomMemory();
        const chatContext = this.chat.currentChatContext || '';
        
        const darkModeToggle = document.getElementById('darkModeToggle');
        const customMemoryInput = document.getElementById('customMemoryInput');
        const chatContextInput = document.getElementById('chatContextInput');
        
        if (darkModeToggle) darkModeToggle.checked = darkMode;
        if (customMemoryInput) customMemoryInput.value = customMemory;
        if (chatContextInput) chatContextInput.value = chatContext;
        
        this.ui.showModal('settingsModal');
    }
    
    closeSettings() {
        this.ui.hideModal('settingsModal');
    }
    
    toggleDarkMode() {
        this.ui.toggleTheme();
    }
    
    saveCustomMemory() {
        const input = document.getElementById('customMemoryInput');
        if (input) {
            this.storage.saveCustomMemory(input.value);
            this.ui.showNotification('✅ Custom memory saved!');
        }
    }
    
    saveChatContext() {
        const input = document.getElementById('chatContextInput');
        if (input) {
            this.chat.currentChatContext = input.value;
            if (this.chat.currentChatId) {
                this.storage.updateConversationContext(this.chat.currentChatId, input.value);
            }
            this.ui.showNotification('✅ Chat context saved!');
        }
    }
    
    clearAllChats() {
        if (this.ui.showConfirm('Are you sure you want to delete all chat history? This action cannot be undone.')) {
            this.storage.clearAllConversations();
            this.chat.updateChatHistoryUI();
            this.ui.showNotification('✅ All chats cleared!');
        }
    }
    
    async renameChat(chatId) {
        const conv = this.storage.getConversation(chatId);
        if (conv) {
            const newTitle = await this.ui.showPrompt('Rename Chat', 'Enter new name:', conv.title);
            if (newTitle && newTitle.trim()) {
                this.storage.renameConversation(chatId, newTitle.trim());
                this.chat.updateChatHistoryUI();
                if (this.chat.currentChatId === chatId) {
                    this.chat.currentChatTitle = newTitle.trim();
                }
                this.ui.showNotification('✅ Chat renamed!');
            }
        }
    }
    
    deleteChat(chatId) {
        if (this.ui.showConfirm('Are you sure you want to delete this chat?')) {
            this.storage.deleteConversation(chatId);
            this.chat.updateChatHistoryUI();
            if (this.chat.currentChatId === chatId) {
                this.chat.startNewChat();
            }
            this.ui.showNotification('✅ Chat deleted!');
        }
    }
    
    openNewChatModal() {
        const input = document.getElementById('newChatNameInput');
        if (input) input.value = '';
        this.ui.showModal('newChatModal');
    }
    
    closeNewChatModal() {
        this.ui.hideModal('newChatModal');
    }
    
    createNewChat() {
        const input = document.getElementById('newChatNameInput');
        const customName = input && input.value.trim() ? input.value.trim() : null;
        this.chat.startNewChat(customName);
        this.closeNewChatModal();
        if (customName) {
            this.ui.showNotification(`✅ New chat "${customName}" created!`);
        }
    }
    
    switchToCloudMode() {
        window.location.href = '/';
    }
}

// Create and export global instance
const app = new DualMindApp();

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => app.initialize());
} else {
    app.initialize();
}

// Expose to window for HTML onclick handlers
window.dualmind = app;

export default app;

