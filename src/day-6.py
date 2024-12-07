import numpy as np
import argparse
import matplotlib.pyplot as plt

def simulate_guard(lab, start_r, start_c, start_dir):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    rows = len(lab)
    cols = len(lab[0]) if rows > 0 else 0

    visited_positions = set()
    visited_states = set()  # (r, c, d)
    path = []

    r, c, d = start_r, start_c, start_dir
    visited_positions.add((r, c))
    visited_states.add((r, c, d))
    path.append((r, c))

    while True:
        dr, dc = directions[d]
        nr, nc = r + dr, c + dc

        # Check bounds
        if not (0 <= nr < rows and 0 <= nc < cols):
            # Guard leaves map
            return visited_positions, True, path

        if lab[nr][nc] == '#':
            # Turn right
            d = (d + 1) % 4
        else:
            # Move forward
            r, c = nr, nc
            visited_positions.add((r, c))
            path.append((r, c))
            state = (r, c, d)
            if state in visited_states:
                # Loop detected
                return visited_positions, False, path
            visited_states.add(state)

def day_six_p1(in_file):
    with open(in_file, 'r') as file:
        lab = [list(line.strip('\n')) for line in file]

    rows = len(lab)
    cols = len(lab[0]) if rows > 0 else 0
    direction_map = {'^': 0, '>': 1, 'v': 2, '<': 3}
    guard_row, guard_col, guard_dir = None, None, None

    # Find guard start
    for r in range(rows):
        for c in range(cols):
            if lab[r][c] in direction_map:
                guard_row, guard_col = r, c
                guard_dir = direction_map[lab[r][c]]
                lab[r][c] = '.'
                break
        if guard_row is not None:
            break

    visited_positions, left_map, path = simulate_guard(lab, guard_row, guard_col, guard_dir)
    return visited_positions, (rows, cols)

def day_six_p2(in_file):
    with open(in_file, 'r') as file:
        lab = [list(line.strip('\n')) for line in file]

    rows = len(lab)
    cols = len(lab[0]) if rows > 0 else 0
    direction_map = {'^': 0, '>': 1, 'v': 2, '<': 3}
    guard_row, guard_col, guard_dir = None, None, None

    # Find guard start
    for r in range(rows):
        for c in range(cols):
            if lab[r][c] in direction_map:
                guard_row, guard_col = r, c
                guard_dir = direction_map[lab[r][c]]
                lab[r][c] = '.'
                break
        if guard_row is not None:
            break

    # Original run
    visited_positions, left_map_initial, _ = simulate_guard(lab, guard_row, guard_col, guard_dir)
    test_positions = visited_positions - {(guard_row, guard_col)}

    loop_positions = {}
    # Try placing an obstacle at each visited position
    for (rr, cc) in test_positions:
        if lab[rr][cc] == '.':
            lab[rr][cc] = '#'
            # Re-run simulation to see if a loop forms
            _, left_map, path = simulate_guard(lab, guard_row, guard_col, guard_dir)
            if not left_map:
                # Found a loop-inducing position, store its path
                loop_positions[(rr, cc)] = path
            # Remove obstacle
            lab[rr][cc] = '.'

    return visited_positions, loop_positions, (rows, cols)

def plot_positions(visited_positions, rows, cols):
    xs_visited = [c for (r, c) in visited_positions]
    ys_visited = [r for (r, c) in visited_positions]

    plt.figure(figsize=(8,8))
    plt.scatter(xs_visited, ys_visited, marker='s', s=40, c='blue', label='Visited')
    plt.title("Guard's Path")
    plt.xlabel("Column")
    plt.ylabel("Row")
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_loops(loop_positions, rows, cols):
    # loop_positions is a dict: {(r,c): path}, each path showing a loop scenario.
    # We'll plot each loop scenario separately.
    for obstacle, path in loop_positions.items():
        plt.figure(figsize=(8,8))
        xs = [c for (r, c) in path]
        ys = [r for (r, c) in path]
        plt.scatter(xs, ys, marker='s', s=40, c='blue', label='Loop Path')
        # Mark the obstacle position clearly
        plt.scatter([obstacle[1]], [obstacle[0]], marker='X', s=100, c='red', label='Obstacle')

        plt.title(f"Loop Caused by Obstacle at {obstacle}")
        plt.xlabel("Column")
        plt.ylabel("Row")
        plt.gca().invert_yaxis()
        plt.grid(True)
        plt.legend()
        plt.show()

def main():
    parser = argparse.ArgumentParser(description="Load input")
    parser.add_argument('input_path', type=str, help="Path to the file containing input data")
    parser.add_argument('--part', type=int, default=1, help="Puzzle part: 1 or 2 (default=1)")
    parser.add_argument('--display', action='store_true', help="Display a plot of the results")
    args = parser.parse_args()

    if args.part == 1:
        visited_positions, (rows, cols) = day_six_p1(args.input_path)
        print(len(visited_positions))
        if args.display:
            plot_positions(visited_positions, rows, cols)
    else:
        visited_positions, loop_positions, (rows, cols) = day_six_p2(args.input_path)
        print(len(loop_positions))
        if args.display:
            # For Part 2, we now plot the loop scenarios individually
            if len(loop_positions) == 0:
                # If no loops, just show visited positions
                plot_positions(visited_positions, rows, cols)
            else:
                # Show each loop scenario in its own plot
                plot_loops(loop_positions, rows, cols)

if __name__ == "__main__":
    main()
