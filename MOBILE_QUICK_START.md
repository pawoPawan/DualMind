# 📱 DualMind AI Mobile App - Quick Start Guide

## ⚡ Fast Track Setup (5 Minutes)

### Step 1: Run Setup Script
```bash
cd /Users/pawkumar/Documents/pawan/learn
./setup_mobile.sh
```

This will:
- ✅ Check Node.js/npm installation
- ✅ Install Expo CLI
- ✅ Create React Native project
- ✅ Install all dependencies
- ✅ Setup project structure

### Step 2: Start Development
```bash
cd mobile
npm start
```

### Step 3: Test on Your Phone
1. Install **Expo Go** app:
   - [Android](https://play.google.com/store/apps/details?id=host.exp.exponent)
   - [iOS](https://apps.apple.com/app/expo-go/id982107779)

2. Scan QR code from terminal

3. App loads on your phone! 🎉

---

## 🏗️ What Gets Created

```
mobile/
├── package.json              # Dependencies
├── App.js                    # Main app (pre-configured)
├── src/
│   ├── config/
│   │   ├── api.js           # ✅ API configuration
│   │   └── branding.js      # ✅ Branding settings
│   ├── services/
│   │   ├── api.js           # ✅ API client ready
│   │   └── storage.js       # ✅ Storage service ready
│   ├── screens/             # Add your screens here
│   ├── components/          # Add UI components here
│   ├── navigation/          # Navigation setup
│   └── utils/               # Helper functions
├── assets/                   # Images, icons
└── docs/
    └── SETUP.md             # Detailed setup guide
```

---

## 🔌 Connect to Your Backend

### Option 1: Testing on Simulator (Easiest)
```bash
# Terminal 1: Start backend
cd /Users/pawkumar/Documents/pawan/learn
./dualmind.sh start

# Terminal 2: Start mobile app
cd mobile
npm start
# Press 'i' for iOS or 'a' for Android
```

Backend URL: `http://localhost:8000` ✅ (Already configured)

### Option 2: Testing on Real Device
1. Find your computer's IP address:
   ```bash
   # Mac/Linux
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # Example output: 192.168.1.100
   ```

2. Update `mobile/src/config/api.js`:
   ```javascript
   export const API_BASE_URL = 'http://192.168.1.100:8000';
   ```

3. Make sure phone and computer are on **same WiFi network**

---

## 📱 Development Commands

```bash
cd mobile

# Start development server
npm start

# Run on iOS (Mac only)
npm run ios

# Run on Android
npm run android

# Clear cache and restart
expo start -c

# Install new packages
npm install package-name
```

---

## 🎨 Current Features (Out of the Box)

✅ **Basic App Structure**
- App.js with DualMind branding
- Splash screen ready
- StatusBar configured

✅ **API Integration Ready**
- Pre-configured API endpoints
- Connection to your backend
- Error handling setup

✅ **Secure Storage**
- API key encryption (SecureStore)
- Conversation caching (AsyncStorage)
- User preferences storage

✅ **Services Layer**
- API client with axios
- Storage abstraction
- Easy to extend

---

## 🚀 Next: Building the UI

### Add Screens

Create `mobile/src/screens/HomeScreen.js`:
```javascript
import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { BRANDING } from '../config/branding';

export default function HomeScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>
        {BRANDING.APP_ICON} {BRANDING.APP_NAME}
      </Text>
      
      <TouchableOpacity 
        style={[styles.card, styles.cloudCard]}
        onPress={() => navigation.navigate('CloudMode')}
      >
        <Text style={styles.cardIcon}>{BRANDING.MODES.CLOUD.ICON}</Text>
        <Text style={styles.cardTitle}>{BRANDING.MODES.CLOUD.NAME}</Text>
        <Text style={styles.cardDesc}>{BRANDING.MODES.CLOUD.DESCRIPTION}</Text>
      </TouchableOpacity>
      
      <TouchableOpacity 
        style={[styles.card, styles.localCard]}
        onPress={() => navigation.navigate('LocalMode')}
      >
        <Text style={styles.cardIcon}>{BRANDING.MODES.LOCAL.ICON}</Text>
        <Text style={styles.cardTitle}>{BRANDING.MODES.LOCAL.NAME}</Text>
        <Text style={styles.cardDesc}>{BRANDING.MODES.LOCAL.DESCRIPTION}</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f8f9fa',
    justifyContent: 'center',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 40,
  },
  card: {
    padding: 30,
    borderRadius: 20,
    marginVertical: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
  },
  cloudCard: {
    backgroundColor: '#667eea',
  },
  localCard: {
    backgroundColor: '#f093fb',
  },
  cardIcon: {
    fontSize: 48,
    textAlign: 'center',
    marginBottom: 10,
  },
  cardTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
    textAlign: 'center',
    marginBottom: 5,
  },
  cardDesc: {
    fontSize: 14,
    color: 'white',
    textAlign: 'center',
    opacity: 0.9,
  },
});
```

### Setup Navigation

Create `mobile/src/navigation/AppNavigator.js`:
```javascript
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import HomeScreen from '../screens/HomeScreen';
// Add more screens as you create them

const Stack = createStackNavigator();

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerStyle: { backgroundColor: '#667eea' },
          headerTintColor: '#fff',
          headerTitleStyle: { fontWeight: 'bold' },
        }}
      >
        <Stack.Screen 
          name="Home" 
          component={HomeScreen}
          options={{ title: '🧠 DualMind AI' }}
        />
        {/* Add more screens here */}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### Update App.js

```javascript
import React from 'react';
import AppNavigator from './src/navigation/AppNavigator';

export default function App() {
  return <AppNavigator />;
}
```

---

## 🧪 Testing Backend Connection

Create a test screen to verify API connection:

```javascript
import React, { useEffect, useState } from 'react';
import { View, Text, ActivityIndicator } from 'react-native';
import ApiService from '../services/api';

export default function TestScreen() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function checkHealth() {
      try {
        const data = await ApiService.checkHealth();
        setHealth(data);
      } catch (error) {
        setHealth({ error: error.message });
      } finally {
        setLoading(false);
      }
    }
    checkHealth();
  }, []);

  if (loading) return <ActivityIndicator size="large" />;

  return (
    <View style={{ padding: 20 }}>
      <Text>Backend Status:</Text>
      <Text>{JSON.stringify(health, null, 2)}</Text>
    </View>
  );
}
```

---

## 📦 Building for Production

### Android APK
```bash
cd mobile
expo build:android -t apk
```

Download link will be provided after build completes.

### iOS IPA (Requires Mac)
```bash
cd mobile
expo build:ios
```

### Alternative: Local Builds
```bash
# Generate native projects
expo eject

