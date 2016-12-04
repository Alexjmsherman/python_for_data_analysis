# -*- coding: utf-8 -*-
"""
Created on Fri Dec 02 12:34:52 2016

@author: alsherman
"""

import csv
import zipfile
import urllib
import pandas as pd

def download_zip_file(link, pandas=False):

    zfile = _download_zip(link)
    num_zip_files = len(zfile.filelist)
    
    if num_zip_files > 1:
        print("""There is more than one zip file. 
                Please select which one you want to open, '\n' """)    
        selected_file = _select_zip_file(zfile)
    else:
        selected_file = 0
        
    data = _open_zip(zfile, filename=selected_file)

    if pandas:
        data = pd.DataFrame(data[1:], columns=data[0])

    return data


def _download_zip(raw_data_path):

    """ helper function to download a zip and handle errors

    :return: downloaded zip file
    """

    try:
        zfile, _ = urllib.urlretrieve(raw_data_path)  # download zip file
        print('Collected Zfile: {}'.format(zfile))
    except:
        print('URL ERROR: {} no longer a valid URL'.format(raw_data_path))
    zfile = zipfile.ZipFile(zfile)  # open zip file
    
    return zfile
    
def _select_zip_file(zfile):
    file_names = {}
    for ind, f in enumerate(zfile.filelist):
        file_names[f.filename] = ind
    
    for k, v in file_names.items():
        print('To select "{}" press: {}'.format(k,v))
    selected_file = input('TYPE THE SELECTED FILE NUMBER HERE: ')
    
    return selected_file

def _open_zip(zfile, filename):

    with zfile.open(zfile.filelist[filename]) as f:
        print('Collected zip_file: {}'.format(zfile.filelist[filename]))
        data = [row for row in csv.reader(f.readlines())]  # extract data                
        
    return data
