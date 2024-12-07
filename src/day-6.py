#!/usr/bin/env python

"""Day 6: Guard's Path Simulation.

This module contains the solution for Day 6, which simulates the guard's path
through a labyrinth and identifies loop-inducing positions.

Functions:
    simulate_guard: Simulates the guard's movement and detects loops or exits.
    day_six_p1: Solves part 1 by counting visited positions.
    day_six_p2: Solves part 2 by identifying loop-inducing positions.
    plot_positions: Visualizes visited positions.
    plot_loops: Visualizes loop scenarios caused by obstacles.
"""

import argparse

import matplotlib.pyplot as plt


def simulate_guard(lab, start_r, start_c, start_dir):
    """Simulate the guard's movement through the labyrinth.

    Args:
        lab (list of list of str): The labyrinth represented as a grid.
        start_r (int): Starting row of the guard.
        start_c (int): Starting column of the guard.
        start_dir (int): Initial direction of the guard
                    (0: up, 1: right, 2: down, 3: left).

    Returns:
        tuple: A set of visited positions, a boolean
                indicating if the guard left the map,
                and the path taken by the guard.
    """
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

        if lab[nr][nc] == "#":
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
    """Solve part 1 by simulating the guard's movement and logging positions.

    Args:
        in_file (str): Path to the input file containing the labyrinth.

    Returns:
        tuple: A set of visited positions and the dimensions
            of the labyrinth (rows, cols).
    """
    with open(in_file) as file:
        lab = [list(line.strip("\n")) for line in file]

    rows = len(lab)
    cols = len(lab[0]) if rows > 0 else 0
    direction_map = {"^": 0, ">": 1, "v": 2, "<": 3}
    guard_row, guard_col, guard_dir = None, None, None

    # Find guard start
    for r in range(rows):
        for c in range(cols):
            if lab[r][c] in direction_map:
                guard_row, guard_col = r, c
                guard_dir = direction_map[lab[r][c]]
                lab[r][c] = "."
                break
        if guard_row is not None:
            break

    visited_positions, left_map, path = simulate_guard(
        lab, guard_row, guard_col, guard_dir
    )
    return visited_positions, (rows, cols)


def day_six_p2(in_file):
    """Solve part 2 by identifying loop-inducing positions.

    Args:
        in_file (str): Path to the input file containing the labyrinth.

    Returns:
        tuple: A set of visited positions, a dictionary of
                loop-causing positions to their paths,
                and the dimensions of the labyrinth (rows, cols).
    """
    with open(in_file) as file:
        lab = [list(line.strip("\n")) for line in file]

    rows = len(lab)
    cols = len(lab[0]) if rows > 0 else 0
    direction_map = {"^": 0, ">": 1, "v": 2, "<": 3}
    guard_row, guard_col, guard_dir = None, None, None

    # Find guard start
    for r in range(rows):
        for c in range(cols):
            if lab[r][c] in direction_map:
                guard_row, guard_col = r, c
                guard_dir = direction_map[lab[r][c]]
                lab[r][c] = "."
                break
        if guard_row is not None:
            break

    visited_positions, _, _ = simulate_guard(lab, guard_row, guard_col, guard_dir)
    test_positions = visited_positions - {(guard_row, guard_col)}

    loop_positions = {}
    for rr, cc in test_positions:
        if lab[rr][cc] == ".":
            lab[rr][cc] = "#"
            _, left_map, path = simulate_guard(lab, guard_row, guard_col, guard_dir)
            if not left_map:
                loop_positions[(rr, cc)] = path
            lab[rr][cc] = "."

    return visited_positions, loop_positions, (rows, cols)


def plot_positions(visited_positions, rows, cols):
    """Plot the guard's visited positions in the labyrinth.

    Args:
        visited_positions (set of tuple): Set positions visited by the guard.
        rows (int): Number of rows in the labyrinth.
        cols (int): Number of columns in the labyrinth.
    """
    xs_visited = [c for (r, c) in visited_positions]
    ys_visited = [r for (r, c) in visited_positions]

    plt.figure(figsize=(8, 8))
    plt.scatter(xs_visited, ys_visited, marker="s", s=40, c="blue", label="Visited")
    plt.title("Guard's Path")
    plt.xlabel("Column")
    plt.ylabel("Row")
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_loops(loop_positions, rows, cols):
    """Plot loop scenarios caused by placing obstacles.

    Args:
        loop_positions (dict): Dictionary of obstacles and loop paths.
        rows (int): Number of rows in the labyrinth.
        cols (int): Number of columns in the labyrinth.
    """
    for obstacle, path in loop_positions.items():
        plt.figure(figsize=(8, 8))
        xs = [c for (r, c) in path]
        ys = [r for (r, c) in path]
        plt.scatter(xs, ys, marker="s", s=40, c="blue", label="Loop Path")
        plt.scatter(
            [obstacle[1]], [obstacle[0]], marker="X", s=100, c="red", label="Obstacle"
        )
        plt.title(f"Loop Caused by Obstacle at {obstacle}")
        plt.xlabel("Column")
        plt.ylabel("Row")
        plt.gca().invert_yaxis()
        plt.grid(True)
        plt.legend()
        plt.show()


def main():
    """Main function to parse arguments and execute solutions."""
    parser = argparse.ArgumentParser(description="Load input")
    parser.add_argument(
        "input_path", type=str, help="Path to the file containing input data"
    )
    parser.add_argument(
        "--part", type=int, default=1, help="Puzzle part: 1 or 2 (default=1)"
    )
    parser.add_argument(
        "--display", action="store_true", help="Display a plot of the results"
    )
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
            if len(loop_positions) == 0:
                plot_positions(visited_positions, rows, cols)
            else:
                plot_loops(loop_positions, rows, cols)


if __name__ == "__main__":
    main()
