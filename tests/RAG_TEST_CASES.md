# Per-Chat RAG Test Cases

## Overview

Comprehensive test cases for per-chat document management, ensuring:
1. ✅ Document isolation between chats
2. ✅ Proper deletion of chat-specific documents
3. ✅ New chats don't show documents from other chats

## Test Files Created

### 1. `tests/integration/test_per_chat_rag.py`
Integration tests for document management logic

### 2. `tests/ui/test_per_chat_rag_ui.py`
UI/manual tests for user interface behavior

## Integration Tests (8 Test Cases)

### Test Case 1: Create Multiple Chats with Documents
**Scenario:**
```
1. Create Chat A with 2 documents (pricing.txt, guide.md)
2. Create Chat B with 1 document (terms.txt)
3. Create Chat C with 1 document (notes.txt)
```

**Expected Results:**
- ✅ Each chat has its own isolated documents
- ✅ Documents stored with chat ID as key
- ✅ No cross-contamination between chats

**Verification:**
```javascript
localStorage["dualmind_chat_documents"] = {
  "1730678400000": [pricing.txt, guide.md],  // Chat A
  "1730678500000": [terms.txt],              // Chat B
  "1730678600000": [notes.txt]               // Chat C
}
```

---

### Test Case 2: Document Isolation Between Chats
**Scenario:**
```
1. Create Chat A with pricing.txt
2. Create Chat B with terms.txt
3. Load Chat A documents → Verify only pricing.txt
4. Load Chat B documents → Verify only terms.txt
```

**Expected Results:**
- ✅ Chat A shows ONLY pricing.txt
- ✅ Chat B shows ONLY terms.txt
- ✅ No cross-chat document visibility

**Code Verification:**
```javascript
// Load Chat A
chatA_docs = getChatDocuments(chatA_id);
assert chatA_docs.length === 1;
assert chatA_docs[0].name === 'pricing.txt';
assert !chatA_docs.find(doc => doc.name === 'terms.txt');

// Load Chat B
chatB_docs = getChatDocuments(chatB_id);
assert chatB_docs.length === 1;
assert chatB_docs[0].name === 'terms.txt';
assert !chatB_docs.find(doc => doc.name === 'pricing.txt');
```

---

### Test Case 3: Delete Chat Removes ONLY Its Documents ⭐
**Scenario:**
```
1. Create Chat A with 2 documents
2. Create Chat B with 1 document  
3. Create Chat C with 1 document
4. DELETE Chat B
5. Verify Chat B documents removed
6. Verify Chat A documents intact
7. Verify Chat C documents intact
```

**Expected Results:**
- ✅ Chat B completely removed
- ✅ Chat A still has 2 documents
- ✅ Chat C still has 1 document
- ✅ Storage has only Chat A and Chat C

**Storage Before Deletion:**
```javascript
{
  "chatA": [doc1, doc2],  // 2 docs
  "chatB": [doc3],        // 1 doc ← TO BE DELETED
  "chatC": [doc4]         // 1 doc
}
```

**Storage After Deletion:**
```javascript
{
  "chatA": [doc1, doc2],  // 2 docs ✅ INTACT
  // "chatB" REMOVED ✅
  "chatC": [doc4]         // 1 doc ✅ INTACT
}
```

---

### Test Case 4: New Chat Has NO Documents from Other Chats ⭐
**Scenario:**
```
1. Create Chat A with 2 documents
2. Create Chat B with 1 document
3. Create NEW Chat D (empty)
4. Verify Chat D has NO documents
5. Verify Chat D doesn't see Chat A or B documents
```

**Expected Results:**
- ✅ New Chat D starts with 0 documents
- ✅ Chat D has no access to other chats' documents
- ✅ Chat A and B documents remain untouched

**Verification:**
```javascript
// Create new chat
newChatId = Date.now();
newChatDocs = getChatDocuments(newChatId);

// Verify empty
assert newChatDocs.length === 0;
assert !newChatDocs.find(doc => doc.name === 'pricing.txt');
assert !newChatDocs.find(doc => doc.name === 'guide.md');
assert !newChatDocs.find(doc => doc.name === 'terms.txt');

// Verify other chats unchanged
assert getChatDocuments(chatA_id).length === 2;
assert getChatDocuments(chatB_id).length === 1;
```

---

### Test Case 5: Switch Between Chats Loads Correct Documents
**Scenario:**
```
1. Create Chat A with pricing.txt
2. Create Chat B with terms.txt
3. Create Chat C with notes.txt
4. Load Chat A → Verify only pricing.txt
5. Load Chat B → Verify only terms.txt
6. Load Chat A again → Verify pricing.txt still there
7. Load Chat C → Verify only notes.txt
```

