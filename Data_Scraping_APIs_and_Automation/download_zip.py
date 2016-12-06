# -*- coding: utf-8 -*-
"""
Created on Fri Dec 02 12:34:52 2016

@author: alsherman
"""

import csv
import zipfile
import urllib
import pandas as pd
from collections import OrderedDict

class download_zip_file():
    """ download, select, and open zip files """
    
    def __init__(self, link, pandas=False):
        """ download the csv
        
        :param: link - link to download a zip file
        :param: pandas - specify whether to convert data into a dataframe  
        """
        
        self.zfile = self._download_zip(link)
        self.num_zip_files = len(self.zfile.filelist)
        self.pandas = pandas
        
    def open_zip(self):
        """ Select and open a zip file
        
        Note: this will only work for csvs with headers in the first row
        
        :returns: data - a list or dataframe of data from the selected file        
        """
        
        # select which file to open (if the zip has many files) 
        if self.num_zip_files > 1:
            print(" Please select a file to open'\n'")    
            selected_file_num = self._select_zip_file()
        else:
            selected_file_num = 0
        selected_file = self.zfile.filelist[selected_file_num]
        
        # open the selected file
        # assumes the file is a csv
        with self.zfile.open(selected_file) as f:
            print('Collected zip_file: {}'.format(selected_file.filename))
            data = [row for row in csv.reader(f.readlines())]  # extract data                

        # create a dataframe
        # assumes the data has headers in the first row
        if self.pandas:
            data = pd.DataFrame(data[1:], columns=data[0])
        
        return data


    def _download_zip(self, raw_data_path):    
        """ helper function to download a zip and handle errors
    
        :returns: zfile - downloaded zip file
        """
    
        try:
            zfile, _ = urllib.urlretrieve(raw_data_path)  # download zip file
            print("Collected Zfile: {} '\n' ".format(zfile))
        except:
            print("URL ERROR: {} no longer a valid URL '\n' ".format(raw_data_path))
        zfile = zipfile.ZipFile(zfile)  # open zip file
        
        return zfile
        
    def _select_zip_file(self):
        """ select a zip file if the zip has many files

        :returns: selected_file_num - index of selected file        
        """
        
        # store the file names
        file_names = OrderedDict()
        for ind, f in enumerate(self.zfile.filelist):
            file_names[f.filename] = ind
        
        # show file names
        for k, v in file_names.items():
            print('Type: "{}" to select file: {}'.format(v,k))
        
        # user selects a file
        selected_file_num = input('TYPE THE SELECTED FILE NUMBER HERE: ')
        
        return selected_file_num
    
