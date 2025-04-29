"""
FileContents: A library for extracting file contents from directories.

This library provides functionality to extract the contents of files from
a directory and write them to a single output file.
"""

from filecontents.core import extract_file_contents, is_likely_binary
from filecontents.cli import main

__version__ = "0.1.0"
__author__ = "MMWilliams"
__all__ = ['extract_file_contents', 'is_likely_binary', 'main']