# visualize_years.py
#
# Course: programmeerplatform
# Name: Seda den Boer
# Student number: 12179981
#
# This program visualizes the popularity of the top 50 actors of the top 5 IMDb movies from 1930-2020.
# - Has to be paired with top5.csv which is a file containing top 5 movie data from IMDb .
# - Command line includes the input file and output file.
# - Contains function to calculate the number of appearances of the actors and returns it in a dictionary.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse


def main(input, plot):
    """
    Reads CSV datafile into a dataframe, calls top50_actors(df), selects first 50 actors with most appearances
    and the number of appearances, makes a barplot and saves it as a PNG file.
    """
    # reading datafile
    df = pd.read_csv(input)
    actor_frequencies = top_actors(df)

    # getting first 50 actors with most appearances
    actors_50 = list(actor_frequencies.keys())[:50]
    appearances_50 = list(actor_frequencies.values())[:50]

    # plotting
    plt.figure(figsize=(90,55))
    plt.bar(actors_50, appearances_50, color='coral')
    plt.xlim(-1, 50)
    plt.xticks(np.arange(0, 50, 1), rotation=80, fontsize=30)
    plt.yticks(fontsize=40)
    plt.title('First 50 actors with the most appearances in top 5 IMDb movies from 1930-2020', fontsize=80)
    plt.xlabel('Actor', fontsize=50)
    plt.ylabel('Number of appearances', fontsize=50)
    plt.savefig(plot)


def top_actors(df):
    """
    Creates a sorted dictionary with actor frequencies retrieved from the top 5 dataframe.
    """
    actor_dict = {}
    actors = df['actors'].values
    actors = [word for line in actors for word in line.split(';')]

    for actor in actors:
        if actor in actor_dict:
            actor_dict[actor] += 1
        else:
            actor_dict[actor] = 1

    actor_dict = dict(sorted(actor_dict.items(), key=lambda item: item[1], reverse=True))
 
    return actor_dict


if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "plot top 50 actors with most appearances (1930-2020)")

    # Adding arguments
    parser.add_argument("input_file", help = "input file (csv)")
    parser.add_argument("plot", help = "plot (png)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(args.input_file, args.plot)