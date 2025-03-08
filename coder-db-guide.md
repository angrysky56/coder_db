# Coder DB - AI Memory Enhancement System Usage Guide

This guide provides practical instructions for using the AI memory enhancement system to improve your coding capabilities through structured database integration.

## System Overview

The Coder DB system integrates three powerful database technologies to enhance AI coding capabilities:

1. **Qdrant Vector Database**: Semantic search and retrieval of code patterns
2. **SQLite Database**: Structured algorithm storage with versioning
3. **Knowledge Graph**: Representing relationships between coding concepts

All three systems are **already set up and operational** in your environment.

## How to Use the System

### 1. Storing Code Patterns in Qdrant

Use the Qdrant memory system to store reusable code patterns, solutions, and best practices:

```python
# Store a code pattern in Qdrant
qdrant-store-memory({
    "type": "code_pattern",
    "name": "Python decorator pattern",
    "language": "python",
    "code": "def my_decorator(func):\n    def wrapper(*args, **kwargs):\n        # Do something before\n        result = func(*args, **kwargs)\n        # Do something after\n        return result\n    return wrapper",
    "explanation": "Decorators provide a way to modify functions without changing their code.",
    "tags": ["python", "decorator", "metaprogramming"],
    "complexity": "intermediate"
})
```

### 2. Retrieving Code from Qdrant

Search for previously stored code patterns using natural language queries:

```python
# Find code patterns by description
qdrant-find-memories("efficient searching algorithm")

# Find code patterns by specific tag or concept
qdrant-find-memories("python decorator pattern")
```

### 3. Working with the SQLite Algorithm Database

The SQLite database provides structured storage for algorithms with versioning. Use SQL queries to interact with the database:

**View all algorithms:**
```sql
SELECT * FROM algorithms;
```

**Get specific algorithm versions:**
```sql
SELECT a.name, v.version_number, v.code 
FROM algorithms a 
JOIN algorithm_versions v ON a.id = v.algorithm_id 
WHERE a.name = 'Binary Search';
```

**Add a new algorithm:**
```sql
-- First, insert the algorithm metadata
INSERT INTO algorithms (name, description) 
VALUES ('Insertion Sort', 'A simple sorting algorithm');

-- Then, add the implementation
INSERT INTO algorithm_versions (algorithm_id, version_number, code) 
VALUES (
    (SELECT id FROM algorithms WHERE name = 'Insertion Sort' ORDER BY id DESC LIMIT 1), 
    1, 
    'def insertion_sort(arr):\n    for i in range(1, len(arr)):\n        key = arr[i]\n        j = i-1\n        while j >= 0 and key < arr[j]:\n            arr[j+1] = arr[j]\n            j -= 1\n        arr[j+1] = key\n    return arr'
);
```

**Store performance metrics:**
```sql
INSERT INTO performance_metrics (version_id, input_size, execution_time_ms, memory_usage_kb) 
VALUES (
    (SELECT id FROM algorithm_versions WHERE algorithm_id = 
        (SELECT id FROM algorithms WHERE name = 'Insertion Sort') AND version_number = 1),
    1000, 
    25.3, 
    512.0
);
```

### 4. Knowledge Graph Integration

The Knowledge Graph represents relationships between coding concepts, patterns, and solutions:

**Search for nodes:**
```python
# Search for specific concepts in the graph
search_nodes("sorting algorithm")
```

**Add a new concept:**
```python
# Add a new concept to the graph
create_entities({
    "entities": [
        {
            "name": "Dynamic Programming",
            "entityType": "Technique",
            "observations": [
                "An algorithmic technique for solving complex problems by breaking them down into simpler subproblems",
                "Uses memoization to avoid redundant calculations"
            ]
        }
    ]
})
```

**Create relationships:**
```python
# Connect concepts in the graph
create_relations({
    "relations": [
        {
            "from": "Dynamic Programming", 
            "to": "Recursion", 
            "relationType": "related to"
        }
    ]
})
```

