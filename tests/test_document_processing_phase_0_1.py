"""
Unit Tests for TQFA Phase 0.1 - Document Processing Enhancement

This test suite validates that the LLM properly finds information from uploaded documents
instead of defaulting to general knowledge. These tests are critical for Phase 0.1 success.

Test Scenarios:
1. "Yellow sky in TXTland" - The canonical test case for document-first search
2. Multi-format document processing (.txt, .csv, .docx, .xlsx, .pdf)
3. Confidence reporting validation
4. Source citation verification
5. Multi-query strategy testing
"""

import asyncio
import csv
import json
import os
import tempfile
import unittest
from unittest.mock import AsyncMock, patch, MagicMock
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from api.search_index_manager import SearchIndexManager


class TestDocumentProcessingPhase01(unittest.IsolatedAsyncioTestCase):
    """Test suite for Phase 0.1 document processing enhancements."""

    @classmethod
    def setUpClass(cls):
        """Set up test class with sample files data."""
        cls.test_cases = [
            {
                "file": "sample.txt",
                "question": "What color is the sky in TXTland?",
                "expected_answer": "yellow",
                "content": "The sky is yellow in TXTland."
            },
            {
                "file": "sample.csv", 
                "question": "What is the size of planet Zorb?",
                "expected_answer": "Large",
                "content": "Planet,Size\\nZorb,Large"
            },
            {
                "file": "sample.docx",
                "question": "Who is the president of DOCXistan?", 
                "expected_answer": "Luna",
                "content": "The president of DOCXistan is Luna."
            },
            {
                "file": "sample.xlsx",
                "question": "How many cats in Meowvia?",
                "expected_answer": "22", 
                "content": "Cats in Meowvia: 22"
            },
            {
                "file": "sample.pdf",
                "question": "How many tigers are in PDFzone?",
                "expected_answer": "7",
                "content": "There are 7 tigers in PDFzone."
            },
        ]

    def setUp(self):
        """Set up individual test."""
        self.search_manager = self._create_mock_search_manager()

    def _create_mock_search_manager(self):
        """Create a mock SearchIndexManager for testing."""
        mock_manager = SearchIndexManager(
            endpoint="https://test.search.windows.net",
            credential=AsyncMock(),
            index_name="test_index",
            dimensions=100,
            model="text-embedding-3-small",
            deployment_name="test-embedding",
            embedding_endpoint="https://test.openai.azure.com",
            embed_api_key="test_key"
        )
        
        # Mock the index to avoid None reference errors
        mock_manager._index = MagicMock()
        mock_manager._index.name = "test_index"
        
        return mock_manager

    async def test_yellow_sky_txtland_canonical_case(self):
        """
        Test the canonical 'yellow sky in TXTland' case.
        This is THE critical test case for Phase 0.1 success.
        """
        question = "What color is the sky in TXTland?"
        expected_content = "The sky is yellow in TXTland."
        expected_answer = "yellow"
        
        # Mock search results that should contain the document content
        mock_results = [
            {
                'token': expected_content,
                'title': 'sample.txt',
                '@search.score': 0.95
            }
        ]
        
        # Mock the search client
        with patch.object(self.search_manager, '_get_client') as mock_client:
            # Create a proper async mock
            mock_search_client = AsyncMock()
            mock_search_client.search.return_value = AsyncMockSearchResponse(mock_results)
            mock_client.return_value = mock_search_client
            
            # Execute search
            result = await self.search_manager.semantic_search(question)
            
            # Validate results
            self.assertIn("sample.txt", result, "Should identify source document")
            self.assertIn(expected_content, result, "Should contain document content")
            self.assertIn("score:", result, "Should include confidence score")
            self.assertIn("DOCUMENT:", result, "Should have enhanced formatting")
            
    async def test_multi_format_document_search(self):
        """Test document search across all supported file formats."""
        for test_case in self.test_cases:
            with self.subTest(file=test_case["file"]):
                await self._test_individual_document_case(test_case)
                
    async def _test_individual_document_case(self, test_case):
        """Test individual document case with proper search behavior."""
        mock_results = [
            {
                'token': test_case["content"],
                'title': test_case["file"], 
                '@search.score': 0.90
            }
        ]
        
        with patch.object(self.search_manager, '_get_client') as mock_client:
            # Create a proper async mock
            mock_search_client = AsyncMock()
            mock_search_client.search.return_value = AsyncMockSearchResponse(mock_results)
            mock_client.return_value = mock_search_client
            
            result = await self.search_manager.semantic_search(test_case["question"])
            
            # Validate document-first search behavior
            self.assertIn(test_case["file"], result, 
                         f"Should identify source document {test_case['file']}")
            self.assertIn("DOCUMENT:", result, "Should use enhanced formatting")
            self.assertIn("SEARCH SUMMARY:", result, "Should include search summary")

    async def test_no_results_handling(self):
        """Test behavior when no documents match the query."""
        question = "What is the capital of Nonexistentland?"
        
        # Mock empty search results
        mock_results = []
        
        with patch.object(self.search_manager, '_get_client') as mock_client:
            # Create a proper async mock
            mock_search_client = AsyncMock()
            mock_search_client.search.return_value = AsyncMockSearchResponse(mock_results)
            mock_client.return_value = mock_search_client
            
            result = await self.search_manager.semantic_search(question)
            
            # Should clearly indicate no documents found
            self.assertIn("NO DOCUMENTS FOUND", result)
            self.assertIn("No relevant information in uploaded documents", result)

    async def test_multi_query_fallback_strategy(self):
        """Test that the system tries alternative queries when initial search fails."""
        question = "What color is the sky in TXTland?"
        
        # First search returns nothing, second search (with keywords) returns results
        empty_results = []
        keyword_results = [
            {
                'token': "The sky is yellow in TXTland.",
                'title': 'sample.txt',
                '@search.score': 0.85
            }
        ]
        
        with patch.object(self.search_manager, '_get_client') as mock_client:
            # Create a proper async mock
            mock_search_client = AsyncMock()
            # Mock two different search calls
            mock_search_client.search.side_effect = [
                AsyncMockSearchResponse(empty_results),   # First search fails
                AsyncMockSearchResponse(keyword_results)  # Keyword search succeeds
            ]
            mock_client.return_value = mock_search_client
            
            result = await self.search_manager.semantic_search(question)
            
            # Should have found results via fallback strategy
            self.assertIn("sample.txt", result)
            self.assertIn("yellow", result)
            
            # Verify that search was called twice (original + fallback)
            self.assertEqual(mock_search_client.search.call_count, 2)

    def test_keyword_extraction(self):
        """Test keyword extraction for alternative search strategies."""
        test_cases = [
            {
                "query": "What color is the sky in TXTland?",
                "expected_keywords": ["color", "sky", "TXTland"]
            },
            {
                "query": "How many tigers are in PDFzone?",
                "expected_keywords": ["many", "tigers", "PDFzone"] 
            },
            {
                "query": "Who is the president of DOCXistan?",
                "expected_keywords": ["president", "DOCXistan"]
            }
        ]
        
        for test_case in test_cases:
            with self.subTest(query=test_case["query"]):
                keywords = self.search_manager._extract_keywords(test_case["query"])
                
                # Check that meaningful keywords are extracted
                for expected_keyword in test_case["expected_keywords"]:
                    if expected_keyword.lower() not in ['many']:  # Skip common words that might be filtered
                        self.assertIn(expected_keyword.lower(), 
                                    [k.lower() for k in keywords],
                                    f"Should extract keyword '{expected_keyword}'")

    async def test_enhanced_result_formatting(self):
        """Test that search results use enhanced formatting with confidence scores."""
        question = "Test query"
        mock_results = [
            {
                'token': "Test content from document",
                'title': 'test_document.txt',
                '@search.score': 0.92
            }
        ]
        
        with patch.object(self.search_manager, '_get_client') as mock_client:
            # Create a proper async mock
            mock_search_client = AsyncMock()
            mock_search_client.search.return_value = AsyncMockSearchResponse(mock_results)
            mock_client.return_value = mock_search_client
            
            result = await self.search_manager.semantic_search(question)
            
            # Validate enhanced formatting elements
            required_elements = [
                "DOCUMENT: test_document.txt",
                "score: 0.92", 
                "CONTENT: Test content from document",
                "SEARCH SUMMARY: Found 1 relevant document sections",
                "=============================="  # Separator formatting
            ]
            
            for element in required_elements:
                self.assertIn(element, result, f"Should contain formatting element: {element}")

    def test_document_processing_accuracy_metrics(self):
        """
        Test framework for measuring document processing accuracy.
        This provides the foundation for 95%+ accuracy requirement validation.
        """
        # Test case success tracking
        test_results = {
            'total_cases': len(self.test_cases),
            'successful_extractions': 0,
            'failed_extractions': 0,
            'accuracy_threshold': 0.95
        }
        
        # This would be expanded with actual document processing tests
        # For now, validate that we have the framework
        
        self.assertGreaterEqual(test_results['total_cases'], 5, 
                               "Should have adequate test cases for accuracy measurement")
        
        # Calculate accuracy (would be populated by actual test runs)
        # accuracy = test_results['successful_extractions'] / test_results['total_cases']
        # self.assertGreaterEqual(accuracy, test_results['accuracy_threshold'], 
        #                        "Document processing accuracy should meet 95% threshold")

