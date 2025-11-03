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
        this.availableModels = config.getModels();
        const savedModel = storage.getCurrentModel();
        
        if (savedModel) {
            const model = this.availableModels.find(m => m.id === savedModel);
            if (model) {
                // Don't auto-load, just show as selected
                ui.updateModelDisplay(model.name, model.desc);
                config.currentModel = model.id;
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
        
        ui.updateModelDisplay('Loading...', 'Downloading model...');
        
        try {
            if (!window.CreateMLCEngine) {
                throw new Error('WebLLM not loaded');
            }
            
            config.engine = await window.CreateMLCEngine(model.id, {
                initProgressCallback: (progress) => {
                    ui.updateModelDisplay('Loading...', progress.text || 'Downloading...');
                }
            });
            
            config.currentModel = model.id;
            storage.saveCurrentModel(model.id);
            
            ui.updateModelDisplay(model.name, model.desc);
            ui.setInputEnabled(true);
            
            console.log('Model loaded successfully:', model.id);
            
        } catch (error) {
            console.error('Error loading model:', error);
            ui.updateModelDisplay('Error', 'Failed to load model');
            ui.showNotification('Failed to load model. Please try again.');
        }
    }
}

export const models = new ModelManager();

