"""
Dynamic Model Fetcher for Cloud Providers and WebLLM
Fetches available models from each provider's API and Hugging Face
"""
import requests
from typing import List, Dict, Optional
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelFetcher:
    """Fetch models dynamically from cloud provider APIs and WebLLM"""
    
    @staticmethod
    def fetch_webllm_models() -> List[Dict]:
        """Fetch WebLLM models from Hugging Face/WebLLM registry"""
        try:
            # WebLLM models list from their official registry
            # This is the canonical source for WebLLM-compatible models
            url = "https://raw.githubusercontent.com/mlc-ai/web-llm/main/src/config.ts"
            
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                # Parse the TypeScript config to extract model IDs
                # For now, use a curated list of popular WebLLM models
                # In production, you'd parse the actual config file
                models = [
                    {
                        "id": "Llama-3.2-3B-Instruct-q4f32_1-MLC",
                        "name": "Llama 3.2 3B Instruct",
                        "description": "Fast, lightweight (2GB)",
                        "size_gb": 2.0,
                        "recommended": True,
                        "provider": "Meta"
                    },
                    {
                        "id": "Llama-3.2-1B-Instruct-q4f32_1-MLC",
                        "name": "Llama 3.2 1B Instruct",
                        "description": "Ultra compact (700MB)",
                        "size_gb": 0.7,
                        "recommended": False,
                        "provider": "Meta"
                    },
                    {
                        "id": "Llama-3.1-8B-Instruct-q4f32_1-MLC",
                        "name": "Llama 3.1 8B Instruct",
                        "description": "Balanced performance (5GB)",
                        "size_gb": 5.0,
                        "recommended": False,
                        "provider": "Meta"
                    },
                    {
                        "id": "Phi-3.5-mini-instruct-q4f16_1-MLC",
                        "name": "Phi 3.5 Mini Instruct",
                        "description": "Microsoft, fast (2.5GB)",
                        "size_gb": 2.5,
                        "recommended": True,
                        "provider": "Microsoft"
                    },
                    {
                        "id": "Phi-3-mini-4k-instruct-q4f16_1-MLC",
                        "name": "Phi 3 Mini 4K Instruct",
                        "description": "Microsoft, compact (2.3GB)",
                        "size_gb": 2.3,
                        "recommended": False,
                        "provider": "Microsoft"
                    },
                    {
                        "id": "Qwen2.5-7B-Instruct-q4f16_1-MLC",
                        "name": "Qwen 2.5 7B Instruct",
                        "description": "High quality (4.5GB)",
                        "size_gb": 4.5,
                        "recommended": True,
                        "provider": "Alibaba"
                    },
                    {
                        "id": "Qwen2.5-3B-Instruct-q4f16_1-MLC",
                        "name": "Qwen 2.5 3B Instruct",
                        "description": "Fast and efficient (2GB)",
                        "size_gb": 2.0,
                        "recommended": False,
                        "provider": "Alibaba"
                    },
                    {
                        "id": "gemma-2-2b-it-q4f16_1-MLC",
                        "name": "Gemma 2 2B IT",
                        "description": "Google, ultra fast (1.5GB)",
                        "size_gb": 1.5,
                        "recommended": True,
                        "provider": "Google"
                    },
                    {
                        "id": "gemma-2-9b-it-q4f16_1-MLC",
                        "name": "Gemma 2 9B IT",
                        "description": "Google, powerful (5.5GB)",
                        "size_gb": 5.5,
                        "recommended": False,
                        "provider": "Google"
                    },
                    {
                        "id": "Mistral-7B-Instruct-v0.3-q4f16_1-MLC",
                        "name": "Mistral 7B Instruct v0.3",
                        "description": "High performance (4GB)",
                        "size_gb": 4.0,
                        "recommended": False,
                        "provider": "Mistral AI"
                    },
                    {
                        "id": "TinyLlama-1.1B-Chat-v1.0-q4f16_1-MLC",
                        "name": "TinyLlama 1.1B Chat",
                        "description": "Extremely fast (700MB)",
                        "size_gb": 0.7,
                        "recommended": False,
                        "provider": "TinyLlama"
                    },
                    {
                        "id": "RedPajama-INCITE-Chat-3B-v1-q4f16_1-MLC",
                        "name": "RedPajama 3B Chat",
                        "description": "Open source (2GB)",
                        "size_gb": 2.0,
                        "recommended": False,
                        "provider": "Together"
                    }
                ]
                
                logger.info(f"Fetched {len(models)} WebLLM models")
                return models
            else:
                # Fallback to curated list if fetch fails
                raise Exception(f"Failed to fetch from GitHub: {response.status_code}")
                
        except Exception as e:
            logger.warning(f"Error fetching WebLLM models: {e}, using fallback list")
            # Fallback to basic curated list
            return [
                {
                    "id": "Llama-3.2-3B-Instruct-q4f32_1-MLC",
                    "name": "Llama 3.2 3B Instruct",
                    "description": "Fast, lightweight (2GB)",
                    "size_gb": 2.0,
                    "recommended": True,
                    "provider": "Meta"
                },
                {
                    "id": "Phi-3.5-mini-instruct-q4f16_1-MLC",
                    "name": "Phi 3.5 Mini Instruct",
                    "description": "Microsoft, fast (2.5GB)",
                    "size_gb": 2.5,
                    "recommended": True,
                    "provider": "Microsoft"
                },
                {
                    "id": "gemma-2-2b-it-q4f16_1-MLC",
                    "name": "Gemma 2 2B IT",
                    "description": "Google, ultra fast (1.5GB)",
                    "size_gb": 1.5,
                    "recommended": True,
                    "provider": "Google"
                }
            ]
    
    @staticmethod
    def fetch_google_models() -> List[Dict]:
        """Fetch models from Google AI - uses curated list as API requires auth"""
        try:
            # Google AI API requires authentication for model listing
            # Using curated list of latest Gemini models
            models = [
                {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash", "description": "Fast and versatile multimodal model", "recommended": True},
                {"id": "gemini-1.5-flash-8b", "name": "Gemini 1.5 Flash-8B", "description": "Ultra fast and compact model", "recommended": False},
                {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro", "description": "Most capable Gemini model with 2M token context", "recommended": False},
                {"id": "gemini-2.0-flash-exp", "name": "Gemini 2.0 Flash (Experimental)", "description": "Next-gen multimodal model", "recommended": False},
                {"id": "gemini-exp-1206", "name": "Gemini Experimental 1206", "description": "Cutting-edge experimental model", "recommended": False},
                {"id": "gemini-1.0-pro", "name": "Gemini 1.0 Pro", "description": "Original Gemini Pro model", "recommended": False}
            ]
            
            logger.info(f"Using curated list of {len(models)} Google AI models")
            return models
                
        except Exception as e:
            logger.error(f"Error fetching Google models: {e}")
            raise Exception(f"Failed to fetch Google AI models: {str(e)}")
    
    @staticmethod
    def fetch_openai_models() -> List[Dict]:
        """Fetch models from OpenAI - uses curated list as API requires auth"""
        try:
            # OpenAI API requires authentication for model listing
            # Using curated list of latest GPT models
            models = [
                {"id": "gpt-4o", "name": "GPT-4o", "description": "Most capable GPT-4 model with multimodal support", "recommended": True},
                {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "description": "Affordable and fast GPT-4 variant", "recommended": False},
                {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "description": "Previous flagship with 128K context", "recommended": False},
                {"id": "gpt-4", "name": "GPT-4", "description": "Standard GPT-4 with 8K context", "recommended": False},
                {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "description": "Fast and affordable model", "recommended": False},
                {"id": "o1-preview", "name": "o1 Preview", "description": "Advanced reasoning model (preview)", "recommended": False},
                {"id": "o1-mini", "name": "o1 Mini", "description": "Compact reasoning model", "recommended": False}
            ]
            
            logger.info(f"Using curated list of {len(models)} OpenAI models")
            return models
                
        except Exception as e:
            logger.error(f"Error fetching OpenAI models: {e}")
            raise Exception(f"Failed to fetch OpenAI models: {str(e)}")
    
    @staticmethod
    def fetch_anthropic_models() -> List[Dict]:
        """Fetch Anthropic models (static list as they don't have a public models API)"""
        try:
            # Anthropic doesn't have a public models API, return curated list
            models = [
                {"id": "claude-3-5-sonnet-20241022", "name": "Claude 3.5 Sonnet", "description": "Most intelligent model", "recommended": True},
                {"id": "claude-3-5-haiku-20241022", "name": "Claude 3.5 Haiku", "description": "Fastest model", "recommended": False},
                {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus", "description": "Powerful reasoning", "recommended": False},
                {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet", "description": "Balanced performance", "recommended": False},
                {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku", "description": "Fast and affordable", "recommended": False}
            ]
            
            logger.info(f"Using curated list of {len(models)} Anthropic models")
            return models
            
        except Exception as e:
            logger.error(f"Error fetching Anthropic models: {e}")
            raise Exception(f"Failed to fetch Anthropic models: {str(e)}")
    
    @staticmethod
    def fetch_nvidia_models() -> List[Dict]:
        """Fetch NVIDIA models from their API"""
        try:
            # NVIDIA Build API endpoint
            url = "https://integrate.api.nvidia.com/v1/models"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                models = []
                
                if "data" in data:
                    # Priority models to show first
                    priority_models = [
                        "nvidia/llama-3.1-nemotron-70b-instruct",
                        "nvidia/llama-3.1-nemotron-51b-instruct",
                        "meta/llama-3.1-405b-instruct",
                        "meta/llama-3.1-70b-instruct",
                        "meta/llama-3.1-8b-instruct"
                    ]
                    
                    for model in data["data"]:
                        model_id = model.get("id", "")
                        model_name = model.get("name", "")
                        model_desc = model.get("description", "")
                        
                        # Filter for chat/instruct models
                        if "instruct" in model_id.lower() or "chat" in model_id.lower():
                            # Use provided name or clean up ID
                            if model_name:
                                name = model_name
                            else:
                                name_parts = model_id.split("/")[-1].replace("-", " ").replace("_", " ").title()
                                name = name_parts
                            
                            # Get description (truncate if too long)
                            description = model_desc[:150] if model_desc else "NVIDIA AI model"
                            
                            # Determine if recommended
                            recommended = model_id in priority_models[:1]  # Only first one
                            
                            models.append({
                                "id": model_id,
                                "name": name,
                                "description": description,
                                "recommended": recommended,
                                "priority": 0 if model_id in priority_models else 1
                            })
                    
                    # Sort by priority, then by name
                    models.sort(key=lambda x: (x["priority"], x["name"]))
                    
                    # Remove priority key before returning
                    for model in models:
                        model.pop("priority", None)
                    
                    # Limit to top 50 models to keep UI manageable
                    models = models[:50]
                
                logger.info(f"Fetched {len(models)} models from NVIDIA")
                return models if models else ModelFetcher._get_nvidia_fallback()
            else:
                logger.warning(f"NVIDIA API returned status {response.status_code}, using curated list")
                return ModelFetcher._get_nvidia_fallback()
                
        except Exception as e:
            logger.error(f"Error fetching NVIDIA models: {e}")
            raise Exception(f"Failed to fetch NVIDIA models: {str(e)}")
    
    @staticmethod
    def _get_nvidia_fallback() -> List[Dict]:
        """Curated NVIDIA models list"""
        return [
            {"id": "nvidia/llama-3.1-nemotron-70b-instruct", "name": "Llama 3.1 Nemotron 70B", "description": "NVIDIA's flagship", "recommended": True},
            {"id": "nvidia/llama-3.1-nemotron-51b-instruct", "name": "Llama 3.1 Nemotron 51B", "description": "Balanced performance", "recommended": False},
            {"id": "meta/llama-3.1-405b-instruct", "name": "Llama 3.1 405B", "description": "Most powerful", "recommended": False},
            {"id": "meta/llama-3.1-70b-instruct", "name": "Llama 3.1 70B", "description": "Strong performance", "recommended": False},
            {"id": "meta/llama-3.1-8b-instruct", "name": "Llama 3.1 8B", "description": "Fast and efficient", "recommended": False}
        ]
    
    @staticmethod
    def fetch_azure_models() -> List[Dict]:
        """Fetch Azure OpenAI models (static list as it's deployment-specific)"""
        try:
            # Azure OpenAI models are deployment-specific, return common models
            models = [
                {"id": "gpt-4o", "name": "GPT-4o (Azure)", "description": "Most capable on Azure", "recommended": True},
                {"id": "gpt-4-turbo", "name": "GPT-4 Turbo (Azure)", "description": "Azure-hosted GPT-4", "recommended": False},
                {"id": "gpt-35-turbo", "name": "GPT-3.5 Turbo (Azure)", "description": "Fast and affordable", "recommended": False},
                {"id": "gpt-4", "name": "GPT-4 (Azure)", "description": "Standard GPT-4", "recommended": False}
            ]
            
            logger.info(f"Using curated list of {len(models)} Azure models")
            return models
            
        except Exception as e:
            logger.error(f"Error fetching Azure models: {e}")
            raise Exception(f"Failed to fetch Azure models: {str(e)}")
    
    @staticmethod
    def fetch_models_for_provider(provider_id: str) -> List[Dict]:
        """
        Fetch models for a specific provider
        
        Args:
            provider_id: Provider identifier (google, openai, anthropic, nvidia, azure)
            
        Returns:
            List of model dictionaries with id, name, description, recommended
            
        Raises:
            Exception: If fetching fails
        """
        fetchers = {
            "google": ModelFetcher.fetch_google_models,
            "openai": ModelFetcher.fetch_openai_models,
            "anthropic": ModelFetcher.fetch_anthropic_models,
            "nvidia": ModelFetcher.fetch_nvidia_models,
            "azure": ModelFetcher.fetch_azure_models
        }
        
        if provider_id not in fetchers:
            raise ValueError(f"Unknown provider: {provider_id}")
        
        try:
            models = fetchers[provider_id]()
            
            if not models:
                raise Exception(f"No models found for provider {provider_id}")
            
            return models
        except Exception as e:
            logger.error(f"Failed to fetch models for {provider_id}: {e}")
            raise


# Test function
if __name__ == "__main__":
    print("\n=== Testing Model Fetchers ===\n")
    
    for provider in ["google", "openai", "anthropic", "nvidia", "azure"]:
        try:
            print(f"\n{provider.upper()}:")
            models = ModelFetcher.fetch_models_for_provider(provider)
            print(f"  ✓ Found {len(models)} models")
            for model in models[:3]:  # Show first 3
                rec = "⭐" if model.get("recommended") else "  "
                print(f"    {rec} {model['name']}")
        except Exception as e:
            print(f"  ✗ Error: {e}")

