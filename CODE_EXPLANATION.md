# Code Explanation (Full Project)

This document explains every file and the major functions/classes in the project. It is written as a reference that maps code to behavior.

## Top Level Files

### `a_maze_ing.py`
Purpose: Application entry point for generating and rendering a maze.

Key parts:
- `_validate_entry_exit(maze, entry, exit_pos)`: Checks that entry and exit are different, in bounds, and not inside the blocked “42” pattern.
- `main()`: Reads the config file, builds the maze, validates entry/exit, writes the output file, and starts the curses renderer. Handles error cases and prints helpful messages.

Flow:
1. Read config from CLI arg or `config.txt`.
2. Build `Maze` and generate it with algorithm/seed/perfect.
3. Warn if 42 pattern could not be placed.
4. Validate entry/exit.
5. Write hex output file (and shortest-path moves).
6. Launch curses UI with `curses.wrapper`.

### `config.txt`
Purpose: Example configuration file used by the app.

Format:
- One `KEY=VALUE` per line.
- Lines beginning with `#` are ignored.

### `maze.txt`
Purpose: Example generated output file. Shows the hex-encoded maze and the path data at the end.

### `README.md`
Purpose: Project overview, setup, usage, and format description.

### `CHANGELOG.md`
Purpose: Notes on changes over time.

### `Makefile`
Purpose: Short commands for common tasks.

Targets:
- `install`: Install dependencies from `requirements.txt`.
- `run`: Run the app (`python3 a_maze_ing.py config.txt`).
- `debug`: Run the app in `pdb`.
- `lint`: Run `flake8` and `mypy`.
- `clean`: Remove caches/build artifacts.
- `build`: Build the Python package.

### `pyproject.toml`
Purpose: Packaging metadata, dependencies, and tool configuration.

Key sections:
- `[project]`: Package name, version, metadata.
- `[project.scripts]`: Installs a CLI entry point `a-maze-ing` -> `a_maze_ing:main`.
- `[tool.mypy]` and `[tool.flake8]`: Lint and type-check settings.

### `tests/test_maze.py`
Purpose: Basic validation of maze creation, generation, pathfinding, config parsing, and 42 pattern placement.

Tests:
- `test_maze_creation`: Maze dimensions are stored correctly.
- `test_maze_generation`: Algorithms run and produce walls.
- `test_pathfinding`: BFS returns a valid path.
- `test_path_to_moves`: Path converts to move string correctly.
- `test_config_validation`: Valid config passes; invalid config fails.
- `test_42_pattern`: Pattern placed for large maze; not placed for small.

## `mazegen/` Package

### `mazegen/__init__.py`
Purpose: Public API exports for the package.

Exports:
- `Maze`, `MazeRenderer`.
- Parsing utilities: `parse_file`, `parse_dict`, `MazeConfig`.
- Path utilities: `bfs_find_path`, `path_to_moves`.
- Output utilities: `write_output_file`, `maze_to_hex_rows`.
- Renderers: `render_maze_curses`, `render_maze`.
- UI helper: `get_user_position`.

### `mazegen/__main__.py`
Purpose: Allows `python -m mazegen` to run the same entry point as `a_maze_ing.py`.

### `mazegen/maze_generator.py`
Purpose: Core maze structure and generation algorithms.

Key attributes:
- `Maze.N, Maze.E, Maze.S, Maze.W`: Wall bit masks.
- `four_pattern` and `two_pattern`: Coordinate offsets for the “42” pattern.
- `self.walls`: 2D array of wall bitmasks, initialized to `15` (all walls closed).
- `self.blocked_cells`: Set of blocked coordinates for the “42” pattern.
- `self.pattern_origin`: Where the pattern is centered, or `None` if it could not be placed.

Key methods:
- `in_bounds(x, y)`: Bounds check.
- `is_blocked(x, y)`: Checks if cell is part of the blocked pattern.
- `reset()`: Restores a clean grid, clears blocked cells.
- `create_42_pattern()`: Places the “42” pattern if the maze is big enough.
- `_carve_passage(...)`: Centralized wall carving helper. Also triggers optional per-step callback.
- `generate_maze(seed, algo, perfect, on_step=None)`: Chooses DFS, Prim’s, or Hunt-and-Kill, optionally adds loops, and can emit carve-step events for animation.
- `_dfs_algo(rng, on_step=None)`: Recursive backtracker. Carves passages by clearing wall bits in both cells.
- `_prim_algo(rng, on_step=None)`: Prim’s algorithm using a randomized frontier.
- `hunt_and_kill(rng, on_step=None)`: Hunt-and-kill implementation (randomized walks with hunts for new starts).
- `add_loops(rng, loop_chance, on_step=None)`: Randomly breaks extra walls to create loops in non-perfect mazes.

