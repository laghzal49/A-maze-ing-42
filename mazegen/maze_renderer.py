"""
This file has been replaced by render.py

The new renderer uses pygame for interactive visualization:
- Real-time maze rendering
- Animated path display with A* algorithm
- Color cycling for walls and "42" pattern
- Interactive entry/exit point selection
- Multiple maze generation algorithms

Usage:
    python3 -m mazegen.render

    Or programmatically:
    from mazegen.render import MazeRenderer

    renderer = MazeRenderer(width=30, height=20, cell_size=25)
    renderer.run()

Controls:
    R - Regenerate maze
    P - Show/animate path (A* algorithm)
    A - Switch algorithm (DFS/Binary Tree)
    C - Cycle wall color
    F - Cycle 42 color
    E - Set entry point (click)
    X - Set exit point (click)
    Q - Quit
"""

# For backwards compatibility
from .render import MazeRenderer

__all__ = ["MazeRenderer"]
