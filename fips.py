import pandas as pd
import pickle_data
import requests
#from bs4 import BeautifulSoup

# get page source
sauce = requests.get('https://www.census.gov/geo/reference/ansi_statetables.html').text
#soup = BeautifulSoup(sauce, 'html.parser')

# table html summary headers of table
table_summary = ('table showing ANSI state codes for the'
                 ' states and the District of Columbia')
headers = ['Name','Code','Abbr']

# create dataframe of state fip codes
df = pd.read_html(sauce)[0]
df.dropna(inplace=True)
df.columns = headers

"""
# get all rows from table
num_cols = len(headers)
columns = [[] for _ in range(num_cols)]
row_data = [datum.text.strip() for datum in
            soup.find('table', {'summary':table_summary}).find_all('td')]
rows = [row_data[num_cols*i:num_cols*(i+1)] for i in
        range(int(len(row_data)/num_cols))]
for row in rows:
    for i in range(num_cols):
        columns[i].append(row[i])
df = pd.DataFrame(dict(zip(headers,columns)))
"""

# pickle a pandas DataFrame of the table
pickle_data.pickle_data(df, './fips.pickle')