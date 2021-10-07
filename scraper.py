# Name: Seda den Boer
# Student number: 12179981
"""
Scrape top movies from www.imdb.com between start_year and end_year (e.g., 1930 and 2020)
Continues scraping until at least a top 5 for each year can be created.
Saves results to a CSV file
"""

from helpers import simple_get
from bs4 import BeautifulSoup
import re
import pandas as pd
import argparse
import numpy as np


def main(output_file_name, start_year, end_year):
    """
    Collects the top N rated movies, with at least 5 movies for every year on a specified year interal.
    Does this by calling extract_movies(dom) in a loop until conditions are met. Eventually puts all data
    in a dataframe and saves the result in movies.csv.
    """

    # calculate the amount of years specified in the time interval
    year_interval = end_year - start_year + 1

    # initialize
    df_list = []
    total_counts = pd.Series([], dtype='object')
    page = 1

    while True:
        # changeable page url, based on what page we're looking at
        page_url = f"https://www.imdb.com/search/title/?title_type=feature&release_date={start_year}-01-01,{end_year + 1}-01-01&num_votes=5000,&sort=user_rating,desc&start=" + str(page) + "&view=advanced"

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
        
        # condition 1: movies from every year of the time interval
        counted_years = total_counts.size
        # condition 2: at least 5 movies for every year
        threshold = total_counts >= 5

        # .all() checks if threshold is True for all years and number of years in db should be equal to specified year interval
        if threshold.all() and counted_years == year_interval:
            break

        # change pagenumber to retrieve movie data from multiple pages if necessary
        page += 50

        # print statements for testing
        print(total_counts)
        print(threshold)
        print('counted_years', counted_years)
        print("NUMBER OF YEARS", year_interval, threshold.size)


    # join all gathered dataframes from the loop into one big dataframe
    all_movies_df = pd.concat(df_list).sort_values(['year', 'rating'], ascending=False)
    print(all_movies_df)

    # save results to output file
    all_movies_df.to_csv(output_file_name, index=False)


def extract_movies(dom):
    """
    Extracts movie data from html parsed IMDb page. Each movie entry is a dictionary with specified movie data fields.
    All movie dictionaries created will be put in a list and eventually be converted into a dataframe.
    """
    movies_list = []
    movie_containers = dom.find_all('div', class_ = 'lister-item-content')

    # retrieve all wanted information from the IMDb website
    for movie in movie_containers:
        # get title of movie
        title = movie.h3.a.string

        # retrieve rating and avoid None values
        rating = movie.find('div', class_ = 'inline-block ratings-imdb-rating')
        if rating:
            rating = rating['data-value']
        else:
            rating = 'No rating found'
        
        # retrieve year and avoid None values
        year_unstripped = movie.find('span', class_ = 'lister-item-year text-muted unbold')
        if year_unstripped:
            year = int(re.sub("[^0-9]", "", year_unstripped.string))
        else:
            'No year found'

        # retrieve actors and avoid None values
        actor_search = movie.find('p', class_= '').find('span', class_='ghost')
        if actor_search:
            actor = ';'.join([actor.string for actor in actor_search.find_next_siblings('a')])
        else:
            actor = 'No actors found'

        # retrieve runtime and avoid None values
        runtime = movie.find('span', class_ = 'runtime')
        if runtime:
            runtime = runtime.string.strip('min')
        else:
            runtime = '-'

        # movie url IMDb link
        url = ('https://www.imdb.com/' + movie.a['href'])

        # put movie information together in a dictionary
        movie_data = {'title': title, 'rating': rating, 'year': year, 'actors': actor, 'runtime': runtime, 'url': url}

        # put the dictionaries with movie information in a general list for all movies
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