*This project has been created as part of the 42 curriculum by tlaghzal.*

# A-Maze-ing: This is the Way

## Description
A-Maze-ing is a Python 3.10+ maze generator that reads a configuration file, builds a maze with a visible "42" pattern, writes the result using a hexadecimal wall encoding, and displays the maze in a terminal interface using curses. The maze generator is reusable as a standalone module.

## Instructions

### Requirements
- Python 3.10+
- Optional dev tools: flake8, mypy, pytest

### Run
```bash
python3 a_maze_ing.py config.txt
```

### Makefile
```bash
make install
make run
make debug
make lint
make clean
```

## Configuration File Format
One `KEY=VALUE` per line. Lines starting with `#` are ignored.

Mandatory keys:
```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

Optional keys:
```
SEED=42
ALGO=dfs        # dfs, binary_tree, or prim
DELAY=0.05
```

## Maze Generation Algorithm
- Default: **DFS (Recursive Backtracker)** for a perfect maze (single path between entry and exit).
- Optional: **Prim's Algorithm** when `ALGO=prim` (perfect maze).
- Optional: **Binary Tree** when `PERFECT=False` and `ALGO=binary_tree` (DFS is forced when `PERFECT=True`).

### Why DFS?
DFS is simple, fast, and guarantees a perfect maze by construction. It also avoids large open areas because it generates a spanning tree over the grid.

## Output File Format (Hexadecimal)
Each cell is a single hex digit representing closed walls:
- Bit 0: North
- Bit 1: East
- Bit 2: South
- Bit 3: West

Rows are written top-to-bottom, one line per row. After an empty line:
1) Entry coordinates (`x,y`)
2) Exit coordinates (`x,y`)
3) Shortest path as a string of `N`, `E`, `S`, `W`

## Visual Representation
The terminal UI (curses) supports:
- Regenerate a new maze
- Show/Hide the shortest path
- Change wall colors
- Adjust entry/exit positions
- Toggle perfect maze mode (binary tree is always imperfect)
- Save the current maze to the output file

## Reusable Module
Core generator: `mazegen/maze_generator.py` (class `Maze`).

Example:
```python
from mazegen.maze_generator import Maze

maze = Maze(21, 21)
maze.generate_maze(seed=42, algo="dfs", perfect=True)
```

Output writer:
```python
from mazegen.output_writer import write_output_file

write_output_file("maze.txt", maze, (0, 0), (20, 20))
```

## Packaging (mazegen-*)
Build the reusable module as a pip-installable package:
```bash
make build
```
The resulting `mazegen-*.whl` and/or `mazegen-*.tar.gz` are copied to the repository root.

## Team and Project Management
- **Roles**: duo project (tlaghzal) responsible implementation, tests, and documentation.
                            (mel-asla)  for design, Makefile....
- **Planning**: Started with maze generation and validation, then added output format, and finally the UI.
- **What worked well**: Modular separation between generation, parsing, and rendering.
- **Improvements**: Add more algorithms and improve UI usability.
- **Tools used**: Git, Makefile, flake8, mypy, pytest.

## Resources
- Maze generation algorithms (Wikipedia)
- PEP 8 and PEP 484 (Python style and typing)
- curses module documentation

### AI Usage
Used AI to review edge cases in configuration parsing and to draft an initial README outline. All code and explanations were verified and edited manually.
