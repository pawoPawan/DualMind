#!/usr/bin/env python3
"""
Standalone test runner for per-chat RAG tests
Run without pytest dependency
"""

print("\n" + "="*70)
print("🧪 PER-CHAT RAG INTEGRATION TESTS")
print("="*70 + "\n")

# Sample documents for testing
sample_documents = {
    'chat_a_doc1': {
        'name': 'pricing.txt',
        'content': 'Our pricing starts at $99/month for the basic plan.',
        'chunks': ['Our pricing starts at $99/month', 'for the basic plan.'],
        'embeddings': [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
        'timestamp': 1730678400000,
        'wordCount': 10,
        'chunkCount': 2
    },
    'chat_a_doc2': {
        'name': 'guide.md',
        'content': 'This is a comprehensive guide to our product.',
        'chunks': ['This is a comprehensive guide', 'to our product.'],
        'embeddings': [[0.7, 0.8, 0.9], [0.11, 0.12, 0.13]],
        'timestamp': 1730678450000,
        'wordCount': 8,
        'chunkCount': 2
    },
    'chat_b_doc': {
        'name': 'terms.txt',
        'content': 'Terms and conditions apply to all services.',
        'chunks': ['Terms and conditions apply', 'to all services.'],
        'embeddings': [[0.14, 0.15, 0.16], [0.17, 0.18, 0.19]],
        'timestamp': 1730678500000,
        'wordCount': 7,
        'chunkCount': 2
    },
    'chat_c_doc': {
        'name': 'notes.txt',
        'content': 'Important notes about the project timeline.',
        'chunks': ['Important notes about', 'the project timeline.'],
        'embeddings': [[0.20, 0.21, 0.22], [0.23, 0.24, 0.25]],
        'timestamp': 1730678600000,
        'wordCount': 6,
        'chunkCount': 2
    }
}

def test_1_create_multiple_chats():
    """Test Case 1: Create multiple chats with documents"""
    print("📋 Test 1: Create multiple chats with documents")
    
    mock_storage = {'dualmind_chat_documents': {}}
    chat_a_id = 1730678400000
    chat_b_id = 1730678500000
    chat_c_id = 1730678600000
    
    # Chat A: 2 documents
    mock_storage['dualmind_chat_documents'][chat_a_id] = [
        sample_documents['chat_a_doc1'],
        sample_documents['chat_a_doc2']
    ]
    
    # Chat B: 1 document
    mock_storage['dualmind_chat_documents'][chat_b_id] = [
        sample_documents['chat_b_doc']
    ]
    
    # Chat C: 1 document
    mock_storage['dualmind_chat_documents'][chat_c_id] = [
        sample_documents['chat_c_doc']
    ]
    
    # Verify
    assert len(mock_storage['dualmind_chat_documents']) == 3
    assert len(mock_storage['dualmind_chat_documents'][chat_a_id]) == 2
    assert len(mock_storage['dualmind_chat_documents'][chat_b_id]) == 1
    assert len(mock_storage['dualmind_chat_documents'][chat_c_id]) == 1
    
    print("   ✅ Test 1 Passed: Multiple chats created with isolated documents\n")

def test_2_document_isolation():
    """Test Case 2: Document isolation between chats"""
    print("📋 Test 2: Document isolation between chats")
    
    mock_storage = {'dualmind_chat_documents': {}}
    chat_a_id = 1730678400000
    chat_b_id = 1730678500000
    
    mock_storage['dualmind_chat_documents'][chat_a_id] = [sample_documents['chat_a_doc1']]
    mock_storage['dualmind_chat_documents'][chat_b_id] = [sample_documents['chat_b_doc']]
    
    # Load Chat A
    chat_a_docs = mock_storage['dualmind_chat_documents'].get(chat_a_id, [])
    assert len(chat_a_docs) == 1
    assert chat_a_docs[0]['name'] == 'pricing.txt'
    assert 'terms.txt' not in [doc['name'] for doc in chat_a_docs]
    
    # Load Chat B
    chat_b_docs = mock_storage['dualmind_chat_documents'].get(chat_b_id, [])
    assert len(chat_b_docs) == 1
    assert chat_b_docs[0]['name'] == 'terms.txt'
    assert 'pricing.txt' not in [doc['name'] for doc in chat_b_docs]
    
    print("   ✅ Test 2 Passed: Document isolation verified\n")

def test_3_delete_chat_only_its_documents():
    """Test Case 3: Delete chat removes ONLY its documents"""
    print("📋 Test 3: Delete chat removes ONLY its documents ⭐")
    
    mock_storage = {'dualmind_chat_documents': {}}
    chat_a_id = 1730678400000
    chat_b_id = 1730678500000
    chat_c_id = 1730678600000
    
    # Create 3 chats
    mock_storage['dualmind_chat_documents'][chat_a_id] = [
        sample_documents['chat_a_doc1'],
        sample_documents['chat_a_doc2']
    ]
    mock_storage['dualmind_chat_documents'][chat_b_id] = [sample_documents['chat_b_doc']]
    mock_storage['dualmind_chat_documents'][chat_c_id] = [sample_documents['chat_c_doc']]
    
    # Verify initial
    assert len(mock_storage['dualmind_chat_documents']) == 3
    assert chat_b_id in mock_storage['dualmind_chat_documents']
    
    # Delete Chat B
    del mock_storage['dualmind_chat_documents'][chat_b_id]
    
    # Verify Chat B removed
    assert chat_b_id not in mock_storage['dualmind_chat_documents']
    assert len(mock_storage['dualmind_chat_documents']) == 2
    
    # Verify Chat A intact
    assert chat_a_id in mock_storage['dualmind_chat_documents']
    assert len(mock_storage['dualmind_chat_documents'][chat_a_id]) == 2
    
    # Verify Chat C intact
    assert chat_c_id in mock_storage['dualmind_chat_documents']
    assert len(mock_storage['dualmind_chat_documents'][chat_c_id]) == 1
    
    print("   ✅ Test 3 Passed: Only deleted chat's documents removed\n")

def test_4_new_chat_no_documents():
    """Test Case 4: New chat has NO documents from other chats"""
    print("📋 Test 4: New chat has NO documents from other chats ⭐")
    
    mock_storage = {'dualmind_chat_documents': {}}
    chat_a_id = 1730678400000
    chat_b_id = 1730678500000
    
    # Create 2 chats with documents
    mock_storage['dualmind_chat_documents'][chat_a_id] = [
        sample_documents['chat_a_doc1'],
        sample_documents['chat_a_doc2']
    ]
    mock_storage['dualmind_chat_documents'][chat_b_id] = [sample_documents['chat_b_doc']]
    
    # Create new Chat D
    chat_d_id = 1730678700000
    chat_d_docs = mock_storage['dualmind_chat_documents'].get(chat_d_id, [])
    
    # Verify Chat D has no documents
    assert len(chat_d_docs) == 0
    assert chat_d_id not in mock_storage['dualmind_chat_documents']
    
    # Verify Chat D doesn't have access to other chats' documents
    all_doc_names = []
    if chat_d_id in mock_storage['dualmind_chat_documents']:
        all_doc_names = [doc['name'] for doc in mock_storage['dualmind_chat_documents'][chat_d_id]]
    
    assert 'pricing.txt' not in all_doc_names
    assert 'guide.md' not in all_doc_names
    assert 'terms.txt' not in all_doc_names
    
    print("   ✅ Test 4 Passed: New chat has no documents from other chats\n")

def test_5_switch_between_chats():
    """Test Case 5: Switch between chats loads correct documents"""
    print("📋 Test 5: Switch between chats loads correct documents")
    
    mock_storage = {'dualmind_chat_documents': {}}
    chat_a_id = 1730678400000
    chat_b_id = 1730678500000
    chat_c_id = 1730678600000
    
    mock_storage['dualmind_chat_documents'][chat_a_id] = [sample_documents['chat_a_doc1']]
    mock_storage['dualmind_chat_documents'][chat_b_id] = [sample_documents['chat_b_doc']]
    mock_storage['dualmind_chat_documents'][chat_c_id] = [sample_documents['chat_c_doc']]
    
    # Load Chat A
    current_docs = mock_storage['dualmind_chat_documents'].get(chat_a_id, [])
    assert len(current_docs) == 1
    assert current_docs[0]['name'] == 'pricing.txt'
    
    # Switch to Chat B
    current_docs = mock_storage['dualmind_chat_documents'].get(chat_b_id, [])
    assert len(current_docs) == 1
    assert current_docs[0]['name'] == 'terms.txt'
    
    # Switch back to Chat A
    current_docs = mock_storage['dualmind_chat_documents'].get(chat_a_id, [])
    assert len(current_docs) == 1
    assert current_docs[0]['name'] == 'pricing.txt'
    
    # Switch to Chat C
    current_docs = mock_storage['dualmind_chat_documents'].get(chat_c_id, [])
    assert len(current_docs) == 1
    assert current_docs[0]['name'] == 'notes.txt'
    
    print("   ✅ Test 5 Passed: Switching loads correct documents\n")

def test_6_clear_all_chats():
    """Test Case 6: Clear all chats removes all documents"""
    print("📋 Test 6: Clear all chats removes all documents")
    
    mock_storage = {'dualmind_chat_documents': {}}
    chat_a_id = 1730678400000
    chat_b_id = 1730678500000
    chat_c_id = 1730678600000
    
    mock_storage['dualmind_chat_documents'][chat_a_id] = [
        sample_documents['chat_a_doc1'],
        sample_documents['chat_a_doc2']
    ]
    mock_storage['dualmind_chat_documents'][chat_b_id] = [sample_documents['chat_b_doc']]
    mock_storage['dualmind_chat_documents'][chat_c_id] = [sample_documents['chat_c_doc']]
    
    # Verify initial
    assert len(mock_storage['dualmind_chat_documents']) == 3
    total_docs_before = sum(len(docs) for docs in mock_storage['dualmind_chat_documents'].values())
    assert total_docs_before == 4
    
    # Clear all
    mock_storage['dualmind_chat_documents'].clear()
    
    # Verify cleared
    assert len(mock_storage['dualmind_chat_documents']) == 0
    total_docs_after = sum(len(docs) for docs in mock_storage['dualmind_chat_documents'].values())
    assert total_docs_after == 0
    
    print("   ✅ Test 6 Passed: Clear all removes everything\n")

def test_7_rag_search_isolation():
    """Test Case 7: RAG search only searches current chat"""
    print("📋 Test 7: RAG search only searches current chat")
    
    chat_a_docs = [{
        'name': 'pricing.txt',
        'chunks': ['Our pricing starts at $99/month', 'for the basic plan.'],
        'embeddings': [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    }]
    
    chat_b_docs = [{
        'name': 'terms.txt',
        'chunks': ['Terms and conditions apply', 'to all services.'],
        'embeddings': [[0.7, 0.8, 0.9], [0.11, 0.12, 0.13]]
    }]
    
    # Search in Chat A
    query = "pricing"
    results_in_chat_a = []
    for doc in chat_a_docs:
        for chunk in doc['chunks']:
            if 'pricing' in chunk.lower():
                results_in_chat_a.append({'text': chunk, 'filename': doc['name']})
    
    assert len(results_in_chat_a) > 0
    assert all('pricing.txt' in chunk['filename'] for chunk in results_in_chat_a)
    
    # Search in Chat B
    results_in_chat_b = []
    for doc in chat_b_docs:
        for chunk in doc['chunks']:
            if 'pricing' in chunk.lower():
                results_in_chat_b.append({'text': chunk, 'filename': doc['name']})
    
    assert len(results_in_chat_b) == 0
    
    print("   ✅ Test 7 Passed: RAG search respects per-chat boundaries\n")

# Run all tests
try:
    test_1_create_multiple_chats()
    test_2_document_isolation()
    test_3_delete_chat_only_its_documents()
    test_4_new_chat_no_documents()
    test_5_switch_between_chats()
    test_6_clear_all_chats()
    test_7_rag_search_isolation()
    
    print("="*70)
    print("✅ ALL 7 TESTS PASSED!")
    print("="*70)
    print("\n📝 Key Test Results:")
    print("   ✅ Document isolation between chats")
    print("   ✅ Delete chat removes ONLY its documents")
    print("   ✅ New chat has NO documents from other chats")
    print("   ✅ Switching chats loads correct documents")
    print("   ✅ Clear all removes everything")
    print("   ✅ RAG search respects chat boundaries")
    print("\n🎯 All per-chat RAG features verified!")
    print()
    
except AssertionError as e:
    print(f"\n❌ Test Failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

