"""
FastAPI Server for GauraAI Chatbot with Web UI
Supports both Cloud Mode (Google ADK) and Local Mode (Browser-based inference)
Reference: https://google.github.io/adk-docs/

All branding and configuration can be customized in branding_config.py
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
import os
from pathlib import Path
import json
import asyncio
import google.generativeai as genai

# Import branding configuration
from branding_config import *

# Create FastAPI app
app = FastAPI(
    title=CHATBOT_TITLE,
    description=CHATBOT_DESCRIPTION,
    version=VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
static_dir = Path("static")
static_dir.mkdir(exist_ok=True)
if static_dir.exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Store user sessions with their API keys
user_sessions = {}


# Pydantic models
class ChatRequest(BaseModel):
    message: str
    api_key: str
    provider: Optional[str] = "nvidia"  # Cloud provider selection
    model: Optional[str] = None  # Selected model ID
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    provider: Optional[str] = None


class RAGChatRequest(BaseModel):
    message: str
    api_key: str
    provider: Optional[str] = "nvidia"
    model: Optional[str] = None
    session_id: Optional[str] = None
    embedding_provider: Optional[str] = "openai"  # Embedding provider
    embedding_model: Optional[str] = None  # Embedding model
    embedding_api_key: Optional[str] = None  # Separate API key for embeddings
    use_rag: bool = True  # Whether to use RAG
    top_k: int = 3  # Number of relevant chunks to retrieve


class DocumentUploadRequest(BaseModel):
    filename: str
    content: str  # Base64 encoded file content
    session_id: str
    embedding_provider: str = "openai"
    embedding_model: Optional[str] = None
    embedding_api_key: Optional[str] = None


class DocumentListResponse(BaseModel):
    documents: List[Dict[str, Any]]
    total: int


class DocumentDeleteRequest(BaseModel):
    session_id: str
    doc_id: str


class EmbeddingProvidersResponse(BaseModel):
    providers: Dict[str, Any]


# Routes
@app.get("/local", response_class=HTMLResponse)
async def local_mode():
    """Serve the modular local browser-based inference UI"""
    # Serve the consolidated modular UI
    with open("static/local.html", "r") as f:
        html_template = f.read()
    return html_template


@app.get("/cloud", response_class=HTMLResponse)
async def cloud_mode():
    """Serve the Cloud Mode UI with provider selection"""
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{CHATBOT_TITLE}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, {COLOR_PRIMARY_START} 0%, {COLOR_PRIMARY_END} 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        
        .modal-overlay.hidden {
            display: none;
        }
        
        .api-key-modal {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 90%;
            text-align: center;
        }
        
        .modal-title {
            font-size: 28px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .modal-subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }
        
        .api-key-input {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            margin-bottom: 10px;
            outline: none;
            transition: border-color 0.3s;
        }
        
        .api-key-input:focus {
            border-color: #667eea;
        }
        
        .modal-button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, {COLOR_PRIMARY_START} 0%, {COLOR_PRIMARY_END} 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
            margin-top: 10px;
        }
        
        .modal-button:hover {
            transform: scale(1.02);
        }
        
        .modal-button:active {
            transform: scale(0.98);
        }
        
        .modal-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .modal-button-secondary {
            padding: 15px 25px;
            background: white;
            color: {COLOR_PRIMARY_START};
            border: 2px solid {COLOR_PRIMARY_START};
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s;
            margin-top: 20px;
        }
        
        .modal-button-secondary:hover {
            background: #f0f4ff;
            transform: scale(1.02);
        }
        
        .modal-button-secondary:active {
            transform: scale(0.98);
        }
        
        .model-card {
            background: #f8f9fa;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 12px;
            margin: 6px 0;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .model-card:hover {
            border-color: {COLOR_PRIMARY_START};
            transform: translateX(4px);
            background: #fff;
        }
        
        .model-card.selected {
            border-color: {COLOR_PRIMARY_START};
            background: #f0f4ff;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
        }
        
        .model-card-title {
            font-weight: bold;
            color: #333;
            font-size: 14px;
            margin-bottom: 4px;
        }
        
        .model-card-description {
            font-size: 12px;
            color: #666;
        }
        
        .model-recommended-badge {
            display: inline-block;
            background: linear-gradient(135deg, {COLOR_PRIMARY_START} 0%, {COLOR_PRIMARY_END} 100%);
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            margin-left: 8px;
        }
        
        .help-text {
            font-size: 14px;
            color: #999;
            margin-top: 20px;
        }
        
        .help-text a {
            color: #667eea;
            text-decoration: none;
        }
        
        .help-text a:hover {
            text-decoration: underline;
        }
        
        .chat-container {
            width: 90%;
            max-width: 800px;
            height: 90vh;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .chat-header {
            background: linear-gradient(135deg, {COLOR_PRIMARY_START} 0%, {COLOR_PRIMARY_END} 100%);
            color: white;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header-title {
            font-size: 24px;
            font-weight: bold;
        }
        
        .settings-btn {
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            padding: 8px 15px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
        }
        
        .settings-btn:hover {
            background: rgba(255,255,255,0.3);
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f7f7f7;
        }
        
        .message {
            margin-bottom: 15px;
            display: flex;
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message-content {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 18px;
            word-wrap: break-word;
            white-space: pre-wrap;
        }
        
        .message.user .message-content {
            background: linear-gradient(135deg, {COLOR_PRIMARY_START} 0%, {COLOR_PRIMARY_END} 100%);
            color: white;
        }
        
        .message.agent .message-content {
            background: white;
            color: #333;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .chat-input-container {
            display: flex;
            padding: 20px;
            background: white;
            border-top: 1px solid #e0e0e0;
        }
        
        #messageInput {
            flex: 1;
            padding: 12px 18px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }
        
        #messageInput:focus {
            border-color: #667eea;
        }
        
        #sendButton {
            margin-left: 10px;
            padding: 12px 30px;
            background: linear-gradient(135deg, {COLOR_PRIMARY_START} 0%, {COLOR_PRIMARY_END} 100%);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        #sendButton:hover {
            transform: scale(1.05);
        }
        
        #sendButton:active {
            transform: scale(0.95);
        }
        
        #sendButton:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .typing-indicator {
            display: none;
            padding: 12px 18px;
            background: white;
            border-radius: 18px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            width: fit-content;
        }
        
        .typing-indicator.active {
            display: block;
        }
        
        .typing-indicator span {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #667eea;
            margin: 0 2px;
            animation: bounce 1.4s infinite ease-in-out both;
        }
        
        .typing-indicator span:nth-child(1) {
            animation-delay: -0.32s;
        }
        
        .typing-indicator span:nth-child(2) {
            animation-delay: -0.16s;
        }
        
        @keyframes bounce {
            0%, 80%, 100% {
                transform: scale(0);
            }
            40% {
                transform: scale(1);
            }
        }
        
        .info-text {
            text-align: center;
            color: #999;
            padding: 20px;
            font-size: 14px;
        }
        
        .mode-info-banner {
            background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%);
            border-left: 4px solid #3b82f6;
            padding: 12px 20px;
            margin: 15px;
            border-radius: 8px;
            font-size: 13px;
            color: #1e40af;
            display: flex;
            align-items: center;
            gap: 10px;
            animation: slideDown 0.5s ease;
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideUp {
            from {
                opacity: 1;
                transform: translateY(0);
            }
            to {
                opacity: 0;
                transform: translateY(-20px);
            }
        }
        
        .mode-info-banner.closeable {
            justify-content: space-between;
        }
        
        .close-banner {
            background: none;
            border: none;
            color: #1e40af;
            cursor: pointer;
            font-size: 18px;
            font-weight: bold;
            padding: 0 5px;
            opacity: 0.6;
        }
        
        .close-banner:hover {
            opacity: 1;
        }
        
        .error-message {
            background: #fee;
            color: #c33;
            padding: 10px;
            border-radius: 8px;
            margin-top: 10px;
            font-size: 14px;
        }
    </style>
    <script>
        // Define navigation functions early so inline onclick handlers work
        function goToLocalMode() {
            window.location.href = '/local';
        }
        
        function goBackToModeSelection() {
            // Navigate back to home page (mode selection)
            window.location.href = '/';
        }
    </script>
</head>
<body>
    <!-- API Key Modal -->
    <div class="modal-overlay" id="apiKeyModal">
        <div class="api-key-modal">
            <div class="modal-title">{CLOUD_MODE_ICON} {CLOUD_MODE_NAME}</div>
            <div class="modal-subtitle">{PROVIDER_SELECTION_SUBTITLE}</div>
            
            <!-- Provider Selection and API Key Section -->
            <div id="apiKeySection">
            <div class="modal-subtitle">Select your AI provider and enter API key</div>
            
            <!-- Provider Selection -->
            <div style="text-align: left; margin: 20px 0;">
                <label style="display: block; margin-bottom: 8px; color: #666; font-weight: bold;">
                    {PROVIDER_SELECTION_LABEL}
                </label>
                <select id="providerSelect" onchange="onProviderChange()" style="width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 14px; background: white; cursor: pointer;">
                    <!-- Populated by JavaScript -->
                </select>
            </div>
            
            <!-- Provider Info Card -->
            <div id="providerInfo" style="background: #f8f9fa; border-left: 4px solid {COLOR_PRIMARY_START}; padding: 12px; margin: 15px 0; border-radius: 8px; font-size: 13px;">
                <div id="providerDescription" style="color: #666; margin-bottom: 8px;"></div>
                <div id="providerFreeTier" style="color: #10b981; font-weight: bold;"></div>
            </div>
            
            <!-- Model Selection -->
            <div id="modelSelection" style="display: none; text-align: left; margin: 20px 0;">
                <label style="display: block; margin-bottom: 8px; color: #666; font-weight: bold;">
                    🤖 Select Model
                </label>
                <div id="modelLoadingMsg" style="text-align: center; padding: 15px; color: #667eea; display: none;">
                    🔄 Loading available models...
                </div>
                <!-- Model Search -->
                <div id="modelSearchContainer" style="display: none; margin-bottom: 10px;">
                    <input 
                        type="text" 
                        id="modelSearch" 
                        placeholder="🔍 Search models..." 
                        style="width: 100%; padding: 10px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 14px; box-sizing: border-box;"
                        oninput="filterModels()"
                    >
                    <div id="modelCount" style="font-size: 12px; color: #666; margin-top: 5px; text-align: right;"></div>
                </div>
                <div id="modelCards" style="max-height: 250px; overflow-y: auto; border: 1px solid #e0e0e0; border-radius: 8px; padding: 8px;">
                    <!-- Model cards will be populated here -->
                </div>
                <div id="selectedModelInfo" style="margin-top: 10px; padding: 10px; background: #f0f4ff; border-radius: 6px; font-size: 13px; display: none;">
                    <strong>Selected:</strong> <span id="selectedModelName"></span>
                </div>
            </div>
            
            <!-- API Key Input -->
            <input 
                type="password" 
                id="apiKeyInput" 
                class="api-key-input" 
                placeholder="Select a provider first..."
                onkeypress="handleApiKeyEnter(event)"
            >
            
            <div style="display: flex; gap: 10px; margin-top: 20px;">
                <button class="modal-button-secondary" onclick="goBackToModeSelection()" title="Go back to mode selection">
                    ← Back
                </button>
                <button class="modal-button" onclick="saveApiKey()" style="flex: 1;">{BTN_START_CHATTING}</button>
            </div>
            
            <div id="apiKeyError" class="error-message" style="display: none;"></div>
            
            <!-- Help Link -->
            <div id="helpLink" style="margin-top: 15px; text-align: center;">
                <a id="providerHelpUrl" href="#" target="_blank" style="color: {COLOR_PRIMARY_START}; text-decoration: none; font-size: 13px;">
                    👉 <span id="providerHelpText">Get API Key</span>
                </a>
            </div>
            </div>
            
            <div class="help-text">
                <small>💡 Each provider has different features and pricing<br>Choose based on your needs!</small>
            </div>
        </div>
    </div>

    <!-- Chat Interface -->
    <div class="chat-container">
        <div class="chat-header">
            <div class="header-title">{CHATBOT_ICON} {CHATBOT_NAME} <span style="font-size: 12px; opacity: 0.8;">{CLOUD_MODE_BADGE}</span></div>
            <div>
                <button class="settings-btn" onclick="goToLocalMode()" title="Switch to privacy-focused local mode">{BTN_SWITCH_TO_LOCAL}</button>
                <button class="settings-btn" onclick="changeApiKey()" title="Change your API key">{BTN_CHANGE_API_KEY}</button>
            </div>
        </div>
        <div class="chat-messages" id="chatMessages">
            <div class="mode-info-banner closeable" id="modeBanner">
                <div>
                    <strong>💡 Tip:</strong> Want more privacy? Try <strong>Local Mode</strong> - no API key needed, runs 100% in your browser!
                    <span style="opacity: 0.7; margin-left: 8px;">Click "Switch to Local Mode" button above</span>
                </div>
                <button class="close-banner" onclick="closeBanner()" title="Close this tip">×</button>
            </div>
            <div class="info-text">
                {WELCOME_MESSAGE_CLOUD}
            </div>
        </div>
        <div class="typing-indicator" id="typingIndicator">
            <span></span>
            <span></span>
            <span></span>
        </div>
        <div class="chat-input-container">
            <input 
                type="text" 
                id="messageInput" 
                placeholder="{INPUT_PLACEHOLDER}" 
                onkeypress="handleKeyPress(event)"
                disabled
            >
            <button id="sendButton" onclick="sendMessage()" disabled>{BTN_SEND}</button>
        </div>
    </div>

    <script>
        let sessionId = null;
        let apiKey = null;
        let selectedProvider = 'nvidia';
        let selectedModel = null;
        let providersData = {};
        let shouldAutoSelect = true;  // Only auto-select on first load

        // Load providers on page load
        async function loadProviders() {
            try {
                const response = await fetch('/api/providers');
                const data = await response.json();
                providersData = data.providers;
                
                const select = document.getElementById('providerSelect');
                select.innerHTML = '';
                
                // Populate dropdown
                Object.keys(providersData).forEach(key => {
                    const provider = providersData[key];
                    const option = document.createElement('option');
                    option.value = key;
                    option.textContent = `${provider.icon} ${provider.name}`;
                    if (key === data.default) {
                        option.selected = true;
                        selectedProvider = key;
                    }
                    select.appendChild(option);
                });
                
                // Update UI for default provider
                onProviderChange();
            } catch (error) {
                console.error('Failed to load providers:', error);
            }
        }

        // Handle provider selection change
        async function onProviderChange() {
            const select = document.getElementById('providerSelect');
            selectedProvider = select.value;
            const provider = providersData[selectedProvider];
            
            if (!provider) return;
            
            // Reset selected model when changing provider
            selectedModel = null;
            allModels = [];
            document.getElementById('selectedModelInfo').style.display = 'none';
            document.getElementById('modelSearch').value = '';
            
            // Update description and free tier info
            document.getElementById('providerDescription').textContent = provider.description;
            document.getElementById('providerFreeTier').textContent = provider.free_tier;
            
            // Update API key placeholder
            document.getElementById('apiKeyInput').placeholder = provider.api_key_placeholder;
            
            // Update help link
            document.getElementById('providerHelpUrl').href = provider.help_url;
            document.getElementById('providerHelpText').textContent = provider.help_text;
            
            // Store selected provider
            localStorage.setItem('{STORAGE_KEY_PROVIDER}', selectedProvider);
            
            // Fetch and display models for this provider
            await loadProviderModels(selectedProvider);
        }
        
        // Fetch and display models for a provider
        async function loadProviderModels(providerId) {
            const modelSelection = document.getElementById('modelSelection');
            const modelLoadingMsg = document.getElementById('modelLoadingMsg');
            const modelCards = document.getElementById('modelCards');
            
            // Show model selection section
            modelSelection.style.display = 'block';
            modelLoadingMsg.style.display = 'block';
            modelCards.innerHTML = '';
            
            try {
                const response = await fetch(`/api/providers/${providerId}/models`);
                
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || `HTTP ${response.status}`);
                }
                
                const data = await response.json();
                
                modelLoadingMsg.style.display = 'none';
                
                if (data.models && data.models.length > 0) {
                    displayModelCards(data.models);
                } else {
                    showModelError('No models found for this provider', providerId);
                }
            } catch (error) {
                console.error('Failed to load models:', error);
                modelLoadingMsg.style.display = 'none';
                showModelError(error.message, providerId);
            }
        }
        
        // Show error UI for model fetching
        function showModelError(errorMessage, providerId) {
            const modelCards = document.getElementById('modelCards');
            const providerName = providersData[providerId]?.name || providerId;
            
            modelCards.innerHTML = `
                <div style="padding: 20px; text-align: center;">
                    <div style="font-size: 48px; margin-bottom: 15px;">❌</div>
                    <div style="font-size: 16px; font-weight: bold; color: #e74c3c; margin-bottom: 10px;">
                        Failed to Load Models
                    </div>
                    <div style="font-size: 14px; color: #666; margin-bottom: 15px;">
                        ${errorMessage}
                    </div>
                    <div style="text-align: left; background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0; font-size: 13px;">
                        <strong>Troubleshooting:</strong>
                        <ul style="margin: 10px 0; padding-left: 20px;">
                            <li>Check your internet connection</li>
                            <li>The ${providerName} API may be temporarily unavailable</li>
                            <li>Try selecting a different provider</li>
                            <li>Refresh the page and try again</li>
                        </ul>
                    </div>
                    <div style="display: flex; gap: 10px; justify-content: center; margin-top: 15px;">
                        <button onclick="loadProviderModels('${providerId}')" 
                                style="padding: 10px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">
                            🔄 Retry
                        </button>
                        <button onclick="goBackToModeSelection()" 
                                style="padding: 10px 20px; background: white; color: #667eea; border: 2px solid #667eea; border-radius: 8px; cursor: pointer; font-weight: bold;">
                            ← Back
                        </button>
                    </div>
                </div>
            `;
        }
        
        // Store all models globally for filtering
        let allModels = [];
        
        // Display model cards
        function displayModelCards(models) {
            allModels = models; // Store for filtering
            const modelCards = document.getElementById('modelCards');
            const modelSearchContainer = document.getElementById('modelSearchContainer');
            const modelCount = document.getElementById('modelCount');
            
            modelCards.innerHTML = '';
            
            // Show search box if more than 6 models
            if (models.length > 6) {
                modelSearchContainer.style.display = 'block';
                modelCount.textContent = `Showing ${models.length} model${models.length !== 1 ? 's' : ''}`;
            } else {
                modelSearchContainer.style.display = 'none';
            }
            
            models.forEach((model, index) => {
                const card = document.createElement('div');
                card.className = 'model-card';
                card.dataset.modelId = model.id;
                card.dataset.modelName = model.name;
                card.dataset.modelDescription = model.description;
                
                const recommendedBadge = model.recommended ? 
                    '<span class="model-recommended-badge">⭐ Recommended</span>' : '';
                
                card.innerHTML = `
                    <div class="model-card-title">${model.name}${recommendedBadge}</div>
                    <div class="model-card-description">${model.description}</div>
                `;
                
                card.addEventListener('click', function() {
                    selectModel(model.id, model.name);
                });
                
                modelCards.appendChild(card);
                
                // Auto-select first recommended model or first model (only on first load)
                if (shouldAutoSelect && !selectedModel) {
                    if ((model.recommended && !selectedModel) || (index === 0 && !selectedModel)) {
                        selectModel(model.id, model.name, false);  // Don't show selection info for auto-select
                    }
                }
            });
            
            // After first display, don't auto-select anymore
            shouldAutoSelect = false;
        }
        
        // Filter models based on search input
        function filterModels() {
            const searchInput = document.getElementById('modelSearch');
            const searchTerm = searchInput.value.toLowerCase().trim();
            const modelCards = document.querySelectorAll('.model-card');
            const modelCount = document.getElementById('modelCount');
            
            let visibleCount = 0;
            
            modelCards.forEach(card => {
                const name = card.dataset.modelName.toLowerCase();
                const description = card.dataset.modelDescription.toLowerCase();
                const modelId = card.dataset.modelId.toLowerCase();
                
                // Search in name, description, and ID
                if (name.includes(searchTerm) || description.includes(searchTerm) || modelId.includes(searchTerm)) {
                    card.style.display = 'block';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });
            
            // Update count
            if (searchTerm) {
                modelCount.textContent = `Found ${visibleCount} model${visibleCount !== 1 ? 's' : ''} matching "${searchTerm}"`;
            } else {
                modelCount.textContent = `Showing ${allModels.length} model${allModels.length !== 1 ? 's' : ''}`;
            }
            
            // Show message if no results
            const modelCardsContainer = document.getElementById('modelCards');
            if (visibleCount === 0 && searchTerm) {
                const noResultsMsg = document.createElement('div');
                noResultsMsg.id = 'noResultsMsg';
                noResultsMsg.style.cssText = 'padding: 30px; text-align: center; color: #999;';
                noResultsMsg.innerHTML = `
                    <div style="font-size: 48px; margin-bottom: 10px;">🔍</div>
                    <div style="font-size: 14px;">No models found matching "<strong>${searchTerm}</strong>"</div>
                    <div style="font-size: 12px; margin-top: 5px;">Try a different search term</div>
                `;
                
                // Remove old no results message if exists
                const oldMsg = document.getElementById('noResultsMsg');
                if (oldMsg) oldMsg.remove();
                
                modelCardsContainer.appendChild(noResultsMsg);
            } else {
                // Remove no results message if it exists
                const oldMsg = document.getElementById('noResultsMsg');
                if (oldMsg) oldMsg.remove();
            }
        }
        
        // Select a model
        function selectModel(modelId, modelName, showSelectionInfo = true) {
            selectedModel = modelId;
            
            // Update UI - highlight selected model
            document.querySelectorAll('.model-card').forEach(card => {
                card.classList.remove('selected');
            });
            document.querySelector(`[data-model-id="${modelId}"]`).classList.add('selected');
            
            // Only show selected model info if explicitly requested (for manual selections)
            if (showSelectionInfo) {
                document.getElementById('selectedModelInfo').style.display = 'block';
                document.getElementById('selectedModelName').textContent = modelName;
            }
            
            // Enable API key input
            document.getElementById('apiKeyInput').disabled = false;
            document.getElementById('apiKeyInput').placeholder = providersData[selectedProvider].api_key_placeholder;
            
            console.log('Selected model:', modelId);
        }

        // Note: goBackToModeSelection and goToLocalMode are defined in head for early access
        
        function closeBanner() {
            const banner = document.getElementById('modeBanner');
            if (banner) {
                banner.style.animation = 'slideUp 0.3s ease';
                setTimeout(() => {
                    banner.style.display = 'none';
                }, 300);
            }
            // Remember user dismissed the banner
            localStorage.setItem('cloudModeBannerDismissed', 'true');
        }
        
        // Check if banner was previously dismissed
        window.addEventListener('DOMContentLoaded', function() {
            const bannerDismissed = localStorage.getItem('cloudModeBannerDismissed');
            if (bannerDismissed === 'true') {
                const banner = document.getElementById('modeBanner');
                if (banner) {
                    banner.style.display = 'none';
                }
            }
        });

        // Check if API key is stored in localStorage
        window.onload = function() {
            // Load providers immediately since we're on /cloud page
            loadProviders();
            
            const storedKey = localStorage.getItem('{STORAGE_KEY_API_KEY}');
            const storedProvider = localStorage.getItem('{STORAGE_KEY_PROVIDER}');
            
            if (storedKey && storedProvider) {
                // If both key and provider are stored, skip provider selection and go directly to chat
                apiKey = storedKey;
                selectedProvider = storedProvider;
                document.getElementById('apiKeyModal').classList.add('hidden');
                enableChat();
            } else {
                // If no stored credentials, show provider selection modal
                // Modal is already visible by default
            }
        };

        function handleApiKeyEnter(event) {
            if (event.key === 'Enter') {
                saveApiKey();
            }
        }

        async function saveApiKey() {
            const input = document.getElementById('apiKeyInput');
            const key = input.value.trim();
            const errorDiv = document.getElementById('apiKeyError');
            const startButton = document.querySelector('.modal-button');
            
            if (!selectedModel) {
                errorDiv.textContent = 'Please select a model first';
                errorDiv.style.display = 'block';
                return;
            }
            
            if (!key) {
                errorDiv.textContent = '{ERROR_EMPTY_KEY}';
                errorDiv.style.display = 'block';
                return;
            }
            
            // Disable button and show validating message
            startButton.disabled = true;
            startButton.textContent = '🔄 Validating API Key...';
            errorDiv.style.display = 'none';
            
            try {
                // Validate API key with the backend
                const response = await fetch('/api/validate-key', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        provider: selectedProvider,
                        api_key: key,
                        model: selectedModel
                    })
                });
                
                const data = await response.json();
                
                if (response.ok && data.valid) {
                    // Key is valid - store it and proceed
                    apiKey = key;
                    localStorage.setItem('{STORAGE_KEY_API_KEY}', key);
                    
                    // Hide modal and enable chat
                    document.getElementById('apiKeyModal').classList.add('hidden');
                    enableChat();
                    
                    // Clear input
                    input.value = '';
                    
                    // Show success message briefly
                    errorDiv.style.color = '#10b981';
                    errorDiv.textContent = '✓ API key validated successfully!';
                    errorDiv.style.display = 'block';
                    setTimeout(() => {
                        errorDiv.style.display = 'none';
                        errorDiv.style.color = '#c33';
                    }, 2000);
                } else {
                    // Invalid key
                    errorDiv.textContent = data.detail || 'Invalid API key. Please check and try again.';
                    errorDiv.style.display = 'block';
                }
            } catch (error) {
                console.error('API key validation error:', error);
                errorDiv.textContent = 'Failed to validate API key. Please check your internet connection and try again.';
                errorDiv.style.display = 'block';
            } finally {
                // Re-enable button
                startButton.disabled = false;
                startButton.textContent = '{BTN_START_CHATTING}';
            }
        }

        function changeApiKey() {
            if (confirm('{CONFIRM_CHANGE_KEY}')) {
                localStorage.removeItem('{STORAGE_KEY_API_KEY}');
                apiKey = null;
                sessionId = null;
                document.getElementById('chatMessages').innerHTML = '<div class="info-text">{WELCOME_MESSAGE_CLOUD}</div>';
                document.getElementById('apiKeyModal').classList.remove('hidden');
                disableChat();
            }
        }

        function enableChat() {
            document.getElementById('messageInput').disabled = false;
            document.getElementById('sendButton').disabled = false;
            document.getElementById('messageInput').focus();
        }

        function disableChat() {
            document.getElementById('messageInput').disabled = true;
            document.getElementById('sendButton').disabled = true;
        }

        function generateSessionId() {
            return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        }

        function addMessage(content, isUser) {
            const messagesDiv = document.getElementById('chatMessages');
            
            // Remove info text if present
            const infoText = messagesDiv.querySelector('.info-text');
            if (infoText && isUser) {
                infoText.remove();
            }
            
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'agent'}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = content;
            
            messageDiv.appendChild(contentDiv);
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        function showTypingIndicator() {
            document.getElementById('typingIndicator').classList.add('active');
            const messagesDiv = document.getElementById('chatMessages');
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        function hideTypingIndicator() {
            document.getElementById('typingIndicator').classList.remove('active');
        }

        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const sendButton = document.getElementById('sendButton');
            const message = input.value.trim();
            
            if (!message || !apiKey) return;
            
            // Initialize session if needed
            if (!sessionId) {
                sessionId = generateSessionId();
            }
            
            // Disable input
            input.disabled = true;
            sendButton.disabled = true;
            
            // Add user message
            addMessage(message, true);
            input.value = '';
            
            // Show typing indicator
            showTypingIndicator();
            
            try {
                // Use streaming endpoint
                const response = await fetch('/api/chat/stream', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        api_key: apiKey,
                        provider: selectedProvider,
                        model: selectedModel,
                        session_id: sessionId
                    })
                });
                
                if (!response.ok) {
                    throw new Error('Failed to connect to streaming endpoint');
                }
                
                // Hide typing indicator and add streaming message
                hideTypingIndicator();
                
                // Create a new message element for streaming
                const messagesDiv = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message agent';
                const contentDiv = document.createElement('div');
                contentDiv.className = 'message-content';
                contentDiv.textContent = '';
                messageDiv.appendChild(contentDiv);
                messagesDiv.appendChild(messageDiv);
                
                // Read the stream
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let buffer = '';
                
                while (true) {
                    const { done, value } = await reader.read();
                    
                    if (done) break;
                    
                    buffer += decoder.decode(value, { stream: true });
                    const lines = buffer.split('\\n');
                    
                    // Keep last incomplete line in buffer
                    buffer = lines.pop();
                    
                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            try {
                                const data = JSON.parse(line.substring(6));
                                
                                if (data.type === 'session') {
                                    sessionId = data.session_id;
                                } else if (data.type === 'chunk') {
                                    // Append chunk to the message
                                    contentDiv.textContent += data.content;
                                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                                } else if (data.type === 'done') {
                                    // Stream complete
                                    console.log('Stream complete');
                                } else if (data.type === 'error') {
                                    contentDiv.textContent = '❌ Error: ' + data.error;
                                    
                                    // Check for API key errors
                                    if (data.error && data.error.includes('API key')) {
                                        setTimeout(() => {
                                            if (confirm('{ERROR_INVALID_KEY_API}')) {
                                                changeApiKey();
                                            }
                                        }, 1000);
                                    }
                                }
                            } catch (e) {
                                console.error('Error parsing SSE data:', e);
                            }
                        }
                    }
                }
                
            } catch (error) {
                hideTypingIndicator();
                addMessage('{ERROR_CONNECTION}', false);
                console.error('Error:', error);
            }
            
            // Re-enable input
            input.disabled = false;
            sendButton.disabled = false;
            input.focus();
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
    </script>
</body>
</html>
    """
    
    # Replace all branding variables using string replacement
    html = html_template
    html = html.replace("{CHATBOT_TITLE}", CHATBOT_TITLE)
    html = html.replace("{COLOR_PRIMARY_START}", COLOR_PRIMARY_START)
    html = html.replace("{COLOR_PRIMARY_END}", COLOR_PRIMARY_END)
    html = html.replace("{COLOR_SECONDARY_START}", COLOR_SECONDARY_START)
    html = html.replace("{COLOR_SECONDARY_END}", COLOR_SECONDARY_END)
    html = html.replace("{MODAL_TITLE_WELCOME}", MODAL_TITLE_WELCOME)
    html = html.replace("{MODAL_SUBTITLE_CHOOSE_MODE}", MODAL_SUBTITLE_CHOOSE_MODE)
    html = html.replace("{CLOUD_MODE_ICON}", CLOUD_MODE_ICON)
    html = html.replace("{CLOUD_MODE_NAME}", CLOUD_MODE_NAME)
    html = html.replace("{CLOUD_MODE_DESCRIPTION}", CLOUD_MODE_DESCRIPTION)
    html = html.replace("{LOCAL_MODE_ICON}", LOCAL_MODE_ICON)
    html = html.replace("{LOCAL_MODE_NAME}", LOCAL_MODE_NAME)
    html = html.replace("{LOCAL_MODE_DESCRIPTION}", LOCAL_MODE_DESCRIPTION)
    html = html.replace("{PROVIDER_SELECTION_SUBTITLE}", PROVIDER_SELECTION_SUBTITLE)
    html = html.replace("{PROVIDER_SELECTION_LABEL}", PROVIDER_SELECTION_LABEL)
    html = html.replace("{API_KEY_PLACEHOLDER}", API_KEY_PLACEHOLDER)
    html = html.replace("{BTN_START_CHATTING}", BTN_START_CHATTING)
    html = html.replace("{INFO_NO_API_KEY}", INFO_NO_API_KEY)
    html = html.replace("{INFO_FREE_TIER}", INFO_FREE_TIER)
    html = html.replace("{CHATBOT_ICON}", CHATBOT_ICON)
    html = html.replace("{CHATBOT_NAME}", CHATBOT_NAME)
    html = html.replace("{CLOUD_MODE_BADGE}", CLOUD_MODE_BADGE)
    html = html.replace("{ROUTE_LOCAL}", ROUTE_LOCAL)
    html = html.replace("{BTN_SWITCH_TO_LOCAL}", BTN_SWITCH_TO_LOCAL)
    html = html.replace("{BTN_CHANGE_API_KEY}", BTN_CHANGE_API_KEY)
    html = html.replace("{WELCOME_MESSAGE_CLOUD}", WELCOME_MESSAGE_CLOUD)
    html = html.replace("{INPUT_PLACEHOLDER}", INPUT_PLACEHOLDER)
    html = html.replace("{BTN_SEND}", BTN_SEND)
    html = html.replace("{ERROR_EMPTY_KEY}", ERROR_EMPTY_KEY)
    html = html.replace("{ERROR_INVALID_KEY_FORMAT}", ERROR_INVALID_KEY_FORMAT)
    html = html.replace("{STORAGE_KEY_API_KEY}", STORAGE_KEY_API_KEY)
    html = html.replace("{STORAGE_KEY_PROVIDER}", STORAGE_KEY_PROVIDER)
    html = html.replace("{CONFIRM_CHANGE_KEY}", CONFIRM_CHANGE_KEY)
    html = html.replace("{ERROR_INVALID_KEY_API}", ERROR_INVALID_KEY_API)
    html = html.replace("{ERROR_CONNECTION}", ERROR_CONNECTION)
    
    return html


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the mode selection page"""
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{CHATBOT_TITLE} - Choose Your Mode</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, {COLOR_PRIMARY_START} 0%, {COLOR_PRIMARY_END} 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            text-align: center;
            color: white;
            max-width: 900px;
            width: 100%;
        }
        
        .logo {
            font-size: 80px;
            margin-bottom: 20px;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-20px); }}
        }}
        
        .title {
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .subtitle {
            font-size: 20px;
            margin-bottom: 50px;
            opacity: 0.95;
        }
        
        .mode-cards {
            display: flex;
            gap: 30px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .mode-card {
            background: white;
            border-radius: 20px;
            padding: 40px 30px;
            width: 380px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
            display: block;
        }
        
        .mode-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 30px 80px rgba(0,0,0,0.4);
        }
        
        .mode-icon {
            font-size: 64px;
            margin-bottom: 20px;
        }
        
        .mode-title {
            font-size: 28px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
        }
        
        .mode-description {
            font-size: 16px;
            color: #666;
            line-height: 1.6;
            margin-bottom: 20px;
        }
        
        .mode-features {
            list-style: none;
            text-align: left;
            margin-bottom: 25px;
        }
        
        .mode-features li {
            font-size: 14px;
            color: #555;
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .mode-features li:last-child {
            border-bottom: none;
        }
        
        .mode-features li::before {
            content: "✓ ";
            color: #667eea;
            font-weight: bold;
            margin-right: 8px;
        }
        
        .mode-button {
            background: linear-gradient(135deg, {COLOR_PRIMARY_START} 0%, {COLOR_PRIMARY_END} 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 15px 30px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
            width: 100%;
        }
        
        .mode-button:hover {
            transform: scale(1.05);
        }
        
        .mode-card.local .mode-button {
            background: linear-gradient(135deg, {COLOR_SECONDARY_START} 0%, {COLOR_SECONDARY_END} 100%);
        }
        
        .footer {
            margin-top: 50px;
            font-size: 14px;
            opacity: 0.8;
        }
        
        @media (max-width: 768px) {{
            .title {{
                font-size: 32px;
            }}
            .subtitle {{
                font-size: 16px;
            }}
            .mode-cards {{
                flex-direction: column;
                align-items: center;
            }}
            .mode-card {{
                width: 100%;
                max-width: 400px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">{CHATBOT_ICON}</div>
        <h1 class="title">{CHATBOT_NAME}</h1>
        <p class="subtitle">{CHATBOT_DESCRIPTION}</p>
        
        <div class="mode-cards">
            <!-- Cloud Mode Card -->
            <a href="/cloud" class="mode-card cloud">
                <div class="mode-icon">{CLOUD_MODE_ICON}</div>
                <div class="mode-title">{CLOUD_MODE_NAME}</div>
                <p class="mode-description">{CLOUD_MODE_DESCRIPTION}</p>
                <ul class="mode-features">
                    <li>Choose from 5 powerful AI providers</li>
                    <li>Latest models (GPT-4, Claude, Gemini, etc.)</li>
                    <li>Superior performance & speed</li>
                    <li>Requires API key (most have FREE tiers)</li>
                </ul>
                <button class="mode-button">Launch Cloud Mode →</button>
            </a>
            
            <!-- Local Mode Card -->
            <a href="/local" class="mode-card local">
                <div class="mode-icon">{LOCAL_MODE_ICON}</div>
                <div class="mode-title">{LOCAL_MODE_NAME}</div>
                <p class="mode-description">{LOCAL_MODE_DESCRIPTION}</p>
                <ul class="mode-features">
                    <li>100% private - runs in your browser</li>
                    <li>No API key required - completely FREE</li>
                    <li>Offline capable after model download</li>
                    <li>Document upload & RAG support</li>
                </ul>
                <button class="mode-button">Launch Local Mode →</button>
            </a>
        </div>
        
        <div class="footer">
            <p>🔒 Your privacy matters. Choose the mode that fits your needs.</p>
            <p style="margin-top: 10px; font-size: 12px;">Version {VERSION}</p>
        </div>
    </div>
</body>
</html>
    """
    
    # Replace all branding variables
    html = html_template
    html = html.replace("{CHATBOT_TITLE}", CHATBOT_TITLE)
    html = html.replace("{CHATBOT_NAME}", CHATBOT_NAME)
    html = html.replace("{CHATBOT_DESCRIPTION}", CHATBOT_DESCRIPTION)
    html = html.replace("{CHATBOT_ICON}", CHATBOT_ICON)
    html = html.replace("{VERSION}", VERSION)
    html = html.replace("{COLOR_PRIMARY_START}", COLOR_PRIMARY_START)
    html = html.replace("{COLOR_PRIMARY_END}", COLOR_PRIMARY_END)
    html = html.replace("{COLOR_SECONDARY_START}", COLOR_SECONDARY_START)
    html = html.replace("{COLOR_SECONDARY_END}", COLOR_SECONDARY_END)
    html = html.replace("{CLOUD_MODE_ICON}", CLOUD_MODE_ICON)
    html = html.replace("{CLOUD_MODE_NAME}", CLOUD_MODE_NAME)
    html = html.replace("{CLOUD_MODE_DESCRIPTION}", CLOUD_MODE_DESCRIPTION)
    html = html.replace("{LOCAL_MODE_ICON}", LOCAL_MODE_ICON)
    html = html.replace("{LOCAL_MODE_NAME}", LOCAL_MODE_NAME)
    html = html.replace("{LOCAL_MODE_DESCRIPTION}", LOCAL_MODE_DESCRIPTION)
    
    return html


