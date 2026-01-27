# A-maze-ing 🎯

*This project has been created as part of the 42 curriculum by tlaghzal.*

## Description

A Python-based maze generator and solver with animated pathfinding visualization featuring the iconic "42" pattern. This project implements various maze generation algorithms with perfect maze support (single path between entrance and exit), hexadecimal wall encoding output, and interactive terminal-based visualization.

The project generates mazes using the Recursive Backtracker algorithm, ensuring proper connectivity, wall coherence, and the ability to produce perfect mazes. It includes BFS pathfinding to find the shortest solution and provides an ASCII terminal display with customizable wall colors and path visualization.

## Instructions

### Installation

```bash
git clone <your-repo-url>
cd A-maze-ing

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make install
```

### Running the Program

```bash
# Basic usage
python3 a_maze_ing.py config.txt

# Or using the Makefile
make run
```

### Building the Package

```bash
# Build the distributable package
make build

# The package will be created in the dist/ directory
# and copied as mazegen-1.0.0-py3-none-any.whl at the root
```

### Configuration File Format

The `config.txt` file must contain the following mandatory keys (one KEY=VALUE per line):

```ini
# Maze dimensions
WIDTH=21                # Maze width (number of cells)
HEIGHT=21               # Maze height (number of cells)

# Entry and exit points (x,y coordinates)
ENTRY=1,1               # Entry coordinates
EXIT=19,19              # Exit coordinates

# Output configuration
OUTPUT_FILE=maze.txt    # Output filename for hex format

# Generation parameters
PERFECT=true            # Generate perfect maze (single path)

# Optional parameters
# SEED=42               # Random seed for reproducibility
# DELAY=0.05            # Animation delay in seconds
```

Lines starting with `#` are treated as comments.

## Features

- **Recursive Backtracker Algorithm**: Generates perfect mazes with guaranteed solutions
- **"42" Pattern**: Automatically embeds a stylized "42" in the center of each maze
- **BFS Pathfinding**: Finds the shortest path from entry to exit
- **Hexadecimal Output**: Saves mazes in hex format (bit-encoded walls)
- **Animated Visualization**: Watch the solution path animate in real-time
- **Interactive Controls**: Toggle features and regenerate mazes on-the-fly
- **Configurable**: Customize maze size, entry/exit points, colors, and more
- **Validation**: Ensures wall coherence, connectivity, and proper structure

### Interactive Controls

While running, use these keys:

- **Q**: Quit the program
- **F**: Force path (turn solution cells into walls)
- **P**: Toggle perfect maze mode
- **S**: Toggle random seed
- **H**: Toggle path display on/off
- **4**: Toggle "42" pattern highlighting
- **C**: Change wall colors (cycles through white, cyan, green, yellow, magenta, red)
- **V**: Save current maze to file in hexadecimal format

## Maze Generation Algorithm

### Chosen Algorithm: Recursive Backtracker

The Recursive Backtracker is a depth-first search algorithm that creates perfect mazes (mazes with exactly one path between any two points).

### Why This Algorithm?

1. **Simplicity**: Easy to implement and understand
2. **Perfect Mazes**: Naturally creates mazes with a single solution path
3. **Memory Efficient**: Uses a simple stack-based approach
4. **Long Corridors**: Creates interesting, challenging mazes with long, winding paths
5. **Well-Suited for Grid**: Works perfectly with 2D grid-based mazes

### How It Works

1. Start at a random cell and mark it as visited
2. While there are unvisited neighbors:
   - Choose a random unvisited neighbor
   - Remove the wall between the current cell and the chosen neighbor
   - Recursively visit the chosen neighbor
3. If no unvisited neighbors, backtrack to the previous cell
4. Continue until all cells are visited

### "42" Pattern Integration

After maze generation, the program:
1. Calculates the center position of the maze
2. Clears a rectangular area in the center
3. Stamps a predefined "42" ASCII pattern as walls
4. Ensures entry and exit remain accessible
5. In perfect mode, validates that only one path exists after stamping

### Output File Format

The maze is saved in hexadecimal format where each cell is encoded as a single hex digit (0-F):

- **Bit 0 (LSB)**: North wall (1 = closed, 0 = open)
- **Bit 1**: East wall
- **Bit 2**: South wall
- **Bit 3**: West wall

Example: `A` (binary 1010) = East and West walls closed, North and South open

Format structure:
```
[Hex grid - one row per line]

[Empty line]
[Entry coordinates: x,y]
[Exit coordinates: x,y]
[Shortest path: NESW directions]
```

## Project Structure

```
A-maze-ing/
├── a_maze_ing.py            # Main entry point
├── config_parser.py          # Configuration file parser
├── maze_generator.py         # Core maze generation logic (REUSABLE)
├── maze_42_generator.py      # "42" pattern integration
├── maze_validator.py         # Maze validation functions
├── pathfinder.py             # BFS pathfinding algorithm (REUSABLE)
├── maze_renderer.py          # Terminal visualization
├── utils.py                  # Utility functions (hex encoding, file I/O)
├── config.txt                # Default configuration file
├── Makefile                  # Build and run commands
├── pyproject.toml            # Package configuration
├── requirements.txt          # Dependencies
├── test_maze.py              # Unit tests
├── mazegen-1.0.0-py3-none-any.whl  # Distributable package
└── README.md                 # This file
```

