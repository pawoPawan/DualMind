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
        
        // Available models
        this.models = [
            { id: 'Llama-3.2-3B-Instruct-q4f32_1-MLC', name: 'Llama 3.2 3B Instruct', desc: 'Fast, lightweight (2GB)', recommended: true },
            { id: 'Llama-3.1-8B-Instruct-q4f32_1-MLC', name: 'Llama 3.1 8B Instruct', desc: 'Balanced performance (5GB)' },
            { id: 'Phi-3.5-mini-instruct-q4f16_1-MLC', name: 'Phi 3.5 Mini Instruct', desc: 'Microsoft, fast (2.5GB)' },
            { id: 'Qwen2.5-7B-Instruct-q4f16_1-MLC', name: 'Qwen 2.5 7B Instruct', desc: 'High quality (4.5GB)' },
            { id: 'gemma-2-2b-it-q4f16_1-MLC', name: 'Gemma 2 2B IT', desc: 'Google, ultra fast (1.5GB)' },
        ];
    }
    
    async initialize() {
        console.log('DualMind initialized');
    }
    
    getModels() {
        return this.models;
    }
}

export const config = new DualMindConfig();