@app.get(ROUTE_HEALTH)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": HEALTH_CHECK_MESSAGE,
        "version": VERSION
    }


@app.get("/api/providers")
async def get_providers():
    """Get list of available cloud providers"""
    return {
        "providers": CLOUD_PROVIDERS,
        "default": DEFAULT_PROVIDER
    }


@app.get("/api/providers/{provider_id}/models")
async def get_provider_models(provider_id: str):
    """Get available models for a specific provider - fetched dynamically"""
    if provider_id not in CLOUD_PROVIDERS:
        raise HTTPException(status_code=404, detail="Provider not found")
    
    try:
        from model_fetcher import ModelFetcher
        
        # Fetch models dynamically from provider API
        models = ModelFetcher.fetch_models_for_provider(provider_id)
        
        provider = CLOUD_PROVIDERS[provider_id]
        return {
            "provider": provider_id,
            "provider_name": provider["name"],
            "models": models
        }
    except Exception as e:
        # If dynamic fetching fails, raise error (no fallback)
        error_msg = f"Failed to fetch models for {provider_id}: {str(e)}"
        raise HTTPException(status_code=500, detail=error_msg)


@app.get("/api/webllm/models")
async def get_webllm_models():
    """Get available WebLLM models dynamically from Hugging Face"""
    try:
        from model_fetcher import ModelFetcher
        models = ModelFetcher.fetch_webllm_models()
        return {
            "source": "WebLLM/Hugging Face",
            "count": len(models),
            "models": models
        }
    except Exception as e:
        error_msg = f"Failed to fetch WebLLM models: {str(e)}"
        raise HTTPException(status_code=500, detail=error_msg)


