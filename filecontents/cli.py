"""Command-line interface for the filecontents library."""

import argparse
import sys
import logging
from filecontents.core import extract_file_contents

def main():
    """Run the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Extract the contents of all files in a directory to a single text file"
    )
    parser.add_argument("directory", help="Directory to process")
    parser.add_argument("output", help="Output text file")
    
    # Processing options
    parser.add_argument("-r", "--recursive", action="store_true", default=True,
                        help="Process subdirectories recursively (default: True)")
    parser.add_argument("--no-recursive", action="store_false", dest="recursive",
                        help="Do not process subdirectories recursively")
    parser.add_argument("-b", "--include-binary", action="store_true", 
                        help="Attempt to include binary files (may cause errors)")
    
    # File filtering options
    parser.add_argument("-i", "--include", action="append", metavar="PATTERN",
                        help="Include only files matching the pattern (e.g., '*.py'). Can be specified multiple times.")
    parser.add_argument("-e", "--exclude", action="append", metavar="PATTERN",
                        help="Exclude files matching the pattern (e.g., '*.log'). Can be specified multiple times.")
    
    # Output options
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose output")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Suppress all output except errors")
    
    args = parser.parse_args()
    
    # Configure logging based on verbosity
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    elif args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    # Run the core function
    success = extract_file_contents(
        directory=args.directory, 
        output_file=args.output, 
        recursive=args.recursive, 
        include_binary=args.include_binary,
        file_patterns=args.include,
        exclude_patterns=args.exclude,
        verbose=args.verbose
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())