/**
 * CloudModeManager - Handles cloud provider API calls
 */

import { ChatManager } from './chat.js';

export class CloudModeManager extends ChatManager {
  constructor(storage, ui) {
    super(storage, ui);
    this.provider = null;
    this.model = null;
    this.apiKey = null;
  }
  
  async init() {
    await super.init();
    
    // Load saved provider and model
    const settings = await this.storage.getSettings();
    this.provider = settings.cloudProvider || 'google';
    this.model = await this.storage.getSelectedModel('cloud') || this.getDefaultModel(this.provider);
    
    // Get API key
    this.apiKey = await this.storage.getApiKey(this.provider);
    
    if (!this.apiKey) {
      this.ui.showError('No API key found. Please set your API key in settings.');
      this.ui.updateModelInfo('⚠️ No API Key');
    } else {
      this.ui.updateModelInfo(`☁️ ${this.provider} / ${this.model}`);
    }
  }
  
  getMode() {
    return 'cloud';
  }
  
  getDefaultModel(provider) {
    const defaults = {
      'google': 'gemini-1.5-flash',
      'openai': 'gpt-4o-mini',
      'anthropic': 'claude-3-5-sonnet-20241022',
      'nvidia': 'meta/llama-3.1-8b-instruct',
      'azure': 'gpt-4o'
    };
    return defaults[provider] || 'gemini-1.5-flash';
  }
  
  async generateResponse(message) {
    if (!this.apiKey) {
      throw new Error('No API key configured. Please set your API key in settings.');
    }
    
    try {
      switch (this.provider) {
        case 'google':
          return await this.callGoogleAI(message);
        case 'openai':
          return await this.callOpenAI(message);
        case 'anthropic':
          return await this.callAnthropic(message);
        default:
          throw new Error(`Provider ${this.provider} not implemented yet`);
      }
    } catch (error) {
      console.error('API call failed:', error);
      throw new Error(`Failed to get response: ${error.message}`);
    }
  }
  
  async callGoogleAI(message) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${this.model}:generateContent?key=${this.apiKey}`;
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contents: [{
          parts: [{
            text: message
          }]
        }]
      })
    });
    
    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Google AI API error: ${error}`);
    }
    
    const data = await response.json();
    return data.candidates[0].content.parts[0].text;
  }
  
  async callOpenAI(message) {
    const url = 'https://api.openai.com/v1/chat/completions';
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      },
      body: JSON.stringify({
        model: this.model,
        messages: [
          { role: 'user', content: message }
        ]
      })
    });
    
    if (!response.ok) {
      const error = await response.text();
      throw new Error(`OpenAI API error: ${error}`);
    }
    
    const data = await response.json();
    return data.choices[0].message.content;
  }
  
  async callAnthropic(message) {
    const url = 'https://api.anthropic.com/v1/messages';
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': this.apiKey,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: this.model,
        max_tokens: 1024,
        messages: [
          { role: 'user', content: message }
        ]
      })
    });
    
    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Anthropic API error: ${error}`);
    }
    
    const data = await response.json();
    return data.content[0].text;
  }
}

