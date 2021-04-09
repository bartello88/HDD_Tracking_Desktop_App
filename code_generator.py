import os
import time
from random import randint
from datetime import date

def code_generator(car, date, n):
    if car=='no hdd':
        return 'no hdd'
    else:
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return f'{car}-{date}-{randint(range_start, range_end)}'

def get_last_file_modified_data(filePath):
    modTimesinceEpocNew = os.path.getmtime(filePath)
    # Convert seconds since epoch to readable timestamp
    modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpocNew))
    return modificationTime
