# Project Files and Functions Reference (Detailed)

This document lists every file, function, class, and important data format. It includes parameters, return values, and side effects.

## Top-Level Files

**a_maze_ing.py**
Purpose: CLI entry point that loads config, builds a maze, writes output, and runs the curses UI.

Function ` _validate_entry_exit(maze, entry, exit_pos) -> None`
- Parameters:
  - `maze: Maze`: maze instance.
  - `entry: Tuple[int, int]`: start coordinates (x, y).
  - `exit_pos: Tuple[int, int]`: exit coordinates (x, y).
- Returns: `None`.
- Raises: `ValueError` if entry/exit are equal, out of bounds, or blocked by the 42 pattern.
- Side effects: none.

Function `main() -> None`
- Parameters: none.
- Returns: `None`.
- Behavior:
  - Reads config file from `sys.argv[1]` or defaults to `config.txt`.
  - Parses config via `parse_file`.
  - Creates `Maze`, generates it, validates entry/exit, writes output file, and runs curses UI.
- Raises/handles:
  - Catches `FileNotFoundError`, `ValueError`, `KeyboardInterrupt`, and generic `Exception` to print errors and exit.
- Side effects:
  - Reads config file.
  - Writes maze output file.
  - Starts curses UI.

**CHANGELOG.md**
Purpose: Release history and changes per version.

**CODE_EXPLANATION.md**
Purpose: High-level architecture and module summaries.

**Makefile**
Purpose: Convenience commands for install/run/debug/clean/lint/build.

**README.md**
Purpose: User documentation, config format, and algorithm descriptions.

**config.txt**
Purpose: Example configuration file.
- Format: `KEY=VALUE` per line (see parser for supported keys).

**maze.txt**
Purpose: Example output file written by `write_output_file`.
- Format:
  1. `height` lines of hex digits representing wall bitmasks.
  2. Blank line.
  3. `entry` as `x,y`.
  4. `exit` as `x,y`.
  5. Move string of `N/E/S/W`.

**pyproject.toml**
Purpose: Packaging metadata and tool configuration (mypy/flake8).

**tests/test_maze.py**
Purpose: Unit tests for maze generation and parsing.

Function `test_maze_creation() -> None`
- Verifies Maze dimensions after construction.

Function `test_maze_generation() -> None`
- Verifies DFS and Prim generate wall data.

Function `test_pathfinding() -> None`
- Verifies BFS returns a valid path for a generated maze.

Function `test_path_to_moves() -> None`
- Verifies path-to-moves conversion.

Function `test_config_validation() -> None`
- Verifies valid config accepted and invalid config rejected.

Function `test_42_pattern() -> None`
- Verifies 42 pattern placement success/failure by size.

## Package: mazegen

**mazegen/__init__.py**
Purpose: Exposes public package API.
- Exports: `Maze`, `MazeRenderer`, `bfs_find_path`, `path_to_moves`, `parse_file`, `parse_dict`, `MazeConfig`, `write_output_file`, `maze_to_hex_rows`, `render_maze_curses`, `render_maze`, `get_user_position`.

**mazegen/__main__.py**
Purpose: `python -m mazegen` entry point.
- Behavior: Calls `a_maze_ing.main()`.

### mazegen/ascii_renderer.py
Purpose: ASCII fallback renderer.

Function `_is_wall_between(maze, x, y, dx, dy) -> bool`
- Parameters:
  - `maze: Maze`: maze instance.
  - `x, y: int`: current cell.
  - `dx, dy: int`: direction offset.
- Returns: `True` if a wall blocks movement to neighbor or neighbor is out of bounds/blocked.
- Side effects: none.

Class `AsciiCorner`
- Purpose: Choose line-drawing characters for wall junctions.

Method `AsciiCorner.get_corner(left, right, up, down) -> str`
- Parameters: four booleans indicating adjacent walls.
- Returns: line-drawing character (e.g., `┳`, `┛`, `━`).

Function `render_maze(maze, path=None, start=None, end=None) -> None`
- Parameters:
  - `maze: Maze`.
  - `path: Optional[List[Tuple[int, int]]]`: path cells (drawn as `.`).
  - `start: Optional[Tuple[int, int]]`: start (drawn as `@`).
  - `end: Optional[Tuple[int, int]]`: end (drawn as `E`).
- Returns: `None`.
- Side effects: prints maze to stdout.

### mazegen/curses_renderer.py
Purpose: Interactive curses renderer and gameplay loop.

Type `LineParts = List[Tuple[str, int]]`
- Purpose: list of `(text, color_pair)` for composing a line.

