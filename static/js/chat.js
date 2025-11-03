/**
 * DualMind Chat Module
 * Handles chat functionality and message processing
 */

import { ui } from './ui.js';
import { storage } from './storage.js';
import { config } from './config.js';

export class ChatManager {
    constructor() {
        this.chatHistory = [];
    }
    
    async sendMessage(message) {
        if (!message || !message.trim() || !config.engine || config.isGenerating) {
            return;
        }
        
        config.isGenerating = true;
        ui.setInputEnabled(false);
        ui.hideEmptyState();
        
        // Add user message
        ui.addMessage('user', message);
        this.chatHistory.push({ role: 'user', content: message });
        
        // Add loading placeholder
        const agentMessageId = ui.addMessage('agent', '<div class="loading-dots"><span></span><span></span><span></span></div>');
        
        try {
            let fullResponse = '';
            
            // Get custom memory if any
            const customMemory = storage.getCustomMemory();
            const messages = customMemory ? 
                [{ role: 'system', content: customMemory }, ...this.chatHistory] :
                this.chatHistory;
            
            // Generate response
            const response = await config.engine.chat.completions.create({
                messages: messages,
                stream: true,
            });
            
            for await (const chunk of response) {
                const content = chunk.choices[0]?.delta?.content || '';
                fullResponse += content;
                
                // Update with markdown rendering
                if (window.marked) {
                    ui.updateMessage(agentMessageId, window.marked.parse(fullResponse));
                } else {
                    ui.updateMessage(agentMessageId, fullResponse);
                }
            }
            
            this.chatHistory.push({ role: 'assistant', content: fullResponse });
            ui.addMessageActions(agentMessageId);
            
            // Save conversation
            storage.saveConversation(this.chatHistory);
            this.updateChatHistoryUI();
            
        } catch (error) {
            console.error('Error generating response:', error);
            ui.updateMessage(agentMessageId, 'Sorry, I encountered an error. Please try again.');
        } finally {
            config.isGenerating = false;
            ui.setInputEnabled(true);
            ui.clearInput();
        }
    }
    
    async regenerateLastResponse() {
        if (this.chatHistory.length < 2 || config.isGenerating) return;
        
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
            await this.sendMessage(lastUserMessage.content);
        }
    }
    
    startNewChat() {
        if (this.chatHistory.length > 0) {
            storage.saveConversation(this.chatHistory);
            this.updateChatHistoryUI();
        }
        
        this.chatHistory = [];
        ui.clearMessages();
        ui.showEmptyState();
    }
    
    loadConversation(id) {
        const conv = storage.getConversation(id);
        if (conv) {
            this.chatHistory = conv.messages;
            ui.clearMessages();
            ui.hideEmptyState();
            
            conv.messages.forEach(msg => {
                const role = msg.role === 'user' ? 'user' : 'agent';
                const content = msg.role === 'assistant' ? 
                    (window.marked ? window.marked.parse(msg.content) : msg.content) :
                    msg.content;
                const messageId = ui.addMessage(role, content);
                
                if (msg.role === 'assistant') {
                    ui.addMessageActions(messageId);
                }
            });
        }
    }
    
    updateChatHistoryUI() {
        const conversations = storage.getAllConversations();
        ui.updateChatHistory(conversations);
    }
    
    exportChat() {
        const data = JSON.stringify(this.chatHistory, null, 2);
        const blob = new Blob([data], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `dualmind-chat-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }
    
    copyMessage(messageId) {
        const message = document.getElementById(messageId);
        if (message) {
            const text = message.querySelector('.message-text').textContent;
            navigator.clipboard.writeText(text).then(() => {
                ui.showNotification('Message copied to clipboard!');
            });
        }
    }
}

export const chat = new ChatManager();

