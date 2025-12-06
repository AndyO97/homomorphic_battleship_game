"""
Pytest configuration for test discovery and path setup.

This module ensures the src directory is added to sys.path BEFORE
any test modules are imported. This allows tests to use clean,
simple imports like 'from board import Board' instead of using
sys.path manipulation in each test file.

The conftest.py file is automatically loaded by pytest before
collecting tests, making it the ideal place for this setup.
"""

import sys
from pathlib import Path

# Add src directory to path - only once, and only if not already present
src_path = str(Path(__file__).parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)
