#!/usr/bin/env python3
"""
Enhanced Code Storage Utility

This script provides a comprehensive system for storing and retrieving code patterns using
the Qdrant memory system with enriched metadata, quality metrics, and versioning.
"""

import json
import sys
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple

class CodeQualityAnalyzer:
    """
    Analyzes code quality metrics before storage.
    
    This class provides methods to calculate various code quality metrics
    such as cyclomatic complexity, documentation coverage, and style conformance.
    """
    
    @staticmethod
    def calculate_cyclomatic_complexity(code: str, language: str = "python") -> int:
        """
        Calculate cyclomatic complexity of code.
        
        Parameters:
        -----------
        code : str
            The code to analyze
        language : str
            Programming language of the code (default: "python")
            
        Returns:
        --------
        int
            Estimated cyclomatic complexity score
            
        Note:
        -----
        This is a simplified implementation. In production, you would
        use language-specific tools like radon (Python), escomplex (JavaScript), etc.
        """
        if language.lower() == "python":
            # Simple heuristic: count control flow statements
            # In production, use a proper tool like radon
            control_statements = [
                r'\bif\b', r'\belif\b', r'\belse\b', r'\bfor\b', 
                r'\bwhile\b', r'\bwith\b', r'\btry\b', r'\bexcept\b'
            ]
            complexity = 1  # Start with 1 for the function/method itself
            
            for statement in control_statements:
                complexity += len(re.findall(statement, code))
            
            return complexity
        else:
            # Default complexity estimation for other languages
            return 1
    
    @staticmethod
    def calculate_doc_coverage(code: str, language: str = "python") -> float:
        """
        Calculate documentation coverage.
        
        Parameters:
        -----------
        code : str
            The code to analyze
        language : str
            Programming language of the code (default: "python")
            
        Returns:
        --------
        float
            Documentation coverage between 0 and 1
            
        Note:
        -----
        This is a simplified implementation. In production, use
        language-specific tools for more accurate measurement.
        """
        if language.lower() == "python":
            # Count docstrings
            docstring_count = len(re.findall(r'"""[\s\S]*?"""', code))
            docstring_count += len(re.findall(r"'''[\s\S]*?'''", code))
            
            # Count functions and classes
            func_count = len(re.findall(r'\bdef\s+\w+\s*\(', code))
            class_count = len(re.findall(r'\bclass\s+\w+\s*[:\(]', code))
            
            total_definitions = func_count + class_count
            if total_definitions == 0:
                return 1.0  # No definitions to document
                
            # Simple heuristic: assume one docstring per function/class is ideal
            coverage = min(1.0, docstring_count / total_definitions)
            return coverage
        else:
            # Default coverage estimation for other languages
            return 0.5

