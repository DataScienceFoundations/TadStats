"""This file provides functions for pickles.

This functions in this file are simple helper methods
to be used for quickly pickling and reading pickled
data. The functions are:
- pickle_data:
    parameters: data, file
- get_pickled_data:
    parameters: file
"""

import pickle

def pickle_data(data, file):
    '''Pickles the object in the specified file.'''
    with open(file, 'wb') as f:
        pickle.dump(data, f)

        
def get_pickled_data(file):
    '''Gets the object from the pickle.'''
    with open(file, 'rb') as f:
        data = pickle.load(f)
    return data
