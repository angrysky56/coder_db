#!/usr/bin/env python3
"""
Python Project Template Generator

This script generates a standardized Python project structure with
best practices for documentation, testing, and code quality.
"""

import os
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Union, Any


class ProjectTemplate:
    """
    Python project template generator with best practices built-in.
    
    This class helps create a new Python project with a standardized directory
    structure, documentation templates, testing setup, and development tools.
    """
    
    def __init__(
        self,
        project_name: str,
        description: str,
        author: str,
        email: str,
        use_venv: bool = True,
        include_tests: bool = True,
        use_black: bool = True,
        use_flake8: bool = True,
        use_mypy: bool = True,
        include_ci: bool = True
    ):
        """
        Initialize project template generator.
        
        Parameters
        ----------
        project_name : str
            Name of the project (will be used for the main package)
        description : str
            Short description of the project
        author : str
            Author's name
        email : str
            Author's email
        use_venv : bool, optional
            Set up a virtual environment, by default True
        include_tests : bool, optional
            Set up testing with pytest, by default True
        use_black : bool, optional
            Set up Black for code formatting, by default True
        use_flake8 : bool, optional
            Set up Flake8 for linting, by default True
        use_mypy : bool, optional
            Set up mypy for type checking, by default True
        include_ci : bool, optional
            Set up GitHub Actions CI, by default True
        """
        self.project_name = project_name
        self.package_name = project_name.replace('-', '_').lower()
        self.description = description
        self.author = author
        self.email = email
        self.use_venv = use_venv
        self.include_tests = include_tests
        self.use_black = use_black
        self.use_flake8 = use_flake8
        self.use_mypy = use_mypy
        self.include_ci = include_ci
        
        # Base directory
        self.base_dir = Path(self.project_name)
    
    def create_directories(self) -> None:
        """Create the standard directory structure for the project."""
        # Create base directories
        dirs = [
            self.base_dir,
            self.base_dir / self.package_name,
            self.base_dir / "docs",
            self.base_dir / "scripts",
        ]
        
        # Add tests directory if requested
        if self.include_tests:
            dirs.append(self.base_dir / "tests")
        
        # Create all directories
        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)
            
        # Create empty __init__.py files
        init_files = [
            self.base_dir / self.package_name / "__init__.py",
        ]
        
        if self.include_tests:
            init_files.append(self.base_dir / "tests" / "__init__.py")
        
        for init_file in init_files:
            self._create_file(init_file, '')
    
    def create_readme(self) -> None:
        """Create a comprehensive README.md file."""
        readme_content = f"""# {self.project_name}

{self.description}

## Installation

```bash
# Clone the repository
git clone https://github.com/{self.author}/{self.project_name}.git
cd {self.project_name}

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install the package in development mode
pip install -e .
```

## Usage

```python
import {self.package_name}

# Add examples here
```

## Development

This project uses:
"""
        
        # Add development tools
        tools = []
        if self.use_black:
            tools.append("- [Black](https://black.readthedocs.io/) for code formatting")
        if self.use_flake8:
            tools.append("- [Flake8](https://flake8.pycqa.org/) for code linting")
        if self.use_mypy:
            tools.append("- [mypy](https://mypy.readthedocs.io/) for static type checking")
        if self.include_tests:
            tools.append("- [pytest](https://docs.pytest.org/) for testing")
        
        readme_content += "\n".join(tools)
        
        # Add development setup instructions
        readme_content += f"""

### Development Setup

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Check code style
black .
flake8
mypy {self.package_name}
```
"""
        
        # Add license information
        readme_content += f"""
## License

MIT License

## Author

{self.author} <{self.email}>
"""
        
        self._create_file(self.base_dir / "README.md", readme_content)
    
    def create_setup_py(self) -> None:
        """Create setup.py file for package installation."""
        setup_content = f"""#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="{self.project_name}",
    version="0.1.0",
    description="{self.description}",
    author="{self.author}",
    author_email="{self.email}",
    url="https://github.com/{self.author}/{self.project_name}",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        # Add your package dependencies here
    ],
    extras_require={{
        "dev": [
            "pytest>=7.0.0",
            {"'black>=22.1.0'," if self.use_black else ""}
            {"'flake8>=4.0.1'," if self.use_flake8 else ""}
            {"'mypy>=0.931'," if self.use_mypy else ""}
        ],
    }},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
"""
        self._create_file(self.base_dir / "setup.py", setup_content)
    
    def create_gitignore(self) -> None:
        """Create .gitignore file."""
        gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
dist/
build/
*.egg-info/

# Unit test / coverage reports
htmlcov/
.coverage
.coverage.*
.pytest_cache/

# Virtual environments
venv/
env/

# IDE files
.idea/
.vscode/
*.swp
*.swo

