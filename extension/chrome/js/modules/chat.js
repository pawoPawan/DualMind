/**
 * ChatManager - Base class for chat management
 * Extended by LocalModeManager and CloudModeManager
 */

export class ChatManager {
  constructor(storage, ui) {
    this.storage = storage;
    this.ui = ui;
    this.currentChat = null;
  }
  
  async init() {
    // Load current chat or create new one
    const savedChat = await this.storage.getCurrentChat();
    if (savedChat) {
      this.currentChat = savedChat;
      this.loadChatHistory();
    } else {
      await this.startNewChat();
    }
  }
  
  async startNewChat() {
    this.currentChat = {
      id: Date.now(),
      messages: [],
      createdAt: new Date().toISOString(),
      mode: this.getMode()
    };
    
    await this.storage.setCurrentChat(this.currentChat);
    await this.storage.saveChat(this.currentChat);
    
    this.ui.clearMessages();
    console.log('🆕 Started new chat:', this.currentChat.id);
  }
  
  async sendMessage(text) {
    if (!text.trim()) return;
    
    // Add user message
    this.ui.addUserMessage(text);
    
    // Save user message
    this.currentChat.messages.push({
      role: 'user',
      content: text,
      timestamp: new Date().toISOString()
    });
    
    await this.storage.saveChat(this.currentChat);
    
    // Show loading indicator
    const agentMessage = this.ui.addAgentMessage();
    
    try {
      // Generate response (implemented by subclasses)
      const response = await this.generateResponse(text);
      
      // Update agent message
      this.ui.updateMessage(agentMessage, response);
      
      // Save agent message
      this.currentChat.messages.push({
        role: 'assistant',
        content: response,
        timestamp: new Date().toISOString()
      });
      
      await this.storage.saveChat(this.currentChat);
      
    } catch (error) {
      console.error('Failed to generate response:', error);
      this.ui.updateMessage(agentMessage, `❌ Error: ${error.message}`);
    }
  }
  
  loadChatHistory() {
    this.ui.clearMessages();
    
    if (this.currentChat && this.currentChat.messages) {
      this.currentChat.messages.forEach(msg => {
        if (msg.role === 'user') {
          this.ui.addUserMessage(msg.content);
        } else {
          this.ui.addAgentMessage(msg.content);
        }
      });
    }
  }
  
  // To be implemented by subclasses
  async generateResponse(message) {
    throw new Error('generateResponse must be implemented by subclass');
  }
  
  getMode() {
    throw new Error('getMode must be implemented by subclass');
  }
}

