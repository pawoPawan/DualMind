/**
 * DualMind Storage Module
 * Handles localStorage operations
 */

export class StorageManager {
    constructor() {
        this.KEYS = {
            CHATS: 'dualmind_chats',
            KB: 'dualmind_kb',
            CUSTOM_MEMORY: 'dualmind_custom_memory',
            DARK_MODE: 'dualmind_dark_mode',
            CURRENT_MODEL: 'dualmind_current_model',
            EMBEDDING_MODEL: 'dualmind_embedding_model'
        };
    }
    
    // Chat History
    saveConversation(messages, customTitle = null, chatId = null, context = null) {
        if (!messages || messages.length === 0) return;
        
        const conversations = this.getAllConversations();
        const title = customTitle || messages[0]?.content?.substring(0, 50) || 'New Chat';
        const timestamp = chatId || Date.now();
        
        // Check if conversation exists
        const existingIndex = conversations.findIndex(c => c.id === timestamp);
        
        const conversation = {
            id: timestamp,
            title: title,
            messages: messages,
            timestamp: timestamp,
            context: context || null
        };
        
        if (existingIndex >= 0) {
            // Update existing conversation
            conversations[existingIndex] = conversation;
        } else {
            // Add new conversation
            conversations.unshift(conversation);
        }
        
        localStorage.setItem(this.KEYS.CHATS, JSON.stringify(conversations.slice(0, 50)));
        return timestamp;
    }
    
    getAllConversations() {
        const data = localStorage.getItem(this.KEYS.CHATS);
        return data ? JSON.parse(data) : [];
    }
    
    getConversation(id) {
        const conversations = this.getAllConversations();
        return conversations.find(c => c.id === id);
    }
    
    deleteConversation(id) {
        const conversations = this.getAllConversations();
        const filtered = conversations.filter(c => c.id !== id);
        localStorage.setItem(this.KEYS.CHATS, JSON.stringify(filtered));
    }
    
    renameConversation(id, newTitle) {
        const conversations = this.getAllConversations();
        const conv = conversations.find(c => c.id === id);
        if (conv) {
            conv.title = newTitle;
            localStorage.setItem(this.KEYS.CHATS, JSON.stringify(conversations));
        }
    }
    
    updateConversationContext(id, context) {
        const conversations = this.getAllConversations();
        const conv = conversations.find(c => c.id === id);
        if (conv) {
            conv.context = context;
            localStorage.setItem(this.KEYS.CHATS, JSON.stringify(conversations));
        }
    }
    
    clearAllConversations() {
        localStorage.removeItem(this.KEYS.CHATS);
    }
    
    // Knowledge Base
    getKnowledgeBase() {
        const data = localStorage.getItem(this.KEYS.KB);
        return data ? JSON.parse(data) : [];
    }
    
    saveKnowledgeBase(kb) {
        localStorage.setItem(this.KEYS.KB, JSON.stringify(kb));
    }
    
    // Custom Memory
    getCustomMemory() {
        return localStorage.getItem(this.KEYS.CUSTOM_MEMORY) || '';
    }
    
    saveCustomMemory(memory) {
        localStorage.setItem(this.KEYS.CUSTOM_MEMORY, memory);
    }
    
    // Dark Mode
    getDarkMode() {
        return localStorage.getItem(this.KEYS.DARK_MODE) === 'true';
    }
    
    saveDarkMode(enabled) {
        localStorage.setItem(this.KEYS.DARK_MODE, enabled.toString());
    }
    
    // Current Model
    getCurrentModel() {
        return localStorage.getItem(this.KEYS.CURRENT_MODEL);
    }
    
    saveCurrentModel(modelId) {
        localStorage.setItem(this.KEYS.CURRENT_MODEL, modelId);
    }
    
    // Embedding Model
    getEmbeddingModel() {
        return localStorage.getItem(this.KEYS.EMBEDDING_MODEL) || 'Xenova/all-MiniLM-L6-v2';
    }
    
    saveEmbeddingModel(modelId) {
        localStorage.setItem(this.KEYS.EMBEDDING_MODEL, modelId);
    }
}

export const storage = new StorageManager();

