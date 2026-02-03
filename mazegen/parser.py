"""Configuration parser for maze generation."""

from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any


@dataclass
class MazeConfig:
    """Configuration for maze generation."""
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None
    algo: str = "dfs"
    delay: Optional[float] = None


def _parse_bool(value: str) -> bool:
    value_lower = value.strip().lower()
    if value_lower in {"true", "1", "yes", "y"}:
        return True
    if value_lower in {"false", "0", "no", "n"}:
        return False
    raise ValueError("PERFECT must be True or False")


def _validate_config(config: Dict[str, Any]) -> MazeConfig:
    width = config.get("width")
    height = config.get("height")
    entry = config.get("entry")
    exit_pos = config.get("exit")
    output_file = config.get("output_file")
    perfect = config.get("perfect")

    if width is None or height is None:
        raise ValueError("WIDTH and HEIGHT are required")
    if not isinstance(width, int) or not isinstance(height, int):
        raise ValueError("WIDTH and HEIGHT must be integers")
    if width <= 0 or height <= 0:
        raise ValueError("WIDTH and HEIGHT must be positive")

    if entry is None or exit_pos is None:
        raise ValueError("ENTRY and EXIT are required")
    if not (isinstance(entry, tuple) and isinstance(exit_pos, tuple)):
        raise ValueError("ENTRY and EXIT must be in x,y format")
    if entry == exit_pos:
        raise ValueError("ENTRY and EXIT must be different")
    if not (0 <= entry[0] < width and 0 <= entry[1] < height):
        raise ValueError("ENTRY is out of bounds")
    if not (0 <= exit_pos[0] < width and 0 <= exit_pos[1] < height):
        raise ValueError("EXIT is out of bounds")

    if output_file is None or not isinstance(output_file, str):
        raise ValueError("OUTPUT_FILE is required")
    if not output_file.strip():
        raise ValueError("OUTPUT_FILE must be a non-empty filename")

    if perfect is None or not isinstance(perfect, bool):
        raise ValueError("PERFECT is required")

    algo = config.get("algo", "dfs")
    if algo not in {"dfs", "binary_tree", "prim"}:
        raise ValueError("ALGO must be 'dfs', 'binary_tree', or 'prim'")

    seed = config.get("seed")
    delay = config.get("delay")

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit_pos,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
        algo=algo,
        delay=delay,
    )


def parse_dict(raw: Dict[str, Any]) -> MazeConfig:
    """Parse configuration from a dict (tests/helpers)."""
    return _validate_config(raw)


def parse_file(filepath: str) -> MazeConfig:
    """Parse configuration from text file.

    File format (one key=value per line):
    WIDTH=30
    HEIGHT=20
    ENTRY=0,0
    EXIT=29,19
    SEED=42
    ALGO=dfs

    Args:
        filepath: Path to configuration file

    Returns:
        MazeConfig: Configuration object

    Raises:
        FileNotFoundError: If file not found
        ValueError: If parsing fails
    """
    config: Dict[str, Any] = {}

    with open(filepath, "r") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(
                    f"Line {line_num}: Invalid format, expected KEY=VALUE"
                )

            key, value = line.split("=", 1)
            key = key.strip().upper()
            value = value.strip()

            try:
                if key == "WIDTH":
                    config["width"] = int(value)
                elif key == "HEIGHT":
                    config["height"] = int(value)
                elif key == "ENTRY":
                    coords = tuple(map(int, value.split(",")))
                    if len(coords) != 2:
                        raise ValueError("Must have exactly 2 coordinates")
                    config["entry"] = coords
                elif key == "EXIT":
                    coords = tuple(map(int, value.split(",")))
                    if len(coords) != 2:
                        raise ValueError("Must have exactly 2 coordinates")
                    config["exit"] = coords
                elif key == "OUTPUT_FILE":
                    config["output_file"] = value
                elif key == "PERFECT":
                    config["perfect"] = _parse_bool(value)
                elif key == "SEED":
                    config["seed"] = int(value)
                elif key == "DELAY":
                    config["delay"] = float(value)
                elif key == "ALGO":
                    config["algo"] = value.lower()
            except ValueError as e:
                raise ValueError(f"Line {line_num}: {e}")

    return _validate_config(config)
