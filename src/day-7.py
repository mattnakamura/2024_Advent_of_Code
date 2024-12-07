#!/usr/bin/env python
"""Day 7: Solve calibration problems by evaluating expressions.

This module contains the solutions for Day 7, which involve evaluating
expressions with various operators and checking their solvability.
"""

import argparse
from itertools import product

import pandas as pd
from tqdm import tqdm


def evaluate_expression(operands, operators):
    """Evaluate an expression using the given operands and operators.

    Args:
        operands (list): List of integers representing operands.
        operators (list): List of operators as strings ('+', '*', '|').

    Returns:
        int: The result of the evaluated expression.
    """
    result = operands[0]
    for i in range(len(operators)):
        if operators[i] == "+":
            result += operands[i + 1]
        elif operators[i] == "*":
            result *= operands[i + 1]
        elif operators[i] == "|":
            result = int(str(result) + str(operands[i + 1]))
    return result


def check_solvability(row, operator_set="+*|"):
    """Check if the expression represented by the row can be solved.

    Args:
        row (pd.Series): A row of the DataFrame containing test value and operands.
        operator_set (str): String of operators to use for evaluation.

    Returns:
        bool: True if the expression can be solved, False otherwise.
    """
    test_value = row["test_value"]
    operands = row.dropna().values[1:]  # Skip test value and drop NaN
    num_operators = len(operands) - 1
    operator_combinations = product(operator_set, repeat=num_operators)
    for operators in operator_combinations:
        if evaluate_expression(operands, operators) == test_value:
            return True
    return False


def solve_calibration_problem(in_file, operator_set="+*|"):
    """Solve the calibration problem by checking expression solvability.

    Args:
        in_file (str): Path to the input file containing test values and operands.
        operator_set (str): String of operators to use for evaluation.
    """
    data = []
    with open(in_file) as file:
        for line in file:
            parts = line.strip().split(":")
            if len(parts) == 2:
                key = int(parts[0])  # Convert key to integer
                values = list(map(int, parts[1].strip().split()))
                data.append([key] + values)

    # Create DataFrame
    df = pd.DataFrame(data)
    df.columns = ["test_value"] + [f"operand_{i}" for i in range(df.shape[1] - 1)]

    # Apply the function to each row with a progress bar
    tqdm.pandas(desc="Processing rows")
    df["valid"] = df.progress_apply(
        lambda row: check_solvability(row, operator_set), axis=1
    )

    # Filter valid rows
    valid_df = df[df["valid"]]

    # Count the sum of test values in valid rows
    cal = valid_df["test_value"].sum()
    print(f"Calibration reports: {cal}")


def main():
    """Main function to parse arguments and execute the solution."""
    parser = argparse.ArgumentParser(description="Solve Day 7 calibration problem.")
    parser.add_argument(
        "input_path", type=str, help="Path to the file containing input data"
    )
    parser.add_argument(
        "--part", type=int, default=1, help="Puzzle part: 1 or 2 (default=1)"
    )
    args = parser.parse_args()

    operator_set = "+*" if args.part == 1 else "+*|"
    solve_calibration_problem(args.input_path, operator_set)


if __name__ == "__main__":
    main()
