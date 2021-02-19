import pathlib
import os
import pandas as pd
from typing import List

def file_list(path: str, filetype: str = 'csv', key: str = None) -> List:
    '''
    Creates a list of all <filetype> files found in directory at <path>

    Args:
        path:     path pointing to a file directory
        filetype: file extension accepted files
        key:      file name search key
        
    Returns:
        files: List of <filetype> files in <path> directory.
    '''
    pattern = '*' + key + '*.' + filetype if key else '*.' + filetype
    files = pathlib.Path(path).glob(pattern)
    return files
   
def rename_csvs(paths: str):
    '''
    Renames Facebook .csv data files with dates only, e.g. 'XYZ_2020-03-26 0000.csv' becomes '2020-03-26 0000.csv'.
    
    Args:    
        paths: List of either str or pathlib.Path objects pointing to files        
    '''
    for path in paths:
        new = (pathlib.Path(path).name)[-19:]
        path.rename(pathlib.Path(pathlib.Path(path).parent, new))
        
def check_for_missing_file(paths: str, show: bool = False) -> List[pd.Timestamp]:
    '''
    Takes a list pathlib.Path objects and returns list with timestamps from missing dates.
    Optionally prints name of missing date-times.
    Files must end with format '*YYYY-MM-DD TTTT.csv' like 'XYZ_2020-03-26 0000.csv'.

    Args:
        paths: List of pathlib.Path objects to files
        
    Returns:
        missing: List of pandas.Timestamp objects of missing date-times
    '''
    timestamps = set()
    for path in paths:
        date = path.name[-19:-9]
        time = path.name[-8:-6]
        timestamps.add(pd.Timestamp(date + ' '+ time))
    
    missing = []
    current, end = min(timestamps), max(timestamps)
    while(current < end):
        if(current not in timestamps):
            missing.append(current)
        current += pd.Timedelta(hours = 8)
    if(show):
        print('Missing dates:')
        for date in missing:
            print(date)
    return missing