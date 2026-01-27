import time
import sys
import shutil
from mazegen.pathfinder import solve_maze
from mazegen.maze_renderer import display_terminal, RED, BOLD, BLINK, RESET
from mazegen.config_parser import parser
from mazegen.utils import get_dynamic_sleep, force_path, save_maze_to_file
from mazegen.maze_42_generator import generate_perfect_maze_with_42
import random


def main() -> None:
    # Load configuration
    try:
        cfg = parser("config.txt")
        w = int(cfg.get('width', 21))
        h = int(cfg.get('height', 21))
        delay = float(cfg.get('delay', 0.05))
        seed = cfg.get('seed')
        perfect = cfg.get('perfect', True)
        show_path = True  # Toggle for showing solution path
        highlight_42 = False  # Toggle for highlighting 42 pattern
        wall_color = 'white'  # Current wall color

        while True:
            cols, lines = shutil.get_terminal_size()
            max_x, max_y = cols, lines
            if h + 4 > max_y or (w * 2) + 2 > max_x:
                print(BOLD + "TERMINAL TOO SMALL!" + RESET)
                print(f"Required: {w*2}x{h+4} | Current: {max_x}x{max_y}")
                prompt = "Resize your window. Press Q to quit, Enter to retry: "
                ans = input(prompt).strip().lower()
                if ans == 'q':
                    break
                continue

            start_pt = cfg.get('entry', (1, 1))
            end_pt = cfg.get('exit', (w - 2, h - 2))

            my_maze = generate_perfect_maze_with_42(
                w, h, start_pt, end_pt, perfect, seed
            )

            path_found = solve_maze(my_maze, start_pt, end_pt)

            if path_found and show_path:
                for i in range(1, len(path_found) + 1):
                    display_terminal(my_maze, start_pt, end_pt,
                                     path_found[:i], highlight_42, wall_color)
                    time.sleep(get_dynamic_sleep(i, delay))
                # Keep final path displayed
                display_terminal(my_maze, start_pt, end_pt,
                                 path_found, highlight_42, wall_color)
            elif path_found and not show_path:
                display_terminal(my_maze, start_pt, end_pt,
                                 None, highlight_42, wall_color)
            else:
                display_terminal(my_maze, start_pt, end_pt,
                                 None, highlight_42, wall_color)
                print(RED + BLINK + "!! NO PATH FOUND !!" + RESET)

            menu = (
                "Q: Quit | F: Force Path | P: Toggle Perfect | S: Toggle Seed\n"
                "H: Toggle Path | 4: Toggle 42 | C: Change Wall Color | V: Save\n"
            )
            cmd = input(menu).strip()
            if cmd == 'q' or cmd == 'Q':
                sys.exit(0)
            if cmd == 'f' or cmd == 'F':
                force_path(my_maze, path_found if path_found else [])
            if cmd == 'p' or cmd == 'P':
                perfect = not perfect
            if cmd == 's' or cmd == 'S':
                seed = None if seed is not None else random.randint(0, 10000)
            if cmd == 'h' or cmd == 'H':
                show_path = not show_path
                status = "ON" if show_path else "OFF"
                print(BOLD + f"Path display: {status}" + RESET)
            if cmd == '4':
                highlight_42 = not highlight_42
                status = "ON" if highlight_42 else "OFF"
                print(BOLD + f"42 highlight: {status}" + RESET)
            if cmd == 'c' or cmd == 'C':
                colors = ['white', 'cyan', 'green', 'yellow', 'magenta', 'red']
                current_idx = colors.index(wall_color) if wall_color in colors else 0
                wall_color = colors[(current_idx + 1) % len(colors)]
                print(BOLD + f"Wall color: {wall_color}" + RESET)
            if cmd == 'v' or cmd == 'V':
                output_file = cfg.get('output_file', 'maze.txt')
                save_maze_to_file(my_maze, output_file, start_pt,
                                  end_pt, path_found)
                print(BOLD + f"Maze saved to '{output_file}'" + RESET)
            time.sleep(0.05)
    except Exception as e:
        print(RED + f"Error: {e}" + RESET)
        print(RED + "Exiting program." + RESET)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExited by user.")
        sys.exit(0)
