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
    # Load website with BeautifulSoup
    pages = np.arange(1, 101, 50)
    df_list = []

    for page in pages:
        page_url = "https://www.imdb.com/search/title/?title_type=feature&release_date=1930-01-01,2020-01-01&num_votes=5000,&sort=user_rating,desc&start=" + str(page) + "&view=advanced"

        html = simple_get(page_url)
        dom = BeautifulSoup(html, 'html.parser')

        # Extract movies from website
        movies_df = extract_movies(dom)
        df_list.append(movies_df)


    # Save results to output file
    all_movies_df = pd.concat(df_list).sort_values(['year', 'rating'], ascending=False)
    all_movies_df['year'] = np.clip(all_movies_df['year'], a_min = start_year, a_max = end_year)

    print(all_movies_df)

    print(all_movies_df['year'].value_counts())

    all_movies_df.to_csv(output_file_name, index=False)

def extract_movies(dom):
    """
    Info
    """
    movies_list = []
    movie_containers = dom.find_all('div', class_ = 'lister-item-content')

    # titles = []
    # ratings = []
    # years = []
    # actors = []
    # runtimes = []
    # urls = []

    for movie in movie_containers:
        title = movie.h3.a.string
        rating = movie.find('div', class_ = 'inline-block ratings-imdb-rating')['data-value']
        year_unstripped = movie.find('span', class_ = 'lister-item-year text-muted unbold').string
        year = int(re.sub("[^0-9]", "", year_unstripped))
        actor = ';'.join([a.string for a in movie.find('p', class_ = '').find_all('a')[1:]])
        runtime = movie.find('span', class_ = 'runtime').string.strip('min')
        url = ('https://www.imdb.com/' + movie.a['href'])

        # titles.append(title)
        # ratings.append(rating)
        # years.append(year)
        # actors.append(actor)
        # runtimes.append(runtime)
        # urls.append(url)

        movie_data = [title, rating, year, actor, runtime, url]
        movies_list.append(movie_data)

    movies_df = pd.DataFrame(movies_list, columns = ['title', 'rating', 'year', 'actors', 'runtime', 'url']).fillna('Not available')
    # movies_df = pd.DataFrame({'title': titles, 'rating': ratings, 'year': years, 'actors': actors, 'runtime': runtimes, 'url': urls})
    # print(movies_df['year'].value_counts())
    return movies_df


# def all_movies(df):
#     """
#     info
#     """
#     pages = np.arrange(1, N, 50)

#     for page in pages:
#         page = requests.get("https://www.imdb.com/search/title/?title_type=feature&release_date=1930-01-01,2020-01-01&num_votes=5000,&sort=user_rating,desc&start=" + str(page) + "&view=advanced")


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
