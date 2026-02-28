*This project has been created as part of the 42 curriculum by tlaghzal.*

# A-Maze-ing — This is the Way

## Overview
A-Maze-ing is a Python 3.10+ maze generator and terminal renderer. It reads a configuration file, generates a maze (optionally with a visible “42” blocked pattern), can compute a shortest path, writes a compact hex-encoded maze file, and renders the maze in either curses mode or ASCII fallback.

The project is structured to be both:
- A runnable application (`a_maze_ing.py`)
- A reusable module (`mazegen/`)

## Quick Start
```bash
python3 a_maze_ing.py config.txt
```

### Makefile Targets
```bash
make install
make run
make debug
make lint
make clean
make build
```

Notes:
- `make run` calls `python3 a_maze_ing.py config.txt`.
- If curses is not available in your terminal (e.g., non-interactive environments), the app will fall back to ASCII rendering.

## Project Layout
- `a_maze_ing.py`: Main entry point. Reads config, builds maze, handles rendering.
- `config.txt`: Example configuration file.
- `maze.txt`: Example output file produced by the generator.
- `mazegen/`: Reusable maze package:
  - `maze_generator.py`: Maze data structure and generation algorithms.
  - `path_finder.py`: Shortest-path search (BFS).
  - `parser.py`: Reads and validates config keys.
  - `output_writer.py`: Writes the hex-encoded maze output format.
  - `maze_renderer.py`: Orchestrates curses vs ASCII rendering.
  - `curses_renderer.py`: Interactive terminal UI.
  - `ascii_renderer.py`: ASCII fallback renderer.
  - `position_selector.py`: Input handling for entry/exit positions (if used by UI).
- `tests/`: Unit tests.
- `pyproject.toml`: Packaging and tooling configuration.
- `Makefile`: Shortcuts for run/build/lint/test.

## Configuration File
Each line is `KEY=VALUE`. Lines starting with `#` are ignored.

### Mandatory Keys
```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

### Optional Keys
```
SEED=42
ALGO=dfs        # dfs, prim, or hunt
DELAY=0.05
```

### Meaning of Each Key
- `WIDTH`, `HEIGHT`: Maze dimensions in cells.
- `ENTRY`, `EXIT`: Coordinates as `x,y`. Must be inside the maze and not blocked.
- `OUTPUT_FILE`: Where the hex-encoded maze will be written.
- `PERFECT`: If `True`, generates a perfect maze (one unique path between any two cells). If `False`, loops may be added.
- `SEED`: RNG seed for reproducible mazes.
- `ALGO`: Maze generation algorithm (`dfs`, `prim`, or `hunt`).
- `DELAY`: (If used by UI) Controls animation speed in curses.

## Maze Data Model
The maze grid is stored as a 2D array of wall bitmasks. Each cell uses 4 bits to indicate which walls are still closed:
- Bit 0 (`1`): North wall
- Bit 1 (`2`): East wall
- Bit 2 (`4`): South wall
- Bit 3 (`8`): West wall

A fresh maze starts with all walls present (`15`). When a passage is carved between two adjacent cells, the corresponding wall bits are cleared in both cells to keep walls consistent.

Blocked cells (the “42” pattern) are treated as solid obstacles. They are excluded from maze carving and rendering.

## Maze Generation Algorithms
### DFS (Recursive Backtracker)
- Starts from a cell and randomly explores neighbors.
- Produces long corridors and a classic maze appearance.
- Always perfect when used without extra loops.

### Prim’s Algorithm
- Grows the maze by adding random frontier edges.
- Produces a more uniform and “braided” look than DFS.
- Also perfect by default.

### Hunt-and-Kill
- A randomized hunt-and-kill algorithm that creates winding passages by
  alternating between randomized walks and hunts for new starting points.
  Produces mazes that are different in texture from DFS and Prim.

### Non-Perfect Mazes
If `PERFECT=False`, the generator adds loops with a low probability. This creates multiple paths between cells and removes the “single-solution” property.

## “42” Pattern
The maze can embed a fixed “42” pattern by marking specific cells as blocked. When the maze size allows, the pattern is centered and carved around, leaving a closed “42” shape inside the maze.

If the maze is too small to place the pattern:
- Generation continues without it.
- The application prints a warning.

## Path Finding
The shortest path from `ENTRY` to `EXIT` is computed with BFS:
- Guaranteed shortest path in unweighted grids.
- Used for the on-screen path overlay and for writing the path to the output file.

## Output File Format (Hex Encoding)
The output file stores the maze compactly:
- Each cell is a single hex digit (0–F) representing closed walls.
- Rows are written top-to-bottom, one line per row.

After a blank line, the file contains:
1. `entry_x,entry_y`
2. `exit_x,exit_y`
3. Path as a string of `N`, `E`, `S`, `W`

This format is designed for easy parsing and small file size.

## Rendering
### Curses (Interactive)
The curses UI displays the maze and allows interaction:
- Arrow keys to move
- Toggle path display
- Regenerate maze
- Change algorithm and seed
- Toggle perfect mode
- Save output
- Change wall colors

If curses fails to initialize (e.g., non-interactive environment), the app falls back to ASCII rendering.

### ASCII Renderer
ASCII mode prints the maze with box-drawing characters. It is static but works in any terminal. It can show:
- Start (`@`)
- End (`E`)
- Path (`.`)
- Blocked cells (`█`)

## Reusable Module Usage
```python
from mazegen.maze_generator import Maze

maze = Maze(21, 21)
maze.generate_maze(seed=42, algo="dfs", perfect=True)
```

Writing output:
```python
from mazegen.output_writer import write_output_file

write_output_file("maze.txt", maze, (0, 0), (20, 20))
```

## Tests
Unit tests live in `tests/`. Run them with:
```bash
pytest
```

## Build and Packaging
The reusable module can be built as a distributable package:
```bash
make build
```
This creates `mazegen-*.whl` and/or `mazegen-*.tar.gz` in the repository root.

## Troubleshooting
- **Curses error (`nocbreak() returned ERR`)**:
  - Usually caused by running in a non-interactive environment.
  - Use a real terminal, or rely on ASCII rendering.

- **Entry/Exit inside blocked cells**:
  - Update `ENTRY` / `EXIT` in `config.txt` to avoid the “42” pattern.

- **Maze too small for “42”**:
  - Increase `WIDTH` and `HEIGHT`.

## Design Notes
- Maze carving is symmetric between cells to keep walls consistent.
- Blocked cells are treated as solid obstacles to preserve the “42” shape.
- Separation of concerns: generation, parsing, rendering, and output writing are decoupled for easier testing.

## Team and Project Management
- **Roles**: Solo project (tlaghzal) responsible for design, implementation, tests, and documentation.
- **Planning**: Started with maze generation and validation, then added output format and UI.
- **Improvements**: Add more algorithms, improve UI usability, and add new render styles.

## Resources
- Maze generation algorithms (Wikipedia)
- Python curses documentation
- PEP 8 / PEP 484

### AI Usage
Used AI to review edge cases in configuration parsing and to draft an initial README outline. All code and explanations were verified and edited manually.
