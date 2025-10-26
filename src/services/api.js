import axios from 'axios';
import { API_BASE_URL, API_ENDPOINTS } from '../config/api';

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async checkHealth() {
    const response = await this.client.get(API_ENDPOINTS.HEALTH);
    return response.data;
  }

  async getProviders() {
    const response = await this.client.get(API_ENDPOINTS.PROVIDERS);
    return response.data;
  }

  async getModels(providerId) {
    const response = await this.client.get(API_ENDPOINTS.MODELS(providerId));
    return response.data;
  }

  async validateApiKey(provider, apiKey, model) {
    const response = await this.client.post(API_ENDPOINTS.VALIDATE_KEY, {
      provider,
      api_key: apiKey,
      model,
    });
    return response.data;
  }

  async sendMessage(message, provider, model, apiKey, sessionId) {
    const response = await this.client.post(API_ENDPOINTS.CHAT, {
      message,
      session_id: sessionId,
      provider,
      model,
      api_key: apiKey,
    });
    return response.data;
  }
}

export default new ApiService();

