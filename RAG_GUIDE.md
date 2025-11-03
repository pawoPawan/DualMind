# 📚 RAG (Retrieval-Augmented Generation) Guide

## Overview

DualMind AI's Local Mode now includes a **complete RAG (Retrieval-Augmented Generation) system** that runs entirely in your browser. Upload documents and chat with their content using your local LLM - all without any data leaving your device!

## 🌟 Key Features

### ✅ What's Included

1. **📤 File Upload**
   - Support for TXT, MD, PDF, DOC, DOCX files
   - Drag & drop interface (coming soon)
   - Multiple file upload support

2. **🧠 Local Embeddings with Model Selection**
   - Uses Transformers.js for browser-based embeddings
   - **6 embedding models to choose from**:
     - `all-MiniLM-L6-v2` (Default - Fast, 22MB)
     - `all-mpnet-base-v2` (Better Quality, 80MB)
     - `BGE-small-en-v1.5` (Fast, 33MB)
     - `BGE-base-en-v1.5` (High Quality, 109MB)
     - `GTE-small` (Multilingual, 33MB)
     - `E5-small-multilingual` (Multilingual, 118MB)
   - Choose based on your needs (speed vs quality vs language support)

3. **📦 Persistent Storage**
   - IndexedDB for local storage
   - No data uploaded to servers
   - Survives page refreshes

4. **🔍 Semantic Search**
   - Cosine similarity for relevance scoring
   - Smart chunking with overlap
   - Top-K retrieval

5. **💬 Context-Aware Chat**
   - Automatic context injection
   - Visual RAG indicators
   - Streaming responses with document context

6. **📊 Document Management**
   - View uploaded documents
   - Delete individual documents
   - Clear all documents
   - Storage statistics

## 🚀 How It Works

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   User Interface                        │
│  ┌─────────────┐ ┌──────────────┐ ┌──────────────┐     │
│  │Model Select │ │ File Upload  │ │ Document List│     │
│  └─────────────┘ └──────────────┘ └──────────────┘     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Processing Pipeline                         │
│                                                          │
│  1. Text Extraction → 2. Chunking → 3. Embedding        │
│     (FileReader)       (500 chars)    (Transformers.js) │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                 Vector Storage                           │
│                                                          │
│  IndexedDB: {id, filename, chunks[], embeddings[]}      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Query Pipeline                              │
│                                                          │
│  User Query → Embed Query → Semantic Search →           │
│               (Transformers.js) (Cosine Similarity)     │
│               → Retrieve Top-K → Augment Prompt →       │
│                  Context Chunks    (RAG Template)       │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  WebLLM Inference                        │
│                                                          │
│  Augmented Prompt → LLM → Streaming Response            │
└─────────────────────────────────────────────────────────┘
```

### Document Processing Flow

1. **Upload**: User selects files via file picker
2. **Read**: FileReader reads file content as text
3. **Chunk**: Text is split into ~500 character chunks with 50 char overlap
4. **Embed**: Each chunk is embedded using Transformers.js
5. **Store**: Document with chunks and embeddings saved to IndexedDB
6. **Index**: Chunks added to in-memory knowledge base for fast search

### Query Flow

1. **Question**: User asks a question
2. **Embed**: Question is embedded using the same model
3. **Search**: Cosine similarity calculated between question and all chunks
4. **Rank**: Chunks sorted by similarity score
5. **Filter**: Top-K chunks above similarity threshold selected
6. **Augment**: Question augmented with relevant context
7. **Generate**: WebLLM generates answer using augmented prompt
8. **Stream**: Response streamed back with RAG indicator

## 📖 Usage Guide

### Step 1: Access Knowledge Base

1. Open Local Mode: `http://localhost:8000/local`
2. Load your preferred LLM model
3. Click the **"📚 Knowledge Base"** button in the header

### Step 2: Upload Documents

1. Click the **file upload area** or drag files
2. Select one or more supported files (TXT, MD, PDF*, DOC*, DOCX*)
3. Wait for processing (first time will download embedding model ~22MB)
4. See confirmation: "✓ Successfully processed X file(s)!"

*Note: PDF, DOC, DOCX support is basic. For best results, convert to TXT/MD*

### Step 3: View Your Documents

The **"📄 Uploaded Documents"** section shows:
- Document name
- Number of chunks created
- File size
- Upload date
- Delete button

### Step 4: Check Statistics

The stats panel displays:
- **Total Chunks**: Number of text chunks across all documents
- **Embeddings**: Number of vector embeddings stored
- **Storage Used**: IndexedDB storage size

