import pickle

def pickle_data(data, pickle_file):
    '''Pickles the object in the specified file.'''
    with open(pickle_file, 'wb') as f:
        pickle.dump(data, f)

        
def get_pickled_data(pickle_file):
    '''Gets the object from the pickle'''
    with open(pickle_file, 'rb') as f:
        data = pickle.load(f)
    return data