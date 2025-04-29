# FileContents

A Python library for extracting file contents from directories and compiling them into a single output file.

## Installation

```bash
pip install filecontents
```

Or install directly from the repository:

```bash
pip install git+https://github.com/MMWilliams/filecontents.git
```

## Usage

### As a Library

```python
from filecontents import extract_file_contents

# Extract all files from a directory to an output file
extract_file_contents(
    directory="path/to/directory",
    output_file="output.txt",
    recursive=True,  # Process subdirectories recursively (default)
    include_binary=False  # Skip binary files (default)
)
```

### Command-Line Interface

```bash
# Basic usage
filecontents /path/to/directory output.txt

# Skip subdirectories
filecontents /path/to/directory output.txt --no-recursive

# Include binary files (may cause errors)
filecontents /path/to/directory output.txt -b
```

## Features

- Extract text content from all files in a directory
- Optional recursive traversal of subdirectories
- Skip binary files by default (can be included with a flag)
- Formatted output with clear file boundaries and headers
- Subdirectory listings in the output file

## License

MIT