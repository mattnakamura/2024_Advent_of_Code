#!/usr/bin/env python

"""Day 1 solutions for Advent of Code 2024.

This module contains functions for solving the puzzles in Day 1 of
the Advent of Code 2024 challenge. Each function represents a part
of the challenge, with `day_one_p1` for Part 1 and `day_one_p2` for Part 2.
"""

import argparse
from collections import Counter

import numpy as np
import pandas as pd


def day_one_p1(in_file):
    """Solve Part 1 of Day 1."""
    df = pd.read_csv(in_file, sep=r"\s+", header=None)
    series_a = df[1].sort_values().reset_index(drop=True)
    series_b = df[0].sort_values().reset_index(drop=True)
    dist = np.abs(series_a - series_b)
    total = np.sum(dist)
    print(f"Total Distance: {total}")


def day_one_p2(in_file):
    """Solve Part 2 of Day 1."""
    df = pd.read_csv(in_file, sep=r"\s+", header=None)
    series_a = df[1].sort_values().reset_index(drop=True)
    series_b = df[0].sort_values().reset_index(drop=True)
    freq_count = Counter(series_a)
    similarity_score = sum(x * freq_count[x] for x in series_b)
    print(f"Similarity Score: {similarity_score}")


def main():
    """Main."""
    parser = argparse.ArgumentParser(description="Load input")
    parser.add_argument(
        "input_path", type=str, help="Path to the file containing input data"
    )
    args = parser.parse_args()
    day_one_p1(args.input_path)
    day_one_p2(args.input_path)


if __name__ == "__main__":
    main()
