# A-maze-ing Changelog

## v1.1.0 (2026-02-03)
### Added
- Added Prim's algorithm (`ALGO=prim`) for perfect maze generation.
- Added perfect mode toggle in curses UI (`T` key).
- Added save key in curses UI (`S`) to write current maze to the output file.
- Added seed change key in curses UI (`G`) to regenerate with a new random seed.
- Added hex output writer module.

### Changed
- Config parser now enforces required keys (`OUTPUT_FILE`, `PERFECT`).
 
### Removed
- README aligned with subject requirements.
- Updated Makefile lint flags and Python version requirement (3.10+).

### Removed
- Removed dependency on pygame (terminal-only rendering).

### Fixed
- Mypy type issues and lint warnings in core modules and tests.
- Correct handling of “42” pattern when maze too small.

## v1.0.0 (initial)
- Initial maze generator with curses rendering, config parsing, and hex output.
