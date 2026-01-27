

def get_dynamic_sleep(index, base_delay):
    return max(0.005, float(base_delay) - (index * 0.001))


def encode_cell_walls(maze, x, y):
    """Encode walls of a cell as hexadecimal.

    Bit 0 (LSB): North wall
    Bit 1: East wall
    Bit 2: South wall
    Bit 3: West wall
    """
    value = 0

    # Check North wall (y-1)
    if y == 0 or maze.grid[y-1][x] == maze.WALL:
        value |= 0x1

    # Check East wall (x+1)
    if x == maze.width - 1 or maze.grid[y][x+1] == maze.WALL:
        value |= 0x2

    # Check South wall (y+1)
    if y == maze.height - 1 or maze.grid[y+1][x] == maze.WALL:
        value |= 0x4

    # Check West wall (x-1)
    if x == 0 or maze.grid[y][x-1] == maze.WALL:
        value |= 0x8

    return format(value, 'X')


def save_maze_to_file(maze, filename, entry=None, exit_pt=None, path=None):
    """Save maze in hexadecimal format with entry, exit, and path."""
    try:
        with open(filename, 'w') as f:
            # Write maze in hex format
            for y in range(maze.height):
                line = ''
                for x in range(maze.width):
                    if maze.grid[y][x] == maze.PATH:
                        line += encode_cell_walls(maze, x, y)
                    else:
                        line += 'F'  # All walls closed
                f.write(line + '\n')

            # Add empty line
            f.write('\n')

            # Add entry, exit, and path
            if entry and exit_pt and path:
                f.write(f"{entry[0]},{entry[1]}\n")
                f.write(f"{exit_pt[0]},{exit_pt[1]}\n")

                # Convert path to directions
                directions = []
                for i in range(len(path) - 1):
                    x1, y1 = path[i]
                    x2, y2 = path[i + 1]
                    if y2 < y1:
                        directions.append('N')
                    elif y2 > y1:
                        directions.append('S')
                    elif x2 > x1:
                        directions.append('E')
                    elif x2 < x1:
                        directions.append('W')
                f.write(''.join(directions) + '\n')
    except Exception as e:
        print(f"Error saving maze to file {filename}: {e}")
