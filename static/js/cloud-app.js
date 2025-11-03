/**
 * DualMind Cloud Mode Application
 * Handles cloud-based AI chat with multiple providers
 */

import { storage } from './storage.js';
import { ui } from './ui.js';

class CloudModeApp {
    constructor() {
        this.storage = storage;
        this.ui = ui;
        this.chatHistory = [];
        this.currentChatId = null;
        this.currentChatTitle = null;
        this.currentChatContext = null;
        this.sessionId = null;
        this.currentProvider = null;
        this.currentModel = null;
        this.apiKey = null;
        this.isGenerating = false;
        this.availableModels = {};
    }
    
    async initialize() {
        console.log('☁️ Initializing Cloud Mode...');
        
        // Initialize UI
        this.ui.initialize();
        
        // Load saved settings
        this.loadSettings();
        
        // Load chat history
        this.updateChatHistoryUI();
        
        // Setup global event handlers
        this.setupGlobalEvents();
        
        // Check if we have saved API key and provider
        if (this.apiKey && this.currentProvider) {
            this.ui.hideModal('apiKeyModal');
            await this.loadModelsForProvider();
        }
        
        console.log('✅ Cloud Mode ready!');
    }
    
    loadSettings() {
        this.apiKey = localStorage.getItem('dualmind_cloud_api_key');
        this.currentProvider = localStorage.getItem('dualmind_cloud_provider');
        this.currentModel = localStorage.getItem('dualmind_cloud_model');
        
        if (this.currentProvider && this.currentModel) {
            this.ui.updateModelDisplay(
                `${this.currentProvider} - ${this.currentModel}`,
                'Click to change'
            );
        }
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
            
            input.addEventListener('input', () => {
                this.ui.updateSendButton();
            });
        }
    }
    
    // Provider & Model Management
    async openModelSelector() {
        const providerSelect = document.getElementById('providerSelect');
        if (providerSelect && this.currentProvider) {
            providerSelect.value = this.currentProvider;
            await this.loadModelsForProvider();
        }
        this.ui.showModal('modelModal');
    }
    
    closeModelSelector() {
        this.ui.hideModal('modelModal');
    }
    
    async loadModelsForProvider() {
        const providerSelect = document.getElementById('providerSelect');
        const provider = providerSelect.value;
        
        if (!provider) {
            document.getElementById('modelListContainer').style.display = 'none';
            return;
        }
        
        try {
            const response = await fetch(`/api/providers/${provider}/models`);
            const data = await response.json();
            
            this.availableModels[provider] = data.models || [];
            this.renderModelList(provider);
            
            document.getElementById('modelListContainer').style.display = 'block';
        } catch (error) {
            console.error('Error loading models:', error);
            alert('Failed to load models. Please try again.');
        }
    }
    
    renderModelList(provider) {
        const modelList = document.getElementById('modelList');
        const models = this.availableModels[provider] || [];
        
        modelList.innerHTML = '';
        models.forEach(model => {
            const option = document.createElement('div');
            option.className = 'model-option';
            if (this.currentModel === model.id) {
                option.classList.add('selected');
            }
            
            option.innerHTML = `
                <h4>${model.name} ${model.recommended ? '⭐' : ''}</h4>
                <p>${model.description}</p>
            `;
            
            option.onclick = () => this.selectModel(provider, model);
            modelList.appendChild(option);
        });
    }
    
    selectModel(provider, model) {
        this.currentProvider = provider;
        this.currentModel = model.id;
        
        localStorage.setItem('dualmind_cloud_provider', provider);
        localStorage.setItem('dualmind_cloud_model', model.id);
        
        this.ui.updateModelDisplay(model.name, model.description);
        this.closeModelSelector();
        
        // Check if we need API key
        if (!this.apiKey) {
            this.ui.showModal('apiKeyModal');
        }
    }
    
    // API Key Management
    changeApiKey() {
        document.getElementById('apiKeyInput').value = '';
        this.ui.showModal('apiKeyModal');
    }
    
    saveApiKey() {
        const input = document.getElementById('apiKeyInput');
        const key = input.value.trim();
        
        if (!key) {
            alert('Please enter an API key');
            return;
        }
        
        this.apiKey = key;
        localStorage.setItem('dualmind_cloud_api_key', key);
        
        this.ui.hideModal('apiKeyModal');
        alert('✅ API key saved!');
    }
    
    // Chat Management
    async sendMessage() {
        const input = document.getElementById('userInput');
        const message = input.value.trim();
        
        if (!message || this.isGenerating) return;
        
        if (!this.apiKey || !this.currentProvider || !this.currentModel) {
            alert('Please select a provider and model, and enter your API key');
            return;
        }
        
        this.isGenerating = true;
        this.ui.setInputEnabled(false);
        this.ui.hideEmptyState();
        
        // Add user message
        this.ui.addMessage('user', message);
        this.chatHistory.push({ role: 'user', content: message });
        
        // Add loading placeholder
        const agentMessageId = this.ui.addMessage('agent', '<div class="loading-dots"><span></span><span></span><span></span></div>');
        
        try {
            // Get custom memory and chat context
            const customMemory = this.storage.getCustomMemory();
            const chatContext = this.currentChatContext || '';
            
            let systemMessages = [];
            if (customMemory) {
                systemMessages.push({ role: 'system', content: customMemory });
            }
            if (chatContext) {
                systemMessages.push({ role: 'system', content: chatContext });
            }
            
            const messages = systemMessages.length > 0 ?
                [...systemMessages, ...this.chatHistory] :
                this.chatHistory;
            
            // Send to cloud API
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    api_key: this.apiKey,
                    provider: this.currentProvider,
                    model: this.currentModel,
                    session_id: this.sessionId,
                    chat_history: messages
                })
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let fullResponse = '';
            let buffer = '';
            
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                
                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop();
                
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.substring(6));
                            
                            if (data.type === 'session') {
                                this.sessionId = data.session_id;
                            } else if (data.type === 'chunk') {
                                fullResponse += data.content;
                                // Update with markdown rendering
                                if (window.marked) {
                                    this.ui.updateMessage(agentMessageId, window.marked.parse(fullResponse));
                                } else {
                                    this.ui.updateMessage(agentMessageId, fullResponse);
                                }
                            } else if (data.type === 'error') {
                                this.ui.updateMessage(agentMessageId, '❌ Error: ' + data.error);
                                if (data.error && data.error.includes('API key')) {
                                    setTimeout(() => {
                                        if (confirm('Invalid API key. Would you like to change it?')) {
                                            this.changeApiKey();
                                        }
                                    }, 1000);
                                }
                            }
                        } catch (e) {
                            console.error('Error parsing SSE data:', e);
                        }
                    }
                }
            }
            
            this.chatHistory.push({ role: 'assistant', content: fullResponse });
            this.ui.addMessageActions(agentMessageId);
            
            // Save conversation
            this.currentChatId = this.storage.saveConversation(
                this.chatHistory,
                this.currentChatTitle,
                this.currentChatId,
                this.currentChatContext
            );
            this.updateChatHistoryUI();
            
        } catch (error) {
            console.error('Error generating response:', error);
            this.ui.updateMessage(agentMessageId, 'Sorry, I encountered an error. Please try again.');
        } finally {
            this.isGenerating = false;
            this.ui.setInputEnabled(true);
            this.ui.clearInput();
        }
    }
    
    regenerateResponse() {
        if (this.chatHistory.length < 2 || this.isGenerating) return;
        
        // Remove last assistant message
        this.chatHistory.pop();
        
        // Remove last message from UI
        const messages = document.querySelectorAll('.message');
        if (messages.length > 0) {
            messages[messages.length - 1].remove();
        }
        
        // Get last user message
        const lastUserMessage = this.chatHistory[this.chatHistory.length - 1];
        if (lastUserMessage && lastUserMessage.role === 'user') {
            // Remove it from history and resend
            this.chatHistory.pop();
            document.getElementById('userInput').value = lastUserMessage.content;
            this.sendMessage();
        }
    }
    
    copyMessage(messageId) {
        const message = document.getElementById(messageId);
        if (message) {
            const text = message.querySelector('.message-text').textContent;
            navigator.clipboard.writeText(text).then(() => {
                alert('📋 Message copied to clipboard!');
            });
        }
    }
    
    startNewChat(customTitle = null) {
        if (this.chatHistory.length > 0) {
            this.storage.saveConversation(
                this.chatHistory,
                this.currentChatTitle,
                this.currentChatId,
                this.currentChatContext
            );
            this.updateChatHistoryUI();
        }
        
        this.chatHistory = [];
        this.currentChatId = null;
        this.currentChatTitle = customTitle;
        this.currentChatContext = null;
        this.sessionId = null;
        this.ui.clearMessages();
        this.ui.showEmptyState();
    }
    
    loadConversation(id) {
        const conv = this.storage.getConversation(id);
        if (conv) {
            this.chatHistory = conv.messages;
            this.currentChatId = conv.id;
            this.currentChatTitle = conv.title;
            this.currentChatContext = conv.context || null;
            
            this.ui.clearMessages();
            this.ui.hideEmptyState();
            
            conv.messages.forEach(msg => {
                const role = msg.role === 'user' ? 'user' : 'agent';
                const content = msg.role === 'assistant' ?
                    (window.marked ? window.marked.parse(msg.content) : msg.content) :
                    msg.content;
                const messageId = this.ui.addMessage(role, content);
                
                if (msg.role === 'assistant') {
                    this.ui.addMessageActions(messageId);
                }
            });
        }
    }
    
    updateChatHistoryUI() {
        const conversations = this.storage.getAllConversations();
        this.ui.updateChatHistory(conversations);
    }
    
    exportChat() {
        const data = JSON.stringify(this.chatHistory, null, 2);
        const blob = new Blob([data], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `dualmind-cloud-chat-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }
    
    // Settings Management
    openSettings() {
        const darkMode = this.storage.getDarkMode();
        const customMemory = this.storage.getCustomMemory();
        const chatContext = this.currentChatContext || '';
        
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
            this.currentChatContext = input.value;
            if (this.currentChatId) {
                this.storage.updateConversationContext(this.currentChatId, input.value);
            }
            alert('✅ Chat context saved!');
        }
    }
    
    clearAllChats() {
        if (confirm('Are you sure you want to delete all chat history? This action cannot be undone.')) {
            this.storage.clearAllConversations();
            this.updateChatHistoryUI();
            alert('✅ All chats cleared!');
        }
    }
    
    // Chat Management
    async renameChat(chatId) {
        const conv = this.storage.getConversation(chatId);
        if (conv) {
            const newTitle = prompt('Enter new name:', conv.title);
            if (newTitle && newTitle.trim()) {
                this.storage.renameConversation(chatId, newTitle.trim());
                this.updateChatHistoryUI();
                if (this.currentChatId === chatId) {
                    this.currentChatTitle = newTitle.trim();
                }
                alert('✅ Chat renamed!');
            }
        }
    }
    
    deleteChat(chatId) {
        if (confirm('Are you sure you want to delete this chat?')) {
            this.storage.deleteConversation(chatId);
            this.updateChatHistoryUI();
            if (this.currentChatId === chatId) {
                this.startNewChat();
            }
            alert('✅ Chat deleted!');
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
        this.startNewChat(customName);
        this.closeNewChatModal();
        if (customName) {
            alert(`✅ New chat "${customName}" created!`);
        }
    }
    
    // Voice Input
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
                alert('Voice input failed. Please try again.');
            };
            
            recognition.start();
        } else {
            alert('Voice input is not supported in your browser.');
        }
    }
    
    switchToLocalMode() {
        window.location.href = '/local';
    }
}

// Create and export global instance
const app = new CloudModeApp();

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => app.initialize());
} else {
    app.initialize();
}

// Expose to window for HTML onclick handlers
window.cloudApp = app;

export default app;

