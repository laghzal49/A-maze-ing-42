import pytest
from mazegen.maze_generator import Maze
from mazegen.pathfinder import solve_maze
from mazegen.maze_validator import validate_entry_exit, has_3x3_open_areas
from mazegen.config_parser import parser


class TestMazeGenerator:
    def test_maze_creation(self):
        """Test basic maze creation."""
        maze = Maze(21, 21)
        assert maze.width == 21
        assert maze.height == 21
        assert len(maze.grid) == 21
        assert len(maze.grid[0]) == 21

    def test_maze_generation(self):
        """Test maze generation completes."""
        maze = Maze(21, 21)
        maze.generation(1, 1, perfect=True, seed=42)
        # Check that some paths exist
        path_count = sum(
            1 for row in maze.grid
            for cell in row if cell == Maze.PATH
        )
        assert path_count > 0

    def test_maze_odd_dimensions(self):
        """Test that even dimensions are converted to odd."""
        maze = Maze(20, 20)
        assert maze.width == 21
        assert maze.height == 21


class TestPathfinder:
    def test_simple_path(self):
        """Test pathfinding on a simple maze."""
        maze = Maze(5, 5)
        # Create a simple path
        for i in range(5):
            maze.grid[2][i] = Maze.PATH

        path = solve_maze(maze, (0, 2), (4, 2))
        assert path is not None
        assert len(path) > 0
        assert path[0] == (0, 2)
        assert path[-1] == (4, 2)

    def test_no_path(self):
        """Test pathfinding when no path exists."""
        maze = Maze(5, 5)
        # All walls except start and end
        maze.grid[0][0] = Maze.PATH
        maze.grid[4][4] = Maze.PATH

        path = solve_maze(maze, (0, 0), (4, 4))
        assert path is None


class TestMazeValidator:
    def test_validate_entry_exit_valid(self):
        """Test validation of valid entry/exit."""
        maze = Maze(5, 5)
        maze.grid[1][1] = Maze.PATH
        maze.grid[3][3] = Maze.PATH

        assert validate_entry_exit(maze, (1, 1), (3, 3))

    def test_validate_entry_exit_invalid(self):
        """Test validation of invalid entry/exit."""
        maze = Maze(5, 5)
        maze.grid[1][1] = Maze.WALL
        maze.grid[3][3] = Maze.PATH

        assert not validate_entry_exit(maze, (1, 1), (3, 3))

    def test_validate_entry_exit_out_of_bounds(self):
        """Test validation with out of bounds coordinates."""
        maze = Maze(5, 5)

        assert not validate_entry_exit(maze, (-1, 0), (3, 3))
        assert not validate_entry_exit(maze, (1, 1), (10, 10))

    def test_has_3x3_open_areas(self):
        """Test detection of 3x3 open areas."""
        maze = Maze(7, 7)
        # Create a 3x3 open area
        for y in range(2, 5):
            for x in range(2, 5):
                maze.grid[y][x] = Maze.PATH

        assert has_3x3_open_areas(maze)

    def test_no_3x3_open_areas(self):
        """Test that perfect mazes don't have 3x3 open areas."""
        maze = Maze(11, 11)
        maze.generation(1, 1, perfect=True, seed=42)

        # Perfect mazes generated with recursive backtracker
        # shouldn't have 3x3 open areas
        assert not has_3x3_open_areas(maze)


class TestConfigParser:
    def test_parser_valid_config(self, tmp_path):
        """Test parsing a valid config file."""
        config_file = tmp_path / "test_config.txt"
        config_file.write_text("""
WIDTH=21
HEIGHT=21
ENTRY=1,1
EXIT=19,19
OUTPUT_FILE=maze.txt
PERFECT=true
""")

        config = parser(str(config_file))
        assert config.get('width') == 21
        assert config.get('height') == 21
        assert config.get('entry') == (1, 1)
        assert config.get('exit') == (19, 19)
        assert config.get('perfect') is True

    def test_parser_invalid_file(self):
        """Test parser with non-existent file."""
        config = parser("nonexistent.txt")
        assert config == {}

    def test_parser_missing_keys(self, tmp_path):
        """Test parser with missing required keys."""
        config_file = tmp_path / "incomplete_config.txt"
        config_file.write_text("WIDTH=21\n")
        config = parser(str(config_file))
        assert config == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