# Then use Android Studio or Xcode to build
```

---

## 🔧 Troubleshooting

### Problem: "Cannot connect to backend"
**Solution:**
1. Check backend is running: `./dualmind.sh status`
2. Check firewall allows port 8000
3. For real device: Verify IP address in `api.js`
4. Ensure same WiFi network

### Problem: "Metro bundler won't start"
**Solution:**
```bash
cd mobile
expo start -c  # Clear cache
```

### Problem: "Module not found"
**Solution:**
```bash
cd mobile
rm -rf node_modules
npm install
```

### Problem: "Expo Go not loading app"
**Solution:**
1. Ensure phone and computer on same network
2. Try scanning QR code again
3. Manually enter URL shown in terminal

---

## 📚 Resources

### Documentation
- `MOBILE_APP_PLAN.md` - Complete architecture
- `mobile/README.md` - Mobile-specific docs
- `mobile/docs/SETUP.md` - Detailed setup

### Learn More
- [Expo Documentation](https://docs.expo.dev/)
- [React Native Docs](https://reactnative.dev/)
- [React Navigation](https://reactnavigation.org/)

---

## 🎯 Recommended Development Flow

1. **Day 1: Setup & Structure**
   - ✅ Run `./setup_mobile.sh`
   - Create screens (Home, Cloud, Local, Chat)
   - Setup navigation

2. **Day 2: Cloud Mode**
   - Provider selector
   - Model selector  
   - API key input
   - Connect to backend API

3. **Day 3: Chat Interface**
   - Message list
   - Input field
   - Streaming responses
   - Message bubbles

4. **Day 4: Local Mode**
   - WebView setup
   - Load WebLLM
   - Communication bridge

5. **Day 5: Polish**
   - Biometric auth
   - Secure storage
   - Dark mode
   - Error handling

6. **Day 6: Build & Test**
   - Build APK/IPA
   - Test on real devices
   - Fix bugs

7. **Day 7: Deploy**
   - Prepare store listings
   - Upload builds
   - Or distribute directly

---

## ✅ Checklist

Setup:
- [ ] Node.js installed
- [ ] Expo CLI installed
- [ ] `./setup_mobile.sh` executed
- [ ] Backend server running

Development:
- [ ] Created screens
- [ ] Setup navigation
- [ ] Connected to API
- [ ] Tested on device

Features:
- [ ] Cloud Mode working
- [ ] Local Mode working
- [ ] Chat interface complete
- [ ] Biometric auth added

Deployment:
- [ ] Built APK
- [ ] Built IPA (if targeting iOS)
- [ ] Tested builds
- [ ] Ready to distribute

---

**You're all set! Start building your mobile app now! 🚀**

```bash
cd /Users/pawkumar/Documents/pawan/learn
./setup_mobile.sh
```

