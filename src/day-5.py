import numpy as np
import pandas as pd
import argparse
import sys


def day_five_p1(in_file):
    rules = []
    sequences = []

    with open(in_file, 'r') as file:
        # Read rules until a blank line is encountered
        reading_rules = True
        for line in file:
            stripped_line = line.strip()
            if stripped_line == '':
                # Blank line marks end of rules
                reading_rules = False
                continue

            if reading_rules:
                # Split rule by "|" and convert to integers
                parts = stripped_line.split('|')
                rules.append(tuple(map(int, parts)))
            else:
                # After the blank line, read sequences
                sequences.append(stripped_line)
    # Convert sequences to a pandas DataFrame, assuming sequences are CSV strings
    sequences_df = pd.DataFrame([seq.split(',') for seq in sequences])

    # Check if each row contains values x and y from rules and if the column index of x is < column index of y
    def rules_checker(row):
        for x, y in rules:
            x = str(x)
            y = str(y)
            if x in row.values and y in row.values:
                x_index = row[row == x].index[0]
                y_index = row[row == y].index[0]
                if x_index >= y_index:
                    return False
        return True

    sequences_df['valid'] = sequences_df.apply(rules_checker, axis=1)

    # Calculate the sum of the middle index for every valid sequence
    valid_sequences = sequences_df[sequences_df['valid']].drop(columns=['valid']).copy()
    middle_sum = 0
    for _, row in valid_sequences.iterrows():
        row = np.array(row.dropna())
        mid_row = len(row) // 2
        middle_value = row[mid_row]
        middle_sum += int(middle_value)

    print("Sum of middle index for valid sequences:", middle_sum)


def day_five_p2(in_file):
    rules = []
    sequences = []

    with open(in_file, 'r') as file:
        # Read rules until a blank line is encountered
        reading_rules = True
        for line in file:
            stripped_line = line.strip()
            if stripped_line == '':
                # Blank line marks end of rules
                reading_rules = False
                continue

            if reading_rules:
                # Split rule by "|" and convert to integers
                parts = stripped_line.split('|')
                rules.append(tuple(map(int, parts)))
            else:
                # After the blank line, read sequences
                sequences.append(stripped_line)
    # Convert sequences to a pandas DataFrame, assuming sequences are CSV strings
    sequences_df = pd.DataFrame([seq.split(',') for seq in sequences])

    # Check if each row contains values x and y from rules and if the column index of x is < column index of y
    def rules_checker(row):
        for x, y in rules:
            x = str(x)
            y = str(y)
            if x in row.values and y in row.values:
                x_index = row[row == x].index[0]
                y_index = row[row == y].index[0]
                if x_index >= y_index:
                    return False
        return True

    sequences_df['valid'] = sequences_df.apply(rules_checker, axis=1)

    # Extract the invalid sequences
    invalid_sequences = sequences_df[~sequences_df['valid']].drop(columns=['valid']).copy()

    # Rearrange the columns in invalid sequences to create a valid sequence
    rearranged_sequences = []
    for idx, row in invalid_sequences.iterrows():
        row = row.dropna()
        len_row = len(row)

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
                        row_list[x_index], row_list[y_index] = row_list[y_index], row_list[x_index]
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
    parser = argparse.ArgumentParser(description="Load input")
    parser.add_argument('input_path', type=str,
                        help="Path to the file containing input data")
    args = parser.parse_args()
    day_five_p1(args.input_path)
    day_five_p2(args.input_path)


if __name__ == "__main__":
    main()
