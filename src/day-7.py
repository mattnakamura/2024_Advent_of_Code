import pandas as pd
import sys
import argparse
from itertools import product
from tqdm import tqdm
from multiprocessing import Pool, cpu_count


def day_seven_p1(in_file):
    # Load input Data
    data = []
    with open(in_file, 'r') as file:
        for line in file:
            parts = line.strip().split(":")
            if len(parts) == 2:  # Ensure line contains expected structure
                key = int(parts[0])  # Convert key to integer
                values = list(map(int, parts[1].strip().split()))  # Convert values to integers
                data.append([key] + values)

    # Create DataFrame
    df = pd.DataFrame(data)
    df.columns = ["test_value"] + [f"operand_{i}" for i in range(df.shape[1] - 1)]

    def evaluate_expression(operands, operators):
        result = operands[0]
        for i in range(len(operators)):
            if operators[i] == "+":
                result += operands[i + 1]
            elif operators[i] == "*":
                result *= operands[i + 1]
        return result

    def check_solvability(row):
        # Extract test value and operands
        test_value = row["test_value"]
        operands = row.dropna().values[1:]  # Skip test value and drop NaN
        num_operators = len(operands) - 1
        operator_combinations = product("+*", repeat=num_operators)
        is_solvable = False
        # Check each combination
        for operators in operator_combinations:
            if evaluate_expression(operands, operators) == test_value:
                is_solvable = True
                break
        return is_solvable

    # Apply the function to each row with a progress bar
    tqdm.pandas(desc="Processing rows")
    df['valid'] = df.progress_apply(check_solvability, axis=1)

    # Filter valid rows
    valid_df = df[df["valid"] == True]

    # Count the sum of test values in valid rows
    cal = valid_df["test_value"].sum()

    print(f"Calibration reports: {cal}")


def day_seven_p2(in_file):
    # Load input Data
    data = []
    with open(in_file, 'r') as file:
        for line in file:
            parts = line.strip().split(":")
            if len(parts) == 2:  # Ensure line contains expected structure
                key = int(parts[0])  # Convert key to integer
                values = list(map(int, parts[1].strip().split()))  # Convert values to integers
                data.append([key] + values)

    # Create DataFrame
    df = pd.DataFrame(data)
    df.columns = ["test_value"] + [f"operand_{i}" for i in range(df.shape[1] - 1)]

    def evaluate_expression(operands, operators):
        result = operands[0]
        for i in range(len(operators)):
            if operators[i] == "+":
                result += operands[i + 1]
            elif operators[i] == "*":
                result *= operands[i + 1]
            elif operators[i] == "|":
                result = int(result)
                operand = int(operands[i + 1])
                result = int(str(result)+str(operand))
        return result

    def check_solvability(row):
        # Extract test value and operands
        test_value = row["test_value"]
        operands = row.dropna().values[1:]  # Skip test value and drop NaN
        num_operators = len(operands) - 1
        operator_combinations = product("+*|", repeat=num_operators)
        is_solvable = False
        # Check each combination
        for operators in operator_combinations:
            if evaluate_expression(operands, operators) == test_value:
                is_solvable = True
                break
        return is_solvable

    # Apply the function to each row with a progress bar
    tqdm.pandas(desc="Processing rows")
    df['valid'] = df.progress_apply(check_solvability, axis=1)

    # Filter valid rows
    valid_df = df[df["valid"] == True]

    # Count the sum of test values in valid rows
    cal = valid_df["test_value"].sum()

    print(f"Calibration reports: {cal}")


def main():
    parser = argparse.ArgumentParser(description="Load input")
    parser.add_argument('input_path', type=str,
                        help="Path to the file containing input data")
    parser.add_argument('--part', type=int, default=1
                        , help="Puzzle part: 1 or 2 (default=1)")
    args = parser.parse_args()

    if args.part == 1:
        day_seven_p1(args.input_path)
    else:
        day_seven_p2(args.input_path)


if __name__ == "__main__":
    main()