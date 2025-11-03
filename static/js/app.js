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
        // TODO: Implement settings panel
        this.ui.showNotification('Settings panel coming soon!');
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

