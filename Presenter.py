# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 11:07:14 2024

@author: Tony
"""
import threading
import queue
import Translation

class Presenter(object):
    def __init__(self, model, view, config):
        self._view = view
        self._sound_device = model
        
        self._config = config
        self._config.load_json()
        
        self._translator = Translation.Translate(self._config.load_values())
        self._device_list = self._sound_device.enumerate_devices()
        self._device_selected = False
        
        self._stop_threads = True
        self._workers_running = False
        
        self._audio_queue = queue.Queue()
        self._translated_queue = queue.Queue()
        self._audio_time_acquire = 5
        self._translator_index = 0
                
    def initialize(self):
        self._view.initialize()    
        
    def get_device_list(self):
        return self._device_list
    
    def get_device_host_api_info(self, index):
        return self._sound_device.get_device_host_api_info(index)
    
    def set_device(self, index):
        self._sound_device.set_device(index)
        self._device_selected = True
    
    def set_translation_lang(self, source, target):
        self._translator.set_translation_config(source, target)
    
    def set_translator(self, index):
        self._translator_index = index
    
    def set_audio_time_acquire(self, acq_time):
        self._audio_time_acquire = acq_time
    
    def set_api_keys(self, keys):
        self._translator.set_api_keys(keys)
    
    def start_translating(self):
        self._stop_threads = False
        audio_config = self._sound_device.open_stream()
        self._translator.set_audio_data_config(audio_config)
        
        if not self._audio_queue.empty:
            self.clear_queues()
        
        self._audio_queue = queue.Queue()
        self._translated_queue = queue.Queue() 
        
        self._acquire_th = threading.Thread(target=self.acquire_audio, daemon=True).start()
        self._translate_th = threading.Thread(target=self.translate_audio, daemon=True).start()
        
        self._workers_running = True
    
    def stop_translating(self):
        self._stop_threads = True
        self._workers_running = False
        
    def acquire_audio(self):
        while not self._stop_threads:
            data = self._sound_device.record_audio(self._audio_time_acquire)
            self._audio_queue.put(data)
            
        self._sound_device.close_stream()
            
    def translate_audio(self):
        while not self._stop_threads:
            audio = self._audio_queue.get()
            
            transcribed_text, translated_text = self._translator.process_data(audio, self._translator_index)            
            
            if str(transcribed_text) == str(" you"):
                self._audio_queue.task_done()
                continue
            
            self._view.UpdateTextFields(transcribed_text, translated_text)
            
            self._audio_queue.task_done()
            