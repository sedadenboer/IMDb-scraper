# Name: Seda den Boer
# Student number: 12179981
"""
Scrape top movies from www.imdb.com between start_year and end_year (e.g., 1930 and 2020)
Continues scraping until at least a top 5 for each year can be created.
Saves results to a CSV file
"""

from helpers import simple_get
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from math import ceil
import argparse
import numpy as np

IMDB_URL = 'https://www.imdb.com/search/title/?title_type=feature&release_date=1930-01-01,2020-01-01&num_votes=5000,&sort=user_rating,desc&start=1&view=advanced'

def main(output_file_name, start_year, end_year):
    """
    Info
    """
    # random years to test program with
    start_year = 2014
    end_year = 2018

    # calculate the amount of years specified in the time interval
    year_interval = end_year - start_year + 1
    print('year interval', year_interval)

    # initialize
    df_list = []
    total_counts = pd.Series([], dtype='object')
    page = 1

    while True:
        # changeable page url, based on what page we're looking at
        page_url = "https://www.imdb.com/search/title/?title_type=feature&release_date=1930-01-01,2020-01-01&num_votes=5000,&sort=user_rating,desc&start=" + str(page) + "&view=advanced"

        # load website with BeautifulSoup
        html = simple_get(page_url)
        dom = BeautifulSoup(html, 'html.parser')

        # extract movies from website
        movies_df = extract_movies(dom).sort_values('year', ascending=False)

        # mask values that are not in the specified year interval range and put dataframes in a list
        movies_df = movies_df[np.logical_and(movies_df.year >= start_year, movies_df.year <= end_year)]
        df_list.append(movies_df)

        # tracking counts of movies in every year and adding these up as we're looping
        counts = movies_df['year'].value_counts().sort_index(ascending=False)
        total_counts = total_counts.add(counts, fill_value=0).sort_index(ascending=False)
        print(total_counts)

        # amount of movies retrieved of a certain year has to be greater than or equal to 5
        threshold = total_counts.value_counts() < 2 # for now I set this value to 1, to make testing the code easier
        print(threshold)

        # print(movies_df)

        # condition 1: movies from every year of the time interval, condition 2: at least 5 movies for every year
        counted_years = total_counts.size
        if counted_years == year_interval and not threshold.any():
            break
        
        # change pagenumber to retrieve movie data from multiple pages if necessary
        page += 50
        

    print('size', total_counts.size)

    # join all gathered dataframes from the loop into one big dataframe
    all_movies_df = pd.concat(df_list).sort_values(['year', 'rating'], ascending=False)
    print(all_movies_df)

    # save results to output file
    # all_movies_df.to_csv(output_file_name, index=False)


def extract_movies(dom):
    """
    Info
    """
    movies_list = []
    movie_containers = dom.find_all('div', class_ = 'lister-item-content')

    # retrieve all wanted information from the IMDb website
    for movie in movie_containers:
        title = movie.h3.a.string
        rating = movie.find('div', class_ = 'inline-block ratings-imdb-rating')['data-value']
        year_unstripped = movie.find('span', class_ = 'lister-item-year text-muted unbold').string
        year = int(re.sub("[^0-9]", "", year_unstripped))
        actor = ';'.join([a.string for a in movie.find('p', class_ = '').find_all('a')[1:]])
        runtime = movie.find('span', class_ = 'runtime').string.strip('min')
        url = ('https://www.imdb.com/' + movie.a['href'])

        # put movie information together in a list
        movie_data = [title, rating, year, actor, runtime, url]

        # put the lists with movie information in a general list for all movies
        movies_list.append(movie_data)

    # make a dataframe out of the lists with movie information
    movies_df = pd.DataFrame(movies_list, columns = ['title', 'rating', 'year', 'actors', 'runtime', 'url']).fillna('Not available')

    return movies_df


if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "extract top N movies from IMDB")

    # Adding arguments
    parser.add_argument("output", help = "output file (csv)")
    parser.add_argument("-s", "--start_year", type=int, default = 1930, help="starting year (default: 1930)")
    parser.add_argument("-e", "--end_year",   type=int, default = 2020, help="starting year (default: 2020)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.output, args.start_year, args.end_year)
