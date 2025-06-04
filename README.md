# FileContents

A Python library for extracting file contents from directories and compiling them into a single output file with advanced filtering capabilities.

## Installation

```bash
pip install filecontents
```

Or install directly from the repository:

```bash
pip install git+https://github.com/MMWilliams/filecontents.git
```

## Quick Start

```bash
# Basic usage - extract all text files
filecontents /path/to/directory output.txt

# Skip common directories and only include source code
filecontents my_project source.txt -i "*.py" -i "*.js" -s "__pycache__" -s "node_modules" -s ".git"
```

## Usage

### As a Library

```python
from filecontents import extract_file_contents

# Basic extraction
extract_file_contents(
    directory="path/to/directory",
    output_file="output.txt",
    recursive=True,  # Process subdirectories recursively (default)
    include_binary=False  # Skip binary files (default)
)

# Advanced filtering - Python project example
extract_file_contents(
    directory="my_project",
    output_file="python_code.txt",
    recursive=True,
    file_patterns=["*.py"],  # Only include Python files
    exclude_patterns=["*_test.py", "*_tests.py"],  # Exclude test files
    skip_dirs=["__pycache__", ".git", "venv", "env", "*.egg-info"]  # Skip these directories
)

# Web development project example
extract_file_contents(
    directory="web_app", 
    output_file="web_source.txt",
    file_patterns=["*.js", "*.css", "*.html", "*.json"],
    exclude_patterns=["*.min.js", "*.min.css"],
    skip_dirs=["node_modules", "dist", "build", ".git", ".next"]
)
```

### Command-Line Interface

```bash
# Basic usage
filecontents /path/to/directory output.txt

# Process only top-level files (no subdirectories)
filecontents /path/to/directory output.txt --no-recursive

# Include binary files (may cause encoding errors)
filecontents /path/to/directory output.txt -b

# Skip specific directories (can use multiple times)
filecontents /path/to/directory output.txt --skip-dirs node_modules --skip-dirs __pycache__

# Complete example: Python project with filtering
filecontents my_project python_files.txt \
  -i "*.py" -i "*.md" \
  -e "*_test.py" -e "*.pyc" \
  -s "__pycache__" -s ".git" -s "venv" -s "build"

# Web project example
filecontents web_app source.txt \
  -i "*.js" -i "*.css" -i "*.html" -i "*.json" \
  -e "*.min.*" \
  -s "node_modules" -s "dist" -s ".git"
```

## Features

- 📁 **Extract text content** from all files in a directory
- 🔄 **Recursive traversal** of subdirectories (optional)
- 🚫 **Skip binary files** by default (configurable)
- 📂 **Skip directories by pattern** - exclude `node_modules`, `__pycache__`, `.git`, etc.
- 🎯 **File filtering** with include/exclude patterns (wildcards supported)
- 📝 **Formatted output** with clear file boundaries and headers
- 📊 **Directory listings** included in output
- 🔍 **Verbose logging** for debugging
- ⚡ **Performance optimized** - skipped directories aren't traversed

## Advanced Filtering

### File Patterns
- **Include patterns** (`-i` or `--include`): Only process files matching these patterns
- **Exclude patterns** (`-e` or `--exclude`): Skip files matching these patterns
- **Examples**: `*.py`, `*.txt`, `config.*`, `*_backup.*`, `test_*.py`

### Directory Patterns  
- **Skip directories** (`-s` or `--skip-dirs`): Skip directories matching these patterns
- **Common examples**:
  - `node_modules` - Skip Node.js dependencies
  - `__pycache__` - Skip Python cache directories  
  - `.git` - Skip Git repositories
  - `venv` or `env` - Skip Python virtual environments
  - `*.tmp` - Skip any directory ending with .tmp
  - `build`, `dist` - Skip build/distribution directories
  - `coverage` - Skip test coverage directories

### Pattern Syntax
- Use `*` as a wildcard for any characters
- Use exact names for specific directories/files
- Patterns are case-sensitive
- Examples:
  - `*.log` matches `error.log`, `debug.log`, `app.log`
  - `test_*` matches `test_file.py`, `test_data.txt`
  - `node_modules` matches exactly `node_modules`
  - `*.egg-info` matches `mypackage.egg-info`

## Real-World Examples

### Python Development
```bash
# Extract all Python source code, skip virtual env and cache
filecontents my_python_app python_source.txt \
  -i "*.py" -i "*.pyi" -i "requirements*.txt" -i "*.toml" \
  -e "*_test.py" -e "*_tests.py" \
  -s "__pycache__" -s "venv" -s "env" -s ".git" -s "*.egg-info" -s "build" -s "dist"
```

### Web Development (React/Node.js)
```bash
# Extract frontend source code, skip dependencies and build files  
filecontents react_app frontend_source.txt \
  -i "*.js" -i "*.jsx" -i "*.ts" -i "*.tsx" -i "*.css" -i "*.scss" -i "*.json" \
  -e "*.min.*" -e "*.d.ts" \
  -s "node_modules" -s "build" -s "dist" -s ".next" -s "coverage" -s ".git"
```

### Documentation Only
```bash
# Extract only documentation and configuration files
filecontents project documentation.txt \
  -i "*.md" -i "*.rst" -i "*.txt" -i "*.yaml" -i "*.yml" -i "*.toml" \
  -s ".git" -s "node_modules" -s "__pycache__" -s "images" -s "assets"
```

### Configuration Files
```bash
# Extract configuration files from a server setup
filecontents server_configs config_files.txt \
  -i "*.conf" -i "*.ini" -i "*.yaml" -i "*.yml" -i "*.json" -i "*.toml" \
  -s "logs" -s "tmp" -s "temp" -s "*.bak" -s "backups" -s ".git"
```

### Large Codebase Analysis
```bash
# Extract with verbose logging for debugging
filecontents large_project analysis.txt \
  -i "*.py" -i "*.js" -i "*.java" -i "*.cpp" -i "*.h" \
  -e "*.min.*" -e "*_old.*" -e "*.backup" \
  -s "__pycache__" -s "node_modules" -s ".git" -s "build" -s "target" \
  --verbose
```

## CLI Options Reference

| Option | Short | Description |
|--------|-------|-------------|
| `--recursive` | `-r` | Process subdirectories recursively (default) |
| `--no-recursive` | | Skip subdirectories |
| `--include-binary` | `-b` | Include binary files (may cause errors) |
| `--include PATTERN` | `-i` | Include only files matching pattern |
| `--exclude PATTERN` | `-e` | Exclude files matching pattern |
| `--skip-dirs PATTERN` | `-s` | Skip directories matching pattern |
| `--verbose` | `-v` | Enable detailed logging |
| `--quiet` | `-q` | Suppress output except errors |

## Performance Tips

- Use `--skip-dirs` to avoid traversing large directories like `node_modules`
- Use specific `--include` patterns instead of broad extraction + exclusion
- Enable `--verbose` mode to see what's being processed
- The tool automatically skips hidden files and directories (starting with `.`)

## License

MIT