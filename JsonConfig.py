# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 09:28:33 2024

@author: Tony
"""

import os.path as os
import json

class Config:
    def __init__(self, filename: str):
        self._values = ""
        self._dict_values = None
        self._filename = filename
        
        if not os.isfile(self._filename):
            self._dict_values = {
                "deepl": ""
            }
            
            file = open(self._filename, "w")
            json.dump(self._dict_values, file, indent=3)
            file.close()
            
        print(f'JsonConfig object created.')
        
    def load_json(self):
        print(f'Loading Json file {self._filename}')
        # if file does not exist, create new file
        file = open(self._filename)
        self._dict_values = json.load(file)
        file.close()
        
    def save_json(self, dict_values):
        self._dict_values = dict_values
        
        file = open(self._filename, "w")
        json.dump(self._dict_values, file, indent=3)
        file.close()
        
        print('Saved values to {self._filename}.')
        
    def load_values(self):
        print(f'Loading Json values: \n{self._dict_values}')
        return self._dict_values