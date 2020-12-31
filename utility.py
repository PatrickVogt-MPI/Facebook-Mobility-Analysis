from pathlib import Path

# works
def file_list(path: str, filetype: str = 'csv', key: str = None) -> list:
    '''
    Creates a list of all <filetype> files found in directory at <path>

    Args:
        path:     path pointing to a file directory
        filetype: file extension accepted files
        key:      file name search key
        
    Returns:
        files: List <filetype> files in <path> directory.
    '''
    pattern = '*' + key + '*.' + filetype if key else '*.' + filetype
    files = Path(path).glob(pattern)
    return files
   