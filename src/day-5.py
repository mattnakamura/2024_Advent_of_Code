#!/usr/bin/env python

"""Day 5: Sequence Rule Checker.

This module processes sequences and checks their validity based on given rules.
It also rearranges invalid sequences to make them valid and computes the sum
of the middle index values for both valid and rearranged sequences.
"""

import argparse

import numpy as np
import pandas as pd


def day_five_p1(in_file):
    """Solve part 1 by checking sequence validity and summing middle values.

    Args:
        in_file (str): Path to the input file containing rules and sequences.
    """
    rules = []
    sequences = []

    with open(in_file) as file:
        # Read rules until a blank line is encountered
        reading_rules = True
        for line in file:
            stripped_line = line.strip()
            if stripped_line == "":
                # Blank line marks end of rules
                reading_rules = False
                continue

            if reading_rules:
                # Split rule by "|" and convert to integers
                parts = stripped_line.split("|")
                rules.append(tuple(map(int, parts)))
            else:
                # After the blank line, read sequences
                sequences.append(stripped_line)

    # Convert sequences to a pandas DataFrame, assuming sequences are CSV strings
    sequences_df = pd.DataFrame([seq.split(",") for seq in sequences])

    def rules_checker(row):
        """Check if a sequence row satisfies the rules.

        Args:
            row (pd.Series): A row of the sequence DataFrame.

        Returns:
            bool: True if the row satisfies all rules, False otherwise.
        """
        for x, y in rules:
            x = str(x)
            y = str(y)
            if x in row.values and y in row.values:
                x_index = row[row == x].index[0]
                y_index = row[row == y].index[0]
                if x_index >= y_index:
                    return False
        return True

    sequences_df["valid"] = sequences_df.apply(rules_checker, axis=1)

    # Calculate the sum of the middle index for every valid sequence
    valid_sequences = sequences_df[sequences_df["valid"]].drop(columns=["valid"]).copy()
    middle_sum = 0
    for _, row in valid_sequences.iterrows():
        row = np.array(row.dropna())
        mid_row = len(row) // 2
        middle_value = row[mid_row]
        middle_sum += int(middle_value)

    print("Sum of middle index for valid sequences:", middle_sum)


def rules_checker(row, rules):
    """Check if a sequence row satisfies the rules.

    Args:
        row (pd.Series): A row of the sequence DataFrame.

    Returns:
        bool: True if the row satisfies all rules, False otherwise.
    """
    for x, y in rules:
        x = str(x)
        y = str(y)
        if x in row.values and y in row.values:
            x_index = row[row == x].index[0]
            y_index = row[row == y].index[0]
            if x_index >= y_index:
                return False
    return True


def day_five_p2(in_file):
    """Solve part 2 by rearranging invalid sequences and summing middle values.

    Args:
        in_file (str): Path to the input file containing rules and sequences.
    """
    rules = []
    sequences = []

    with open(in_file) as file:
        # Read rules until a blank line is encountered
        reading_rules = True
        for line in file:
            stripped_line = line.strip()
            if stripped_line == "":
                # Blank line marks end of rules
                reading_rules = False
                continue

            if reading_rules:
                # Split rule by "|" and convert to integers
                parts = stripped_line.split("|")
                rules.append(tuple(map(int, parts)))
            else:
                # After the blank line, read sequences
                sequences.append(stripped_line)

    # Convert sequences to a pandas DataFrame, assuming sequences are CSV strings
    sequences_df = pd.DataFrame([seq.split(",") for seq in sequences])
    sequences_df["valid"] = sequences_df.apply(
        lambda row: rules_checker(row, rules), axis=1
    )

    # Extract the invalid sequences
    invalid_sequences = (
        sequences_df[~sequences_df["valid"]].drop(columns=["valid"]).copy()
    )

    # Rearrange the columns in invalid sequences to create a valid sequence
    rearranged_sequences = []
    for _, row in invalid_sequences.iterrows():
        row = row.dropna()
        # Heuristic approach to rearrange row based on rules
        row_list = row.tolist()
        changed = True
        while changed:
            changed = False
            for x, y in rules:
                x = str(x)
                y = str(y)
                if x in row_list and y in row_list:
                    x_index = row_list.index(x)
                    y_index = row_list.index(y)
                    if x_index > y_index:
                        # Swap x and y to satisfy the rule
                        row_list[x_index], row_list[y_index] = (
                            row_list[y_index],
                            row_list[x_index],
                        )
                        changed = True
        rearranged_sequences.append(row_list)

    middle_sum = 0
    for row_list in rearranged_sequences:
        row = np.array([val for val in row_list if val is not None])
        mid_row = len(row) // 2
        middle_value = row[mid_row]
        middle_sum += int(middle_value)

    print("Sum of middle index for rearranged sequences:", middle_sum)


def main():
    """Main function to parse arguments and execute solutions."""
    parser = argparse.ArgumentParser(description="Load input")
    parser.add_argument(
        "input_path", type=str, help="Path to the file containing input data"
    )
    args = parser.parse_args()
    day_five_p1(args.input_path)
    day_five_p2(args.input_path)


if __name__ == "__main__":
    main()
