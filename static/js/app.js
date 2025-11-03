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
        
        // Start with a new chat (will have empty documents)
        this.chat.currentChatId = Date.now();
        this.rag.setCurrentChat(this.chat.currentChatId);
        console.log(`🆕 Initialized with new chat: ${this.chat.currentChatId}`);
        
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
    
    async loadConversation(id) {
        await this.chat.loadConversation(id);
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
            alert('✅ Custom memory saved!');
        }
    }
    
    saveChatContext() {
        const input = document.getElementById('chatContextInput');
        if (input) {
            this.chat.currentChatContext = input.value;
            if (this.chat.currentChatId) {
                this.storage.updateConversationContext(this.chat.currentChatId, input.value);
            }
            alert('✅ Chat context saved!');
        }
    }
    
    async clearAllChats() {
        if (confirm('Clear all chat history? This will also delete all associated documents. This cannot be undone.')) {
            this.storage.clearAllConversations();
            await this.chat.startNewChat();
            this.chat.updateChatHistoryUI();
            alert('✅ All chats and documents cleared!');
        }
    }
    
    async renameChat(chatId) {
        const conv = this.storage.getConversation(chatId);
        if (conv) {
            const newTitle = prompt('Enter new name:', conv.title);
            if (newTitle && newTitle.trim()) {
                this.storage.renameConversation(chatId, newTitle.trim());
                this.chat.updateChatHistoryUI();
                if (this.chat.currentChatId === chatId) {
                    this.chat.currentChatTitle = newTitle.trim();
                }
                alert('✅ Chat renamed!');
            }
        }
    }
    
    async deleteChat(chatId) {
        const conv = this.storage.getConversation(chatId);
        const docCount = this.storage.getChatDocuments(chatId).length;
        
        let confirmMessage = 'Are you sure you want to delete this chat?';
        if (docCount > 0) {
            confirmMessage = `Are you sure you want to delete this chat?\n\nThis will also delete ${docCount} associated document(s).`;
        }
        
        if (confirm(confirmMessage)) {
            this.storage.deleteConversation(chatId);
            this.chat.updateChatHistoryUI();
            
            // If deleting current chat, start a new one
            if (this.chat.currentChatId === chatId) {
                await this.chat.startNewChat();
            }
            
            console.log(`✅ Deleted chat ${chatId} with ${docCount} document(s)`);
        }
    }
    
    openNewChatModal() {
        // Directly create new chat without modal
        this.createNewChat();
    }
    
    closeNewChatModal() {
        // No longer needed, kept for compatibility
    }
    
    async createNewChat() {
        // Simply create a new chat - it will be named from first message
        await this.chat.startNewChat(null);
    }
    
    switchToCloudMode() {
        window.location.href = '/';
    }
}

// Create and export global instance
const app = new DualMindApp();

// Expose to window FIRST for HTML onclick handlers
window.dualmind = app;

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', async () => {
        await app.initialize();
        console.log('✅ DualMind initialized and ready');
    });
} else {
    app.initialize().then(() => {
        console.log('✅ DualMind initialized and ready');
    });
}

export default app;