@app.post("/api/validate-key")
async def validate_api_key(request: dict):
    """Validate API key for a specific provider"""
    try:
        provider = request.get("provider", "nvidia")
        api_key = request.get("api_key", "")
        model = request.get("model")
        
        if not api_key:
            raise HTTPException(status_code=400, detail="API key is required")
        
        from cloud_providers import CloudProviderClient
        
        # Try to create client and make a simple test call
        client = CloudProviderClient(provider=provider, api_key=api_key, model=model)
        
        # Make a minimal test request to validate the key
        try:
            # Send a very simple test message
            test_response = client.chat("Hi", history=[])
            
            # If we got a response, the key is valid
            return {
                "valid": True,
                "message": "API key is valid",
                "provider": provider
            }
        except Exception as e:
            error_msg = str(e)
            
            # Check for common authentication errors
            if any(keyword in error_msg.lower() for keyword in ['invalid', 'unauthorized', 'authentication', 'api key', 'forbidden', '401', '403']):
                raise HTTPException(
                    status_code=401, 
                    detail=f"Invalid API key for {CLOUD_PROVIDERS[provider]['name']}. Please check your key and try again."
                )
            else:
                # Other errors (network, etc.)
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to validate API key: {error_msg}"
                )
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the selected cloud provider using user's API key"""
    try:
        from cloud_providers import CloudProviderClient
        
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        provider = request.provider or "nvidia"
        model = request.model  # Selected model from user
        
        # Initialize session storage if needed
        if session_id not in user_sessions:
            user_sessions[session_id] = {
                "history": [],
                "provider": provider,
                "model": model
            }
        
        session = user_sessions[session_id]
        
        # Create cloud provider client with selected model
        client = CloudProviderClient(provider=provider, api_key=request.api_key, model=model)
        
        # Prepare history in the format expected by cloud_providers
        history_for_provider = [
            {
                "is_user": msg["role"] == "user",
                "content": msg["content"]
            }
            for msg in session["history"]
        ]
        
        # Generate response using selected provider
        response_text = client.chat(request.message, history=history_for_provider)
        
        # Add user message to history
        session["history"].append({
            "role": "user",
            "content": request.message
        })
        
        # Add assistant response to history
        session["history"].append({
            "role": "assistant",
            "content": response_text
        })
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            provider=provider
        )
        
    except Exception as e:
        error_msg = str(e)
        raise HTTPException(status_code=500, detail=error_msg)


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """Stream chat responses in real-time using Server-Sent Events"""
    async def generate_stream():
        try:
            from cloud_providers import CloudProviderClient
            
            # Generate session ID if not provided
            session_id = request.session_id or str(uuid.uuid4())
            provider = request.provider or "nvidia"
            model = request.model
            
            # Initialize session storage if needed
            if session_id not in user_sessions:
                user_sessions[session_id] = {
                    "history": [],
                    "provider": provider,
                    "model": model
                }
            
            session = user_sessions[session_id]
            
            # Create cloud provider client
            client = CloudProviderClient(provider=provider, api_key=request.api_key, model=model)
            
            # Prepare history
            history_for_provider = [
                {
                    "is_user": msg["role"] == "user",
                    "content": msg["content"]
                }
                for msg in session["history"]
            ]
            
            # Get the full response first (we'll simulate streaming for now)
            full_response = client.chat(request.message, history=history_for_provider)
            
            # Send session info first
            yield f"data: {json.dumps({'type': 'session', 'session_id': session_id})}\n\n"
            
            # Stream the response word by word
            words = full_response.split()
            current_text = ""
            
            for i, word in enumerate(words):
                current_text += word + (" " if i < len(words) - 1 else "")
                
                # Send chunk
                yield f"data: {json.dumps({'type': 'chunk', 'content': word + (' ' if i < len(words) - 1 else '')})}\n\n"
                
                # Small delay to simulate streaming (adjust as needed)
                await asyncio.sleep(0.03)
            
            # Add to history
            session["history"].append({
                "role": "user",
                "content": request.message
            })
            
            session["history"].append({
                "role": "assistant",
                "content": full_response
            })
            
            # Send done signal
            yield f"data: {json.dumps({'type': 'done', 'full_response': full_response})}\n\n"
            
        except Exception as e:
            error_data = {
                'type': 'error',
                'error': str(e)
            }
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


