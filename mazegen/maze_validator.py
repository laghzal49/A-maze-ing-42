"""
This file has been replaced by parser.py

The new parser.py includes validation in the MazeConfig dataclass:
- WIDTH, HEIGHT > 0
- ENTRY and EXIT within bounds
- ENTRY != EXIT
- OUTPUT_FILE not empty
- PERFECT must be True/False
- Optional: SEED, ALGO, DISPLAY

All validation happens in MazeConfig.__post_init__()

Usage:
    from mazegen.parser import MazeConfig, parse_file

    # Validation happens automatically
    try:
        config = parse_file('config.txt')
        print("Valid configuration!")
    except ValueError as e:
        print(f"Invalid config: {e}")
"""

# For backwards compatibility
from .parser import MazeConfig


def validate_maze_config(config_dict):
    """Validate maze configuration dictionary."""
    try:
        MazeConfig(
            width=config_dict.get('width', 0),
            height=config_dict.get('height', 0),
            entry=config_dict.get('entry', (0, 0)),
            exit=config_dict.get('exit', (0, 0)),
            perfect=config_dict.get('perfect', True),
            output_file=config_dict.get('output_file', 'maze.txt'),
            seed=config_dict.get('seed'),
            algo=config_dict.get('algo', 'dfs'),
            display=config_dict.get('display', False)
        )
        return True
    except ValueError:
        return False


__all__ = ["validate_maze_config", "MazeConfig"]
