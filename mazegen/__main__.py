"""Test and demonstrate path finding with real maze data."""

from .maze_generator import Maze
from .path_finder import bfs_find_path, path_to_moves

# Create and generate maze
maze = Maze(15, 12)
entry = (0, 0)
exit_pt = (14, 11)

maze.generate(entry[0], entry[1], seed=42, algo="dfs")

print("=" * 60)
print("MAZE PATHFINDER TEST")
print("=" * 60)

# Display maze
print("\nMaze (2x scaled with Unicode walls):")
print(maze)

# Find path
print("\n" + "=" * 60)
print("Finding shortest path from entry to exit...")
path = bfs_find_path(maze, entry, exit_pt)

if path:
    print(f"✓ Path found! Length: {len(path)} cells")
    print(f"\nPath coordinates: {path}")

    # Convert to moves
    moves = path_to_moves(path)
    print(f"\nMove sequence: {moves}")
    print(f"Total moves: {len(moves)}")

    # Show move breakdown
    print("\nMove breakdown:")
    north = moves.count("N")
    south = moves.count("S")
    east = moves.count("E")
    west = moves.count("W")
    print(f"  North (N): {north}")
    print(f"  South (S): {south}")
    print(f"  East  (E): {east}")
    print(f"  West  (W): {west}")
else:
    print("✗ No path found!")

print("\n" + "=" * 60)
