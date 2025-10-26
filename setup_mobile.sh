#!/bin/bash

# DualMind AI Mobile App Setup Script
# This script sets up the React Native + Expo mobile app development environment

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "============================================================"
echo "     📱 DualMind AI - Mobile App Setup"
echo "============================================================"
echo -e "${NC}"

# Check if Node.js is installed
echo -e "${YELLOW}Checking prerequisites...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed!${NC}"
    echo "Please install Node.js from https://nodejs.org/"
    echo "Recommended version: 18.x or higher"
    exit 1
fi

NODE_VERSION=$(node -v)
echo -e "${GREEN}✅ Node.js ${NODE_VERSION} found${NC}"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is not installed!${NC}"
    exit 1
fi

NPM_VERSION=$(npm -v)
echo -e "${GREEN}✅ npm ${NPM_VERSION} found${NC}"

# Install Expo CLI globally
echo -e "\n${YELLOW}Installing Expo CLI...${NC}"
npm install -g expo-cli

# Create mobile directory
echo -e "\n${YELLOW}Creating mobile app directory...${NC}"
mkdir -p mobile

# Initialize Expo project
echo -e "\n${YELLOW}Initializing React Native project with Expo...${NC}"
cd mobile

# Create Expo app
npx create-expo-app@latest . --template blank

# Install additional dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
npm install axios react-navigation @react-navigation/native @react-navigation/stack
npm install react-native-async-storage/async-storage
npm install expo-secure-store
npm install expo-local-authentication
npm install expo-notifications
npm install react-native-webview

# Create project structure
echo -e "\n${YELLOW}Creating project structure...${NC}"
mkdir -p src/{config,screens,components,services,navigation,utils}
mkdir -p assets docs

# Create configuration files
echo -e "\n${YELLOW}Creating configuration files...${NC}"

# Create API config
cat > src/config/api.js << 'EOF'
// API Configuration
// Change this to your server's IP address when testing on real device
export const API_BASE_URL = __DEV__ 
  ? 'http://localhost:8000'  // Development (simulator)
  : 'http://192.168.1.x:8000'; // Development (real device) - Update with your IP

export const API_ENDPOINTS = {
  HEALTH: '/health',
  PROVIDERS: '/api/providers',
  CHAT: '/api/chat',
  CHAT_STREAM: '/api/chat/stream',
  VALIDATE_KEY: '/api/validate-key',
  MODELS: (providerId) => `/api/providers/${providerId}/models`,
};
EOF

# Create branding config
cat > src/config/branding.js << 'EOF'
// Branding Configuration
// This will be synced with your backend's branding_config.py

export const BRANDING = {
  APP_NAME: 'DualMind AI',
  APP_ICON: '🧠',
  VERSION: '1.0.0',
  
  COLORS: {
    PRIMARY_START: '#667eea',
    PRIMARY_END: '#764ba2',
    SECONDARY_START: '#f093fb',
    SECONDARY_END: '#f5576c',
    BACKGROUND: '#f8f9fa',
    TEXT_PRIMARY: '#333333',
    TEXT_SECONDARY: '#666666',
    SUCCESS: '#10b981',
    ERROR: '#ef4444',
    WARNING: '#f59e0b',
  },
  
  MODES: {
    CLOUD: {
      NAME: 'Cloud Mode',
      ICON: '☁️',
      DESCRIPTION: 'Connect to powerful cloud AI',
    },
    LOCAL: {
      NAME: 'Local Mode',
      ICON: '🔒',
      DESCRIPTION: 'Private AI on your device',
    },
  },
};
EOF

# Create API service
cat > src/services/api.js << 'EOF'
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
EOF

# Create storage service
cat > src/services/storage.js << 'EOF'
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as SecureStore from 'expo-secure-store';

class StorageService {
  // Secure storage for sensitive data (API keys)
  async saveApiKey(provider, apiKey) {
    await SecureStore.setItemAsync(`api_key_${provider}`, apiKey);
  }

  async getApiKey(provider) {
    return await SecureStore.getItemAsync(`api_key_${provider}`);
  }

  async deleteApiKey(provider) {
    await SecureStore.deleteItemAsync(`api_key_${provider}`);
  }

  // Regular storage for non-sensitive data
  async saveData(key, value) {
    await AsyncStorage.setItem(key, JSON.stringify(value));
  }

  async getData(key) {
    const value = await AsyncStorage.getItem(key);
    return value ? JSON.parse(value) : null;
  }