### Step 5: Chat with Your Documents

1. Close the Knowledge Base modal
2. Notice the **"RAG ON"** indicator in the header badge
3. Ask questions about your documents
4. AI responses will include a **"📚 Answer enhanced with your documents"** badge when RAG is used

### Step 6: Manage Documents

- **Delete Individual**: Click "Delete" button on a document
- **Clear All**: Click "🗑️ Clear All Documents" button
- **View Console**: Open browser DevTools to see RAG logs with similarity scores

## 🎯 Best Practices

### Document Preparation

✅ **DO:**
- Use plain text (.txt) or Markdown (.md) for best results
- Keep documents focused and well-structured
- Use clear headings and paragraphs
- Include relevant keywords

❌ **DON'T:**
- Upload extremely large files (>5MB) - browser may slow down
- Use heavily formatted documents (formatting is lost)
- Upload encrypted or password-protected PDFs
- Mix multiple unrelated topics in one file

### Asking Questions

✅ **DO:**
- Ask specific questions about document content
- Use keywords from your documents
- Reference concepts mentioned in uploaded files
- Ask for summaries or explanations

❌ **DON'T:**
- Ask about information not in documents (AI may hallucinate)
- Use very vague or general questions
- Expect perfect accuracy on complex reasoning
- Assume documents are "understood" conceptually

### Performance Tips

1. **Chunk Size**: Default 500 chars works well for most content
2. **Number of Chunks**: System retrieves top 3 most relevant chunks
3. **Similarity Threshold**: 0.3 minimum (adjustable in code)
4. **Model Size**: Embedding model is 22MB (one-time download)
5. **Storage Limit**: IndexedDB typically allows 50-100MB

## 🔧 Technical Details

### Embedding Model

- **Model**: `Xenova/all-MiniLM-L6-v2`
- **Type**: Sentence transformer
- **Dimensions**: 384
- **Size**: ~22MB
- **Library**: Transformers.js (Xenova)
- **CDN**: jsdelivr

### Chunking Algorithm

```javascript
function chunkText(text, chunkSize = 500, overlap = 50) {
    // Split by sentences
    // Combine into ~500 char chunks
    // Keep ~50 char overlap between chunks
    // Return array of chunks
}
```

### Similarity Calculation

```javascript
function cosineSimilarity(vecA, vecB) {
    // Dot product of normalized vectors
    // Returns score between -1 and 1
    // Higher = more similar
}
```

### Storage Schema

```javascript
{
    id: 1,                    // Auto-increment
    filename: "doc.txt",      // Original filename
    uploadDate: "2025-10-15", // ISO timestamp
    size: 12345,              // Bytes
    chunks: [
        {
            text: "...",           // Chunk text
            embedding: [...],      // 384-dim vector
            chunkIndex: 0          // Position in doc
        }
    ],
    totalChunks: 5
}
```

### RAG Prompt Template

```javascript
`Context from uploaded documents:

[Document: filename.txt]
<relevant chunk 1>

---

[Document: filename.txt]
<relevant chunk 2>

---

User question: ${question}

Please answer the question based on the context provided above.
If the context doesn't contain relevant information, say so and
provide a general answer.`
```

## 🎨 UI Components

### Knowledge Base Button
- Location: Chat header
- Icon: 📚
- Tooltip: "Upload documents for RAG"

