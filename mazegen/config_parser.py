"""
This file has been replaced by parser.py

The new parser module provides:
- MazeConfig dataclass with validation
- parse_file() for reading config files
- parse_dict() for programmatic config

Usage:
    from mazegen.parser import MazeConfig, parse_file

    config = parse_file('config.txt')
    print(config.width, config.height)
"""

# For backwards compatibility
from .parser import MazeConfig, parse_file, parse_dict

__all__ = ["MazeConfig", "parse_file", "parse_dict"]
