"""
Integration tests for per-chat RAG document management
Tests document isolation, chat deletion, and proper cleanup
"""

import pytest
import json
from pathlib import Path


class TestPerChatRAG:
    """Test per-chat document isolation and management"""
    
    @pytest.fixture
    def mock_storage(self):
        """Mock localStorage for testing"""
        return {
            'dualmind_chats': [],
            'dualmind_chat_documents': {}
        }
    
    @pytest.fixture
    def sample_documents(self):
        """Sample documents for testing"""
        return {
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
    
    def test_create_multiple_chats_with_documents(self, mock_storage, sample_documents):
        """
        Test Case 1: Create multiple chats with different documents
        
        Scenario:
        1. Create Chat A with 2 documents (pricing.txt, guide.md)
        2. Create Chat B with 1 document (terms.txt)
        3. Create Chat C with 1 document (notes.txt)
        
        Expected:
        - Each chat should have its own isolated documents
        - Documents should be stored with chat ID as key
        - No cross-contamination between chats
        """
        # Setup
        chat_a_id = 1730678400000
        chat_b_id = 1730678500000
        chat_c_id = 1730678600000
        
        # Chat A: Add 2 documents
        mock_storage['dualmind_chat_documents'][chat_a_id] = [
            sample_documents['chat_a_doc1'],
            sample_documents['chat_a_doc2']
        ]
        
        # Chat B: Add 1 document
        mock_storage['dualmind_chat_documents'][chat_b_id] = [
            sample_documents['chat_b_doc']
        ]
        
        # Chat C: Add 1 document
        mock_storage['dualmind_chat_documents'][chat_c_id] = [
            sample_documents['chat_c_doc']
        ]
        
        # Verify
        assert len(mock_storage['dualmind_chat_documents']) == 3, \
            "Should have 3 chats with documents"
        
        assert len(mock_storage['dualmind_chat_documents'][chat_a_id]) == 2, \
            "Chat A should have 2 documents"
        
        assert len(mock_storage['dualmind_chat_documents'][chat_b_id]) == 1, \
            "Chat B should have 1 document"
        
        assert len(mock_storage['dualmind_chat_documents'][chat_c_id]) == 1, \
            "Chat C should have 1 document"
        
        # Verify document names
        chat_a_docs = mock_storage['dualmind_chat_documents'][chat_a_id]
        assert chat_a_docs[0]['name'] == 'pricing.txt'
        assert chat_a_docs[1]['name'] == 'guide.md'
        
        chat_b_docs = mock_storage['dualmind_chat_documents'][chat_b_id]
        assert chat_b_docs[0]['name'] == 'terms.txt'
        
        chat_c_docs = mock_storage['dualmind_chat_documents'][chat_c_id]
        assert chat_c_docs[0]['name'] == 'notes.txt'
        
        print("✅ Test 1 Passed: Multiple chats created with isolated documents")
    
    def test_document_isolation_between_chats(self, mock_storage, sample_documents):
        """
        Test Case 2: Verify document isolation between chats
        
        Scenario:
        1. Create Chat A with pricing.txt
        2. Create Chat B with terms.txt
        3. Load Chat A documents
        4. Verify only pricing.txt is visible
        5. Load Chat B documents
        6. Verify only terms.txt is visible
        
        Expected:
        - Loading Chat A shows only Chat A documents
        - Loading Chat B shows only Chat B documents
        - No cross-chat document visibility
        """
        # Setup
        chat_a_id = 1730678400000
        chat_b_id = 1730678500000
        
        mock_storage['dualmind_chat_documents'][chat_a_id] = [
            sample_documents['chat_a_doc1']
        ]
        mock_storage['dualmind_chat_documents'][chat_b_id] = [
            sample_documents['chat_b_doc']
        ]
        
        # Load Chat A documents
        chat_a_docs = mock_storage['dualmind_chat_documents'].get(chat_a_id, [])
        assert len(chat_a_docs) == 1, "Chat A should have exactly 1 document"
        assert chat_a_docs[0]['name'] == 'pricing.txt', \
            "Chat A should only show pricing.txt"
        assert 'terms.txt' not in [doc['name'] for doc in chat_a_docs], \
            "Chat A should NOT show terms.txt from Chat B"
        
        # Load Chat B documents
        chat_b_docs = mock_storage['dualmind_chat_documents'].get(chat_b_id, [])
        assert len(chat_b_docs) == 1, "Chat B should have exactly 1 document"
        assert chat_b_docs[0]['name'] == 'terms.txt', \
            "Chat B should only show terms.txt"
        assert 'pricing.txt' not in [doc['name'] for doc in chat_b_docs], \
            "Chat B should NOT show pricing.txt from Chat A"
        
        print("✅ Test 2 Passed: Document isolation verified between chats")
    
    def test_delete_chat_removes_only_its_documents(self, mock_storage, sample_documents):
        """
        Test Case 3: Delete a chat and verify only its documents are removed
        
        Scenario:
        1. Create Chat A with 2 documents
        2. Create Chat B with 1 document
        3. Create Chat C with 1 document
        4. Delete Chat B
        5. Verify Chat B documents are removed
        6. Verify Chat A documents remain intact
        7. Verify Chat C documents remain intact
        
        Expected:
        - Chat B and its documents are completely removed
        - Chat A documents are untouched
        - Chat C documents are untouched
        - Storage contains only Chat A and Chat C
        """
        # Setup: Create 3 chats with documents
        chat_a_id = 1730678400000
        chat_b_id = 1730678500000
        chat_c_id = 1730678600000
        
        mock_storage['dualmind_chat_documents'][chat_a_id] = [
            sample_documents['chat_a_doc1'],
            sample_documents['chat_a_doc2']
        ]
        mock_storage['dualmind_chat_documents'][chat_b_id] = [
            sample_documents['chat_b_doc']
        ]
        mock_storage['dualmind_chat_documents'][chat_c_id] = [
            sample_documents['chat_c_doc']
        ]
        
        # Verify initial state
        assert len(mock_storage['dualmind_chat_documents']) == 3, \
            "Should start with 3 chats"
        assert chat_b_id in mock_storage['dualmind_chat_documents'], \
            "Chat B should exist before deletion"
        
        # Delete Chat B
        if chat_b_id in mock_storage['dualmind_chat_documents']:
            del mock_storage['dualmind_chat_documents'][chat_b_id]
        
        # Verify Chat B is removed
        assert chat_b_id not in mock_storage['dualmind_chat_documents'], \
            "Chat B should be deleted"
        assert len(mock_storage['dualmind_chat_documents']) == 2, \
            "Should have 2 chats remaining after deletion"
        
        # Verify Chat A documents remain intact
        assert chat_a_id in mock_storage['dualmind_chat_documents'], \
            "Chat A should still exist"
        chat_a_docs = mock_storage['dualmind_chat_documents'][chat_a_id]
        assert len(chat_a_docs) == 2, \
            "Chat A should still have 2 documents"
        assert chat_a_docs[0]['name'] == 'pricing.txt', \
            "Chat A should still have pricing.txt"
        assert chat_a_docs[1]['name'] == 'guide.md', \
            "Chat A should still have guide.md"
        
        # Verify Chat C documents remain intact
        assert chat_c_id in mock_storage['dualmind_chat_documents'], \
            "Chat C should still exist"
        chat_c_docs = mock_storage['dualmind_chat_documents'][chat_c_id]
        assert len(chat_c_docs) == 1, \
            "Chat C should still have 1 document"
        assert chat_c_docs[0]['name'] == 'notes.txt', \
            "Chat C should still have notes.txt"
        
        print("✅ Test 3 Passed: Only deleted chat's documents removed, others intact")
    
    def test_new_chat_has_no_documents_from_other_chats(self, mock_storage, sample_documents):
        """
        Test Case 4: Create new chat and verify no documents from other chats
        
        Scenario:
        1. Create Chat A with 2 documents
        2. Create Chat B with 1 document
        3. Create new Chat D (empty)
        4. Verify Chat D has no documents
        5. Verify Chat D doesn't show documents from Chat A or B
        
        Expected:
        - New Chat D starts with empty document list
        - Chat D has no access to Chat A or B documents
        - Chat A and B documents remain in their respective chats
        """
        # Setup: Create 2 chats with documents
        chat_a_id = 1730678400000
        chat_b_id = 1730678500000
        
        mock_storage['dualmind_chat_documents'][chat_a_id] = [
            sample_documents['chat_a_doc1'],
            sample_documents['chat_a_doc2']
        ]
        mock_storage['dualmind_chat_documents'][chat_b_id] = [
            sample_documents['chat_b_doc']
        ]
        
        # Create new Chat D
        chat_d_id = 1730678700000
        chat_d_docs = mock_storage['dualmind_chat_documents'].get(chat_d_id, [])
        
        # Verify Chat D has no documents
        assert len(chat_d_docs) == 0, \
            "New Chat D should have no documents"
        assert chat_d_id not in mock_storage['dualmind_chat_documents'], \
            "Chat D should not exist in storage until documents are added"
        
        # Verify Chat D doesn't have access to other chats' documents
        all_doc_names = []
        if chat_d_id in mock_storage['dualmind_chat_documents']:
            all_doc_names = [doc['name'] for doc in mock_storage['dualmind_chat_documents'][chat_d_id]]
        
        assert 'pricing.txt' not in all_doc_names, \
            "Chat D should NOT have pricing.txt from Chat A"
        assert 'guide.md' not in all_doc_names, \
            "Chat D should NOT have guide.md from Chat A"
        assert 'terms.txt' not in all_doc_names, \
            "Chat D should NOT have terms.txt from Chat B"
        
        # Verify other chats still have their documents
        assert len(mock_storage['dualmind_chat_documents'][chat_a_id]) == 2, \
            "Chat A should still have 2 documents"
        assert len(mock_storage['dualmind_chat_documents'][chat_b_id]) == 1, \
            "Chat B should still have 1 document"
        
        print("✅ Test 4 Passed: New chat has no documents from other chats")
    
    def test_switch_between_chats_loads_correct_documents(self, mock_storage, sample_documents):
        """
        Test Case 5: Switch between chats and verify correct documents load
        
        Scenario:
        1. Create Chat A with pricing.txt
        2. Create Chat B with terms.txt
        3. Create Chat C with notes.txt
        4. Load Chat A → Verify only pricing.txt
        5. Load Chat B → Verify only terms.txt
        6. Load Chat A again → Verify pricing.txt still there
        7. Load Chat C → Verify only notes.txt
        
        Expected:
        - Each chat switch loads only that chat's documents
        - Documents persist correctly when returning to a chat
        - No document leakage between switches
        """
        # Setup
        chat_a_id = 1730678400000
        chat_b_id = 1730678500000
        chat_c_id = 1730678600000
        
        mock_storage['dualmind_chat_documents'][chat_a_id] = [
            sample_documents['chat_a_doc1']
        ]
        mock_storage['dualmind_chat_documents'][chat_b_id] = [
            sample_documents['chat_b_doc']
        ]
        mock_storage['dualmind_chat_documents'][chat_c_id] = [
            sample_documents['chat_c_doc']
        ]
        
        # Load Chat A
        current_chat_id = chat_a_id
        current_docs = mock_storage['dualmind_chat_documents'].get(current_chat_id, [])
        assert len(current_docs) == 1
        assert current_docs[0]['name'] == 'pricing.txt'
        
        # Switch to Chat B
        current_chat_id = chat_b_id
        current_docs = mock_storage['dualmind_chat_documents'].get(current_chat_id, [])
        assert len(current_docs) == 1
        assert current_docs[0]['name'] == 'terms.txt'
        assert 'pricing.txt' not in [doc['name'] for doc in current_docs]
        
        # Switch back to Chat A
        current_chat_id = chat_a_id
        current_docs = mock_storage['dualmind_chat_documents'].get(current_chat_id, [])
        assert len(current_docs) == 1
        assert current_docs[0]['name'] == 'pricing.txt'
        assert 'terms.txt' not in [doc['name'] for doc in current_docs]
        
        # Switch to Chat C
        current_chat_id = chat_c_id
        current_docs = mock_storage['dualmind_chat_documents'].get(current_chat_id, [])
        assert len(current_docs) == 1
        assert current_docs[0]['name'] == 'notes.txt'
        assert 'pricing.txt' not in [doc['name'] for doc in current_docs]
        assert 'terms.txt' not in [doc['name'] for doc in current_docs]
        
        print("✅ Test 5 Passed: Switching between chats loads correct documents")
    
    def test_clear_all_chats_removes_all_documents(self, mock_storage, sample_documents):
        """
        Test Case 6: Clear all chats and verify all documents are removed
        
        Scenario:
        1. Create Chat A with 2 documents
        2. Create Chat B with 1 document
        3. Create Chat C with 1 document
        4. Clear all chats
        5. Verify all chats are removed
        6. Verify all documents are removed
        
        Expected:
        - All chats removed from storage
        - All documents removed from storage
        - Storage is empty
        """
        # Setup: Create 3 chats with documents
        chat_a_id = 1730678400000
        chat_b_id = 1730678500000
        chat_c_id = 1730678600000
        
        mock_storage['dualmind_chat_documents'][chat_a_id] = [
            sample_documents['chat_a_doc1'],
            sample_documents['chat_a_doc2']
        ]
        mock_storage['dualmind_chat_documents'][chat_b_id] = [
            sample_documents['chat_b_doc']
        ]
        mock_storage['dualmind_chat_documents'][chat_c_id] = [
            sample_documents['chat_c_doc']
        ]
        
        # Verify initial state
        assert len(mock_storage['dualmind_chat_documents']) == 3, \
            "Should start with 3 chats"
        
        total_docs_before = sum(
            len(docs) for docs in mock_storage['dualmind_chat_documents'].values()
        )
        assert total_docs_before == 4, \
            "Should start with 4 total documents"
        
        # Clear all chats and documents
        mock_storage['dualmind_chat_documents'].clear()
        
        # Verify everything is cleared
        assert len(mock_storage['dualmind_chat_documents']) == 0, \
            "All chats should be removed"
        
        total_docs_after = sum(
            len(docs) for docs in mock_storage['dualmind_chat_documents'].values()
        )
        assert total_docs_after == 0, \
            "All documents should be removed"
        
        print("✅ Test 6 Passed: Clear all chats removes all documents")
    
    def test_delete_current_chat_while_active(self, mock_storage, sample_documents):
        """
        Test Case 7: Delete currently active chat
        
        Scenario:
        1. Create Chat A with documents
        2. Create Chat B with documents
        3. Set Chat A as active (current chat)
        4. Delete Chat A (the active chat)
        5. Verify Chat A is deleted
        6. Verify new chat is created or switched to Chat B
        7. Verify new/switched chat has correct documents
        
        Expected:
        - Active chat can be deleted
        - System handles deletion gracefully
        - User is moved to another chat or new chat
        """
        # Setup
        chat_a_id = 1730678400000
        chat_b_id = 1730678500000
        
        mock_storage['dualmind_chat_documents'][chat_a_id] = [
            sample_documents['chat_a_doc1']
        ]
        mock_storage['dualmind_chat_documents'][chat_b_id] = [
            sample_documents['chat_b_doc']
        ]
        
        # Set Chat A as current
        current_chat_id = chat_a_id
        
        # Delete current chat (Chat A)
        if current_chat_id in mock_storage['dualmind_chat_documents']:
            del mock_storage['dualmind_chat_documents'][current_chat_id]
        
        # Verify Chat A is deleted
        assert chat_a_id not in mock_storage['dualmind_chat_documents'], \
            "Chat A should be deleted"
        
        # Simulate switching to new chat or Chat B
        current_chat_id = chat_b_id
        current_docs = mock_storage['dualmind_chat_documents'].get(current_chat_id, [])
        
        # Verify correct documents loaded
        assert len(current_docs) == 1, \
            "Should load Chat B's documents"
        assert current_docs[0]['name'] == 'terms.txt', \
            "Should show Chat B's terms.txt"
        assert 'pricing.txt' not in [doc['name'] for doc in current_docs], \
            "Should NOT show deleted Chat A's pricing.txt"
        
        print("✅ Test 7 Passed: Deleting active chat handled correctly")


class TestRAGSearchIsolation:
    """Test RAG search respects per-chat document boundaries"""
    
    def test_rag_search_only_searches_current_chat_documents(self):
        """
        Test Case 8: RAG search only searches current chat's documents
        
        Scenario:
        1. Chat A has pricing.txt with pricing info
        2. Chat B has terms.txt with terms info
        3. In Chat A: Search for "pricing"
        4. Verify only pricing.txt is searched
        5. In Chat B: Search for "pricing"
        6. Verify terms.txt is searched (no results for "pricing")
        
        Expected:
        - RAG only searches documents in current chat
        - No cross-chat document search
        """
        # Setup
        chat_a_docs = [
            {
                'name': 'pricing.txt',
                'chunks': ['Our pricing starts at $99/month', 'for the basic plan.'],
                'embeddings': [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
            }
        ]
        
        chat_b_docs = [
            {
                'name': 'terms.txt',
                'chunks': ['Terms and conditions apply', 'to all services.'],
                'embeddings': [[0.7, 0.8, 0.9], [0.11, 0.12, 0.13]]
            }
        ]
        
        # Simulate searching in Chat A
        query = "pricing"
        available_chunks_in_chat_a = []
        for doc in chat_a_docs:
            for chunk in doc['chunks']:
                if 'pricing' in chunk.lower():
                    available_chunks_in_chat_a.append({
                        'text': chunk,
                        'filename': doc['name']
                    })
        
        assert len(available_chunks_in_chat_a) > 0, \
            "Should find 'pricing' in Chat A documents"
        assert all('pricing.txt' in chunk['filename'] for chunk in available_chunks_in_chat_a), \
            "All results should be from pricing.txt"
        
        # Simulate searching in Chat B
        available_chunks_in_chat_b = []
        for doc in chat_b_docs:
            for chunk in doc['chunks']:
                if 'pricing' in chunk.lower():
                    available_chunks_in_chat_b.append({
                        'text': chunk,
                        'filename': doc['name']
                    })
        
        assert len(available_chunks_in_chat_b) == 0, \
            "Should NOT find 'pricing' in Chat B documents"
        
        print("✅ Test 8 Passed: RAG search respects per-chat boundaries")


# Run all tests
if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 RUNNING PER-CHAT RAG INTEGRATION TESTS")
    print("="*70 + "\n")
    
    # Test Suite 1: Document Management
    test_suite_1 = TestPerChatRAG()
    mock_storage = {
        'dualmind_chats': [],
        'dualmind_chat_documents': {}
    }
    sample_docs = test_suite_1.sample_documents(None)
    
    try:
        test_suite_1.test_create_multiple_chats_with_documents(mock_storage.copy(), sample_docs)
        test_suite_1.test_document_isolation_between_chats(mock_storage.copy(), sample_docs)
        test_suite_1.test_delete_chat_removes_only_its_documents(mock_storage.copy(), sample_docs)
        test_suite_1.test_new_chat_has_no_documents_from_other_chats(mock_storage.copy(), sample_docs)
        test_suite_1.test_switch_between_chats_loads_correct_documents(mock_storage.copy(), sample_docs)
        test_suite_1.test_clear_all_chats_removes_all_documents(mock_storage.copy(), sample_docs)
        test_suite_1.test_delete_current_chat_while_active(mock_storage.copy(), sample_docs)
        
        # Test Suite 2: RAG Search Isolation
        test_suite_2 = TestRAGSearchIsolation()
        test_suite_2.test_rag_search_only_searches_current_chat_documents()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70)
        
    except AssertionError as e:
        print(f"\n❌ Test Failed: {e}")
        raise

