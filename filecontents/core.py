"""Core functionality for extracting file contents."""

import os
from pathlib import Path

def extract_file_contents(directory, output_file, recursive=True, include_binary=False):
    """
    Extract the contents of all files in the given directory and write them to a single output file.
    
    Args:
        directory (str or Path): Path to the directory to process
        output_file (str or Path): Path to the output file
        recursive (bool): Whether to process subdirectories recursively
        include_binary (bool): Whether to include binary files
        
    Returns:
        bool: True if successful, False otherwise
    """
    dir_path = Path(directory)
    if not dir_path.exists() or not dir_path.is_dir():
        print(f"Error: {directory} is not a valid directory")
        return False
    
    try:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            # Function to process each file
            def process_file(file_path):
                try:
                    # Skip binary files unless explicitly included
                    if not include_binary:
                        # Try to read the first few bytes to check if it might be binary
                        with open(file_path, 'rb') as test_f:
                            content_start = test_f.read(1024)
                            # Crude binary check (could be improved)
                            if b'\x00' in content_start:
                                print(f"Skipping binary file: {file_path}")
                                return
                    
                    # Read and write the file content
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as in_f:
                        # Get the file content
                        file_content = in_f.read()
                        
                        # Write file header
                        out_f.write(f"\n{'=' * 80}\n")
                        out_f.write(f"FILE: {file_path}\n")
                        out_f.write(f"{'=' * 80}\n\n")
                        
                        # Add file path as first line
                        out_f.write(f"# File: {file_path}\n")
                        out_f.write(file_content)
                        out_f.write("\n\n")
                    print(f"Processed: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
            
            # Always crawl through all subdirectories
            if recursive:
                for root, dirs, files in os.walk(dir_path):
                    # Process each file in the current directory
                    for file in files:
                        process_file(Path(root) / file)
                    
                    # Print subdirectory info to output file
                    if dirs:
                        subdirs = ", ".join(dirs)
                        out_f.write(f"\n{'=' * 80}\n")
                        out_f.write(f"SUBDIRECTORIES in {root}:\n{subdirs}\n")
                        out_f.write(f"{'=' * 80}\n\n")
            else:
                # Just process files in the top directory
                for item in dir_path.iterdir():
                    if item.is_file():
                        process_file(item)
                    elif item.is_dir():
                        out_f.write(f"\n{'=' * 80}\n")
                        out_f.write(f"SUBDIRECTORY (not processed): {item}\n")
                        out_f.write(f"{'=' * 80}\n\n")
            
            print(f"\nAll file contents have been written to {output_file}")
            return True
            
    except Exception as e:
        print(f"Error: {e}")
        return False