**Expected Results:**
- ✅ Each switch loads correct documents
- ✅ Documents persist when returning
- ✅ No document leakage

**Test Flow:**
```
Load Chat A → [pricing.txt] ✅
Switch to Chat B → [terms.txt] ✅ (no pricing.txt)
Switch to Chat A → [pricing.txt] ✅ (restored)
Switch to Chat C → [notes.txt] ✅ (no pricing, no terms)
```

---

### Test Case 6: Clear All Chats Removes ALL Documents
**Scenario:**
```
1. Create Chat A with 2 documents
2. Create Chat B with 1 document
3. Create Chat C with 1 document
4. CLEAR ALL CHATS
5. Verify all chats removed
6. Verify all documents removed
```

**Expected Results:**
- ✅ All chats removed
- ✅ All documents removed (4 total)
- ✅ Storage completely empty

**Before:**
```javascript
dualmind_chat_documents = {
  "chatA": [doc1, doc2],
  "chatB": [doc3],
  "chatC": [doc4]
}
// Total: 4 documents
```

**After:**
```javascript
dualmind_chat_documents = {}
// Total: 0 documents ✅
```

---

### Test Case 7: Delete Currently Active Chat
**Scenario:**
```
1. Create Chat A with documents
2. Create Chat B with documents
3. Set Chat A as ACTIVE (current chat)
4. DELETE Chat A (the active chat)
5. Verify Chat A deleted
6. Verify system switches to new/other chat
7. Verify new chat has correct documents
```

**Expected Results:**
- ✅ Active chat can be deleted
- ✅ System handles gracefully
- ✅ User moved to another chat
- ✅ No crashes or errors

---

### Test Case 8: RAG Search Only Searches Current Chat
**Scenario:**
```
1. Chat A has pricing.txt with "$99/month"
2. Chat B has terms.txt (no pricing info)
3. In Chat A: Search for "pricing"
4. Verify only pricing.txt searched
5. In Chat B: Search for "pricing"
6. Verify no results (pricing.txt not available)
```

**Expected Results:**
- ✅ RAG only searches current chat's documents
- ✅ No cross-chat document search
- ✅ Results are chat-specific

---

## UI Manual Test Cases (6 Test Cases)

### Test Case UI-1: Knowledge Base Shows Only Current Chat Documents
**Steps:**
```
1. Open http://localhost:8000/local
2. Create Chat A, upload pricing.txt
3. Open Knowledge Base (📎 button)
   ✅ Verify: Only pricing.txt visible
4. Create Chat B (New Chat)
5. Open Knowledge Base
   ✅ Verify: Empty (no documents)
6. Upload terms.txt to Chat B
7. Open Knowledge Base
   ✅ Verify: Only terms.txt visible (NOT pricing.txt)
8. Switch to Chat A
9. Open Knowledge Base
   ✅ Verify: Only pricing.txt visible (NOT terms.txt)
```

---

### Test Case UI-2: Delete Confirmation Shows Document Count
**Steps:**
```
1. Create Chat A with 3 documents
2. Click delete (🗑️) on Chat A
   ✅ Verify: "This will also delete 3 associated document(s)"
3. Cancel deletion
   ✅ Verify: Chat A still exists
4. Delete Chat A and confirm
   ✅ Verify: Chat A removed
   ✅ Console: "Deleted chat ... with 3 document(s)"
5. Create Chat B (no documents)
6. Click delete on Chat B
   ✅ Verify: Normal confirmation (no document count)
```

---

### Test Case UI-3: Document Upload Shows Chat Link
**Steps:**
```
1. Create Chat A
2. Upload a document
   ✅ Verify progress: "📚 Initializing..."
   ✅ Verify progress: "🔄 Loading embedding model..."
   ✅ Verify progress: "🧮 Indexing: X/Y chunks..."
   ✅ Verify success: "💬 Documents linked to this chat"
3. Create Chat B, upload another document
   ✅ Verify: Same progress + "linked to this chat"
4. Switch to Chat A
   ✅ Verify: Only Chat A's document visible
   ✅ Console: "📚 RAG: Loaded 1 documents for chat [ID]"
```

---

### Test Case UI-4: RAG Indicators Show Correct Documents
**Steps:**
```
1. Create Chat A, upload pricing.txt
   Content: "Our pricing starts at $99/month"
2. Ask: "What are your prices?"
   ✅ Verify: "🔍 Searching knowledge base..."
   ✅ Verify: "📚 Found relevant information..."
   ✅ Console: "RAG: Using 3 relevant chunks"
   ✅ Console: "1. pricing.txt (similarity: 0.872)"
   ✅ Verify answer: Mentions "$99/month"
3. Create Chat B (no documents)
4. Ask: "What are your prices?"
   ✅ Verify: "🔍 Searching..."
   ✅ Console: "RAG: No relevant chunks found"
   ✅ Verify answer: Generic (no pricing info)
```