## Code Reusability

### Reusable Modules

The following modules can be imported and used in other projects:

#### 1. **maze_generator.py** - Core Maze Generation

```python
from maze_generator import Maze

# Create a maze
maze = Maze(width=21, height=21)

# Generate the maze structure
maze.generation(start_x=1, start_y=1, perfect=True, seed=42)

# Access the grid
grid = maze.grid  # 2D list: 0 = PATH, 1 = WALL
width = maze.width
height = maze.height
```

#### 2. **pathfinder.py** - BFS Pathfinding

```python
from pathfinder import solve_maze

# Find shortest path
path = solve_maze(maze, start=(1, 1), end=(19, 19))
# Returns: list of (x, y) tuples or None if no path
```

#### 3. **maze_validator.py** - Validation Functions

```python
from maze_validator import (
    has_multiple_paths,
    validate_entry_exit,
    has_3x3_open_areas
)

# Check if maze has unique solution
is_perfect = not has_multiple_paths(maze, start, end)

# Validate entry/exit points
is_valid = validate_entry_exit(maze, entry, exit)
```

### Installing the Package

```bash
# Install from the .whl file
pip install mazegen-1.0.0-py3-none-any.whl

# Or build from source
python3 -m build
pip install dist/a_maze_ing-1.0.0-py3-none-any.whl
```

## Team and Project Management

### Team Member

- **tlaghzal**: Project lead, implementation, testing, and documentation

### Planning

**Initial Plan:**
- Days 1-2: Setup and config parser
- Days 3-4: Maze generation algorithm
- Days 5-6: Validation and pathfinding
- Days 7-8: Visual display
- Days 9-10: User interaction
- Days 11-12: Packaging
- Days 13-14: Documentation and testing

**Actual Timeline:**
- Development progressed faster than anticipated due to modular design
- Most core features completed in first week
- Additional time spent on:
  - Hexadecimal output format implementation
  - Wall coherence validation
  - Interactive color changing
  - Comprehensive testing

### What Worked Well

- **Modular Design**: Separating concerns (generation, validation, rendering) made development easier
- **Test-Driven Approach**: Writing tests early helped catch bugs
- **Incremental Features**: Building features one at a time ensured stability
- **Type Hints**: Using mypy caught many potential bugs early

### What Could Be Improved

- **Algorithm Flexibility**: Could add support for multiple maze algorithms (Prim's, Kruskal's)
- **Performance**: Large mazes (>100x100) could benefit from optimization
- **GUI Option**: MLX graphical display could be added as alternative to terminal
- **Advanced Validation**: More comprehensive wall coherence checks

### Tools Used

- **Git**: Version control
- **VS Code**: Primary development environment
- **Python venv**: Virtual environment management
- **flake8**: Code linting
- **mypy**: Static type checking
- **pytest**: Unit testing
- **python-build**: Package building

## Resources

### Classic References

- **Maze Generation Algorithms**: [Wikipedia - Maze Generation](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- **Recursive Backtracker**: [Buckblog - Maze Generation](http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
- **Graph Theory**: [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/books/introduction-algorithms-third-edition)
- **BFS Algorithm**: [GeeksforGeeks - Breadth First Search](https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/)
- **Python Packaging**: [Python Packaging User Guide](https://packaging.python.org/)
- **PEP 8**: [Python Style Guide](https://www.python.org/dev/peps/pep-0008/)

### AI Usage

AI tools (GitHub Copilot, ChatGPT) were used for the following tasks:

1. **Code Generation Assistance**:
   - Boilerplate code for file I/O and error handling
   - Type hints and docstring generation
   - Test case generation

2. **Documentation**:
   - README structure and formatting
   - Docstring improvements
   - Code comments

3. **Debugging**:
   - Identifying edge cases
   - Suggesting fixes for type errors
   - Optimization suggestions

4. **Algorithm Implementation**:
   - Initial recursive backtracker pseudocode
   - BFS pathfinding structure
   - Hexadecimal encoding logic

**Important Note**: All AI-generated code was reviewed, tested, and modified to ensure correctness and understanding. The core algorithm design and project architecture were human-designed.

## Development

### Setup Development Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
make install
```

### Run Tests

```bash
pytest test_maze.py -v
```

### Code Quality

```bash
# Linting
make lint

# Strict type checking
make lint-strict
```

### Debugging

```bash
# Run in debug mode
make debug
```

## Requirements

- Python 3.10+
- No external dependencies (uses only standard library)
- Development dependencies (optional): flake8, mypy, pytest

## License

MIT License

## Acknowledgments

- Inspired by classic maze algorithms and graph theory
- "42" pattern pays homage to Douglas Adams' "The Hitchhiker's Guide to the Galaxy"
- Built as part of the 42 Network curriculum
