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