---

### Test Case UI-5: Clear All Chats Removes All Documents
**Steps:**
```
1. Create Chat A: pricing.txt, guide.md
2. Create Chat B: terms.txt
3. Create Chat C: notes.txt
4. Settings → "Clear All Chats"
   ✅ Verify warning: "This will also delete all associated documents"
5. Confirm
   ✅ Verify: All chats removed
   ✅ Verify: New empty chat created
   ✅ Verify: Knowledge Base is empty
   ✅ DevTools: dualmind_chat_documents = {}
```

---

### Test Case UI-6: Knowledge Base Statistics Per Chat
**Steps:**
```
1. Create Chat A, upload 2 documents
2. Open Knowledge Base
   ✅ Verify: "📊 2 document(s) | X chunks | Y words"
3. Create Chat B, upload 1 document
4. Open Knowledge Base
   ✅ Verify: "📊 1 document(s) | X chunks | Y words"
5. Switch to Chat A
   ✅ Verify: "📊 2 document(s) | X chunks | Y words"
```

---

## Running the Tests

### Integration Tests
```bash
cd /Users/pawkumar/Documents/pawan/DualMind
python3 tests/integration/test_per_chat_rag.py
```

### UI Tests (Manual)
```bash
# Start server
./dualmind.sh start

# Open browser
open http://localhost:8000/local

# Follow test steps in:
python3 tests/ui/test_per_chat_rag_ui.py
```

---

## Test Coverage Summary

| Category | Test Count | Status |
|----------|-----------|--------|
| **Integration Tests** | 8 | ✅ Automated |
| **UI Tests** | 6 | 📝 Manual |
| **Total** | **14** | ✅ Complete |

### Coverage Areas:
- ✅ Document isolation
- ✅ Chat deletion with cleanup
- ✅ New chat initialization
- ✅ Chat switching
- ✅ RAG search boundaries
- ✅ Clear all chats
- ✅ Active chat deletion
- ✅ UI feedback and indicators
- ✅ Progress tracking
- ✅ Statistics display

---

## Success Criteria

### All Tests Must Pass:
1. ✅ Create multiple chats with documents
2. ✅ Documents isolated per chat
3. ✅ Delete chat removes ONLY its documents
4. ✅ New chat has NO documents from other chats
5. ✅ Switch between chats loads correct documents
6. ✅ Clear all removes everything
7. ✅ Active chat deletion handled
8. ✅ RAG searches only current chat
9. ✅ UI shows correct documents
10. ✅ Delete confirmations accurate
11. ✅ Upload progress clear
12. ✅ RAG indicators correct
13. ✅ Statistics accurate
14. ✅ No cross-chat pollution

---

## Test Execution Results

Run tests and document results:

```bash
# Run integration tests
$ python3 tests/integration/test_per_chat_rag.py

Expected Output:
======================================================================
🧪 RUNNING PER-CHAT RAG INTEGRATION TESTS
======================================================================

✅ Test 1 Passed: Multiple chats created with isolated documents
✅ Test 2 Passed: Document isolation verified between chats
✅ Test 3 Passed: Only deleted chat's documents removed, others intact
✅ Test 4 Passed: New chat has no documents from other chats
✅ Test 5 Passed: Switching between chats loads correct documents
✅ Test 6 Passed: Clear all chats removes all documents
✅ Test 7 Passed: Deleting active chat handled correctly
✅ Test 8 Passed: RAG search respects per-chat boundaries

======================================================================
✅ ALL TESTS PASSED!
======================================================================
```

---

## Troubleshooting

### If Tests Fail:

**Document Isolation Issues:**
- Check `storage.js` → `getChatDocuments(chatId)`
- Verify chat ID is passed correctly
- Check `rag.js` → `setCurrentChat(chatId)`

**Deletion Issues:**
- Check `storage.js` → `deleteConversation(id)`
- Verify `clearChatDocuments(id)` is called
- Check localStorage directly in DevTools

**RAG Search Issues:**
- Check `rag.js` → `searchRelevantChunks()`
- Verify it uses `this.knowledgeBase` (current chat's docs)
- Check console logs for RAG behavior

---

## Documentation

- `PER_CHAT_DOCUMENTS.md` - Implementation guide
- `CHAT_DELETION_WITH_DOCUMENTS.md` - Deletion behavior
- `SESSION_SUMMARY.md` - Complete feature overview
- `RAG_TEST_CASES.md` - This file

---

**Status**: ✅ All test cases documented and ready for execution!