## Practical Workflows

### Creating a New Project with Templates

Use the project template generator to create a standardized Python project:

```bash
# Create a new project from template
cd /home/ty/Repositories/ai_workspace
python coder_db/project_templates/python_project_template.py my_new_project --author "Your Name" --email "your.email@example.com"
```

### Solving a Coding Problem

1. **Break down the problem** using sequential thinking
2. **Search for relevant patterns** in Qdrant with `qdrant-find-memories`
3. **Find algorithms** in SQLite that might help solve the problem
4. **Identify relevant concepts** in the Knowledge Graph
5. **Implement a solution** based on retrieved patterns
6. **Store the solution** back in the system for future use

### Enhancing Code Quality

1. Use the `CodeQualityAnalyzer` in `enhanced_code_storage.py` to analyze code quality
2. Calculate cyclomatic complexity and documentation coverage
3. Use the metrics to improve code quality before storing
4. Reference the `quality_metrics.md` document for best practices

## Example: Complete Workflow

Here's a complete workflow example for storing a new sorting algorithm:

1. **Implement the algorithm with proper documentation:**

```python
def heap_sort(arr):
    """
    Implementation of heap sort algorithm.
    
    Args:
        arr: List of elements to be sorted
        
    Returns:
        Sorted list
        
    Time Complexity: O(n log n)
    Space Complexity: O(1)
    """
    n = len(arr)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # Swap
        heapify(arr, i, 0)
    
    return arr

def heapify(arr, n, i):
    """
    Heapify subtree rooted at index i.
    
    Args:
        arr: Array representation of heap
        n: Size of the heap
        i: Index of the subtree root
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    # Check if left child exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    # Check if right child exists and is greater than root
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    # Change root if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # Swap
        heapify(arr, n, largest)  # Heapify the affected subtree
```

2. **Store in SQLite:**

```sql
-- Add algorithm metadata
INSERT INTO algorithms (name, description) 
VALUES ('Heap Sort', 'A comparison-based sorting algorithm that uses a binary heap data structure');

-- Add implementation
INSERT INTO algorithm_versions (algorithm_id, version_number, code) 
VALUES (
    (SELECT id FROM algorithms WHERE name = 'Heap Sort' ORDER BY id DESC LIMIT 1), 
    1, 
    '-- Full heap sort code here'
);
```

3. **Store in Qdrant with quality metrics:**

```python
# Calculate quality metrics
from enhanced_code_storage import CodeQualityAnalyzer, EnhancedCodeStorage

storage = EnhancedCodeStorage()
storage.store_code_pattern(
    name="Heap Sort implementation",
    code="def heap_sort(arr):\n    # Full code here...",
    explanation="An efficient O(n log n) comparison-based sorting algorithm that uses a binary heap data structure.",
    language="python",
    tags=["algorithm", "sorting", "heap", "comparison sort"],
    dependencies=["None - standard library only"]
)
```

4. **Update Knowledge Graph:**

```python
# Add heap sort to knowledge graph
create_entities({
    "entities": [
        {
            "name": "Heap Sort",
            "entityType": "Algorithm",
            "observations": [
                "Comparison-based sorting algorithm with O(n log n) time complexity.",
                "Uses a binary heap data structure."
            ]
        }
    ]
})

# Connect to related concepts
create_relations({
    "relations": [
        {
            "from": "Heap Sort", 
            "to": "Comparison Sort", 
            "relationType": "is a"
        },
        {
            "from": "Heap Sort", 
            "to": "Binary Heap", 
            "relationType": "uses"
        }
    ]
})
```

## Implementation Best Practices

1. **Always provide comprehensive metadata** when storing code patterns
2. **Include documentation and examples** with each stored pattern
3. **Calculate and store quality metrics** to ensure high-quality code
4. **Create relevant knowledge graph connections** to improve retrievability
5. **Version your algorithms** to track improvements and changes
