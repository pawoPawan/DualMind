"""
Model manager for downloading and caching GGUF models from Hugging Face
"""
from huggingface_hub import hf_hub_download, list_repo_files
import os
from pathlib import Path
from typing import Optional, List, Dict

# Available small GGUF models for browser inference
AVAILABLE_MODELS = {
    "tinyllama": {
        "name": "TinyLlama 1.1B Chat",
        "repo_id": "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
        "filename": "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        "size_mb": 669,
        "description": "Fast, small model great for quick responses"
    },
    "phi2": {
        "name": "Phi-2 2.7B", 
        "repo_id": "TheBloke/phi-2-GGUF",
        "filename": "phi-2.Q4_K_M.gguf",
        "size_mb": 1600,
        "description": "Microsoft's powerful small model"
    },
    "qwen": {
        "name": "Qwen2 0.5B",
        "repo_id": "Qwen/Qwen2-0.5B-Instruct-GGUF",
        "filename": "qwen2-0_5b-instruct-q4_k_m.gguf",
        "size_mb": 352,
        "description": "Tiny but capable multilingual model"
    }
}

class ModelManager:
    """Manages GGUF model downloads and caching"""
    
    def __init__(self, cache_dir: str = "./model_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
    def get_available_models(self) -> List[Dict]:
        """Get list of available models"""
        models = []
        for key, info in AVAILABLE_MODELS.items():
            model_path = self.cache_dir / info["filename"]
            models.append({
                "id": key,
                "name": info["name"],
                "size_mb": info["size_mb"],
                "description": info["description"],
                "cached": model_path.exists()
            })
        return models
    
    def get_model_path(self, model_id: str) -> Optional[str]:
        """Get cached model path if exists"""
        if model_id not in AVAILABLE_MODELS:
            return None
            
        info = AVAILABLE_MODELS[model_id]
        model_path = self.cache_dir / info["filename"]
        
        if model_path.exists():
            return str(model_path)
        return None
    
    def download_model(self, model_id: str) -> str:
        """Download model from Hugging Face"""
        if model_id not in AVAILABLE_MODELS:
            raise ValueError(f"Unknown model: {model_id}")
        
        info = AVAILABLE_MODELS[model_id]
        
        print(f"Downloading {info['name']} from Hugging Face...")
        
        # Download to cache directory
        model_path = hf_hub_download(
            repo_id=info["repo_id"],
            filename=info["filename"],
            cache_dir=str(self.cache_dir),
            local_dir=str(self.cache_dir),
            local_dir_use_symlinks=False
        )
        
        print(f"✓ Model downloaded: {model_path}")
        return model_path


# Global model manager
model_manager = ModelManager()


if __name__ == "__main__":
    # Test the model manager
    print("Available models:")
    for model in model_manager.get_available_models():
        print(f"  - {model['name']} ({model['size_mb']}MB) - Cached: {model['cached']}")