Function `_draw_maze_line(stdscr, row, line_parts, start_col, max_x) -> None`
- Parameters:
  - `stdscr: curses.window`: curses screen.
  - `row: int`: row to draw.
  - `line_parts: LineParts`: prebuilt line content.
  - `start_col: int`: horizontal offset for drawing.
  - `max_x: int`: terminal width limit.
- Returns: `None`.
- Side effects: writes to curses window (best-effort, ignores errors).

Function `_build_cell_line(maze, y, player_pos, end, path_set, show_path, color_42, color_wall, vert) -> LineParts`
- Parameters:
  - `maze: Maze`.
  - `y: int`: row index.
  - `player_pos: List[int]`: `[x, y]` current player.
  - `end: Tuple[int, int]`: goal cell.
  - `path_set: Set[Tuple[int, int]]`: path cells.
  - `show_path: bool`: toggle for path rendering.
  - `color_42: int`: color pair index for blocked cells.
  - `color_wall: int`: color pair index for walls/background.
  - `vert: List[List[bool]]`: vertical wall grid.
- Returns: `LineParts` for the cell row.

Function `_build_wall_line(maze, y, color_42, color_wall, horiz, vert) -> LineParts`
- Parameters:
  - `maze: Maze`.
  - `y: int`: wall row index.
  - `color_42: int`: color pair index.
  - `color_wall: int`: color pair index.
  - `horiz: List[List[bool]]`: horizontal wall grid.
  - `vert: List[List[bool]]`: vertical wall grid.
- Returns: `LineParts` for the wall row.

Function `_compute_wall_grids(maze) -> Tuple[List[List[bool]], List[List[bool]]]`
- Parameters: `maze: Maze`.
- Returns:
  - `horiz`: `(height + 1) x width` horizontal wall booleans.
  - `vert`: `(width + 1) x height` vertical wall booleans.
- Side effects: none.

Function `_initialize_colors() -> None`
- Sets curses color pairs 1..7.
- Returns: `None`.

Function `_handle_movement(key, maze, player_pos) -> None`
- Parameters:
  - `key: int`: curses key code.
  - `maze: Maze`.
  - `player_pos: List[int]`: mutable player position.
- Returns: `None`.
- Side effects: updates `player_pos` if movement is valid (in bounds, not blocked, no wall).

Function `moha_animation(stdscr, message) -> None`
- Parameters:
  - `stdscr: curses.window`.
  - `message: str`.
- Returns: `None`.
- Side effects: draws animated text with color cycling and sleeps briefly.

Function `setup_phase(stdscr, maze, config_start, config_end) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]]]`
- Parameters:
  - `stdscr: curses.window`.
  - `maze: Maze`.
  - `config_start: Optional[Tuple[int, int]]`.
  - `config_end: Optional[Tuple[int, int]]`.
- Returns: `(start, end)` (currently just echoes the passed values).
- Side effects: runs intro animations and sets curses flags.

Function `render_maze_curses(stdscr, maze, path=None, start=None, end=None, algo="dfs", seed=None, perfect=True, output_file=None) -> None`
- Parameters:
  - `stdscr: curses.window`.
  - `maze: Maze`.
  - `path: Optional[List[Tuple[int, int]]]`: initial path for display.
  - `start, end: Optional[Tuple[int, int]]`.
  - `algo: str`: `dfs`, `prim`, or `hunt`.
  - `seed: Optional[int]`.
  - `perfect: bool`.
  - `output_file: Optional[str]`.
- Returns: `None`.
- Side effects:
  - Handles interactive input, redraws screen, regenerates maze, writes output file, and may exit.
  - Centers maze rendering based on terminal size.
  - Shows a right-side status/control panel when terminal width allows.
  - Animates initial generation and regeneration when generation animation is enabled.
  - Shows win prompt when reaching `end`.

### mazegen/maze_generator.py
Purpose: Maze data model and generation algorithms.

Class `Maze`
- Fields:
  - `width: int`, `height: int`.
  - `walls: List[List[int]]`: wall bitmasks (N/E/S/W bits).
  - `blocked_cells: Set[Tuple[int, int]]`.
  - `pattern_origin: Optional[Tuple[int, int]]`.

Method `__init__(width, height) -> None`
- Initializes dimensions, wall grid (all walls closed), and blocked state.

Method `in_bounds(x, y) -> bool`
- Returns `True` if `(x, y)` is inside the maze.

Method `is_blocked(x, y) -> bool`
- Returns `True` if `(x, y)` is part of the blocked 42 pattern.

Method `reset() -> None`
- Resets all walls to closed (`15`) and clears blocked cells/pattern origin.

Method `create_42_pattern() -> bool`
- Attempts to place 42 pattern in the center.
- Returns `True` if placed, else `False` if maze too small.
- Side effects: updates `blocked_cells` and `pattern_origin`.

