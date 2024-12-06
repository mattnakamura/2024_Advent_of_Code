import numpy as np
import pandas as pd
import argparse
import re
import sys


def day_three_p1(in_file):
    # Load input Data
    with open(in_file, 'r') as f:
        lines = f.readlines()

    # Remove newline characters and create a DataFrame
    df = pd.DataFrame([line.strip() for line in lines], columns=['Lines'])

    # Function to find mul pattern
    def find_mul_patterns(line):
        # Regex for the pattern: "mul(1-3 digit#,1-3digit#)"
        pattern = r"mul\(\d{1,3},\d{1,3}\)"
        return re.findall(pattern, line)

    # Define a function to compute the sum of products from the matches
    def compute_mul_sum(mul_list):
        total = 0
        for mul in mul_list:
            # Extract numbers from the mul pattern
            numbers = re.findall(r'\d+', mul)
            if len(numbers) == 2:
                total += int(numbers[0]) * int(numbers[1])
        return total

    # Find and Calc muls
    df['Muls'] = df['Lines'].apply(find_mul_patterns)
    df['Sum'] = df['Muls'].apply(compute_mul_sum)

    # Determin sum of muls
    total = df['Sum'].sum()
    print(f"Total is {total}")


def day_three_p2(in_file):
    # Load input data
    with open(in_file, 'r') as f:
        lines = f.readlines()

    # Create DataFrame with cleaned lines
    df = pd.DataFrame([line.strip() for line in lines], columns=['Lines'])

    def clean_line(line):
        # Regex to match "do", "don't", and mul(...) patterns
        pattern = r"(don't|do|mul\(\d{1,3},\d{1,3}\))"

        # Find all matches
        matches = re.findall(pattern, line)

        # Process the matches into tuples
        output = []
        context = None  # Tracks the last "do" or "don't"

        for match in matches:
            if match in {"do", "don't"}:
                # Update the current context
                context = match
            elif match.startswith("mul"):
                # Pair the current context with the mul(...)
                output.append((context, match))
                # Reset context for subsequent mul entries
                context = None
            else:
                # Ignore unrelated matches
                continue

        return output


    def compute_mul_sum(paired_list):
        total = 0
        operation = True  # Tracks whether we are allowed to add `mul` values
        for prefix, mul in paired_list:
            if prefix == "don't":
                operation = False  # Disable processing until a "do" is encountered
            elif prefix == "do":
                operation = True  # Enable processing

            # If operation is allowed, process the `mul`
            if operation:
                # Extract numbers from the mul pattern
                numbers = re.findall(r'\d+', mul)
                if len(numbers) == 2:
                    total += int(numbers[0]) * int(numbers[1])

        return total

    # Apply cleaning to each line
    df['Paired_Lines'] = df['Lines'].apply(clean_line)

    # Apply the sum computation to the paired lines
    df['Sum'] = df['Paired_Lines'].apply(compute_mul_sum)

    # Calculate and print total sum of all mul products
    total = df['Sum'].sum()
    print(f"Total Sum of mul products: {total}")


def day_three_p2_but_im_not_happy(in_file):
    # Load input data
    with open(in_file, 'r') as f:
        lines = f.read().replace('\n', '')

    # Regex to match "do", "don't", and mul(...) patterns
    pattern = r"(don't\(\)|do\(\)|mul\(\d{1,3},\d{1,3}\))"

    # Find all matches
    matches = re.findall(pattern, lines)
    proc_line = []
    opp_state = True
    for match in matches:
        if match == "don't()":
            opp_state = False
            continue
        elif match == "do()":
            opp_state = True
            continue
        if opp_state:
            proc_line.append(match)

    def compute_mul_sum(mul_list):
        total = 0
        for mul in mul_list:
            # Extract numbers from the mul pattern
            numbers = re.findall(r'\d+', mul)
            if len(numbers) == 2:
                total += int(numbers[0]) * int(numbers[1])
        return total
    total = compute_mul_sum(proc_line)
    print(f"Total Sum of mul with do and don't: {total}")


def main():
    parser = argparse.ArgumentParser(description="Load input")
    parser.add_argument('input_path', type=str,
                        help="Path to the file containing input data")
    args = parser.parse_args()
    day_three_p1(args.input_path)
    # day_three_p2(args.input_path) #Why
    day_three_p2_but_im_not_happy(args.input_path)



if __name__ == "__main__":
    main()
