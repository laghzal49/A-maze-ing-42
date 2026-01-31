"""Configuration parser and validator for maze generation."""

from typing import Optional, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class MazeConfig:
    """Configuration for maze generation with validation."""
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None
    algo: str = "dfs"
    display: bool = True

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        self._validate()

    def _validate(self) -> None:
        """Validate all configuration parameters.

        Raises:
            ValueError: If any validation check fails
        """
        # Validate WIDTH and HEIGHT > 0
        if self.width <= 0:
            raise ValueError(f"WIDTH must be > 0, got {self.width}")
        if self.height <= 0:
            raise ValueError(f"HEIGHT must be > 0, got {self.height}")

        # Validate ENTRY and EXIT are inside bounds
        entry_x, entry_y = self.entry
        if not (0 <= entry_x < self.width and 0 <= entry_y < self.height):
            raise ValueError(
                f"ENTRY ({entry_x}, {entry_y}) is out of bounds "
                f"[0-{self.width-1}, 0-{self.height-1}]"
            )

        exit_x, exit_y = self.exit
        if not (0 <= exit_x < self.width and 0 <= exit_y < self.height):
            raise ValueError(
                f"EXIT ({exit_x}, {exit_y}) is out of bounds "
                f"[0-{self.width-1}, 0-{self.height-1}]"
            )

        # Validate ENTRY and EXIT are different
        if self.entry == self.exit:
            raise ValueError(
                f"ENTRY and EXIT must be different, both are {self.entry}"
            )

        # Validate OUTPUT_FILE is not empty
        if not self.output_file or not self.output_file.strip():
            raise ValueError("OUTPUT_FILE cannot be empty")

        # Validate PERFECT is bool
        if not isinstance(self.perfect, bool):
            raise ValueError(f"PERFECT must be True/False, got {self.perfect}")

        # Validate ALGO if provided
        valid_algos = ["dfs", "binary_tree"]
        if self.algo not in valid_algos:
            raise ValueError(
                f"ALGO must be one of {valid_algos}, got {self.algo}"
            )

        # Validate DISPLAY is bool
        if not isinstance(self.display, bool):
            raise ValueError(f"DISPLAY must be True/False, got {self.display}")

        # Validate SEED if provided
        if self.seed is not None and not isinstance(self.seed, int):
            raise ValueError(f"SEED must be an integer, got {self.seed}")


def parse_dict(config_dict: Dict[str, Any]) -> MazeConfig:
    """Parse configuration from dictionary with validation.

    Args:
        config_dict (dict): Configuration dictionary with keys:
            - width (int): Width of maze (required, > 0)
            - height (int): Height of maze (required, > 0)
            - entry (tuple): Entry point (required, must be in bounds)
            - exit (tuple): Exit point (required, must be in bounds)
            - output_file (str): Output file path (required, not empty)
            - perfect (bool): Generate perfect maze (required)
            - seed (int): Random seed (optional)
            - algo (str): Algorithm to use (optional, default "dfs")
            - display (bool): Display output (optional, default True)

    Returns:
        MazeConfig: Validated configuration object

    Raises:
        KeyError: If required keys are missing
        ValueError: If validation fails
    """
    required_keys = {"width", "height", "entry", "exit", "output_file", "perfect"}
    provided_keys = set(config_dict.keys())

    missing_keys = required_keys - provided_keys
    if missing_keys:
        raise KeyError(f"Missing required configuration keys: {missing_keys}")

    return MazeConfig(
        width=config_dict["width"],
        height=config_dict["height"],
        entry=tuple(config_dict["entry"]),
        exit=tuple(config_dict["exit"]),
        output_file=config_dict["output_file"],
        perfect=config_dict["perfect"],
        seed=config_dict.get("seed"),
        algo=config_dict.get("algo", "dfs"),
        display=config_dict.get("display", True),
    )


def parse_file(filepath: str) -> MazeConfig:
    """Parse configuration from text file.

    File format (one key=value per line):
    WIDTH=10
    HEIGHT=10
    ENTRY=0,0
    EXIT=9,9
    OUTPUT_FILE=maze.txt
    PERFECT=True
    SEED=42
    ALGO=dfs
    DISPLAY=True

    Args:
        filepath (str): Path to configuration file

    Returns:
        MazeConfig: Validated configuration object

    Raises:
        FileNotFoundError: If file not found
        ValueError: If parsing or validation fails
    """
    config_dict: Dict[str, Any] = {}

    try:
        with open(filepath, "r") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ValueError(
                        f"Line {line_num}: Invalid format, "
                        f"expected KEY=VALUE"
                    )

                key, value = line.split("=", 1)
                key = key.strip().upper()
                value = value.strip()

                # Parse different types
                if key in ("WIDTH", "HEIGHT"):
                    try:
                        config_dict[key.lower()] = int(value)
                    except ValueError:
                        raise ValueError(
                            f"Line {line_num}: {key} must be an integer, got '{value}'"
                        )

                elif key == "ENTRY" or key == "EXIT":
                    try:
                        coords = tuple(map(int, value.split(",")))
                        if len(coords) != 2:
                            raise ValueError("Must have exactly 2 coordinates")
                        config_dict[key.lower()] = coords
                    except ValueError as e:
                        raise ValueError(
                            f"Line {line_num}:{key} must be X,Y "
                            f"format, got '{value}'. {e}"
                        )

                elif key == "OUTPUT_FILE":
                    config_dict[key.lower()] = value

                elif key == "PERFECT" or key == "DISPLAY":
                    if value.lower() in ("true", "1", "yes"):
                        config_dict[key.lower()] = True
                    elif value.lower() in ("false", "0", "no"):
                        config_dict[key.lower()] = False
                    else:
                        raise ValueError(
                            f"Line {line_num}: {key} must be True/False, got '{value}'"
                        )

                elif key == "SEED":
                    try:
                        config_dict[key.lower()] = int(value)
                    except ValueError:
                        raise ValueError(
                            f"Line {line_num}: SEED must be an integer, got '{value}'"
                        )

                elif key == "ALGO":
                    config_dict[key.lower()] = value.lower()

                else:
                    raise ValueError(
                        f"Line {line_num}: Unknown configuration key '{key}'")

    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {filepath}")

    return parse_dict(config_dict)