@app.get("/api/history/{session_id}")
async def get_history(session_id: str):
    """Get conversation history"""
    if session_id in user_sessions:
        return {
            "session_id": session_id,
            "messages": user_sessions[session_id]["history"]
        }
    return {"session_id": session_id, "messages": []}


@app.delete("/api/session/{session_id}")
async def clear_session(session_id: str):
    """Clear a session"""
    if session_id in user_sessions:
        del user_sessions[session_id]
    return {"message": "Session cleared", "session_id": session_id}


# ============================================================================
# RAG (Retrieval-Augmented Generation) Endpoints for Cloud Mode
# ============================================================================

@app.get("/api/rag/embedding-providers", response_model=EmbeddingProvidersResponse)
async def get_embedding_providers():
    """Get list of available embedding providers"""
    try:
        from embedding_service import list_providers
        providers = list_providers()
        return {"providers": providers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/rag/embedding-models/{provider}")
async def get_embedding_models(provider: str):
    """Get available embedding models for a specific provider"""
    try:
        from embedding_service import EMBEDDING_PROVIDERS
        
        if provider not in EMBEDDING_PROVIDERS:
            raise HTTPException(status_code=404, detail=f"Provider {provider} not found")
        
        provider_info = EMBEDDING_PROVIDERS[provider]
        return {
            "provider": provider,
            "name": provider_info["name"],
            "models": provider_info["models"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/local/embedding-models")
async def get_local_embedding_models():
    """Get available Transformers.js embedding models for local mode"""
    try:
        import json
        from pathlib import Path
        
        # Read from JSON file
        models_file = Path("static/embedding_models.json")
        if models_file.exists():
            with open(models_file, 'r') as f:
                data = json.load(f)
                return {
                    "source": data["transformers_js"]["source"],
                    "models": data["transformers_js"]["models"]
                }
        else:
            # Fallback to hardcoded list
            return {
                "source": "Transformers.js",
                "models": [
                    {
                        "id": "Xenova/all-MiniLM-L6-v2",
                        "name": "all-MiniLM-L6-v2",
                        "description": "Fast, lightweight (22MB)",
                        "size_mb": 22,
                        "dimensions": 384,
                        "category": "speed",
                        "recommended": True
                    }
                ]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/rag/upload")
async def upload_document(request: DocumentUploadRequest):
    """Upload and process a document for RAG"""
    try:
        import base64
        from datetime import datetime
        from document_processor import (
            DocumentProcessor, DocumentChunker, document_store
        )
        from embedding_service import EmbeddingClient
        
        # Decode file content
        file_content = base64.b64decode(request.content)
        
        # Extract text from document
        processor = DocumentProcessor()
        text = processor.extract_text_from_file(file_content, request.filename)
        
        if not text or len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="No text could be extracted from the document")
        
        # Chunk the text
        chunker = DocumentChunker(chunk_size=500, chunk_overlap=50)
        chunks = chunker.chunk_text(text)
        
        if not chunks:
            raise HTTPException(status_code=400, detail="Could not create chunks from document")
        
        # Initialize embedding client
        embedding_client = EmbeddingClient(
            provider=request.embedding_provider,
            api_key=request.embedding_api_key,
            model=request.embedding_model
        )
        
        # Generate embeddings for all chunks
        embeddings = embedding_client.embed_texts(chunks)
        
        # Generate document ID
        doc_id = DocumentProcessor.generate_document_id(request.filename, text)
        
        # Create document object
        document = {
            "id": doc_id,
            "filename": request.filename,
            "text": text,
            "chunks": chunks,
            "embeddings": embeddings,
            "upload_time": datetime.now().isoformat(),
            "embedding_provider": request.embedding_provider,
            "embedding_model": request.embedding_model or "default"
        }
        
        # Store document
        document_store.add_document(request.session_id, document)
        
        return {
            "success": True,
            "doc_id": doc_id,
            "filename": request.filename,
            "chunks": len(chunks),
            "message": f"Document processed successfully with {len(chunks)} chunks"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/rag/documents/{session_id}", response_model=DocumentListResponse)
async def list_documents(session_id: str):
    """List all documents for a session"""
    try:
        from document_processor import document_store
        
        documents = document_store.list_documents(session_id)
        
        return {
            "documents": documents,
            "total": len(documents)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/rag/document")
async def delete_document(request: DocumentDeleteRequest):
    """Delete a document"""
    try:
        from document_processor import document_store
        
        success = document_store.delete_document(request.session_id, request.doc_id)
        
        if success:
            return {"success": True, "message": "Document deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Document not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/rag/documents/{session_id}")
async def clear_documents(session_id: str):
    """Clear all documents for a session"""
    try:
        from document_processor import document_store
        
        document_store.clear_session(session_id)
        
        return {"success": True, "message": "All documents cleared"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/rag/chat/stream")
async def rag_chat_stream(request: RAGChatRequest):
    """Stream chat responses with RAG enhancement"""
    async def generate_stream():
        try:
            from cloud_providers import CloudProviderClient
            from document_processor import document_store
            from embedding_service import EmbeddingClient
            
            # Generate session ID if not provided
            session_id = request.session_id or str(uuid.uuid4())
            provider = request.provider or "nvidia"
            model = request.model
            
            # Initialize session storage if needed
            if session_id not in user_sessions:
                user_sessions[session_id] = {
                    "history": [],
                    "provider": provider,
                    "model": model
                }
            
            session = user_sessions[session_id]
            message = request.message
            
            # RAG Enhancement
            context_chunks = []
            if request.use_rag:
                try:
                    # Initialize embedding client for query
                    embedding_api_key = request.embedding_api_key or request.api_key
                    embedding_client = EmbeddingClient(
                        provider=request.embedding_provider,
                        api_key=embedding_api_key,
                        model=request.embedding_model
                    )
                    
                    # Embed the query
                    query_embedding = embedding_client.embed_query(message)
                    
                    # Search for relevant chunks
                    context_chunks = document_store.search_chunks(
                        session_id=session_id,
                        query_embedding=query_embedding,
                        top_k=request.top_k,
                        similarity_threshold=0.3
                    )
                    
                    # Augment message with context if found
                    if context_chunks:
                        context_text = "\n\n".join([
                            f"[From {chunk['document']}]\n{chunk['chunk']}"
                            for chunk in context_chunks
                        ])
                        
                        augmented_message = f"""Based on the following context, please answer the user's question.

Context:
{context_text}

User Question: {message}

Please provide a comprehensive answer based on the context provided. If the context doesn't contain relevant information, you can use your general knowledge."""
                        
                        message = augmented_message
                        
                        # Send RAG indicator
                        rag_info = {
                            'type': 'rag_info',
                            'chunks_used': len(context_chunks),
                            'sources': [chunk['document'] for chunk in context_chunks]
                        }
                        yield f"data: {json.dumps(rag_info)}\n\n"
                
                except Exception as rag_error:
                    # If RAG fails, continue without it
                    error_info = {
                        'type': 'rag_warning',
                        'message': f"RAG processing failed: {str(rag_error)}"
                    }
                    yield f"data: {json.dumps(error_info)}\n\n"
            
            # Create cloud provider client
            client = CloudProviderClient(
                provider=provider,
                api_key=request.api_key,
                model=model
            )
            
            # Get history
            history = []
            if "history" in session:
                for msg in session["history"]:
                    history.append({
                        "is_user": msg.get("role") == "user",
                        "content": msg.get("content", "")
                    })
            
            # Get response
            full_response = client.chat(message, history=history)
            
            # Stream the response word by word
            words = full_response.split()
            for i, word in enumerate(words):
                yield f"data: {json.dumps({'type': 'chunk', 'content': word + (' ' if i < len(words) - 1 else '')})}\n\n"
                await asyncio.sleep(0.03)
            
            # Add to history (store original user message, not augmented)
            session["history"].append({
                "role": "user",
                "content": request.message
            })
            
            session["history"].append({
                "role": "assistant",
                "content": full_response
            })
            
            # Send done signal with context info
            done_data = {
                'type': 'done',
                'full_response': full_response,
                'rag_used': request.use_rag and len(context_chunks) > 0,
                'sources': [chunk['document'] for chunk in context_chunks] if context_chunks else []
            }
            yield f"data: {json.dumps(done_data)}\n\n"
            
        except Exception as e:
            error_data = {
                'type': 'error',
                'error': str(e)
            }
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", DEFAULT_PORT))
    print("\n" + "="*60)
    print(SERVER_STARTUP_TITLE)
    print("="*60)
    print(f"\n✓ Server starting on http://localhost:{port}")
    print(SERVER_STARTUP_MSG.format(key=API_KEY_LABEL))
    print(f"\n📝 Supported Cloud Providers:")
    for key, provider in CLOUD_PROVIDERS.items():
        print(f"   {provider['icon']} {provider['name']}")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run("server:app", host=DEFAULT_HOST, port=port, reload=True)
