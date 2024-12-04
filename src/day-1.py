import numpy as np
import pandas as pd
import argparse
from collections import Counter


def day_one_p1(in_file):
    df = pd.read_csv(in_file, sep='\s+', header=None)
    series_a = df[1].sort_values().reset_index(drop=True)
    series_b = df[0].sort_values().reset_index(drop=True)
    dist = np.abs(series_a - series_b)
    total = np.sum(dist)
    print(f"Total Distance: {total}")


def day_one_p2(in_file):
    df = pd.read_csv(in_file, sep='\s+', header=None)
    series_a = df[1].sort_values().reset_index(drop=True)
    series_b = df[0].sort_values().reset_index(drop=True)
    freq_count = Counter(series_a)
    similarity_score = sum(x * freq_count[x] for x in series_b)
    print(f"Similarity Score: {similarity_score}")


def main():
    parser = argparse.ArgumentParser(description="Load input")
    parser.add_argument('input_path', type=str,
                        help="Path to the file containing input data")
    args = parser.parse_args()
    day_one_p1(args.input_path)
    day_one_p2(args.input_path)


if __name__ == "__main__":
    main()
