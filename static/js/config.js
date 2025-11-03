/**
 * DualMind Configuration Module
 * Handles initialization and configuration
 */

export class DualMindConfig {
    constructor() {
        this.engine = null;
        this.currentModel = null;
        this.embeddingPipeline = null;
        this.isGenerating = false;
        this.models = [];
        this.modelsLoaded = false;
    }
    
    async initialize() {
        console.log('🧠 DualMind initializing...');
        await this.fetchModels();
        console.log('✅ DualMind initialized');
    }
    
    async fetchModels() {
        try {
            console.log('📡 Fetching WebLLM models from Hugging Face...');
            const response = await fetch('/api/webllm/models');
            const data = await response.json();
            
            if (data.models && data.models.length > 0) {
                this.models = data.models.map(model => ({
                    id: model.id,
                    name: model.name,
                    desc: model.description + (model.provider ? ` [${model.provider}]` : ''),
                    size_gb: model.size_gb,
                    recommended: model.recommended || false,
                    provider: model.provider
                }));
                
                this.modelsLoaded = true;
                console.log(`✅ Loaded ${this.models.length} models from ${data.source}`);
            } else {
                throw new Error('No models returned from API');
            }
        } catch (error) {
            console.error('❌ Error fetching models:', error);
            // Fallback to minimal set if API fails
            this.models = [
                { id: 'Llama-3.2-3B-Instruct-q4f32_1-MLC', name: 'Llama 3.2 3B Instruct', desc: 'Fast, lightweight (2GB)', size_gb: 2.0, recommended: true },
                { id: 'Phi-3.5-mini-instruct-q4f16_1-MLC', name: 'Phi 3.5 Mini Instruct', desc: 'Microsoft, fast (2.5GB)', size_gb: 2.5, recommended: true },
                { id: 'gemma-2-2b-it-q4f16_1-MLC', name: 'Gemma 2 2B IT', desc: 'Google, ultra fast (1.5GB)', size_gb: 1.5, recommended: true },
            ];
            console.warn('⚠️ Using fallback model list');
        }
    }
    
    getModels() {
        return this.models;
    }
}

export const config = new DualMindConfig();

