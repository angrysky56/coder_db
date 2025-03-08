#!/usr/bin/env python3
"""
Sample Code Storage Utility

This script demonstrates how to store and retrieve code patterns using the Qdrant memory system.
It provides utility functions for formatting code patterns with proper metadata for later retrieval.
"""

import json
import sys

def store_code_pattern(name, code, explanation, language="python", tags=None):
    """
    Store a code pattern in Qdrant memory system.
    
    Parameters:
    -----------
    name : str
        Name of the code pattern
    code : str
        The actual code snippet
    explanation : str
        Detailed explanation of how the code works and when to use it
    language : str, optional
        Programming language of the code (default: "python")
    tags : list, optional
        List of relevant tags for better retrieval
        
    Returns:
    --------
    dict
        Formatted information object ready for storage
    
    Example:
    --------
    >>> pattern = store_code_pattern(
    ...     "Binary search implementation",
    ...     "def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1",
    ...     "An efficient O(log n) algorithm for finding elements in a sorted array.",
    ...     tags=["algorithm", "searching", "divide and conquer"]
    ... )
    >>> print(pattern)
    """
    information = {
        "type": "code_pattern",
        "name": name,
        "language": language,
        "code": code,
        "explanation": explanation,
        "tags": tags or []
    }
    
    # In a real implementation, this would call the qdrant-store-memory function
    # For demonstration purposes, we just return the formatted object
    print(f"Would store pattern '{name}' in Qdrant")
    return information

def find_similar_code(query):
    """
    Find code patterns similar to the provided query.
    
    Parameters:
    -----------
    query : str
        Search query describing the code pattern needed
        
    Returns:
    --------
    list
        List of matching code patterns (would be retrieved from Qdrant)
        
    Example:
    --------
    >>> results = find_similar_code("efficient way to search sorted array")
    >>> print(results)
    """
    # In a real implementation, this would call the qdrant-find-memories function
    # For demonstration purposes, we just print the query
    print(f"Would search Qdrant for: {query}")
    return []

def main():
    """Main function to demonstrate the utility."""
    # Example usage
    pattern = store_code_pattern(
        "Context manager implementation",
        """class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
        
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()""",
        "A context manager for automatic resource management of file handles.",
        tags=["resource management", "file handling", "context manager"]
    )
    
    print("\nStored pattern information:")
    print(json.dumps(pattern, indent=2))
    
    print("\nRetrieving similar patterns:")
    find_similar_code("python context manager for files")

if __name__ == "__main__":
    main()
