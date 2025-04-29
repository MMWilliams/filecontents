from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="filecontents",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A library to extract file contents from directories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/filecontents",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "filecontents=filecontents.cli:main",
        ],
    },
)
