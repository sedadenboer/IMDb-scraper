# extract.py
#
# Course: programmeerplatform
# Name: Seda den Boer
# Student number: 12179981
#
# This program creates a file top5.csv containing the top 5 movies of every year from 1930 to 2020.
# - Has to be paired with movies.csv which is a file containing movie data from IMDb.
# - Command line includes an optional -n to adjust the top N amount of movies, input file and output file.

import pandas as pd
import argparse


def main(N, input, output):
    """
    Reads movies.csv and generates a subset containing the top N movies for every year.
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