  async deleteData(key) {
    await AsyncStorage.removeItem(key);
  }

  // Conversation history
  async saveConversation(sessionId, messages) {
    await this.saveData(`conversation_${sessionId}`, messages);
  }

  async getConversation(sessionId) {
    return await this.getData(`conversation_${sessionId}`);
  }

  // User preferences
  async savePreferences(preferences) {
    await this.saveData('user_preferences', preferences);
  }

  async getPreferences() {
    return await this.getData('user_preferences');
  }
}

export default new StorageService();
EOF

# Update App.js
cat > App.js << 'EOF'
import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { BRANDING } from './src/config/branding';

export default function App() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{BRANDING.APP_ICON} {BRANDING.APP_NAME}</Text>
      <Text style={styles.subtitle}>Mobile App Coming Soon!</Text>
      <Text style={styles.info}>Setup completed successfully ✅</Text>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 18,
    color: '#666',
    marginBottom: 20,
  },
  info: {
    fontSize: 14,
    color: '#10b981',
  },
});
EOF

# Create README for mobile
cat > README.md << 'EOF'
# 📱 DualMind AI Mobile App

React Native mobile app for DualMind AI chatbot.

## 🚀 Quick Start

### Development
```bash
# Start Expo development server
npm start

# Run on iOS simulator (Mac only)
npm run ios

# Run on Android emulator
npm run android

# Run on physical device
# 1. Install Expo Go app on your phone
# 2. Scan QR code from terminal
```

### Configuration

1. **Update API URL** (for real device testing):
   - Edit `src/config/api.js`
   - Change `192.168.1.x` to your computer's IP address

2. **Start Backend Server**:
   ```bash
   cd ..
   ./dualmind.sh start
   ```

## 📱 Testing

- **iOS Simulator**: Requires Mac with Xcode
- **Android Emulator**: Requires Android Studio
- **Physical Device**: Install Expo Go app

## 🏗️ Building

```bash
# Build for Android (APK)
expo build:android

# Build for iOS (IPA)
expo build:ios
```

## 📚 Documentation

See `../MOBILE_APP_PLAN.md` for complete architecture and features.
EOF

# Create setup documentation
cat > docs/SETUP.md << 'EOF'
# Mobile App Development Setup

## Prerequisites

- Node.js 18.x or higher
- npm or yarn
- Expo CLI
- For iOS: Mac with Xcode
- For Android: Android Studio

## Installation

Run the setup script:
```bash
cd /path/to/learn
chmod +x setup_mobile.sh
./setup_mobile.sh
```

## Running the App

```bash
cd mobile
npm start
```

Then choose:
- Press `i` for iOS simulator
- Press `a` for Android emulator
- Scan QR code with Expo Go app on your phone

## Connecting to Backend

The mobile app needs to connect to your FastAPI backend:

1. Start the backend server:
   ```bash
   cd ..
   ./dualmind.sh start
   ```

2. For physical device testing, update `src/config/api.js` with your computer's IP address

3. Ensure your phone and computer are on the same network

## Troubleshooting

- **Cannot connect to backend**: Check firewall settings
- **Metro bundler issues**: Clear cache with `expo start -c`
- **Module not found**: Run `npm install` again
EOF

echo -e "\n${GREEN}============================================================${NC}"
echo -e "${GREEN}✅ Mobile app setup completed successfully!${NC}"
echo -e "${GREEN}============================================================${NC}"

echo -e "\n${BLUE}📱 Next Steps:${NC}"
echo -e "1. ${YELLOW}cd mobile${NC}"
echo -e "2. ${YELLOW}npm start${NC} (Start Expo development server)"
echo -e "3. Install ${YELLOW}Expo Go${NC} app on your phone"
echo -e "4. Scan the QR code to test on your device"
echo -e "\n${BLUE}📚 Documentation:${NC}"
echo -e "- Mobile app plan: ${YELLOW}MOBILE_APP_PLAN.md${NC}"
echo -e "- Setup guide: ${YELLOW}mobile/docs/SETUP.md${NC}"
echo -e "- Mobile README: ${YELLOW}mobile/README.md${NC}"

echo -e "\n${BLUE}⚙️  Backend Server:${NC}"
echo -e "Make sure to start the backend:"
echo -e "${YELLOW}./dualmind.sh start${NC}"

echo -e "\n${GREEN}🎉 Ready to build your mobile app!${NC}\n"