# Environment variables
.env

# Jupyter Notebook
.ipynb_checkpoints

# OS specific files
.DS_Store
"""
        self._create_file(self.base_dir / ".gitignore", gitignore_content)
    
    def create_config_files(self) -> None:
        """Create configuration files for development tools."""
        # pyproject.toml for Black and build system
        if self.use_black:
            pyproject_content = """[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
"""
            self._create_file(self.base_dir / "pyproject.toml", pyproject_content)
        
        # setup.cfg for flake8 and mypy
        setup_cfg_content = f"[metadata]\nname = {self.project_name}\n"
        
        if self.use_flake8:
            setup_cfg_content += """
[flake8]
max-line-length = 88
extend-ignore = E203
exclude = .git,__pycache__,build,dist
"""
        
        if self.use_mypy:
            setup_cfg_content += """
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
"""
        
        self._create_file(self.base_dir / "setup.cfg", setup_cfg_content)
    
    def create_test_files(self) -> None:
        """Create basic test files if testing is enabled."""
        if not self.include_tests:
            return
        
        test_content = f"""#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Tests for `{self.package_name}` package.
\"\"\"

import pytest
from {self.package_name} import __version__


def test_version():
    \"\"\"Test version is a string.\"\"\"
    assert isinstance(__version__, str)
"""
        self._create_file(self.base_dir / "tests" / f"test_{self.package_name}.py", test_content)
        
        # Create conftest.py
        conftest_content = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        self._create_file(self.base_dir / "tests" / "conftest.py", conftest_content)
    
    def create_ci_config(self) -> None:
        """Create GitHub Actions workflow for CI."""
        if not self.include_ci:
            return
        
        # Create .github/workflows directory
        workflows_dir = self.base_dir / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        ci_content = f"""name: Python CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10']

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{{{ matrix.python-version }}}}
      uses: actions/setup-python@v2
      with:
        python-version: ${{{{ matrix.python-version }}}}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
    - name: Lint with flake8
      if: ${'true' if self.use_flake8 else 'false'}
      run: |
        flake8 {self.package_name} tests
    - name: Check formatting with black
      if: ${'true' if self.use_black else 'false'}
      run: |
        black --check {self.package_name} tests
    - name: Type check with mypy
      if: ${'true' if self.use_mypy else 'false'}
      run: |
        mypy {self.package_name}
    - name: Test with pytest
      run: |
        pytest
"""
        self._create_file(workflows_dir / "python-ci.yml", ci_content)
    
    def create_docs(self) -> None:
        """Create basic documentation structure with MkDocs."""
        # Create mkdocs.yml
        mkdocs_content = f"""site_name: {self.project_name}
site_description: {self.description}
site_author: {self.author}

theme:
  name: material

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          setup_commands:
            - import sys
            - sys.path.append(".")

nav:
  - Home: index.md
  - Installation: installation.md
  - Usage: usage.md
  - API Reference: api.md
  - Contributing: contributing.md
  - License: license.md

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.inlinehilite
  - pymdownx.tabbed
  - pymdownx.critic
  - pymdownx.tasklist:
      custom_checkbox: true
"""
        self._create_file(self.base_dir / "mkdocs.yml", mkdocs_content)
        
        # Create docs/index.md
        index_content = f"""# {self.project_name}

{self.description}

## Features

* TODO

## Installation

```bash
pip install {self.project_name}
```

## Quick Start

```python
import {self.package_name}

# Add examples here
```
"""
        docs_dir = self.base_dir / "docs" / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)
        self._create_file(docs_dir / "index.md", index_content)
        
        # Create other documentation files
        self._create_file(docs_dir / "installation.md", "# Installation\n\n## From PyPI\n\n```bash\npip install " + self.project_name + "\n```\n\n## From Source\n\n```bash\ngit clone https://github.com/" + self.author + "/" + self.project_name + ".git\ncd " + self.project_name + "\npip install -e .\n```\n")
        self._create_file(docs_dir / "usage.md", "# Usage\n\n## Basic Usage\n\n```python\nimport " + self.package_name + "\n\n# Add examples here\n```\n")
        self._create_file(docs_dir / "api.md", f"# API Reference\n\n## {self.package_name}\n\n::: {self.package_name}\n")
        self._create_file(docs_dir / "contributing.md", "# Contributing\n\n## Development Environment\n\n```bash\n# Clone the repository\ngit clone https://github.com/" + self.author + "/" + self.project_name + ".git\ncd " + self.project_name + "\n\n# Create a virtual environment\npython -m venv venv\nsource venv/bin/activate  # On Windows: venv\\Scripts\\activate\n\n# Install development dependencies\npip install -e \".[dev]\"\n```\n\n## Running Tests\n\n```bash\npytest\n```\n\n## Code Style\n\nThis project uses Black for code formatting, Flake8 for linting, and mypy for type checking.\n\n```bash\nblack .\nflake8\nmypy " + self.package_name + "\n```\n")
        self._create_file(docs_dir / "license.md", "# License\n\nMIT License\n\nCopyright (c) 2025 " + self.author + "\n")
    
    def create_package_files(self) -> None:
        """Create basic files for the package."""
        # Create __init__.py with version
        init_content = f"""\"\"\"
{self.description}
\"\"\"

