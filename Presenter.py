# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 11:07:14 2024

@author: Tony
"""
class Presenter(object):
    def __init__(self, model, view):
        self._view = view
        self._sound_device = model
        self._device_list = self._sound_device.enumerate_devices()
        
    def initialize(self):
        self._view.initialize()    
        
    def get_device_list(self):
        return self._device_list
    
    def get_device_host_api_info(self, index):
        return self._sound_device.get_device_host_api_info(index)