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
        this.currentChatId = null;
        this.currentChatTitle = null;
        this.currentChatContext = null;
    }
    
    async sendMessage(message) {
        if (!message || !message.trim()) {
            return;
        }
        
        // Check if model is loaded
        if (!config.engine) {
            ui.showNotification('⚠️ Please select and load a model first!');
            // Open model selector to help user
            if (window.dualmind && window.dualmind.openModelSelector) {
                window.dualmind.openModelSelector();
            }
            return;
        }
        
        if (config.isGenerating) {
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
            
            // Get custom memory and chat context
            const customMemory = storage.getCustomMemory();
            const chatContext = this.currentChatContext || '';
            
            let systemMessages = [];
            if (customMemory) {
                systemMessages.push({ role: 'system', content: customMemory });
            }
            if (chatContext) {
                systemMessages.push({ role: 'system', content: chatContext });
            }
            
            // Check if we have knowledge base documents and perform RAG
            const { rag } = await import('./rag.js');
            
            // Show RAG search indicator if documents exist
            if (rag.knowledgeBase.length > 0) {
                ui.updateMessage(agentMessageId, '🔍 Searching knowledge base...');
            }
            
            const relevantChunks = await rag.searchRelevantChunks(message, 3);
            
            if (relevantChunks.length > 0) {
                // Update to show RAG is being used
                ui.updateMessage(agentMessageId, '📚 Found relevant information, generating answer...');
                
                console.log(`📚 RAG: Using ${relevantChunks.length} relevant chunks`);
                relevantChunks.forEach((chunk, i) => {
                    console.log(`  ${i+1}. ${chunk.filename} (similarity: ${chunk.similarity.toFixed(3)})`);
                });
                
                let ragContext = "Here is relevant information from uploaded documents:\n\n";
                relevantChunks.forEach((chunk, index) => {
                    ragContext += `[Document: ${chunk.filename}, Relevance: ${(chunk.similarity * 100).toFixed(1)}%]\n${chunk.text}\n\n`;
                });
                ragContext += "Based on the above information and your knowledge, please answer the user's question.";
                systemMessages.push({ role: 'system', content: ragContext });
            } else if (rag.knowledgeBase.length > 0) {
                console.log('📚 RAG: No relevant chunks found for this query');
                ui.updateMessage(agentMessageId, '<div class="loading-dots"><span></span><span></span><span></span></div>');
            }
            
            const messages = systemMessages.length > 0 ?
                [...systemMessages, ...this.chatHistory] :
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
            
            // Save conversation and ensure RAG is linked to this chat
            const savedChatId = storage.saveConversation(
                this.chatHistory, 
                this.currentChatTitle, 
                this.currentChatId,
                this.currentChatContext
            );
            
            // If chat ID was just created, update RAG manager
            if (!this.currentChatId || this.currentChatId !== savedChatId) {
                this.currentChatId = savedChatId;
                const { rag } = await import('./rag.js');
                rag.setCurrentChat(this.currentChatId);
            }
            
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
    
    async startNewChat(customTitle = null) {
        if (this.chatHistory.length > 0) {
            storage.saveConversation(
                this.chatHistory, 
                this.currentChatTitle, 
                this.currentChatId,
                this.currentChatContext
            );
            this.updateChatHistoryUI();
        }
        
        this.chatHistory = [];
        this.currentChatId = Date.now(); // Generate new chat ID immediately
        this.currentChatTitle = customTitle;
        this.currentChatContext = null;
        
        // Clear documents for new chat
        const { rag } = await import('./rag.js');
        rag.setCurrentChat(this.currentChatId);
        
        ui.clearMessages();
        ui.showEmptyState();
        console.log(`🆕 Started new chat: ${this.currentChatId}`);
    }
    
    async loadConversation(id) {
        const conv = storage.getConversation(id);
        if (conv) {
            this.chatHistory = conv.messages;
            this.currentChatId = conv.id;
            this.currentChatTitle = conv.title;
            this.currentChatContext = conv.context || null;
            
            // Load documents for this chat
            const { rag } = await import('./rag.js');
            rag.setCurrentChat(this.currentChatId);
            
            ui.clearMessages();
            ui.hideEmptyState();
            console.log(`📂 Loaded chat: ${this.currentChatId} with ${rag.knowledgeBase.length} documents`);
            
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

