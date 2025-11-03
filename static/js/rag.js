/**
 * DualMind RAG Module
 * Handles knowledge base and document processing
 */

import { ui } from './ui.js';
import { storage } from './storage.js';
import { config } from './config.js';

export class RAGManager {
    constructor() {
        this.knowledgeBase = [];
        this.embeddingModels = [];
        this.currentEmbeddingModel = 'Xenova/all-MiniLM-L6-v2';
    }
    
    async initialize() {
        this.knowledgeBase = storage.getKnowledgeBase();
        this.currentEmbeddingModel = storage.getEmbeddingModel();
        await this.loadAvailableModels();
    }
    
    async loadAvailableModels() {
        try {
            const response = await fetch('/api/local/embedding-models');
            const data = await response.json();
            this.embeddingModels = data.models || [];
        } catch (error) {
            console.error('Error loading embedding models:', error);
        }
    }
    
    openKnowledgeBase() {
        this.displayUploadedFiles();
        ui.showModal('knowledgeModal');
    }
    
    closeKnowledgeBase() {
        ui.hideModal('knowledgeModal');
    }
    
    async handleFileUpload(event) {
        const files = event.target.files;
        if (!files || files.length === 0) return;
        
        for (const file of files) {
            try {
                const text = await file.text();
                this.knowledgeBase.push({
                    name: file.name,
                    content: text,
                    timestamp: Date.now()
                });
            } catch (error) {
                console.error('Error reading file:', error);
                ui.showNotification(`Error reading ${file.name}`);
            }
        }
        
        storage.saveKnowledgeBase(this.knowledgeBase);
        this.displayUploadedFiles();
        ui.showNotification(`${files.length} file(s) uploaded successfully`);
    }
    
    displayUploadedFiles() {
        const container = document.getElementById('uploadedFiles');
        if (!container) return;
        
        container.innerHTML = '';
        
        if (this.knowledgeBase.length === 0) {
            container.innerHTML = '<p style="color: #888; text-align: center;">No documents uploaded yet</p>';
            return;
        }
        
        this.knowledgeBase.forEach((file, index) => {
            const fileDiv = document.createElement('div');
            fileDiv.className = 'chat-item';
            fileDiv.style.display = 'flex';
            fileDiv.style.justifyContent = 'space-between';
            fileDiv.style.alignItems = 'center';
            
            fileDiv.innerHTML = `
                <span>📄 ${file.name}</span>
                <button class="action-btn" onclick="window.dualmind.removeDocument(${index})" style="background: #f44;">✕</button>
            `;
            
            container.appendChild(fileDiv);
        });
    }
    
    removeDocument(index) {
        if (confirm('Remove this document?')) {
            this.knowledgeBase.splice(index, 1);
            storage.saveKnowledgeBase(this.knowledgeBase);
            this.displayUploadedFiles();
        }
    }
    
    clearAllDocuments() {
        if (confirm('Clear all documents?')) {
            this.knowledgeBase = [];
            storage.saveKnowledgeBase(this.knowledgeBase);
            this.displayUploadedFiles();
        }
    }
}

export const rag = new RAGManager();