### RAG ON Badge
- Location: Mode badge in header
- Appears when documents are loaded
- Color: Green (#4CAF50)

### Document Enhancement Badge
- Location: Below AI messages
- Text: "📚 Answer enhanced with your documents"
- Shows when RAG context was used

### Upload Status
- Shows processing progress
- Displays errors if any
- Auto-hides after 2-3 seconds

## 🔍 Troubleshooting

### Problem: "Failed to load embedding model"

**Causes:**
- No internet connection (model downloaded from CDN)
- CDN unavailable
- Browser blocking external scripts

**Solutions:**
- Check internet connection
- Try different browser
- Disable content blockers
- Check browser console for details

### Problem: No RAG indicator appears

**Causes:**
- No documents uploaded
- Question not similar enough to document content (similarity < 0.3)
- Embeddings not generated

**Solutions:**
- Upload relevant documents
- Ask more specific questions with document keywords
- Check console for similarity scores
- Lower threshold in code if needed

### Problem: Slow performance

**Causes:**
- Too many/large documents
- Weak device
- Browser memory pressure

**Solutions:**
- Delete unused documents
- Upload smaller files
- Close other browser tabs
- Use fewer chunks or smaller LLM model

### Problem: Inaccurate answers

**Causes:**
- Irrelevant chunks retrieved
- LLM misinterpreting context
- Insufficient context

**Solutions:**
- Rephrase question
- Check retrieved chunks in console
- Increase top-K value in code
- Use better-structured documents

### Problem: Storage quota exceeded

**Causes:**
- Too many documents stored
- Browser storage limit reached

**Solutions:**
- Clear old documents
- Clear all documents and re-upload essentials
- Use browser's IndexedDB manager to check size
- Consider external storage for large knowledge bases

## 📊 Console Debugging

Open browser DevTools (F12) to see:

```javascript
// On upload
Loading embedding model...
Embedding model loaded successfully
Processing file.txt (1/3)...

// On page load
Loaded 45 chunks from 3 documents

// On query
RAG: Using context from 3 relevant chunks
Similarity scores: ['0.782', '0.654', '0.512']
```

## 🔐 Privacy & Security

### ✅ Privacy Features

- **100% Local**: All processing happens in browser
- **No Upload**: Documents never sent to servers
- **No Tracking**: No analytics or telemetry
- **Persistent**: Data stays in browser's IndexedDB
- **Deletable**: Full control to delete any/all data

### 🔒 Security Considerations

- Files are read as plain text (sanitized)
- No code execution from uploaded content
- IndexedDB isolated to origin
- No external API calls for inference
- Embeddings generated locally

### 🚨 Limitations

- Not suitable for sensitive/classified documents in shared computers
- Browser cache/IndexedDB can be inspected by advanced users
- Incognito mode will clear data on close
- Exporting/backing up documents requires manual copy

## 🎓 Advanced Usage

### Adjusting Similarity Threshold

Edit `index_local.html`:
```javascript
// Lower = more permissive (may include less relevant context)
// Higher = more strict (may miss relevant context)
if (relevantChunks.length > 0 && relevantChunks[0].similarity > 0.3) {
    // Change 0.3 to your preferred threshold (0-1)
}
```

### Changing Number of Retrieved Chunks

```javascript
const relevantChunks = await searchKnowledgeBase(message, 3);
// Change 3 to retrieve more/fewer chunks
```

### Modifying Chunk Size

```javascript
const chunks = chunkText(text, 500, 50);
// chunkSize: 500 characters
// overlap: 50 characters
```

### Choosing Embedding Models

DualMind Local Mode now supports **6 embedding models**. Choose based on your needs:

**For Speed (Quick Responses):**
- `Xenova/all-MiniLM-L6-v2` (default, 22MB) - Best for testing and quick responses
- `Xenova/bge-small-en-v1.5` (33MB) - Slightly better quality

**For Quality (Better Accuracy):**
- `Xenova/all-mpnet-base-v2` (80MB) - Excellent quality for English
- `Xenova/bge-base-en-v1.5` (109MB) - Highest quality for English

**For Multilingual Documents:**
- `Xenova/gte-small` (33MB) - Good for multiple languages
- `Xenova/multilingual-e5-small` (118MB) - Best multilingual support

**How to Select:**
1. Open Knowledge Base modal
2. Choose embedding model from dropdown (before uploading)
3. Model downloads once and is cached
4. Upload your documents

**Note:** Changing models requires re-uploading documents (embeddings are model-specific)

## 📚 Resources

### Documentation
- [Transformers.js Docs](https://huggingface.co/docs/transformers.js)
- [IndexedDB API](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)
- [WebLLM Documentation](https://github.com/mlc-ai/web-llm)

### Models
- [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Xenova Models](https://huggingface.co/Xenova)

### Concepts
- [RAG Explained](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
- [Semantic Search](https://en.wikipedia.org/wiki/Semantic_search)
- [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity)

## 🚀 Future Enhancements

### Planned Features
- [ ] Drag & drop file upload
- [ ] Full PDF parsing support
- [ ] Document preview
- [ ] Export/Import knowledge base
- [ ] Custom chunk size in UI
- [ ] Relevance score display
- [ ] Multi-language support
- [ ] Image OCR support
- [ ] Code file syntax awareness
- [ ] Document search/filter

### Experimental
- [ ] Hybrid search (keyword + semantic)
- [ ] Document summarization
- [ ] Automatic question generation
- [ ] Cross-document reasoning
- [ ] Knowledge graph visualization

## 💬 Feedback

Found a bug or have a suggestion? The RAG system is experimental and we'd love your feedback!

---

**🧠 DualMind AI** - Your documents, your privacy, your AI

