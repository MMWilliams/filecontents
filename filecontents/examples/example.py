#!/usr/bin/env python3
"""
Example demonstrating how to use the filecontents library.
"""

from filecontents import extract_file_contents

def main():
    """Demonstrate various use cases of the filecontents library."""
    # Basic usage
    print("Example 1: Basic Usage - Extract all text files from 'src' directory to 'all_files.txt'")
    result = extract_file_contents(
        directory="src",
        output_file="all_files.txt",
        recursive=True,
        include_binary=False
    )
    print(f"Result: {'Success' if result else 'Failed'}\n")
    
    # Filtering files by pattern
    print("Example 2: Filtering - Extract only Python files from 'src' directory to 'python_files.txt'")
    result = extract_file_contents(
        directory="src",
        output_file="python_files.txt",
        recursive=True,
        include_binary=False,
        file_patterns=["*.py", "*.pyw"],
        exclude_patterns=["*_test.py"]
    )
    print(f"Result: {'Success' if result else 'Failed'}\n")
    
    # Non-recursive extraction
    print("Example 3: Non-recursive - Extract only top-level files from 'docs' directory to 'top_level.txt'")
    result = extract_file_contents(
        directory="docs",
        output_file="top_level.txt",
        recursive=False,
        include_binary=False
    )
    print(f"Result: {'Success' if result else 'Failed'}\n")
    
    # Verbose mode
    print("Example 4: Verbose mode - Extract with detailed logging to 'debug_output.txt'")
    result = extract_file_contents(
        directory="logs",
        output_file="debug_output.txt",
        recursive=True,
        include_binary=False,
        verbose=True
    )
    print(f"Result: {'Success' if result else 'Failed'}\n")

if __name__ == "__main__":
    main()