"""Core functionality for extracting file contents."""

import os
import logging
import re
from pathlib import Path
from typing import Union, Optional, List, Pattern

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def extract_file_contents(
    directory: Union[str, Path], 
    output_file: Union[str, Path], 
    recursive: bool = True, 
    include_binary: bool = False,
    file_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    verbose: bool = False
) -> bool:
    """
    Extract the contents of all files in the given directory and write them to a single output file.
    
    Args:
        directory (str or Path): Path to the directory to process
        output_file (str or Path): Path to the output file
        recursive (bool): Whether to process subdirectories recursively
        include_binary (bool): Whether to include binary files
        file_patterns (List[str], optional): List of file patterns to include (e.g., ["*.py", "*.txt"])
        exclude_patterns (List[str], optional): List of file patterns to exclude (e.g., ["*.log", "*.tmp"])
        verbose (bool): Whether to print detailed progress information
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Set log level based on verbose flag
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    
    dir_path = Path(directory)
    if not dir_path.exists() or not dir_path.is_dir():
        logger.error(f"Error: {directory} is not a valid directory")
        return False
    
    # Compile file patterns if provided
    include_regex = None
    exclude_regex = None
    
    if file_patterns:
        pattern_strings = [pattern.replace('.', '\\.').replace('*', '.*') for pattern in file_patterns]
        include_regex = re.compile('|'.join(f'^{pattern}$' for pattern in pattern_strings))
    
    if exclude_patterns:
        pattern_strings = [pattern.replace('.', '\\.').replace('*', '.*') for pattern in exclude_patterns]
        exclude_regex = re.compile('|'.join(f'^{pattern}$' for pattern in pattern_strings))
    
    # Initialize counters
    processed_files = 0
    skipped_files = 0
    
    try:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            # Function to process each file
            def process_file(file_path: Path) -> None:
                nonlocal processed_files, skipped_files
                
                try:
                    # Check if file matches include/exclude patterns
                    file_name = file_path.name
                    
                    # Skip if file doesn't match include pattern
                    if include_regex and not include_regex.match(file_name):
                        logger.debug(f"Skipping file (doesn't match include pattern): {file_path}")
                        skipped_files += 1
                        return
                    
                    # Skip if file matches exclude pattern
                    if exclude_regex and exclude_regex.match(file_name):
                        logger.debug(f"Skipping file (matches exclude pattern): {file_path}")
                        skipped_files += 1
                        return
                    
                    # Skip binary files unless explicitly included
                    if not include_binary:
                        try:
                            # Try to read the first few bytes to check if it might be binary
                            with open(file_path, 'rb') as test_f:
                                content_start = test_f.read(1024)
                                # Improved binary check
                                if b'\x00' in content_start or is_likely_binary(content_start):
                                    logger.info(f"Skipping binary file: {file_path}")
                                    skipped_files += 1
                                    return
                        except Exception as e:
                            logger.error(f"Error checking if file is binary {file_path}: {e}")
                            skipped_files += 1
                            return
                    
                    # Read and write the file content
                    try:
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
                        
                        logger.info(f"Processed: {file_path}")
                        processed_files += 1
                    except Exception as e:
                        logger.error(f"Error reading file {file_path}: {e}")
                        skipped_files += 1
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")
                    skipped_files += 1
            
            # Process directory
            if recursive:
                for root, dirs, files in os.walk(dir_path):
                    # Skip hidden directories
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    
                    # Process each file in the current directory
                    logger.debug(f"Processing directory: {root}")
                    for file in files:
                        if not file.startswith('.'):  # Skip hidden files
                            process_file(Path(root) / file)
                    
                    # Print subdirectory info to output file
                    if dirs:
                        subdirs = ", ".join(dirs)
                        out_f.write(f"\n{'=' * 80}\n")
                        out_f.write(f"SUBDIRECTORIES in {root}:\n{subdirs}\n")
                        out_f.write(f"{'=' * 80}\n\n")
            else:
                # Just process files in the top directory
                logger.debug(f"Processing top-level directory: {dir_path}")
                for item in dir_path.iterdir():
                    if item.is_file() and not item.name.startswith('.'):  # Skip hidden files
                        process_file(item)
                    elif item.is_dir():
                        out_f.write(f"\n{'=' * 80}\n")
                        out_f.write(f"SUBDIRECTORY (not processed): {item}\n")
                        out_f.write(f"{'=' * 80}\n\n")
            
            logger.info(f"\nAll file contents have been written to {output_file}")
            logger.info(f"Files processed: {processed_files}")
            logger.info(f"Files skipped: {skipped_files}")
            return True
            
    except Exception as e:
        logger.error(f"Error: {e}")
        return False

def is_likely_binary(content: bytes) -> bool:
    """
    Improved check to determine if content is likely binary.
    
    Args:
        content (bytes): File content to check
        
    Returns:
        bool: True if content is likely binary, False otherwise
    """
    # Check for common binary file signatures
    if len(content) > 4:
        # Check for common file signatures
        if (content.startswith(b'PK\x03\x04') or  # ZIP, DOCX, XLSX, etc.
            content.startswith(b'\x1f\x8b') or    # gzip
            content.startswith(b'\x89PNG') or     # PNG
            content.startswith(b'GIF8') or        # GIF
            content.startswith(b'\xff\xd8\xff') or # JPEG
            content.startswith(b'%PDF')):         # PDF
            return True
    
    # Count control characters (excluding new lines, tabs, etc.)
    control_chars = sum(1 for byte in content[:1000] 
                       if byte < 9 or (byte > 13 and byte < 32))
    
    # If more than 10% of the first 1000 bytes are control chars, likely binary
    return (control_chars / min(1000, len(content))) > 0.1