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
        this.currentChatId = null; // Track current chat
    }
    
    async initialize() {
        // Don't load any documents on init - wait for chat to be set
        this.currentEmbeddingModel = storage.getEmbeddingModel();
        await this.loadAvailableModels();
        // Don't load embedder until needed to save resources
    }
    
    // Set current chat and load its documents
    setCurrentChat(chatId) {
        this.currentChatId = chatId;
        this.knowledgeBase = chatId ? storage.getChatDocuments(chatId) : [];
        console.log(`📚 RAG: Loaded ${this.knowledgeBase.length} documents for chat ${chatId}`);
    }
    
    // Get current chat's documents
    getCurrentDocuments() {
        return this.knowledgeBase;
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
        
        ui.showLoadingIndicator('📚 Initializing document processing...');
        
        try {
            // Ensure embedder is loaded first
            ui.updateLoadingProgress(5, '🔄 Loading embedding model...');
            await this.loadEmbedder();
            ui.updateLoadingProgress(10, '✅ Embedding model ready!');
            
            let totalChunks = 0;
            let processedChunks = 0;
            
            for (let fileIndex = 0; fileIndex < files.length; fileIndex++) {
                const file = files[fileIndex];
                try {
                    const fileProgress = (fileIndex / files.length) * 100;
                    
                    ui.updateLoadingProgress(
                        fileProgress, 
                        `📄 Reading ${file.name} (${fileIndex + 1}/${files.length})...`
                    );
                    
                    const text = await file.text();
                    const wordCount = text.split(/\s+/).length;
                    
                    // Split into chunks
                    ui.updateLoadingProgress(
                        fileProgress + 10, 
                        `✂️ Splitting ${file.name} into chunks (${wordCount} words)...`
                    );
                    const chunks = this.chunkText(text);
                    totalChunks += chunks.length;
                    
                    console.log(`📊 ${file.name}: ${chunks.length} chunks created`);
                    
                    // Generate embeddings for all chunks
                    ui.updateLoadingProgress(
                        fileProgress + 20, 
                        `🧮 Indexing ${file.name} (0/${chunks.length} chunks)...`
                    );
                    const embeddings = [];
                    
                    for (let i = 0; i < chunks.length; i++) {
                        const embedding = await this.embed(chunks[i]);
                        if (embedding) {
                            embeddings.push(embedding);
                            processedChunks++;
                        }
                        
                        // Update progress with detailed info
                        const chunkProgress = fileProgress + 20 + ((i + 1) / chunks.length) * 60;
                        ui.updateLoadingProgress(
                            chunkProgress, 
                            `🧮 Indexing ${file.name}: ${i + 1}/${chunks.length} chunks embedded (${Math.round((i + 1) / chunks.length * 100)}%)`
                        );
                    }
                    
                    // Store indexed document
                    this.knowledgeBase.push({
                        name: file.name,
                        content: text,
                        chunks: chunks,
                        embeddings: embeddings,
                        timestamp: Date.now(),
                        wordCount: wordCount,
                        chunkCount: chunks.length
                    });
                    
                    ui.updateLoadingProgress(
                        fileProgress + 80, 
                        `✅ ${file.name} indexed: ${chunks.length} chunks, ${wordCount} words`
                    );
                    
                    console.log(`✅ Successfully indexed: ${file.name}`);
                    
                } catch (error) {
                    console.error('Error processing file:', error);
                    ui.showNotification(`❌ Error processing ${file.name}: ${error.message}`);
                }
            }
            
            // Save documents to current chat
            if (this.currentChatId) {
                storage.saveChatDocuments(this.currentChatId, this.knowledgeBase);
                console.log(`💾 Saved ${this.knowledgeBase.length} documents to chat ${this.currentChatId}`);
            }
            
            this.displayUploadedFiles();
            
            ui.updateLoadingProgress(100, '🎉 All documents indexed!');
            
            // Show success summary
            setTimeout(() => {
                ui.showNotification(
                    `✅ Successfully indexed ${files.length} document(s)\n` +
                    `📊 Total: ${processedChunks} chunks from ${totalChunks} segments\n` +
                    `🔍 Ready for semantic search!\n` +
                    `💬 Documents linked to this chat`
                );
            }, 500);
            
        } catch (error) {
            console.error('Error uploading files:', error);
            ui.showNotification(`❌ Error: ${error.message}`);
        } finally {
            setTimeout(() => {
                ui.hideLoadingIndicator();
            }, 1500);
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
        
        // Add summary header
        const totalChunks = this.knowledgeBase.reduce((sum, doc) => sum + (doc.chunkCount || doc.chunks?.length || 0), 0);
        const totalWords = this.knowledgeBase.reduce((sum, doc) => sum + (doc.wordCount || 0), 0);
        
        const summaryDiv = document.createElement('div');
        summaryDiv.style.cssText = 'padding: 10px; margin-bottom: 10px; background: rgba(0,123,255,0.1); border-radius: 8px; font-size: 0.9em;';
        summaryDiv.innerHTML = `
            <strong>📊 Knowledge Base Summary:</strong><br>
            📄 ${this.knowledgeBase.length} document(s) | 
            🧩 ${totalChunks} chunks | 
            📝 ${totalWords.toLocaleString()} words
        `;
        container.appendChild(summaryDiv);
        
        // Display individual files
        this.knowledgeBase.forEach((file, index) => {
            const fileDiv = document.createElement('div');
            fileDiv.className = 'chat-item';
            fileDiv.style.cssText = 'display: flex; flex-direction: column; gap: 5px; padding: 10px;';
            
            fileDiv.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 500;">📄 ${file.name}</span>
                    <button class="action-btn" onclick="window.dualmind.removeDocument(${index})" 
                            style="background: #f44;" title="Remove document">✕</button>
                </div>
                <div style="font-size: 0.85em; color: #888;">
                    🧩 ${file.chunkCount || file.chunks?.length || 0} chunks | 
                    📝 ${(file.wordCount || 0).toLocaleString()} words |
                    ⏰ ${new Date(file.timestamp).toLocaleString()}
                </div>
            `;
            
            container.appendChild(fileDiv);
        });
    }
    
    removeDocument(index) {
        if (confirm('Remove this document from this chat?')) {
            this.knowledgeBase.splice(index, 1);
            if (this.currentChatId) {
                storage.saveChatDocuments(this.currentChatId, this.knowledgeBase);
            }
            this.displayUploadedFiles();
            console.log(`🗑️ Removed document from chat ${this.currentChatId}`);
        }
    }
    
    clearAllDocuments() {
        if (confirm('Clear all documents from this chat?')) {
            this.knowledgeBase = [];
            if (this.currentChatId) {
                storage.saveChatDocuments(this.currentChatId, this.knowledgeBase);
            }
            this.displayUploadedFiles();
            console.log(`🗑️ Cleared all documents from chat ${this.currentChatId}`);
        }
    }
}

export const rag = new RAGManager();

