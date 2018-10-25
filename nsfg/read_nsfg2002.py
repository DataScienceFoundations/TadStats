"""Reads NSFG data and pickles for quick access.

The code in this file was mostly taken from Allen
Downey's ThinkStats2 repo.
"""

import sys
sys.path.insert(0, '../')

import pandas as pd
import numpy as np
import pickle_data
import re


class FixedWidthVariables(object):
    """Represents a set of variables in a fixed width file."""

    def __init__(self, variables, index_base=0):
        self.variables = variables

        # note: by default, subtract 1 from colspecs
        self.colspecs = variables[['start', 'end']] - index_base

        # convert colspecs to a list of pair of int
        self.colspecs = self.colspecs.astype(np.int).values.tolist()
        self.names = variables['name']

    def ReadFixedWidth(self, filename, **options):
        df = pd.read_fwf(filename,
                         colspecs=self.colspecs, 
                         names=self.names,
                         **options)
        return df

    
def ReadStataDct(dct_file, **options):
    type_map = dict(byte=int, int=int, long=int, float=float, double=float)
    var_info = []
    for line in open(dct_file, **options):
        match = re.search( r'_column\(([^)]*)\)', line)
        if match:
            start = int(match.group(1))
            t = line.split()
            vtype, name, fstring = t[1:4]
            name = name.lower()
            if vtype.startswith('str'):
                vtype = str
            else:
                vtype = type_map[vtype]
            long_desc = ' '.join(t[4:]).strip('"')
            var_info.append((start, vtype, name, fstring, long_desc))
            
    columns = ['start', 'type', 'name', 'fstring', 'desc']
    variables = pd.DataFrame(var_info, columns=columns)

    # fill in the end column by shifting the start column
    variables['end'] = variables.start.shift(-1)
    variables.loc[len(variables)-1, 'end'] = 0

    dct = FixedWidthVariables(variables, index_base=1)
    return dct


def main():
    resp_dct = ReadStataDct('./data/2002FemResp.dct')
    resp_df = resp_dct.ReadFixedWidth('./data/2002FemResp.dat.gz',
                                      compression='gzip')
    preg_dct = ReadStataDct('./data/2002FemPreg.dct')
    preg_df = preg_dct.ReadFixedWidth('./data/2002FemPreg.dat.gz',
                                      compression='gzip')
    male_dct = ReadStataDct('./data/2002Male.dct')
    male_df = male_dct.ReadFixedWidth('./data/2002Male.dat.gz',
                                      compression='gzip')
    
    # mother's age is encoded in centiyears; convert to years
    preg_df.agepreg /= 100.0

    # birthwgt_lb contains at least one bogus value (51 lbs)
    # replace with NaN
    preg_df.loc[preg_df.birthwgt_lb > 20, 'birthwgt_lb'] = np.nan

    # replace 'not ascertained', 'refused', 'don't know' with NaN
    na_vals = [97, 98, 99]
    preg_df.birthwgt_lb.replace(na_vals, np.nan, inplace=True)
    preg_df.birthwgt_oz.replace(na_vals, np.nan, inplace=True)
    preg_df.hpagelb.replace(na_vals, np.nan, inplace=True)
    preg_df.babysex.replace([7, 9], np.nan, inplace=True)
    preg_df.nbrnaliv.replace([9], np.nan, inplace=True)

    # birthweight is stored in two columns, lbs and oz.
    # convert to a single column in lb
    # NOTE: creating a new column requires dictionary syntax,
    # not attribute assignment (like df.totalwgt_lb)
    preg_df['totalwgt_lb'] = preg_df.birthwgt_lb + preg_df.birthwgt_oz / 16.0    

    # due to a bug in ReadStataDct, the last variable gets clipped;
    # so for now set it to NaN
    preg_df.cmintvw = np.nan
    
    pickle_data.pickle_data(resp_df, './fem_resp2002.pickle')
    pickle_data.pickle_data(preg_df, './preg2002.pickle')
    pickle_data.pickle_data(male_df, './male2002.pickle')


if __name__=='__main__':
    main()
else:
    print('File should not be imported. Only run directly.')