### `mazegen/parser.py`
Purpose: Parse and validate configuration files.

Key parts:
- `MazeConfig`: Dataclass for validated config values.
- `_parse_bool(value)`: Accepts `true/false`, `1/0`, `yes/no`, `y/n`.
- `_validate_config(config)`: Ensures required keys, valid types, and valid ranges.
- `parse_dict(raw)`: Validate config from a dict (used by tests).
- `parse_file(filepath)`: Reads `KEY=VALUE` lines, validates, and returns `MazeConfig`.

### `mazegen/path_finder.py`
Purpose: BFS shortest path and direction string generation.

Key functions:
- `bfs_find_path(maze, start, end)`: Returns a list of coordinates for the shortest path, or `None` if unreachable. It respects wall bits and blocked cells.
- `path_to_moves(path)`: Converts a coordinate path to a move string of `N/E/S/W`.

### `mazegen/output_writer.py`
Purpose: Write the maze in a compact hex-encoded format with metadata.

Key functions:
- `maze_to_hex_rows(maze)`: Converts the grid’s wall bitmasks into hex strings, one row per line.
- `write_output_file(output_file, maze, entry, exit_pos)`: Writes hex rows, then entry/exit, then the move string for the shortest path. Raises if no path exists.

### `mazegen/maze_renderer.py`
Purpose: High-level renderer that chooses curses or ASCII.

Key parts:
- `MazeRenderer`: A wrapper class that can build a maze and render it.
- `run()`: Generates a maze, computes a path, and tries to render using curses. If curses fails, falls back to ASCII and prints a warning.

### `mazegen/position_selector.py`
Purpose: Curses UI helper for selecting positions.

Key function:
- `get_user_position(stdscr, maze, prompt, blocked)`: Lets the user move a cursor with arrow keys and confirms with Enter. Shows a “VALID” or “BLOCKED” status.

### `mazegen/ascii_renderer.py`
Purpose: Static ASCII rendering of the maze using box-drawing characters.

Key parts:
- `_is_wall_between(maze, x, y, dx, dy)`: True if there is a wall between a cell and its neighbor or if the neighbor is out-of-bounds or blocked.
- `AsciiCorner.get_corner(left, right, up, down)`: Chooses a box-drawing corner character depending on which edges are present.
- `render_maze(maze, path, start, end)`: Builds horizontal and vertical wall grids, prints corner and wall rows, and prints cell contents (start, end, path, blocked, empty).

### `mazegen/curses_renderer.py`
Purpose: Interactive rendering in a terminal using curses.

Key parts:
- `_draw_maze_line(stdscr, row, line_parts, start_col, max_x)`: Draws a composed line (text + color pairs) safely with horizontal offset.
- `_build_cell_line(...)`: Builds one row of cell contents, including vertical walls.
- `_build_wall_line(...)`: Builds one row of corners and horizontal walls.
- `_compute_wall_grids(maze)`: Creates horizontal and vertical wall grids used by the renderer.
- `_initialize_colors()`: Defines curses color pairs.
- `_handle_movement(key, maze, player_pos)`: Moves the player if a path is open.
- `moha_animation(...)`: Short intro animation.
- `setup_phase(...)`: Setup UI before the main loop.
- `render_maze_curses(...)`: Main interactive loop with centered maze layout and right-side panel.

Main UI behavior now:
- Maze drawing is centered in the terminal.
- A right panel (when there is enough width) shows controls, current mode/state, player position, goal, and status.
- Initial maze generation is animated at startup.
- Regeneration (`R`, `A`, `T`, `G`) uses the generator step callback for animated carving.
- `M` toggles generation animation on/off.
- Status text updates immediately for user-visible changes (path toggle, color changes, save result, movement, generation mode, etc.).

## Rendering Details

### Wall Bitmask Logic
- Each cell’s wall bits use `N/E/S/W` = `1/2/4/8`.
- If a bit is set, the wall is closed.
- If a bit is cleared, the wall is open.

### Corner Logic
The ASCII and curses renderers compute “corner” glyphs based on the presence of walls on the four sides. This produces clean box-drawing intersections (`┗`, `┓`, `┳`, etc.) rather than simple `+---+` styles.

## Common Errors and Causes

### `nocbreak() returned ERR`
- Usually means curses could not initialize in the current terminal (non-interactive, unsupported environment).
- Use a real terminal or fall back to ASCII rendering.

### No Path Found
- `write_output_file` will error if no path exists between entry and exit.
- Causes: entry/exit inside blocked pattern, or maze dimensions too small.

## Key Design Decisions

- Maze carving always clears walls symmetrically between adjacent cells.
- Blocked “42” cells are excluded from carving to preserve the pattern.
- Parsing is strict to catch config errors early.
- Rendering and generation are decoupled to keep the core reusable.
