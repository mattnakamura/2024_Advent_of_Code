#!/usr/bin/env python

"""Day 4: Matrix Pattern Matching.

This module implements solutions for Day 4 of Advent of Code. It processes a
matrix of characters and finds specific patterns ("XMAS" and its reverse) in
different orientations, as well as diagonal occurrences of "X-MAS."
"""

import argparse

import numpy as np


def day_four_p1(in_file):
    """Solve part 1 by finding 'XMAS' or its reverse in the matrix.

    Args:
        in_file (str): Path to the input file containing the matrix.
    """
    with open(in_file) as file:
        lines = file.readlines()  # Read all lines from the file

    # Convert each line to a list of characters and create a numpy array of them
    char_matrix = np.array([list(line.strip()) for line in lines], dtype=object)

    # Replace the characters with corresponding numbers
    char_matrix[char_matrix == "X"] = 1
    char_matrix[char_matrix == "M"] = 2
    char_matrix[char_matrix == "A"] = 3
    char_matrix[char_matrix == "S"] = 4
    char_matrix = char_matrix.astype(int)  # Convert the object array to integer type

    # Define the patterns we are looking for
    pattern = np.array([1, 2, 3, 4])  # XMAS
    reversed_pattern = np.array([4, 3, 2, 1])  # SAMX
    pattern_length = len(pattern)

    # Define rolling window function
    def rolling_window(a, window):
        shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
        strides = a.strides + (a.strides[-1],)
        return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

    # Function to count matches for a given pattern in different directions
    def count_matches(matrix, pattern):
        count = 0

        # Horizontal Search
        count += np.sum(
            np.all(rolling_window(matrix, pattern_length) == pattern, axis=-1)
        )

        # Vertical Search
        count += np.sum(
            np.all(rolling_window(matrix.T, pattern_length) == pattern, axis=-1)
        )

        # Diagonal Search (Top-Left to Bottom-Right)
        def extract_diagonals(mat, length):
            diagonals = [
                mat.diagonal(i)
                for i in range(-mat.shape[0] + length, mat.shape[1] - length + 1)
            ]
            diagonals = [d for d in diagonals if len(d) >= length]
            return diagonals

        diagonals = extract_diagonals(matrix, pattern_length)
        count += sum(
            np.sum(np.all(rolling_window(diag, pattern_length) == pattern, axis=-1))
            for diag in diagonals
        )

        # Diagonal Search (Top-Right to Bottom-Left)
        flipped_matrix = np.fliplr(matrix)
        diagonals_flipped = extract_diagonals(flipped_matrix, pattern_length)
        count += sum(
            np.sum(np.all(rolling_window(diag, pattern_length) == pattern, axis=-1))
            for diag in diagonals_flipped
        )

        return count

    # Count matches for the original pattern
    matches_original = count_matches(char_matrix, pattern)

    # Count matches for the reversed pattern
    matches_reversed = count_matches(char_matrix, reversed_pattern)

    # Total Matches
    total_matches = matches_original + matches_reversed
    print(f"Number of times 'XMAS' or its reverse is found: {total_matches}")


def day_four_p2(in_file):
    """Solve part 2 by finding 'X-MAS' diagonally in the matrix.

    Args:
        in_file (str): Path to the input file containing the matrix.
    """
    with open(in_file) as file:
        lines = file.readlines()  # Read all lines from the file

    # Convert each line to a list of characters and create a numpy array of them
    char_matrix = np.array([list(line.strip()) for line in lines], dtype=object)

    # Replace the characters with corresponding numbers
    char_matrix[char_matrix == "X"] = 1
    char_matrix[char_matrix == "M"] = 2
    char_matrix[char_matrix == "A"] = 3
    char_matrix[char_matrix == "S"] = 4
    char_matrix = char_matrix.astype(int)  # Convert the object array to integer type

    # Find all locations of '3' in the matrix (i.e., occurrences of 'A')
    positions_of_3 = np.argwhere(char_matrix == 3)

    target_count = 0

    # Iterate through the positions where '3' is found
    rows, cols = char_matrix.shape
    for position in positions_of_3:
        i, j = position

        # Skip if '3' is at the edge, as we cannot check diagonals properly
        if i > 0 and i < rows - 1 and j > 0 and j < cols - 1:
            # Check top-left to bottom-right diagonal for "MAS" or "SAM"
            if (
                char_matrix[i - 1, j - 1] == 2 and char_matrix[i + 1, j + 1] == 4
            ) or (  # "M -> A -> S"
                char_matrix[i - 1, j - 1] == 4 and char_matrix[i + 1, j + 1] == 2
            ):  # "S -> A -> M"

                # Check top-right to bottom-left diagonal for "MAS" or "SAM"
                if (
                    char_matrix[i - 1, j + 1] == 2 and char_matrix[i + 1, j - 1] == 4
                ) or (  # "M -> A -> S"
                    char_matrix[i - 1, j + 1] == 4 and char_matrix[i + 1, j - 1] == 2
                ):  # "S -> A -> M"

                    # If both diagonals satisfy the condition, we found an "X-MAS"
                    target_count += 1

    print(f"Number of times 'X-MAS' is found: {target_count}")


def main():
    """Main function to parse arguments and execute solutions."""
    parser = argparse.ArgumentParser(description="Load input")
    parser.add_argument(
        "input_path", type=str, help="Path to the file containing input data"
    )
    args = parser.parse_args()
    day_four_p1(args.input_path)
    day_four_p2(args.input_path)


if __name__ == "__main__":
    main()
