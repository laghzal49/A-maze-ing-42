"""
pygame_renderer.py
Pygame maze renderer with animation.

Uses A* (A-star) pathfinding - the fastest and most optimal algorithm.

Keys:
  R = regenerate maze
  P = find and animate path (A* algorithm)
  C = change wall color
  A = switch algorithm (dfs <-> binary_tree)
  E = set custom entry point (then click on maze)
  X = set custom exit point (then click on maze)
  F = cycle 42 color
  Q / ESC = quit
"""

import pygame
import random
from .maze_generator import Maze
from .path_finder import bfs_find_path
from .forth_two import get_42_pattern, find_42_location
from typing import Optional, List, Tuple, Set

Coord = Tuple[int, int]


class MazeRenderer:
    def __init__(self, width: int, height: int, cell_size: int = 30):
        """Initialize pygame maze renderer.

        Args:
            width: Maze width in cells
            height: Maze height in cells
            cell_size: Size of each cell in pixels
        """
        pygame.init()

        self.maze_width = width
        self.maze_height = height
        self.cell_size = cell_size
        self.wall_width = 3

        # Calculate window size
        self.screen_width = width * cell_size + 40
        self.screen_height = height * cell_size + 120

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Maze Solver")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)

        # Colors
        self.bg_color = (20, 20, 30)
        self.wall_colors = [
            (255, 255, 255),  # White
            (0, 255, 255),    # Cyan
            (0, 255, 0),      # Green
            (255, 255, 0),    # Yellow
            (255, 0, 255),    # Magenta
            (255, 100, 100),  # Red
        ]
        self.fortytwo_colors = [
            (255, 215, 0),    # Gold
            (255, 0, 255),    # Magenta
            (0, 191, 255),    # Deep Sky Blue
            (255, 69, 0),     # Orange Red
            (50, 205, 50),    # Lime Green
            (138, 43, 226),   # Blue Violet
        ]
        self.path_color = (50, 200, 50)
        self.entry_color = (100, 255, 100)
        self.exit_color = (255, 100, 100)
        self.text_color = (200, 200, 200)

        self.wall_color_idx = 0
        self.fortytwo_color_idx = 0

    def get_wall_color(self):
        return self.wall_colors[self.wall_color_idx]

    def cycle_color(self):
        self.wall_color_idx = (self.wall_color_idx + 1) % len(self.wall_colors)

    def get_fortytwo_color(self):
        return self.fortytwo_colors[self.fortytwo_color_idx]

    def cycle_fortytwo_color(self):
        self.fortytwo_color_idx = (
            self.fortytwo_color_idx + 1) % len(self.fortytwo_colors)

    def draw_maze(self, maze: Maze, entry: Coord, exit_pt: Coord,
                  path: Optional[List[Coord]] = None,
                  path_progress: int = -1,
                  fortytwo_cells: Optional[Set[Coord]] = None):
        """Draw the maze on the screen."""
        self.screen.fill(self.bg_color)

        # Draw title
        title = self.title_font.render("MAZE SOLVER", True, self.entry_color)
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 10))

        # Calculate maze offset
        offset_x = 20
        offset_y = 70

        # Determine which path cells to show
        path_set = set()
        if path and path_progress >= 0:
            path_set = set(path[:path_progress + 1])
        elif path:
            path_set = set(path)

        wall_color = self.get_wall_color()
        fortytwo_color = self.get_fortytwo_color()

        # Draw cells and walls
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.walls[y][x]
                px = offset_x + x * self.cell_size
                py = offset_y + y * self.cell_size

                # Draw cell background
                if (x, y) == entry:
                    pygame.draw.rect(
                        self.screen, self.entry_color,
                        (px + 2, py + 2,
                         self.cell_size - 4, self.cell_size - 4))
                elif (x, y) == exit_pt:
                    pygame.draw.rect(
                        self.screen, self.exit_color,
                        (px + 2, py + 2,
                         self.cell_size - 4, self.cell_size - 4))
                elif (x, y) in path_set:
                    pygame.draw.circle(
                        self.screen, self.path_color,
                        (px + self.cell_size // 2,
                         py + self.cell_size // 2),
                        self.cell_size // 4)
                elif fortytwo_cells and (x, y) in fortytwo_cells:
                    # Draw "42" cells with special color
                    pygame.draw.rect(
                        self.screen, fortytwo_color,
                        (px + 2, py + 2,
                         self.cell_size - 4, self.cell_size - 4))

                # Draw walls
                # North wall
                if cell & maze.N:
                    pygame.draw.line(
                        self.screen, wall_color,
                        (px, py), (px + self.cell_size, py),
                        self.wall_width)

                # South wall
                if cell & maze.S:
                    pygame.draw.line(
                        self.screen, wall_color,
                        (px, py + self.cell_size),
                        (px + self.cell_size, py + self.cell_size),
                        self.wall_width)

                # West wall
                if cell & maze.W:
                    pygame.draw.line(
                        self.screen, wall_color,
                        (px, py), (px, py + self.cell_size),
                        self.wall_width)

                # East wall
                if cell & maze.E:
                    pygame.draw.line(
                        self.screen, wall_color,
                        (px + self.cell_size, py),
                        (px + self.cell_size, py + self.cell_size),
                        self.wall_width)

        pygame.display.flip()

    def draw_status(self, algo_name: str, path_active: bool, mode: str = "", is_perfect: bool = True):
        """Draw status bar at bottom."""
        status_y = self.screen_height - 40

        if mode:
            status_text = f">>> Click on maze to set {mode.upper()} <<<"
            color = self.entry_color if mode == "entry" else self.exit_color
        else:
            perfect_label = "PERFECT" if is_perfect else "LOOPS"
            status_text = (
                f"[R] Regen  [P] Path  [A] {algo_name}  [M] {perfect_label}  "
                f"[C] Wall Color  [F] 42 Color  [E] Entry  [X] Exit  [Q] Quit"
            )
            color = self.text_color

        status_surface = self.font.render(status_text, True, color)
        self.screen.blit(status_surface, (20, status_y))

        pygame.display.flip()

    def get_cell_from_click(
            self, pos: Tuple[int, int],
            offset_x: int, offset_y: int) -> Optional[Coord]:
        """Convert mouse click position to maze cell coordinates."""
        x, y = pos
        cell_x = (x - offset_x) // self.cell_size
        cell_y = (y - offset_y) // self.cell_size

        if 0 <= cell_x < self.maze_width and 0 <= cell_y < self.maze_height:
            return (cell_x, cell_y)
        return None

    def run(self):
        """Main game loop."""
        # Maze configuration
        entry = (0, 0)
        exit_pt = (self.maze_width - 1, self.maze_height - 1)

        algos = ["dfs", "binary_tree"]
        algo_idx = 0

        seed = 42
        rng = random.Random(seed)
        
        # Perfect maze toggle (True = perfect, False = with loops)
        is_perfect = True

        # Generate initial maze
        maze = Maze(self.maze_width, self.maze_height)
        maze.generate(
            entry[0], entry[1],
            exit_x=exit_pt[0], exit_y=exit_pt[1],
            seed=seed, algo=algos[algo_idx], perfect=is_perfect)

        # Calculate path first to avoid 42 conflicts
        path = bfs_find_path(maze, entry, exit_pt)
        path_set = set(path) if path else set()
        path_set.add(entry)
        path_set.add(exit_pt)

        # Calculate 42 pattern location avoiding path
        fortytwo_start = find_42_location(maze, path_set)
        fortytwo_cells = get_42_pattern(fortytwo_start[0], fortytwo_start[1])

        show_path = False
        running = True
        setting_mode = None  # None, "entry", or "exit"
        offset_x = 20
        offset_y = 70

        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if setting_mode:
                        cell = self.get_cell_from_click(event.pos, offset_x, offset_y)
                        if cell:
                            if setting_mode == "entry":
                                entry = cell
                            elif setting_mode == "exit":
                                exit_pt = cell

                            # Regenerate maze with new entry/exit
                            maze.generate(
                                entry[0], entry[1],
                                exit_x=exit_pt[0], exit_y=exit_pt[1],
                                seed=seed, algo=algos[algo_idx])
                            # Calculate path first to avoid 42 conflicts
                            path = bfs_find_path(maze, entry, exit_pt)
                            path_set = set(path) if path else set()
                            path_set.add(entry)
                            path_set.add(exit_pt)
                            show_path = False
                            setting_mode = None
                            # Recalculate 42 pattern avoiding path
                            fortytwo_start = find_42_location(maze, path_set)
                            fortytwo_cells = get_42_pattern(
                                fortytwo_start[0], fortytwo_start[1])

                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        if setting_mode:
                            setting_mode = None  # Cancel mode
                        else:
                            running = False

                    elif event.key == pygame.K_e:
                        setting_mode = "entry"

                    elif event.key == pygame.K_x:
                        setting_mode = "exit"

                    elif event.key == pygame.K_c:
                        self.cycle_color()

                    elif event.key == pygame.K_f:
                        self.cycle_fortytwo_color()

                    elif event.key == pygame.K_p:
                        # Path already calculated, just toggle display
                        if path and not show_path:
                            # Animate path
                            show_path = True
                            for i in range(len(path)):
                                self.draw_maze(
                                    maze, entry, exit_pt, path, i,
                                    fortytwo_cells)
                                self.draw_status(
                                    algos[algo_idx], show_path,
                                    setting_mode or "")
                                pygame.time.wait(30)
                        else:
                            show_path = not show_path

                    elif event.key == pygame.K_a:
                        algo_idx = (algo_idx + 1) % len(algos)
                        maze.generate(
                            entry[0], entry[1],
                            exit_x=exit_pt[0], exit_y=exit_pt[1],
                            seed=seed, algo=algos[algo_idx], perfect=is_perfect)
                        # Calculate path first to avoid 42 conflicts
                        path = bfs_find_path(maze, entry, exit_pt)
                        path_set = set(path) if path else set()
                        path_set.add(entry)
                        path_set.add(exit_pt)
                        # Recalculate 42 pattern avoiding path
                        fortytwo_start = find_42_location(maze, path_set)
                        fortytwo_cells = get_42_pattern(
                            fortytwo_start[0], fortytwo_start[1])
                        show_path = False

                    elif event.key == pygame.K_m:
                        # Toggle between perfect and non-perfect mazes
                        is_perfect = not is_perfect
                        maze.generate(
                            entry[0], entry[1],
                            exit_x=exit_pt[0], exit_y=exit_pt[1],
                            seed=seed, algo=algos[algo_idx], perfect=is_perfect)
                        # Calculate path first to avoid 42 conflicts
                        path = bfs_find_path(maze, entry, exit_pt)
                        path_set = set(path) if path else set()
                        path_set.add(entry)
                        path_set.add(exit_pt)
                        # Recalculate 42 pattern avoiding path
                        fortytwo_start = find_42_location(maze, path_set)
                        fortytwo_cells = get_42_pattern(
                            fortytwo_start[0], fortytwo_start[1])
                        show_path = False

                    elif event.key == pygame.K_r:
                        seed = rng.randrange(1_000_000_000)
                        maze.generate(
                            entry[0], entry[1],
                            exit_x=exit_pt[0], exit_y=exit_pt[1],
                            seed=seed, algo=algos[algo_idx], perfect=is_perfect)
                        # Calculate path first to avoid 42 conflicts
                        path = bfs_find_path(maze, entry, exit_pt)
                        path_set = set(path) if path else set()
                        path_set.add(entry)
                        path_set.add(exit_pt)
                        # Recalculate 42 pattern avoiding path
                        fortytwo_start = find_42_location(maze, path_set)
                        fortytwo_cells = get_42_pattern(
                            fortytwo_start[0], fortytwo_start[1])
                        show_path = False

            # Draw
            self.draw_maze(
                maze, entry, exit_pt,
                path if show_path else None,
                fortytwo_cells=fortytwo_cells)
            self.draw_status(algos[algo_idx], show_path, setting_mode or "", is_perfect)

            self.clock.tick(60)

        pygame.quit()


def main():
    renderer = MazeRenderer(width=30, height=20, cell_size=25)
    renderer.run()


if __name__ == "__main__":
    main()
