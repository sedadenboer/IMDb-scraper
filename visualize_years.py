# visualize_years.py
#
# Course: programmeerplatform
# Name: Seda den Boer
# Student number: 12179981
#
# This program visualizes the average rating of the top 5 IMDb movies from 1930-2020.
# - Has to be paired with top5.csv which is a file containing top 5 movie data from IMDb.
# - Command line includes the input file name and plot file name (and storage map).
# - Contains function average(df) to calculate the average rating based on year.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse


def main(input, plot):
    """
    Reads CSV datafile into a dataframe, calls average(df), calculates the maximum average rating
    and it's corresponding year, makes a barplot and saves it as a PNG file.
    """
    # reading datafile
    df = pd.read_csv(input)

    # calculating average rating and the best average score with the corresponding year
    average_rating = average(df)
    max_rating = average_rating.values.max()
    year_max = average_rating[average_rating == max_rating].index[0]

    # plotting
    plt.figure(figsize=(28, 10))
    plt.bar(average_rating.index, average_rating.values, color='goldenrod')
    plt.ylim(0, 10)
    plt.yticks(np.arange(0, 11, 0.5))
    plt.xlim(1929, 2021)
    plt.xticks(np.arange(min(average_rating.index), max(average_rating.index)+1, 1.0), rotation=45)
    plt.title('Average rating of top 5 IMDb movies from 1930-2020', fontsize=25)
    plt.xlabel('Year', fontsize=18)
    plt.ylabel('Average rating', fontsize=18)
    plt.annotate(f'best year for movies: {year_max}, rating: {max_rating}', xy=(year_max, max_rating), xytext=(year_max, max_rating + 0.6),
                 fontsize=15, arrowprops=dict(facecolor="black", width=1, headwidth=4, headlength=4, shrink=0.1))
    plt.savefig(plot)


def average(df):
    """
    Calculates the average of movie ratings based on the same year.
    Takes a dataframe as input. The dataframe requires two columns 'year' and 'rating'.
    """
    avg = df.groupby('year')['rating'].mean()
    return avg


if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="plot average movie rating of top 5 movies (1930-2020)")

    # adding arguments
    parser.add_argument("input_file", help="input file (csv)")
    parser.add_argument("plot", help="plot (png)")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.input_file, args.plot)