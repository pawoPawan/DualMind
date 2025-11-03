"""
Branding and Configuration File
=====================================
Customize all chatbot names, colors, and settings here.
Changes in this file will be reflected throughout the application.
"""

# ============================================
# CHATBOT BRANDING
# ============================================

# Main chatbot name (shown in UI, headers, titles)
CHATBOT_NAME = "DualMind AI"

# Full chatbot title (shown in browser tab)
CHATBOT_TITLE = "DualMind AI Chatbot"

# Chatbot description (for meta tags and API docs)
CHATBOT_DESCRIPTION = "Dual-mode AI chatbot - Cloud power or Local privacy"

# Welcome message (shown when chat starts)
WELCOME_MESSAGE_CLOUD = "Welcome to DualMind AI! Experience powerful cloud-based intelligence."
WELCOME_MESSAGE_LOCAL = "Welcome to DualMind AI Local Mode! Your AI runs privately in your browser."

# Chatbot emoji/icon
CHATBOT_ICON = "🧠"  # Brain emoji represents dual-mind concept

# Version number
VERSION = "2.0.0"

# ============================================
# MODE LABELS
# ============================================

# Cloud mode labels
CLOUD_MODE_NAME = "Cloud Mode"
CLOUD_MODE_ICON = "☁️"
CLOUD_MODE_DESCRIPTION = "Need API key - Faster"
CLOUD_MODE_BADGE = "☁️ Cloud Mode"

# Local mode labels  
LOCAL_MODE_NAME = "Local Mode"
LOCAL_MODE_ICON = "🔒"
LOCAL_MODE_DESCRIPTION = "No API key - Private"
LOCAL_MODE_BADGE = "🔒 Local Mode"

# ============================================
# CLOUD PROVIDERS CONFIGURATION
# ============================================