__version__ = "0.1.0"
"""
        self._create_file(self.base_dir / self.package_name / "__init__.py", init_content)
        
        # Create a core module
        core_content = f"""\"\"\"
Core functionality for {self.project_name}.
\"\"\"

def hello_world() -> str:
    \"\"\"
    Return a greeting message.
    
    Returns
    -------
    str
        A friendly greeting
    
    Examples
    --------
    >>> hello_world()
    'Hello, World!'
    """
    return "Hello, World!"
"""
        self._create_file(self.base_dir / self.package_name / "core.py", core_content)
    
    def create_pre_commit_hooks(self) -> None:
        """Create pre-commit hooks configuration."""
        precommit_content = """repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.1.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

"""
        
        if self.use_black:
            precommit_content += """-   repo: https://github.com/psf/black
    rev: 22.1.0
    hooks:
    -   id: black
        language_version: python3

"""
        
        if self.use_flake8:
            precommit_content += """-   repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
    -   id: flake8
        additional_dependencies: [flake8-docstrings]

"""
        
        if self.use_mypy:
            precommit_content += """-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.931
    hooks:
    -   id: mypy
        additional_dependencies: [types-requests]
"""
        
        self._create_file(self.base_dir / ".pre-commit-config.yaml", precommit_content)
    
    def initialize_git(self) -> None:
        """Initialize Git repository."""
        try:
            subprocess.run(["git", "init"], cwd=self.base_dir, check=True)
            print(f"Initialized Git repository in {self.base_dir}")
        except subprocess.CalledProcessError:
            print("Failed to initialize Git repository. Make sure Git is installed.")
        except FileNotFoundError:
            print("Git command not found. Make sure Git is installed and in your PATH.")
    
    def create_virtual_environment(self) -> None:
        """Create a virtual environment for the project."""
        if not self.use_venv:
            return
            
        try:
            subprocess.run(["python", "-m", "venv", "venv"], cwd=self.base_dir, check=True)
            print(f"Created virtual environment in {self.base_dir / 'venv'}")
        except subprocess.CalledProcessError:
            print("Failed to create virtual environment.")
    
    def _create_file(self, path: Path, content: str) -> None:
        """
        Create a file with the given content.
        
        Parameters
        ----------
        path : Path
            Path to the file
        content : str
            Content to write to the file
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    
    def generate(self) -> None:
        """Generate the complete project structure."""
        print(f"Generating project structure for {self.project_name}...")
        
        # Create directories and files
        self.create_directories()
        self.create_readme()
        self.create_setup_py()
        self.create_gitignore()
        self.create_config_files()
        self.create_test_files()
        self.create_ci_config()
        self.create_docs()
        self.create_package_files()
        self.create_pre_commit_hooks()
        
        # Initialize Git repository and virtual environment
        self.initialize_git()
        self.create_virtual_environment()
        
        print(f"Project {self.project_name} generated successfully!")


def main() -> None:
    """Run the project template generator."""
    parser = argparse.ArgumentParser(description="Generate a Python project structure with best practices.")
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--description", default="A Python project", help="Short description of the project")
    parser.add_argument("--author", default="Your Name", help="Author's name")
    parser.add_argument("--email", default="your.email@example.com", help="Author's email")
    parser.add_argument("--no-venv", action="store_true", help="Don't create a virtual environment")
    parser.add_argument("--no-tests", action="store_true", help="Don't set up testing")
    parser.add_argument("--no-black", action="store_true", help="Don't set up Black for formatting")
    parser.add_argument("--no-flake8", action="store_true", help="Don't set up Flake8 for linting")
    parser.add_argument("--no-mypy", action="store_true", help="Don't set up mypy for type checking")
    parser.add_argument("--no-ci", action="store_true", help="Don't set up GitHub Actions CI")
    
    args = parser.parse_args()
    
    template = ProjectTemplate(
        project_name=args.project_name,
        description=args.description,
        author=args.author,
        email=args.email,
        use_venv=not args.no_venv,
        include_tests=not args.no_tests,
        use_black=not args.no_black,
        use_flake8=not args.no_flake8,
        use_mypy=not args.no_mypy,
        include_ci=not args.no_ci
    )
    
    template.generate()


if __name__ == "__main__":
    main()
