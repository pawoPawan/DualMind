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
    saveConversation(messages) {
        if (!messages || messages.length === 0) return;
        
        const conversations = this.getAllConversations();
        const title = messages[0]?.content?.substring(0, 50) || 'New Chat';
        const timestamp = Date.now();
        
        conversations.unshift({
            id: timestamp,
            title: title,
            messages: messages,
            timestamp: timestamp
        });
        
        localStorage.setItem(this.KEYS.CHATS, JSON.stringify(conversations.slice(0, 50)));
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

