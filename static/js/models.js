/**
 * DualMind Models Module
 * Handles model selection and loading
 */

import { ui } from './ui.js';
import { storage } from './storage.js';
import { config } from './config.js';

export class ModelManager {
    constructor() {
        this.availableModels = [];
    }
    
    async initialize() {
        // Wait for config to load models
        let retries = 0;
        while (!config.modelsLoaded && retries < 10) {
            await new Promise(resolve => setTimeout(resolve, 100));
            retries++;
        }
        
        this.availableModels = config.getModels();
        console.log(`📦 Model manager initialized with ${this.availableModels.length} models`);
        
        const savedModel = storage.getCurrentModel();
        
        if (savedModel) {
            const model = this.availableModels.find(m => m.id === savedModel);
            if (model) {
                // Don't auto-load, just show as selected
                ui.updateModelDisplay(model.name, model.desc);
                config.currentModel = model.id;
            }
        } else if (this.availableModels.length > 0) {
            // Show first recommended model as suggestion
            const recommended = this.availableModels.find(m => m.recommended);
            if (recommended) {
                ui.updateModelDisplay(recommended.name + ' (Recommended)', recommended.desc);
            }
        }
    }
    
    openModelSelector() {
        const modalContent = document.querySelector('#modelModal .model-list');
        if (!modalContent) return;
        
        modalContent.innerHTML = '';
        
        this.availableModels.forEach(model => {
            const option = document.createElement('div');
            option.className = 'model-option';
            if (config.currentModel === model.id) {
                option.classList.add('selected');
            }
            
            option.innerHTML = `
                <h4>${model.name} ${model.recommended ? '⭐' : ''}</h4>
                <p>${model.desc}</p>
            `;
            
            option.onclick = () => this.selectModel(model);
            modalContent.appendChild(option);
        });
        
        ui.showModal('modelModal');
    }
    
    closeModelSelector() {
        ui.hideModal('modelModal');
    }
    
    async selectModel(model) {
        this.closeModelSelector();
        
        // Disable input during model download
        ui.setInputEnabled(false);
        ui.showLoadingIndicator('Downloading model...');
        ui.updateModelDisplay('Loading...', 'Preparing to download...');
        
        try {
            if (!window.CreateMLCEngine) {
                throw new Error('WebLLM not loaded');
            }
            
            config.engine = await window.CreateMLCEngine(model.id, {
                initProgressCallback: (progress) => {
                    const progressText = progress.text || 'Downloading...';
                    const percentage = progress.progress ? Math.round(progress.progress * 100) : 0;
                    
                    // Update loading indicator with progress
                    ui.updateLoadingProgress(percentage, progressText);
                    ui.updateModelDisplay('Loading...', progressText);
                }
            });
            
            config.currentModel = model.id;
            storage.saveCurrentModel(model.id);
            
            // Hide loading indicator and enable input
            ui.hideLoadingIndicator();
            ui.updateModelDisplay(model.name, model.desc);
            ui.setInputEnabled(true);
            
            console.log('Model loaded successfully:', model.id);
            ui.showNotification('✅ Model loaded successfully! You can start chatting now.');
            
        } catch (error) {
            console.error('Error loading model:', error);
            ui.hideLoadingIndicator();
            ui.updateModelDisplay('Error', 'Failed to load model');
            ui.setInputEnabled(false);
            ui.showNotification('❌ Failed to load model. Please try again.');
        }
    }
}

export const models = new ModelManager();

