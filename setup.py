from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="filecontents",
    version="0.1.0",
    author="MMWilliams",
    author_email="maureesewilliams@gmail.com",
    description="A library to extract file contents from directories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MMWilliams/filecontents",
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