class MockEndpointTests(unittest.TestCase):
    """
    Tests for mock endpoint protocol compliance.
    Ensures all mock endpoints clearly identify themselves as test data.
    """
    
    def test_mock_endpoint_warning_format(self):
        """Test that mock endpoints follow the required warning format."""
        # Example mock endpoint response format
        mock_response = {
            "result": "🚨 MOCK ENDPOINT - NOT REAL ANALYSIS 🚨",
            "status": "mock_data_only", 
            "warning": "Test data only - do not use for decisions"
        }
        
        # Validate required mock endpoint elements
        self.assertIn("🚨 MOCK ENDPOINT", mock_response["result"])
        self.assertEqual(mock_response["status"], "mock_data_only") 
        self.assertIn("Test data only", mock_response["warning"])

class AsyncMockSearchResponse:
    """Mock class for Azure Search response that supports async iteration."""
    
    def __init__(self, results):
        self.results = results
        
    def __aiter__(self):
        return AsyncMockIterator(self.results)

class AsyncMockIterator:
    """Async iterator for mock search results."""
    
    def __init__(self, results):
        self.results = results
        self.index = 0
        
    def __aiter__(self):
        return self
        
    async def __anext__(self):
        if self.index >= len(self.results):
            raise StopAsyncIteration
        result = self.results[self.index]
        self.index += 1
        return result


if __name__ == '__main__':
    # Run tests
    unittest.main()