"""Command-line interface for the filecontents library."""

import argparse
import sys
from filecontents.core import extract_file_contents

def main():
    """Run the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Extract the contents of all files in a directory to a single text file"
    )
    parser.add_argument("directory", help="Directory to process")
    parser.add_argument("output", help="Output text file")
    parser.add_argument("-r", "--recursive", action="store_true", default=True,
                        help="Process subdirectories recursively (default: True)")
    parser.add_argument("--no-recursive", action="store_false", dest="recursive",
                        help="Do not process subdirectories recursively")
    parser.add_argument("-b", "--include-binary", action="store_true", 
                        help="Attempt to include binary files (may cause errors)")
    
    args = parser.parse_args()
    
    success = extract_file_contents(
        args.directory, 
        args.output, 
        args.recursive, 
        args.include_binary
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