class EnhancedCodeStorage:
    """
    Enhanced system for storing and retrieving code patterns with rich metadata.
    """
    
    def __init__(self):
        """Initialize the storage system."""
        self.quality_analyzer = CodeQualityAnalyzer()
        
    def store_code_pattern(
        self, 
        name: str, 
        code: str, 
        explanation: str, 
        language: str = "python", 
        tags: Optional[List[str]] = None,
        complexity_level: Optional[str] = None,
        dependencies: Optional[List[str]] = None,
        user_rating: Optional[float] = None,
        version: int = 1,
        previous_version_id: Optional[str] = None,
        change_log: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Store a code pattern with comprehensive metadata.
        
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
        complexity_level : str, optional
            Manual complexity level ("simple", "intermediate", "advanced")
        dependencies : list, optional
            External libraries or frameworks required
        user_rating : float, optional
            User-provided rating (0-5)
        version : int, optional
            Version number of this code pattern (default: 1)
        previous_version_id : str, optional
            ID of the previous version if this is an update
        change_log : str, optional
            Description of changes from previous version
            
        Returns:
        --------
        dict
            Formatted information object ready for storage
        """
        # Calculate quality metrics
        cyclomatic_complexity = self.quality_analyzer.calculate_cyclomatic_complexity(code, language)
        doc_coverage = self.quality_analyzer.calculate_doc_coverage(code, language)
        
        # Determine complexity level if not provided
        if complexity_level is None:
            if cyclomatic_complexity <= 5:
                complexity_level = "simple"
            elif cyclomatic_complexity <= 10:
                complexity_level = "intermediate"
            else:
                complexity_level = "advanced"
        
        # Prepare full metadata
        information = {
            "type": "code_pattern",
            "name": name,
            "language": language,
            "code": code,
            "explanation": explanation,
            "tags": tags or [],
            "complexity_level": complexity_level,
            "dependencies": dependencies or [],
            "quality_metrics": {
                "cyclomatic_complexity": cyclomatic_complexity,
                "documentation_coverage": round(doc_coverage, 2)
            },
            "version_info": {
                "version": version,
                "previous_version_id": previous_version_id,
                "change_log": change_log,
                "updated_at": datetime.now().isoformat()
            }
        }
        
        if user_rating is not None:
            information["user_rating"] = user_rating
        
        # Assign a unique ID (in a real implementation this would be handled by Qdrant)
        information["id"] = f"{name.lower().replace(' ', '_')}_{version}"
        
        # In a real implementation, this would call the qdrant-store-memory function
        # For demonstration purposes, we just return the formatted object
        print(f"Would store pattern '{name}' (version {version}) in Qdrant")
        return information

    def find_similar_code(
        self, 
        query: str,
        language: Optional[str] = None,
        complexity_level: Optional[str] = None,
        min_rating: Optional[float] = None,
        required_tags: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Find code patterns similar to the provided query with filters.
        
        Parameters:
        -----------
        query : str
            Search query describing the code pattern needed
        language : str, optional
            Filter by programming language
        complexity_level : str, optional
            Filter by complexity level
        min_rating : float, optional
            Minimum user rating
        required_tags : list, optional
            Tags that must be present in results
            
        Returns:
        --------
        list
            List of matching code patterns (would be retrieved from Qdrant)
        """
        # Build filter conditions for display purposes
        filters = []
        if language:
            filters.append(f"language='{language}'")
        if complexity_level:
            filters.append(f"complexity_level='{complexity_level}'")
        if min_rating:
            filters.append(f"user_rating>={min_rating}")
        if required_tags:
            filters.append(f"tags include {required_tags}")
        
        filter_str = " AND ".join(filters)
        if filter_str:
            print(f"Would search Qdrant for: '{query}' WITH FILTERS: {filter_str}")
        else:
            print(f"Would search Qdrant for: '{query}'")
        
        # In a real implementation, this would call the qdrant-find-memories function
        # For demonstration purposes, we just return an empty list
        return []

def main():
    """Main function to demonstrate the enhanced utility."""
    storage = EnhancedCodeStorage()
    
    # Example usage
    pattern = storage.store_code_pattern(
        name="Binary search implementation",
        code="""def binary_search(arr, target):
    '''
    Perform binary search on a sorted array.
    
    Args:
        arr: A sorted array of elements
        target: The element to search for
        
    Returns:
        The index of the target if found, -1 otherwise
    '''
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        # Check if target is present at mid
        if arr[mid] == target:
            return mid
        
        # If target is greater, ignore left half
        elif arr[mid] < target:
            left = mid + 1
        
        # If target is smaller, ignore right half
        else:
            right = mid - 1
    
    # Target is not present in the array
    return -1""",
        explanation="An efficient O(log n) algorithm for finding elements in a sorted array.",
        language="python",
        tags=["algorithm", "searching", "divide and conquer", "binary search"],
        dependencies=["None - standard library only"],
        user_rating=4.8
    )
    
    print("\nStored pattern information:")
    print(json.dumps(pattern, indent=2))
    
    print("\nRetrieving similar patterns:")
    storage.find_similar_code(
        query="efficient search algorithm for sorted data",
        language="python",
        complexity_level="intermediate",
        min_rating=4.0,
        required_tags=["algorithm", "searching"]
    )
    
    # Example of storing an updated version
    print("\nStoring updated version:")
    updated_pattern = storage.store_code_pattern(
        name="Binary search implementation",
        code="""def binary_search(arr, target):
    '''
    Perform binary search on a sorted array.
    
    Args:
        arr: A sorted array of elements
        target: The element to search for
        
    Returns:
        The index of the target if found, -1 otherwise
        
    Examples:
        >>> binary_search([1, 2, 3, 4, 5], 3)
        2
        >>> binary_search([1, 2, 3, 4, 5], 6)
        -1
    '''
    left, right = 0, len(arr) - 1
    
    while left <= right:
        # Use bit shift for better performance
        mid = left + ((right - left) >> 1)
        
        # Check if target is present at mid
        if arr[mid] == target:
            return mid
        
        # If target is greater, ignore left half
        elif arr[mid] < target:
            left = mid + 1
        
        # If target is smaller, ignore right half
        else:
            right = mid - 1
    
    # Target is not present in the array
    return -1""",
        explanation="An efficient O(log n) algorithm for finding elements in a sorted array. This implementation uses bit shifting for calculating the middle index for better performance.",
        language="python",
        tags=["algorithm", "searching", "divide and conquer", "binary search", "optimization"],
        dependencies=["None - standard library only"],
        user_rating=4.9,
        version=2,
        previous_version_id="binary_search_implementation_1",
        change_log="Improved performance by using bit shift for mid calculation. Added example usage in docstring."
    )
    
    print("\nUpdated pattern information:")
    print(json.dumps(updated_pattern, indent=2))

if __name__ == "__main__":
    main()
