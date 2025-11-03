/**
 * DualMind UI Module
 * Handles all UI operations and DOM manipulation
 */

import { storage } from './storage.js';

export class UIManager {
    constructor() {
        this.elements = {};
        this.currentTheme = 'dark';
    }
    
    initialize() {
        this.cacheElements();
        this.setupEventListeners();
        this.loadTheme();
        this.setupAutoResize();
    }
    
    cacheElements() {
        this.elements = {
            chatMessages: document.getElementById('chatMessages'),
            userInput: document.getElementById('userInput'),
            sendBtn: document.getElementById('sendBtn'),
            voiceBtn: document.getElementById('voiceBtn'),
            sidebar: document.querySelector('.sidebar'),
            chatHistoryList: document.getElementById('chatHistoryList'),
            currentModelName: document.getElementById('currentModelName'),
            currentModelDesc: document.getElementById('currentModelDesc'),
            emptyState: document.querySelector('.empty-state'),
        };
    }
    
    setupEventListeners() {
        // Input auto-resize
        if (this.elements.userInput) {
            this.elements.userInput.addEventListener('input', () => {
                this.updateSendButton();
            });
        }
    }
    
    setupAutoResize() {
        const input = this.elements.userInput;
        if (input) {
            input.addEventListener('input', () => {
                input.style.height = 'auto';
                input.style.height = Math.min(input.scrollHeight, 200) + 'px';
            });
        }
    }
    
    updateSendButton() {
        if (this.elements.sendBtn && this.elements.userInput) {
            const hasText = this.elements.userInput.value.trim().length > 0;
            this.elements.sendBtn.disabled = !hasText;
        }
    }
    
    loadTheme() {
        const darkMode = storage.getDarkMode();
        if (darkMode) {
            document.body.classList.add('dark-mode');
            this.currentTheme = 'dark';
        } else {
            document.body.classList.remove('dark-mode');
            this.currentTheme = 'light';
        }
    }
    
    toggleTheme() {
        const isDark = document.body.classList.toggle('dark-mode');
        storage.saveDarkMode(isDark);
        this.currentTheme = isDark ? 'dark' : 'light';
    }
    
    hideEmptyState() {
        if (this.elements.emptyState) {
            this.elements.emptyState.style.display = 'none';
        }
    }
    
    showEmptyState() {
        if (this.elements.emptyState) {
            this.elements.emptyState.style.display = 'flex';
        }
    }
    
    addMessage(role, content) {
        const messageId = 'msg-' + Date.now();
        const avatar = role === 'user' ? '👤' : '🤖';
        const name = role === 'user' ? 'You' : 'DualMind AI';
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        messageDiv.id = messageId;
        messageDiv.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <h4>${name}</h4>
                <div class="message-text">${content}</div>
            </div>
        `;
        
        this.elements.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        return messageId;
    }
    
    updateMessage(messageId, content) {
        const message = document.getElementById(messageId);
        if (message) {
            const textDiv = message.querySelector('.message-text');
            textDiv.innerHTML = content;
            
            // Highlight code blocks
            message.querySelectorAll('pre code').forEach((block) => {
                if (window.hljs) {
                    window.hljs.highlightElement(block);
                }
            });
        }
    }
    
    addMessageActions(messageId) {
        const message = document.getElementById(messageId);
        if (message && !message.querySelector('.message-actions')) {
            const actionsDiv = document.createElement('div');
            actionsDiv.className = 'message-actions';
            actionsDiv.innerHTML = `
                <button class="action-btn" onclick="window.dualmind.copyMessage('${messageId}')">📋 Copy</button>
                <button class="action-btn" onclick="window.dualmind.regenerateResponse()">🔄 Regenerate</button>
            `;
            message.querySelector('.message-content').appendChild(actionsDiv);
        }
    }
    
    clearMessages() {
        if (this.elements.chatMessages) {
            this.elements.chatMessages.innerHTML = '';
        }
        this.showEmptyState();
    }
    
    scrollToBottom() {
        if (this.elements.chatMessages) {
            this.elements.chatMessages.scrollTop = this.elements.chatMessages.scrollHeight;
        }
    }
    
    clearInput() {
        if (this.elements.userInput) {
            this.elements.userInput.value = '';
            this.elements.userInput.style.height = 'auto';
        }
        this.updateSendButton();
    }
    
    setInputEnabled(enabled) {
        if (this.elements.userInput) {
            this.elements.userInput.disabled = !enabled;
        }
        if (this.elements.sendBtn) {
            this.elements.sendBtn.disabled = !enabled;
        }
    }
    
    updateModelDisplay(name, description) {
        if (this.elements.currentModelName) {
            this.elements.currentModelName.textContent = name;
        }
        if (this.elements.currentModelDesc) {
            this.elements.currentModelDesc.textContent = description;
        }
    }
    
    updateChatHistory(conversations) {
        if (!this.elements.chatHistoryList) return;
        
        this.elements.chatHistoryList.innerHTML = '';
        conversations.forEach(conv => {
            const item = document.createElement('div');
            item.className = 'chat-item';
            
            const textSpan = document.createElement('span');
            textSpan.className = 'chat-item-text';
            textSpan.textContent = conv.title;
            textSpan.onclick = () => window.dualmind.loadConversation(conv.id);
            
            const actions = document.createElement('div');
            actions.className = 'chat-item-actions';
            actions.innerHTML = `
                <button class="chat-action-btn" onclick="event.stopPropagation(); window.dualmind.renameChat(${conv.id})" title="Rename chat">✏️</button>
                <button class="chat-action-btn" onclick="event.stopPropagation(); window.dualmind.deleteChat(${conv.id})" title="Delete chat">🗑️</button>
            `;
            
            item.appendChild(textSpan);
            item.appendChild(actions);
            this.elements.chatHistoryList.appendChild(item);
        });
    }
    
    showModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
        }
    }
    
    hideModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('active');
        }
    }
    
    showNotification(message, type = 'info') {
        // Simple alert for now, can be enhanced
        alert(message);
    }
    
    toggleSidebar() {
        if (this.elements.sidebar) {
            this.elements.sidebar.classList.toggle('open');
        }
    }
    
    showLoadingIndicator(message = 'Downloading model...') {
        let indicator = document.getElementById('loadingIndicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'loadingIndicator';
            indicator.className = 'model-loading';
            document.body.appendChild(indicator);
        }
        indicator.innerHTML = `
            <div>${message}</div>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill" style="width: 0%"></div>
            </div>
        `;
        indicator.style.display = 'block';
    }
    
    updateLoadingProgress(percentage, message = '') {
        const indicator = document.getElementById('loadingIndicator');
        const fill = document.getElementById('progressFill');
        if (indicator && fill) {
            if (message) {
                indicator.querySelector('div:first-child').textContent = message;
            }
            fill.style.width = percentage + '%';
        }
    }
    
    hideLoadingIndicator() {
        const indicator = document.getElementById('loadingIndicator');
        if (indicator) {
            indicator.style.display = 'none';
        }
    }
    
    showPrompt(title, message, defaultValue = '') {
        return new Promise((resolve) => {
            const result = prompt(message, defaultValue);
            resolve(result);
        });
    }
    
    showConfirm(message) {
        return confirm(message);
    }
}

export const ui = new UIManager();

