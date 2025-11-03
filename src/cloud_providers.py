"""
Multi-Cloud Provider Support
=============================
Unified interface for different cloud AI providers
"""

import os
from typing import Dict, Any, Optional
from branding_config import CLOUD_PROVIDERS, DEFAULT_PROVIDER


class CloudProviderClient:
    """Unified client for multiple cloud AI providers"""
    
    def __init__(self, provider: str = DEFAULT_PROVIDER, api_key: str = None, model: str = None):
        self.provider = provider
        self.api_key = api_key
        
        if provider not in CLOUD_PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}. Available: {list(CLOUD_PROVIDERS.keys())}")
        
        self.config = CLOUD_PROVIDERS[provider]
        # Use provided model or default from config
        self.model = model if model else self.config["model"]
    
    def chat(self, message: str, history: list = None) -> str:
        """
        Send a chat message and get a response
        
        Args:
            message: User message
            history: Conversation history
            
        Returns:
            AI response string
        """
        if self.provider == "google":
            return self._chat_google(message, history)
        elif self.provider == "openai":
            return self._chat_openai(message, history)
        elif self.provider == "anthropic":
            return self._chat_anthropic(message, history)
        elif self.provider == "nvidia":
            return self._chat_nvidia(message, history)
        elif self.provider == "azure":
            return self._chat_azure(message, history)
        else:
            raise NotImplementedError(f"Provider {self.provider} not yet implemented")
    
    def _chat_google(self, message: str, history: list = None) -> str:
        """Google AI (Gemini) implementation"""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)
            
            # Build conversation history
            chat_history = []
            if history:
                for msg in history:
                    chat_history.append({
                        "role": "user" if msg.get("is_user") else "model",
                        "parts": [msg.get("content", "")]
                    })
            
            # Start chat with history
            chat = model.start_chat(history=chat_history)
            
            # Generate response
            response = chat.send_message(message)
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Google AI error: {str(e)}")
    
    def _chat_openai(self, message: str, history: list = None) -> str:
        """OpenAI (GPT) implementation"""
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.api_key)
            
            # Build messages
            messages = []
            if history:
                for msg in history:
                    messages.append({
                        "role": "user" if msg.get("is_user") else "assistant",
                        "content": msg.get("content", "")
                    })
            
            messages.append({"role": "user", "content": message})
            
            # Generate response
            response = client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"OpenAI error: {str(e)}")
    
    def _chat_anthropic(self, message: str, history: list = None) -> str:
        """Anthropic (Claude) implementation"""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            # Build messages
            messages = []
            if history:
                for msg in history:
                    messages.append({
                        "role": "user" if msg.get("is_user") else "assistant",
                        "content": msg.get("content", "")
                    })
            
            messages.append({"role": "user", "content": message})
            
            # Generate response
            response = client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=messages
            )
            
            return response.content[0].text
            
        except Exception as e:
            raise Exception(f"Anthropic error: {str(e)}")
    
    def _chat_nvidia(self, message: str, history: list = None) -> str:
        """NVIDIA AI implementation"""
        try:
            import requests
            
            url = "https://integrate.api.nvidia.com/v1/chat/completions"
            
            # Build messages
            messages = []
            if history:
                for msg in history:
                    messages.append({
                        "role": "user" if msg.get("is_user") else "assistant",
                        "content": msg.get("content", "")
                    })
            
            messages.append({"role": "user", "content": message})
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1024
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            return response.json()["choices"][0]["message"]["content"]
            
        except Exception as e:
            raise Exception(f"NVIDIA AI error: {str(e)}")
    
    def _chat_azure(self, message: str, history: list = None) -> str:
        """Microsoft Azure OpenAI implementation"""
        try:
            import openai
            
            # Note: Azure OpenAI requires additional configuration
            # This is a simplified version - user needs to set AZURE_OPENAI_ENDPOINT
            endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-resource.openai.azure.com")
            
            client = openai.AzureOpenAI(
                api_key=self.api_key,
                api_version="2024-02-01",
                azure_endpoint=endpoint
            )
            
            # Build messages
            messages = []
            if history:
                for msg in history:
                    messages.append({
                        "role": "user" if msg.get("is_user") else "assistant",
                        "content": msg.get("content", "")
                    })
            
            messages.append({"role": "user", "content": message})
            
            # Generate response
            response = client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Azure OpenAI error: {str(e)}")


def get_provider_info(provider: str) -> Dict[str, Any]:
    """Get information about a provider"""
    if provider not in CLOUD_PROVIDERS:
        return None
    return CLOUD_PROVIDERS[provider]


def list_providers() -> Dict[str, Dict[str, Any]]:
    """List all available providers"""
    return CLOUD_PROVIDERS


def validate_api_key(provider: str, api_key: str) -> bool:
    """
    Validate API key format for a provider
    
    Returns:
        True if format is valid, False otherwise
    """
    if not api_key:
        return False
    
    # Basic format validation
    if provider == "google":
        return api_key.startswith("AIza")
    elif provider == "openai":
        return api_key.startswith("sk-")
    elif provider == "anthropic":
        return api_key.startswith("sk-ant-")
    elif provider == "nvidia":
        return len(api_key) > 10  # Basic length check
    elif provider == "azure":
        return len(api_key) > 10  # Basic length check
    
    return True  # Default to true for unknown providers


if __name__ == "__main__":
    # Test/demo
    print("Available Cloud Providers:")
    print("=" * 60)
    for key, provider in CLOUD_PROVIDERS.items():
        print(f"\n{provider['icon']} {provider['name']}")
        print(f"   Model: {provider['model']}")
        print(f"   {provider['description']}")
        print(f"   {provider['free_tier']}")
        if not provider['requires_credit_card']:
            print(f"   ✓ No credit card required")
    print("\n" + "=" * 60)

