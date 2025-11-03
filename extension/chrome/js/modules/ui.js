/**
 * UIManager - Handles all UI operations
 */

export class UIManager {
  constructor() {
    this.messagesContainer = document.getElementById('chat-messages');
    this.loadingOverlay = document.getElementById('loading-overlay');
    this.loadingText = document.getElementById('loading-text');
  }
  
  // Loading
  showLoading(text = 'Loading...') {
    if (this.loadingOverlay) {
      this.loadingOverlay.classList.remove('hidden');
    }
    if (this.loadingText) {
      this.loadingText.textContent = text;
    }
  }
  
  hideLoading() {
    if (this.loadingOverlay) {
      this.loadingOverlay.classList.add('hidden');
    }
  }
  
  // Messages
  clearMessages() {
    if (this.messagesContainer) {
      this.messagesContainer.innerHTML = '';
    }
  }
  
  addUserMessage(text) {
    return this.addMessage('user', text);
  }
  
  addAgentMessage(text = '') {
    return this.addMessage('agent', text);
  }
  
  addMessage(type, text) {
    if (!this.messagesContainer) return null;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${type}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    if (text) {
      contentDiv.innerHTML = this.formatMessage(text);
    } else {
      contentDiv.innerHTML = '<div class="loading-dots"><span></span><span></span><span></span></div>';
    }
    
    messageDiv.appendChild(contentDiv);
    this.messagesContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    this.scrollToBottom();
    
    return messageDiv;
  }
  
  updateMessage(messageElement, text) {
    if (!messageElement) return;
    
    const contentDiv = messageElement.querySelector('.message-content');
    if (contentDiv) {
      contentDiv.innerHTML = this.formatMessage(text);
    }
    
    this.scrollToBottom();
  }
  
  formatMessage(text) {
    // Basic markdown-like formatting
    text = text
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/`(.+?)`/g, '<code>$1</code>')
      .replace(/\n/g, '<br>');
    
    // Code blocks
    text = text.replace(/```(\w+)?\n([\s\S]+?)```/g, (match, lang, code) => {
      return `<pre><code class="language-${lang || 'text'}">${this.escapeHtml(code.trim())}</code></pre>`;
    });
    
    return text;
  }
  
  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
  
  scrollToBottom() {
    if (this.messagesContainer) {
      this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
  }
  
  // Notifications
  showError(message) {
    this.addMessage('agent', `❌ Error: ${message}`);
  }
  
  showSuccess(message) {
    this.addMessage('agent', `✅ ${message}`);
  }
  
  showInfo(message) {
    this.addMessage('agent', `ℹ️ ${message}`);
  }
  
  // Model Info
  updateModelInfo(text) {
    const modelInfo = document.getElementById('model-info');
    if (modelInfo) {
      modelInfo.textContent = text;
    }
  }
}

