// API Configuration
// Change this to your server's IP address when testing on real device
export const API_BASE_URL = __DEV__ 
  ? 'http://localhost:8000'  // Development (simulator)
  : 'http://localhost:8000'; // Update with your computer's IP for real device testing

export const API_ENDPOINTS = {
  HEALTH: '/health',
  PROVIDERS: '/api/providers',
  CHAT: '/api/chat',
  CHAT_STREAM: '/api/chat/stream',
  VALIDATE_KEY: '/api/validate-key',
  MODELS: (providerId) => `/api/providers/${providerId}/models`,
};

