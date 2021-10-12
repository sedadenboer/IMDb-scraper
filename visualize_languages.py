# visualize_languages.py
#
# Course: programmeerplatform
# Name: Seda den Boer
# Student number: 12179981
#
# This program visualizes language influences in the top 5 IMDb movies over the last 9 decades.
# - Has to be paired with top5-with-languages.csv which is a file containing top 5 movie data from IMDb including language data.
# - Command line includes the input file name and plot file name (and storage map).
# - Functions: language_influence(df) returns dict with language counts over full df,
#   language_count_decade(df, dict) returns dict with top 10 languages and counts for every decade.

import matplotlib.pyplot as plt
import pandas as pd
import argparse


def main(input, plot):
    """
    Reads CSV datafile into a dataframe, calls language_influence(df) and language_count_decade(df, dict),
    makes a line graph for every language from the top 10 languages and saves it as a PNG file.
    """

    # reading datafile
    df = pd.read_csv(input)
    dict = language_influence(df)
    occurence_rate = language_count_decade(df, dict)

    # generate lists with keys and values from occurence_rate dictionary (will be used for making plot labels)
    key_list = list(occurence_rate.keys())
    value_list = list(occurence_rate.values())

    # x-axis ticks
    decades = ['1930s', '1940s', '1950s', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s']

    # plot a line graph for every language in the occurence_rate dictionary (top 10 languages)
    for data_list in occurence_rate.values():
        # retrieve and set graph labels by searching for matching key (with value)
        labels = key_list[value_list.index(data_list)]
        # plot graphs in one plot
        plt.plot(decades, data_list, label=labels, linewidth=1)

    # plot characteristics and adjustments
    plt.ylim(-0.2, 50)
    plt.legend(prop={'size': 7})
    plt.title('Development of language occurence over the last 9 decades', fontsize=10)
    plt.xlabel('Decade', fontsize=9)
    plt.ylabel('Number of appearances', fontsize=9)
    plt.savefig(plot, dpi=400)


def language_count_decade(df, dict):
    """
    Returns a dictionary with the top 10 languages as keys and a list with occurence rate counts per decade as value.
    """
    # select top 10 most popular languages
    languages_top10 = list(dict.keys())[:10]

    # adjust dataframe by separating languages and exploding this column to get rows with individual languages
    df['languages'] = df['languages'].str.split(';')
    exploded_df = df.explode('languages')
    adjusted_language_df = exploded_df.loc[exploded_df['languages'].isin(languages_top10)]

    # initialize dictionary with language popularity rates
    top10_dict = {}
    for l in languages_top10:
        top10_dict[l] = []

    # initialize strating year and ending year of first decade
    start_year = 1930
    end_year = 1940

    # retrieve data until 2020
    while end_year <= 2020:
        # generate subdataframe for a decade
        sub_df = adjusted_language_df[(adjusted_language_df.year >= start_year) & (adjusted_language_df.year < end_year)].sort_values('languages')
        # count the occurrences of the most popular languages
        counts = sub_df['languages'].value_counts()

        # add counts for every language in a decade to dictionary
        for language in languages_top10:
            # check for languages if they occur in a decade
            if language in counts.index:
                # calculate the number of appearances and add to dictionary
                count = counts.get(key=language)
                top10_dict[language].append(count)
            else:
                # if a language does not occur in a certain decade add 0 to dictionary
                top10_dict[language].append(0)

        # keep adjusting the boundaries to look at the next decade
        start_year += 10
        end_year += 10

    return top10_dict


def language_influence(df):
    """
    Returns dictionary with all languages from the top 5 movie dataframe as keys and their occurrence rate as value.
    """
    language_dict = {}

    # select languages column from df, split language string from semicolon and put individual languages in a list
    languages = df['languages'].values
    languages = [word for line in languages for word in line.split(';')]

    # count language occurrence rates and add them to dict
    for language in languages:
        # if the language is already in the dictionary
        if language in language_dict:
            language_dict[language] += 1
        else:
            # if language is not yet in the dictionary
            language_dict[language] = 1

    # sort dictionary based on occurence rate from high to low
    language_dict = dict(sorted(language_dict.items(), key=lambda item: item[1], reverse=True))

    return language_dict


if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="plot language influence of top rated movies from 1930-2020")

    # adding arguments
    parser.add_argument("input_file", help="input file (csv)")
    parser.add_argument("plot", help="plot (png)")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.input_file, args.plot)