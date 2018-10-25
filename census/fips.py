"""This file is used to scrape www.census.gov for state FIPS codes.

There are two ways this file gets the state FIPS codes:
- Pandas only
    uses read_html to get dataframe from page source
    much more simple of two functions
- Pandas and BeautifulSoup - add 'soup' as argument to use
    uses BeautifulSoup to read table
    more complex of two functions
    used primarily for learning basic BS4 applications
"""

import sys
sys.path.insert(0, '../')

import pandas as pd
import pickle_data
import requests


def get_fips(sauce, headers):
    '''Returns pandas dataframe with state FIPS codes.'''
    df = pd.read_html(sauce)[0]
    df.dropna(inplace=True)
    df.columns = headers
    return df


def get_fips_soup(sauce, table_summary, headers):
    '''Returns pandas dataframe with state FIPS codes.'''
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(sauce, 'html.parser')

    # set up lists to hold columns
    num_cols = len(headers)
    columns = [[] for _ in range(num_cols)]

    # get all rows from table
    row_data = [datum.text.strip() for datum in
                soup.find('table', {'summary':table_summary}).find_all('td')]
    rows = [row_data[num_cols*i:num_cols*(i+1)] for i in
            range(int(len(row_data)/num_cols))]

    # fill columns from rows
    for row in rows:
        for i in range(num_cols):
            columns[i].append(row[i])

    # create dataframe of state fip codes
    return pd.DataFrame(dict(zip(headers,columns)))

    
def main():
    # get page source
    sauce = requests.get('https://www.census.gov/geo/reference/ansi_statetables.html').text

    # table html summary headers of table
    table_summary = ('table showing ANSI state codes for the'
                     ' states and the District of Columbia')
    headers = ['Name','Code','Abbr']

    # pickle a pandas DataFrame of the table
    if len(sys.argv) > 1 and sys.argv[1] == 'soup':
        pickle_data.pickle_data(get_fips_soup(sauce, table_summary, headers), './fips.pickle')
    else:
        pickle_data.pickle_data(get_fips(sauce, headers), './fips.pickle')
    print('State FIPS codes pickled successfully.')

    
if __name__=="__main__":
    main()
else:
    print('File should not be imported. Only run directly.')

