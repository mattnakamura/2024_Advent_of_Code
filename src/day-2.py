#!/usr/bin/env python

"""Day 2 solutions for Advent of Code 2024.

This module contains functions for solving the puzzles in Day 1 of
the Advent of Code 2024 challenge. Each function represents a part
of the challenge, with `day_two_p1` for Part 1 and `day_two_p2` for Part 2.
"""
import argparse

import numpy as np
import pandas as pd


def day_two_p1(in_file):
    """Solve Part 1 of Day 2."""
    # Load input Data
    df = pd.read_csv(in_file, sep=r"\s+", header=None)

    def check_levels(row):
        """Check levels of data."""
        # Drop NaN values
        row = row.dropna().values

        # Calculate differences
        diffs = np.diff(row)

        # Check if all increasing or all decreasing
        all_increasing = np.all(diffs > 0)
        all_decreasing = np.all(diffs < 0)

        # Check if differences are between 1 and 3
        valid_diffs = np.all((np.abs(diffs) >= 1) & (np.abs(diffs) <= 3))
        return (all_increasing or all_decreasing) and valid_diffs

    # Apply the function to each row
    df["valid"] = df.apply(check_levels, axis=1)

    # Count the number of valid reports
    safe_count = df["valid"].sum()

    print(f"Number of safe reports: {safe_count}")


def day_two_p2(in_file):
    """Solve Part 2 of Day 2."""
    # Load df
    df = pd.read_csv(in_file, sep=r"\s+", header=None)

    def check_levels(row):
        """Function to broadcast firsts check plus return outliers."""
        # Extract numbers only
        row_values = row.dropna().values

        # Ensure at least two values exist
        if len(row_values) < 2:
            return False

        # Calculate differences
        diffs = np.diff(row_values)

        # Check if all increasing or all decreasing
        all_increasing = np.all(diffs > 0)
        all_decreasing = np.all(diffs < 0)

        # Check if differences are between 1 and 3
        valid_diffs = np.all((np.abs(diffs) >= 1) & (np.abs(diffs) <= 3))

        return (all_increasing or all_decreasing) and valid_diffs

    def check_with_dampener(row):
        """Function to remove single outliers and recheck."""
        # Extract numbers only
        row_values = row.dropna().values

        # If the row is already valid, it's safe
        if check_levels(row):
            return True

        # Check removing each level to see if it makes the row valid
        for i in range(len(row_values)):
            # Remove the level at index i
            modified_row = np.delete(row_values, i)

            # Check the modified row
            if check_levels(pd.Series(modified_row)):
                return True
        return False

    # Step 1: Apply the dampener logic
    df["safe"] = df.apply(check_with_dampener, axis=1)

    # Step 2: Count the number of safe reports
    safe_count = df["safe"].sum()

    print(f"Number of safe reports: {safe_count}")


def main():
    """Main."""
    parser = argparse.ArgumentParser(description="Load input")
    parser.add_argument(
        "input_path", type=str, help="Path to the file containing input data"
    )
    args = parser.parse_args()
    day_two_p1(args.input_path)
    day_two_p2(args.input_path)


if __name__ == "__main__":
    main()
