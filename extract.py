# Name: Seda den Boer
# Student number: 12179981
"""

"""

import pandas as pd
import argparse
import numpy as np

def main(N, input, output):
    """
    Info
    """
    df = pd.read_csv(input).sort_values(['year', 'rating', 'title'], ascending=(True, False, True))
    topn_df = df.groupby('year').head(N)
    topn_df.to_csv(output, index=False)

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "get top N movies from movies.csv")

    # Adding arguments
    parser.add_argument("-n", "--top_n", type=int, default = 5, help="top N movies (default 5)")
    parser.add_argument("input_file", help = "input file (csv)")
    parser.add_argument("output_file", help = "output file (csv)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(args.top_n, args.input_file, args.output_file)