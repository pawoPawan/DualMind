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
        this.embedder = null;
        this.isEmbedderLoaded = false;
    }
    
    async initialize() {
        this.knowledgeBase = storage.getKnowledgeBase();
        this.currentEmbeddingModel = storage.getEmbeddingModel();
        await this.loadAvailableModels();
        // Don't load embedder until needed to save resources
    }
    
    async loadEmbedder() {
        if (this.isEmbedderLoaded) return;
        
        try {
            console.log('🔄 Loading embedding model...');
            const { pipeline } = window.transformers;
            this.embedder = await pipeline('feature-extraction', this.currentEmbeddingModel);
            this.isEmbedderLoaded = true;
            console.log('✅ Embedding model loaded!');
        } catch (error) {
            console.error('Error loading embedder:', error);
            throw error;
        }
    }
    
    async embed(text) {
        if (!this.isEmbedderLoaded) {
            await this.loadEmbedder();
        }
        
        try {
            const output = await this.embedder(text, { pooling: 'mean', normalize: true });
            return Array.from(output.data);
        } catch (error) {
            console.error('Error generating embedding:', error);
            return null;
        }
    }
    
    cosineSimilarity(a, b) {
        const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
        const magnitudeA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
        const magnitudeB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));
        return dotProduct / (magnitudeA * magnitudeB);
    }
    
    chunkText(text, chunkSize = 500, overlap = 100) {
        const chunks = [];
        let start = 0;
        
        while (start < text.length) {
            const end = Math.min(start + chunkSize, text.length);
            chunks.push(text.substring(start, end));
            start += chunkSize - overlap;
        }
        
        return chunks;
    }
    
    async searchRelevantChunks(query, topK = 3) {
        if (this.knowledgeBase.length === 0) {
            return [];
        }
        
        try {
            // Embed the query
            const queryEmbedding = await this.embed(query);
            if (!queryEmbedding) return [];
            
            // Calculate similarities with all chunks
            const results = [];
            
            for (const doc of this.knowledgeBase) {
                if (doc.embeddings && doc.chunks) {
                    for (let i = 0; i < doc.chunks.length; i++) {
                        const similarity = this.cosineSimilarity(queryEmbedding, doc.embeddings[i]);
                        results.push({
                            text: doc.chunks[i],
                            similarity: similarity,
                            filename: doc.name
                        });
                    }
                }
            }
            
            // Sort by similarity and return top K
            results.sort((a, b) => b.similarity - a.similarity);
            return results.slice(0, topK);
            
        } catch (error) {
            console.error('Error searching chunks:', error);
            return [];
        }
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
        
        ui.showLoadingIndicator('Processing documents...');
        
        try {
            // Ensure embedder is loaded
            await this.loadEmbedder();
            
            for (const file of files) {
                try {
                    ui.updateLoadingProgress(0, `Processing ${file.name}...`);
                    
                    const text = await file.text();
                    
                    // Split into chunks
                    ui.updateLoadingProgress(30, `Chunking ${file.name}...`);
                    const chunks = this.chunkText(text);
                    
                    // Generate embeddings for all chunks
                    ui.updateLoadingProgress(50, `Generating embeddings for ${file.name}...`);
                    const embeddings = [];
                    
                    for (let i = 0; i < chunks.length; i++) {
                        const embedding = await this.embed(chunks[i]);
                        if (embedding) {
                            embeddings.push(embedding);
                        }
                        
                        // Update progress
                        const progress = 50 + (i / chunks.length) * 40;
                        ui.updateLoadingProgress(progress, `Embedding chunk ${i + 1}/${chunks.length}...`);
                    }
                    
                    this.knowledgeBase.push({
                        name: file.name,
                        content: text,
                        chunks: chunks,
                        embeddings: embeddings,
                        timestamp: Date.now()
                    });
                    
                    ui.updateLoadingProgress(100, `${file.name} processed!`);
                    
                } catch (error) {
                    console.error('Error processing file:', error);
                    alert(`Error processing ${file.name}: ${error.message}`);
                }
            }
            
            storage.saveKnowledgeBase(this.knowledgeBase);
            this.displayUploadedFiles();
            alert(`✅ ${files.length} file(s) processed successfully!`);
            
        } catch (error) {
            console.error('Error uploading files:', error);
            alert(`Error: ${error.message}`);
        } finally {
            ui.hideLoadingIndicator();
        }
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

