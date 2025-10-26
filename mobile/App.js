import React, { useState, useEffect } from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, ActivityIndicator, TouchableOpacity } from 'react-native';
import { BRANDING } from './src/config/branding';
import ApiService from './src/services/api';

export default function App() {
  const [loading, setLoading] = useState(true);
  const [backendStatus, setBackendStatus] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    checkBackendConnection();
  }, []);

  const checkBackendConnection = async () => {
    try {
      setLoading(true);
      setError(null);
      const health = await ApiService.checkHealth();
      setBackendStatus(health);
    } catch (err) {
      setError(err.message || 'Cannot connect to backend');
      setBackendStatus(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.icon}>{BRANDING.APP_ICON}</Text>
      <Text style={styles.title}>{BRANDING.APP_NAME}</Text>
      <Text style={styles.subtitle}>Mobile App v{BRANDING.VERSION}</Text>
      
      <View style={styles.statusContainer}>
        <Text style={styles.sectionTitle}>Backend Connection:</Text>
        {loading ? (
          <ActivityIndicator size="large" color={BRANDING.COLORS.PRIMARY_START} />
        ) : error ? (
          <>
            <Text style={styles.error}>❌ {error}</Text>
            <Text style={styles.helpText}>
              Make sure backend is running:{'\n'}
              ./dualmind.sh start
            </Text>
            <TouchableOpacity 
              style={styles.retryButton}
              onPress={checkBackendConnection}
            >
              <Text style={styles.retryButtonText}>🔄 Retry Connection</Text>
            </TouchableOpacity>
          </>
        ) : (
          <>
            <Text style={styles.success}>✅ Connected!</Text>
            <View style={styles.statusDetails}>
              <Text style={styles.statusText}>Status: {backendStatus?.status}</Text>
              <Text style={styles.statusText}>Message: {backendStatus?.message}</Text>
            </View>
          </>
        )}
      </View>

      <View style={styles.infoContainer}>
        <Text style={styles.infoTitle}>🎉 Setup Complete!</Text>
        <Text style={styles.infoText}>
          • React Native + Expo ✅{'\n'}
          • API Integration ✅{'\n'}
          • Backend Connection ✅{'\n'}
          • Ready to build UI! ✅
        </Text>
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerText}>
          Next: Build screens for Cloud & Local modes
        </Text>
      </View>

      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  icon: {
    fontSize: 80,
    marginBottom: 10,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 5,
    color: '#333',
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    marginBottom: 30,
  },
  statusContainer: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 15,
    width: '100%',
    maxWidth: 400,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  success: {
    fontSize: 20,
    color: '#10b981',
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 15,
  },
  error: {
    fontSize: 16,
    color: '#ef4444',
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
  },
  helpText: {
    fontSize: 12,
    color: '#666',
    textAlign: 'center',
    marginBottom: 15,
  },
  retryButton: {
    backgroundColor: '#667eea',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  retryButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  statusDetails: {
    backgroundColor: '#f8f9fa',
    padding: 15,
    borderRadius: 10,
  },
  statusText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5,
  },
  infoContainer: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 15,
    width: '100%',
    maxWidth: 400,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
  },
  infoTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  infoText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 22,
  },
  footer: {
    marginTop: 20,
    padding: 15,
    backgroundColor: '#e7f0ff',
    borderRadius: 10,
    width: '100%',
    maxWidth: 400,
  },
  footerText: {
    fontSize: 13,
    color: '#667eea',
    textAlign: 'center',
    fontWeight: '600',
  },
});