# Available cloud providers
CLOUD_PROVIDERS = {
    "google": {
        "name": "Google AI (Gemini)",
        "icon": "🔷",
        "api_key_label": "Google AI API Key",
        "api_key_placeholder": "Enter your Google AI API key (starts with AIza...)",
        "help_url": "https://aistudio.google.com/apikey",
        "help_text": "Get FREE API key from Google AI Studio",
        "model": "gemini-1.5-flash",
        "description": "Fast and powerful Gemini models",
        "free_tier": "✓ 60 requests/minute free",
        "requires_credit_card": False,
        "models_api": "https://generativelanguage.googleapis.com/v1beta/models",
        "models": [
            {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash", "description": "Fast and versatile", "recommended": True},
            {"id": "gemini-1.5-flash-8b", "name": "Gemini 1.5 Flash-8B", "description": "Ultra fast and compact", "recommended": False},
            {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro", "description": "Most capable model", "recommended": False},
            {"id": "gemini-2.0-flash-exp", "name": "Gemini 2.0 Flash (Experimental)", "description": "Latest experimental", "recommended": False},
            {"id": "gemini-exp-1206", "name": "Gemini Experimental 1206", "description": "Cutting-edge experimental", "recommended": False}
        ]
    },
    "openai": {
        "name": "OpenAI (GPT)",
        "icon": "🟢",
        "api_key_label": "OpenAI API Key",
        "api_key_placeholder": "Enter your OpenAI API key (starts with sk-...)",
        "help_url": "https://platform.openai.com/api-keys",
        "help_text": "Get API key from OpenAI Platform",
        "model": "gpt-3.5-turbo",
        "description": "ChatGPT-powered responses",
        "free_tier": "✓ $5 free credits for new users",
        "requires_credit_card": True,
        "models_api": "https://api.openai.com/v1/models",
        "models": [
            {"id": "gpt-4o", "name": "GPT-4o", "description": "Most capable GPT-4 model", "recommended": True},
            {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "description": "Affordable and fast", "recommended": False},
            {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "description": "Previous flagship", "recommended": False},
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "description": "Fast and affordable", "recommended": False},
            {"id": "o1-preview", "name": "o1 Preview", "description": "Advanced reasoning", "recommended": False},
            {"id": "o1-mini", "name": "o1 Mini", "description": "Reasoning model", "recommended": False}
        ]
    },
    "anthropic": {
        "name": "Anthropic (Claude)",
        "icon": "🟣",
        "api_key_label": "Anthropic API Key",
        "api_key_placeholder": "Enter your Anthropic API key (starts with sk-ant-...)",
        "help_url": "https://console.anthropic.com/account/keys",
        "help_text": "Get API key from Anthropic Console",
        "model": "claude-3-haiku-20240307",
        "description": "Claude AI - thoughtful and precise",
        "free_tier": "✓ Limited free tier available",
        "requires_credit_card": True,
        "models_api": None,
        "models": [
            {"id": "claude-3-5-sonnet-20241022", "name": "Claude 3.5 Sonnet", "description": "Most intelligent model", "recommended": True},
            {"id": "claude-3-5-haiku-20241022", "name": "Claude 3.5 Haiku", "description": "Fastest model", "recommended": False},
            {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus", "description": "Powerful reasoning", "recommended": False},
            {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet", "description": "Balanced performance", "recommended": False},
            {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku", "description": "Fast and affordable", "recommended": False}
        ]
    },
    "nvidia": {
        "name": "NVIDIA AI",
        "icon": "🟩",
        "api_key_label": "NVIDIA API Key",
        "api_key_placeholder": "Enter your NVIDIA API key...",
        "help_url": "https://build.nvidia.com/explore/discover",
        "help_text": "Get API key from NVIDIA AI Foundation",
        "model": "nvidia/llama-3.1-nemotron-70b-instruct",
        "description": "NVIDIA-optimized AI models",
        "free_tier": "✓ Free credits available",
        "requires_credit_card": False,
        "models_api": None,
        "models": [
            {"id": "nvidia/llama-3.1-nemotron-70b-instruct", "name": "Llama 3.1 Nemotron 70B", "description": "NVIDIA's flagship", "recommended": True},
            {"id": "nvidia/llama-3.1-nemotron-51b-instruct", "name": "Llama 3.1 Nemotron 51B", "description": "Balanced performance", "recommended": False},
            {"id": "meta/llama-3.1-405b-instruct", "name": "Llama 3.1 405B", "description": "Most powerful", "recommended": False},
            {"id": "meta/llama-3.1-70b-instruct", "name": "Llama 3.1 70B", "description": "Strong performance", "recommended": False},
            {"id": "meta/llama-3.1-8b-instruct", "name": "Llama 3.1 8B", "description": "Fast and efficient", "recommended": False}
        ]
    },
    "azure": {
        "name": "Microsoft Azure OpenAI",
        "icon": "🔵",
        "api_key_label": "Azure OpenAI API Key",
        "api_key_placeholder": "Enter your Azure OpenAI API key...",
        "help_url": "https://portal.azure.com",
        "help_text": "Get API key from Azure Portal",
        "model": "gpt-35-turbo",
        "description": "Enterprise-grade OpenAI on Azure",
        "free_tier": "✓ Azure free trial available",
        "requires_credit_card": True,
        "models_api": None,
        "models": [
            {"id": "gpt-4o", "name": "GPT-4o (Azure)", "description": "Most capable on Azure", "recommended": True},
            {"id": "gpt-4-turbo", "name": "GPT-4 Turbo (Azure)", "description": "Azure-hosted GPT-4", "recommended": False},
            {"id": "gpt-35-turbo", "name": "GPT-3.5 Turbo (Azure)", "description": "Fast and affordable", "recommended": False},
            {"id": "gpt-4", "name": "GPT-4 (Azure)", "description": "Standard GPT-4", "recommended": False}
        ]
    }
}

# Default provider (used if none selected)
DEFAULT_PROVIDER = "nvidia"

# API KEY CONFIGURATION (generic, provider-agnostic)
API_KEY_LABEL = "API Key"
API_KEY_PLACEHOLDER = "Enter your API key..."
API_KEY_HELP_TEXT = "Select a provider and get your free API key"
API_KEY_HELP_LINK_TEXT = "Get API Key"

# Provider selection UI text
PROVIDER_SELECTION_TITLE = "Choose Your AI Provider"
PROVIDER_SELECTION_SUBTITLE = "Select from multiple cloud AI providers"
PROVIDER_SELECTION_LABEL = "Select AI Provider:"

# ============================================
# UI TEXT & LABELS
# ============================================

# Button labels
BTN_START_CHATTING = "Start Chatting"
BTN_SEND = "Send"
BTN_CHANGE_API_KEY = "Change Model API Key"
BTN_CHANGE_MODEL = "Change Model"
BTN_SWITCH_TO_LOCAL = "🔒 Switch to Local Mode"
BTN_SWITCH_TO_CLOUD = "☁️ Switch to Cloud Mode"
BTN_DOWNLOAD_MODEL = "Download & Load Model"

# Modal titles
MODAL_TITLE_WELCOME = f"{CHATBOT_ICON} Welcome to {CHATBOT_NAME}"
MODAL_SUBTITLE_CHOOSE_MODE = "Choose your preferred mode"
MODAL_SUBTITLE_API_KEY = f"Please enter your {API_KEY_LABEL} to start chatting"
MODAL_TITLE_LOCAL = f"{CHATBOT_ICON} Welcome to {CHATBOT_NAME} - Local Mode"
MODAL_SUBTITLE_LOCAL = "Choose a model to download and run locally in your browser"

# Input placeholder
INPUT_PLACEHOLDER = "Type your message..."

# Info messages
INFO_NO_API_KEY = "✓ No credit card required"
INFO_FREE_TIER = "✓ 60 requests/minute free tier"
INFO_PRIVACY = "✓ Runs 100% in your browser"
INFO_NO_KEY_NEEDED = "✓ No API key needed"
INFO_PRIVACY_FIRST = "✓ Privacy-first - data never leaves your device"

# Error messages
ERROR_EMPTY_KEY = f"Please enter a {API_KEY_LABEL}"
ERROR_INVALID_KEY_FORMAT = f"Invalid {API_KEY_LABEL} format. Key should start with \"AIza\""
ERROR_INVALID_KEY_API = f"Your {API_KEY_LABEL} appears to be invalid. Would you like to enter a new one?"
ERROR_CONNECTION = "❌ Error: Could not connect to server"

# Confirmation messages
CONFIRM_CHANGE_KEY = f"Are you sure you want to change your {API_KEY_LABEL}? This will clear your current session."
CONFIRM_CHANGE_MODEL = "Changing models will clear your conversation. Continue?"
CONFIRM_SWITCH_MODE = f"Switch to {CLOUD_MODE_NAME}? You'll need a {API_KEY_LABEL}."

# ============================================
# COLORS & STYLING
# ============================================

# Primary gradient colors (for buttons, headers)
COLOR_PRIMARY_START = "#667eea"
COLOR_PRIMARY_END = "#764ba2"

# Secondary gradient (for local mode elements)
COLOR_SECONDARY_START = "#48bb78"
COLOR_SECONDARY_END = "#38a169"

# Background gradient
BACKGROUND_GRADIENT_START = "#667eea"
BACKGROUND_GRADIENT_END = "#764ba2"

# Text colors
COLOR_TEXT_PRIMARY = "#333"
COLOR_TEXT_SECONDARY = "#666"
COLOR_TEXT_LIGHT = "#999"

# Background colors
COLOR_BG_MESSAGE_USER = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
COLOR_BG_MESSAGE_AGENT = "#ffffff"
COLOR_BG_CHAT = "#f7f7f7"

# ============================================
# MODEL CONFIGURATION (for Local Mode)
# ============================================

# Available models for local mode
LOCAL_MODELS = {
    "phi3": {
        "id": "Phi-3-mini-4k-instruct-q4f16_1-MLC",
        "name": "⚡ Phi-3 Mini (Recommended)",
        "description": "Microsoft's small but powerful model",
        "size": "~2GB"
    },
    "tinyllama": {
        "id": "TinyLlama-1.1B-Chat-v0.4-q4f16_1-MLC",
        "name": "🚀 TinyLlama (Fastest)",
        "description": "Ultra-fast responses, good for quick chats",
        "size": "~600MB"
    },
    "llama32": {
        "id": "Llama-3.2-1B-Instruct-q4f16_1-MLC",
        "name": "🔥 Llama 3.2 1B",
        "description": "Meta's latest compact model",
        "size": "~800MB"
    }
}

# ============================================
# SERVER CONFIGURATION
# ============================================

# Default server settings
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000

# Server startup messages
SERVER_STARTUP_TITLE = f"🚀 {CHATBOT_NAME} Chatbot Server"
SERVER_STARTUP_MSG = "✓ Users will enter their {key} in the browser"
SERVER_STARTUP_API_MSG = f"📝 To get a FREE {API_KEY_LABEL}:"

# Health check message
HEALTH_CHECK_MESSAGE = "DualMind AI Chatbot is running"

# ============================================
# PATHS & URLS
# ============================================

# Routes
ROUTE_HOME = "/"
ROUTE_LOCAL = "/local"
ROUTE_HEALTH = "/health"
ROUTE_CHAT = "/api/chat"
ROUTE_HISTORY = "/api/history"
ROUTE_SESSIONS = "/api/sessions"

# External URLs
URL_GOOGLE_AI_STUDIO = "https://aistudio.google.com/apikey"
URL_ADK_DOCS = "https://google.github.io/adk-docs/"

# ============================================
# TYPING INDICATORS & ANIMATIONS
# ============================================

# Typing indicator settings
TYPING_INDICATOR_DOTS = 3
TYPING_INDICATOR_COLOR = COLOR_PRIMARY_START

# Animation speeds (in seconds)
ANIMATION_SLIDE_IN = 0.3
ANIMATION_BUTTON_SCALE = 0.2

# ============================================
# ADVANCED SETTINGS
# ============================================

# Maximum message length
MAX_MESSAGE_LENGTH = 4000

# Session ID prefix
SESSION_ID_PREFIX = "session"

# LocalStorage keys
STORAGE_KEY_API_KEY = "cloudApiKey"
STORAGE_KEY_PROVIDER = "cloudProvider"
STORAGE_KEY_PREFERENCES = "dualmind_preferences"
STORAGE_KEY_LOCAL_BANNER = "localModeBannerDismissed"
STORAGE_KEY_CLOUD_BANNER = "cloudModeBannerDismissed"

# Progress bar colors
PROGRESS_BAR_COLOR = f"linear-gradient(135deg, {COLOR_PRIMARY_START} 0%, {COLOR_PRIMARY_END} 100%)"

# Model cache directory (for server-side, if used)
MODEL_CACHE_DIR = "./model_cache"

# ============================================
# FEATURE FLAGS
# ============================================

# Enable/disable features
ENABLE_LOCAL_MODE = True
ENABLE_CLOUD_MODE = True
ENABLE_MODE_SWITCHING = True
ENABLE_API_KEY_STORAGE = True
ENABLE_CONVERSATION_HISTORY = True

# ============================================
# METADATA (for SEO, sharing)
# ============================================

META_KEYWORDS = f"{CHATBOT_NAME}, AI chatbot, dual-mode AI, cloud AI, local AI, privacy-first AI, Google Gemini"
META_AUTHOR = "Your Name/Organization"
META_OG_IMAGE = "/static/og-image.png"  # Add your own image

# ============================================
# CUSTOM MESSAGES (per language/region)
# ============================================

# You can add language-specific configurations here
MESSAGES = {
    "en": {
        "welcome": WELCOME_MESSAGE_CLOUD,
        "goodbye": "Thank you for using {CHATBOT_NAME}!",
    },
    # Add more languages as needed
    # "es": {...},
    # "fr": {...},
}

# ============================================
# EXPORT ALL SETTINGS
# ============================================

def get_branding_config():
    """Return all branding configuration as a dictionary"""
    return {
        "chatbot_name": CHATBOT_NAME,
        "chatbot_title": CHATBOT_TITLE,
        "chatbot_description": CHATBOT_DESCRIPTION,
        "chatbot_icon": CHATBOT_ICON,
        "version": VERSION,
        "colors": {
            "primary_start": COLOR_PRIMARY_START,
            "primary_end": COLOR_PRIMARY_END,
            "secondary_start": COLOR_SECONDARY_START,
            "secondary_end": COLOR_SECONDARY_END,
        },
        "api_key_label": API_KEY_LABEL,
        "api_key_help_url": API_KEY_HELP_URL,
        "local_models": LOCAL_MODELS,
    }


if __name__ == "__main__":
    # Print configuration for verification
    print("=" * 60)
    print(f"DualMind AI - Branding Configuration")
    print("=" * 60)
    print(f"Chatbot Name: {CHATBOT_NAME}")
    print(f"Version: {VERSION}")
    print(f"Cloud Mode: {CLOUD_MODE_NAME} ({CLOUD_MODE_ICON})")
    print(f"Local Mode: {LOCAL_MODE_NAME} ({LOCAL_MODE_ICON})")
    print(f"API Key Label: {API_KEY_LABEL}")
    print(f"Available Local Models: {len(LOCAL_MODELS)}")
    for key, model in LOCAL_MODELS.items():
        print(f"  - {model['name']}: {model['size']}")
    print("=" * 60)

