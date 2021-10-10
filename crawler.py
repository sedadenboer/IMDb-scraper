# crawler.py
#
# Course: programmeerplatform
# Name: Seda den Boer
# Student number: 12179981
#
# Scrapes language info from individual movie websites and creates a new top5 CSV file including this info.
# - Command line includes the input file name and output file name.
# - Contains get_languages(input) which retrieves and adds language info to the df.
# - Saves result into a CSV file. 

from helpers import simple_get
from bs4 import BeautifulSoup
import pandas as pd
import argparse


def main(input_file_name, output_file_name):
    """
    Gets movies dataframe including languages and converts it to a new CSV.
    """
    df_with_languages = get_languages(input_file_name)
    df_with_languages.to_csv(output_file_name, index=False)


def get_languages(input):
    """
    Takes a CSV file with movie data as input, converts it to df and uses movie urls
    to retrieve info about language. Adds languages to new column in df.
    """
    # create dataframe from CSV, get movie urls and initialize list for retrieved languages
    df = pd.read_csv(input)
    urls = df['url']
    languages_list = []
    
    for link in urls:
        # load and parse through the websites provided by the movie urls
        html = simple_get(link)
        dom = BeautifulSoup(html, 'html.parser')

        # create container with needed language information
        language_containers = dom.find_all('li', {'class':'ipc-metadata-list__item', 'role': 'presentation', 'data-testid':'title-details-languages'})

        # check if language container exist on website
        if language_containers:
             # find all anchor tags
            for item in language_containers:
                first_search = item.find_all('a')

                # make sure searched anchor tags exist
                if first_search:
                    # search for language strings and add to language list
                    languages = ';'.join([language.string for language in item.find_all('a')])
                    languages_list.append(languages)
                else:
                    # if searched anchor tag doesn't exist 
                    languages_list.append('Not available')
        else:
            # if language container doesn't exist
            languages_list.append('Not available')
    
    # add language list as column to df
    df['languages'] = languages_list

    return df


if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "generate top 5 movies with languages")

    # Adding arguments
    parser.add_argument("input_file", help = "input file (csv)")
    parser.add_argument("output_file", help = "output file (csv)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(args.input_file, args.output_file)