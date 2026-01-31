"""A-maze-ing: Maze generator and solver with interactive visualization."""

import sys
from mazegen.render import MazeRenderer
from mazegen.parser import parse_file


def main() -> None:
    """Main entry point for A-maze-ing interactive maze generator."""
    try:
        # Parse config if provided
        config_file = sys.argv[1] if len(sys.argv) > 1 else "config.txt"
        config = parse_file(config_file)
        
        # Initialize and run pygame renderer
        renderer = MazeRenderer(
            width=config.width,
            height=config.height,
            cell_size=25
        )
        renderer.run()
    except FileNotFoundError:
        print(f"Config file not found. Using defaults.")
        renderer = MazeRenderer(width=25, height=25, cell_size=25)
        renderer.run()
    except KeyboardInterrupt:
        print("\nExited by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