Method `_carve_passage(cx, cy, nx, ny, w_bit, opp_bit, on_step=None) -> None`
- Parameters:
  - `cx, cy: int`: current cell coordinates.
  - `nx, ny: int`: neighbor cell coordinates.
  - `w_bit: int`: wall bit to remove in current cell.
  - `opp_bit: int`: opposite wall bit to remove in neighbor.
  - `on_step: Optional[Callable[[int, int, int, int], None]]`: callback per carve.
- Returns: `None`.
- Side effects:
  - Mutates `walls`.
  - Invokes `on_step(cx, cy, nx, ny)` when provided.

Method `generate_maze(seed=None, algo="dfs", perfect=True, on_step=None) -> None`
- Parameters:
  - `seed: Optional[int]` RNG seed.
  - `algo: str` in `{"dfs", "prim", "hunt"}`.
  - `perfect: bool` whether to keep single-solution.
  - `on_step: Optional[Callable[[int, int, int, int], None]]`: optional callback called on each carve event.
- Behavior:
  - Resets the maze, places 42 pattern, runs algorithm, optionally adds loops.
- Side effects: mutates `walls`, `blocked_cells`, `pattern_origin`.

Method `_dfs_algo(rng, on_step=None) -> None`
- Recursive backtracker that carves passages by clearing wall bits.

- Method `_prim_algo(rng, on_step=None) -> None`
- Randomized Prim’s algorithm using a frontier list.

- Method `hunt_and_kill(rng, on_step=None) -> None`
- Hunt-and-kill implementation: performs randomized walks and hunts for
  new starting cells when walkers terminate. Produces a varied maze texture.

- Method `add_loops(rng, loop_chance=0.1, on_step=None) -> None`
- Randomly removes extra walls to create loops (non-perfect mazes).

### mazegen/maze_renderer.py
Purpose: Higher-level renderer that can use curses or ASCII.

Class `MazeRenderer`
- Constructor parameters:
  - `width, height: int`.
  - `cell_size: int` (unused in curses path).
  - `entry, exit: Optional[Tuple[int, int]]`.
  - `seed: Optional[int]`.
  - `algo: str`.
  - `perfect: bool`.
  - `use_curses: bool`.

Method `_build_maze() -> Maze`
- Returns a generated `Maze` based on stored config.

Method `run() -> None`
- Computes optional BFS path.
- Uses curses renderer if enabled, otherwise ASCII.
- Falls back to ASCII if curses fails.

Function `_get_42_cells(maze) -> Set[Tuple[int, int]]`
- Returns `maze.blocked_cells`.

### mazegen/output_writer.py
Purpose: Hex output writer and shortest-path export.

Function `maze_to_hex_rows(maze) -> List[str]`
- Returns list of strings where each char is a hex digit representing one cell’s wall bits.

Function `write_output_file(output_file, maze, entry, exit_pos) -> str`
- Parameters: output file path, maze, entry, exit.
- Returns: move string (`N/E/S/W`).
- Raises: `ValueError` if no valid path exists.
- Side effects: writes output file to disk.

### mazegen/parser.py
Purpose: Configuration parser and validator.

Class `MazeConfig`
- Fields: `width`, `height`, `entry`, `exit`, `output_file`, `perfect`, `seed`, `algo`, `delay`.

Function `_parse_bool(value) -> bool`
- Accepts `true/false`, `1/0`, `yes/no`, `y/n` (case-insensitive).

Function `_validate_config(config) -> MazeConfig`
- Validates required keys, ranges, and types.
- Valid algorithms: `dfs`, `prim`, `binary_tree`.
- Returns a `MazeConfig`.
- Raises `ValueError` on invalid config.
Function `parse_dict(raw) -> MazeConfig`
- Validates a dict and returns `MazeConfig`.

Function `parse_file(filepath) -> MazeConfig`
- Parses a text file with `KEY=VALUE` pairs.
- Returns `MazeConfig`.
- Raises `FileNotFoundError` if missing; `ValueError` on bad data.

### mazegen/path_finder.py
Purpose: Shortest-path computation and move generation.

Function `bfs_find_path(maze, start, end) -> Optional[List[Tuple[int, int]]]`
- Returns list of coordinates from start to end, or `None` if unreachable/invalid.
- Respects walls and blocked cells.

Function `path_to_moves(path) -> str`
- Converts a coordinate path into a string of moves (`N/E/S/W`).

### mazegen/position_selector.py
Purpose: Curses-based coordinate selector.

Function `get_user_position(stdscr, maze, prompt, blocked) -> Tuple[int, int]`
- Parameters:
  - `stdscr: curses.window`.
  - `maze: Maze`.
  - `prompt: str`.
  - `blocked: Set[Tuple[int, int]]`.
- Returns selected `(x, y)` when user presses Enter on a valid cell.
- Side effects: interactive curses UI.

## Libraries and Imports (Why/How/Inputs)

This section explains each imported library/module, why it is used, and the key functions used in this project.

### Standard Library Imports

**sys** (in `a_maze_ing.py`)
- Why: Read CLI arguments and exit with error codes.
- Used functions:
  - `sys.argv`: List of command-line arguments.
  - `sys.exit(code)`: Terminates the program with a status code.
- Inputs/returns:
  - `sys.argv` is a list of strings.
  - `sys.exit(code)` takes an int and does not return.

**curses** (in `a_maze_ing.py`, `mazegen/curses_renderer.py`, `mazegen/position_selector.py`)
- Why: Terminal UI rendering and keyboard input.
- Used functions/classes:
  - `curses.wrapper(func, *args)`: Initializes curses and calls `func(stdscr, *args)`.
  - `curses.curs_set(0)`: Hides cursor.
  - `curses.init_pair(n, fg, bg)`: Defines color pairs.
  - `curses.color_pair(n)`: Gets attribute for color pair.
  - `curses.A_BOLD`: Bold text attribute.
  - `curses.KEY_UP/DOWN/LEFT/RIGHT/ENTER`: Key codes.
- Inputs/returns:
  - `wrapper` takes a callable and arguments; returns whatever the callable returns.
  - `init_pair` and `curs_set` return `None`.
  - `color_pair` returns an attribute for `addstr`.
- How used:
  - Initialize colors and draw maze lines in curses windows.
  - Read keys with `stdscr.getch()`.

**random** (in `mazegen/maze_generator.py`, `mazegen/curses_renderer.py`)
- Why: Randomized maze generation and random seed creation.
- Used functions/classes:
  - `random.Random(seed)`: RNG instance.
  - `rng.shuffle(list)`, `rng.choice(list)`, `rng.randrange(n)`, `rng.random()`.
  - `random.randint(a, b)` in curses renderer for new seeds.
- Inputs/returns:
  - `Random(seed)` takes optional int seed and returns RNG object.
  - `rng.random()` returns float in `[0.0, 1.0)`.
  - `randint(a, b)` returns int in `[a, b]`.

**time** (in `mazegen/curses_renderer.py`)
- Why: Small delay for intro animation.
- Used functions:
  - `time.sleep(seconds)`: Pauses execution.
- Inputs/returns:
  - Takes float seconds; returns `None`.

**collections.deque** (in `mazegen/path_finder.py`)
- Why: Efficient FIFO queue for BFS.
- Used functions/classes:
  - `deque()`: Creates deque.
  - `append`, `popleft` for queue operations.
- Inputs/returns:
  - `append` takes an item, returns `None`.
  - `popleft` returns the leftmost item.

**dataclasses.dataclass** (in `mazegen/parser.py`)
- Why: Quick immutable-like config container with generated `__init__`.
- Used decorator:
  - `@dataclass` on `MazeConfig`.
- Inputs/returns:
  - Decorates a class, generates init and repr; returns class object.

**typing** (multiple files)
- Why: Type annotations for readability and static analysis.
- Used types:
  - `Optional`, `Tuple`, `List`, `Set`, `Dict`, `Any`, `Deque`.
- Inputs/returns:
  - These are type hints only, no runtime behavior change.

### Local Module Imports

**mazegen.maze_generator.Maze**
- Why: Core maze structure and generation algorithms.
- How used:
  - Constructed to generate and render a maze.
  - Provides `walls`, `blocked_cells`, and helper methods used across renderers and pathfinding.

**mazegen.parser.parse_file / parse_dict / MazeConfig**
- Why: Parse config file/dicts and validate values.
- How used:
  - `a_maze_ing.py` calls `parse_file`.
  - Tests call `parse_dict`.

**mazegen.curses_renderer.render_maze_curses**
- Why: Run interactive curses UI.
- How used:
  - Called via `curses.wrapper` in `a_maze_ing.py` and `MazeRenderer.run`.

**mazegen.ascii_renderer.render_maze**
- Why: Render maze to plain ASCII output as fallback.
- How used:
  - `MazeRenderer.run` uses it if curses fails or if `use_curses=False`.

**mazegen.path_finder.bfs_find_path / path_to_moves**
- Why: Compute shortest path and encode it as moves.
- How used:
  - `output_writer.write_output_file` requires the path to produce the move string.

**mazegen.output_writer.write_output_file / maze_to_hex_rows**
- Why: Persist maze to hex-encoded text file.
- How used:
  - `a_maze_ing.py` writes output before launching UI.
  - Curses UI can save the current maze.

**mazegen.position_selector.get_user_position**
- Why: Curses-based coordinate selection (not currently wired into main flow).
- How used:
  - Available for interactive selection in future improvements or tests.
