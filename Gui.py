"""
Created on Fri Mar  8 11:07:14 2024

@author: Tony
"""

import tkinter as tk
from tkinter.ttk import *
import tkinter.scrolledtext as scrolledtext
import time
import datetime

class Gui(object):
    def __init__(self):
        self._root_window = tk.Tk()
        self._root_window.title("Audio Translation")
        
        self._root_window_width = 800
        self._root_window_height = 700
        
        self._presenter = None
        self._main_frame = None
        
        self._selected_from_lang = None
        self._selected_to_lang = None
        self._selected_translator = None
        self._selected_device_index = -1
        self._audio_val = tk.IntVar()
        
        self._supported_langs = ["en", "ja"]
        self._translators = ["Google", "Whisper"]
        
    def __enter__(self):
        return self    
        
    def __exit__(self):
        print('')
        
    def set_presenter(self, presenter):
        self._presenter = presenter
        
    def on_closing(self):        
        self._presenter.stop_translating()
        self._root_window.destroy()
        
    def initialize(self):
        self.create_main_frame()
        self.create_devices_frame()
        
        self._root_window.protocol("WM_DELETE_WINDOW", self.on_closing)  
        self._root_window.geometry(f"{self._root_window_width}x{self._root_window_height}")
        self._root_window.resizable(False, False)
        self._root_window.mainloop()
        
    # GUI Creation
    def create_main_frame(self):
        main_frame = tk.LabelFrame(self._root_window, text="Translation", width=790, height=500)
        main_frame.place(x=5, y=5)
        
        tk.Label(main_frame, text="From: ").place(x=2, y=2)
        self._cb_from_lang = tk.ttk.Combobox(main_frame,
                                             state="readonly",
                                             width=5,
                                             textvariable=self._selected_from_lang,
                                             values=self._supported_langs)
        self._cb_from_lang.bind('<<ComboboxSelected>>', self.onComboBoxSelection)
        self._cb_from_lang.place(x=40, y=2)
        
        tk.Label(main_frame, text="To: ").place(x=110, y=2)
        self._cb_to_lang = tk.ttk.Combobox(main_frame,
                                             state="readonly",
                                             width=5,
                                             textvariable=self._selected_to_lang,
                                             values=self._supported_langs)
        self._cb_to_lang.bind('<<ComboboxSelected>>', self.onComboBoxSelection)
        self._cb_to_lang.place(x=135, y=2)
        self._cb_from_lang.current(1)
        self._cb_to_lang.current(0)
        
        self._btn_start = tk.Button(main_frame, text="Start", width=10, command=self.onBtnStartClick)
        self._btn_start.config(state='disabled')
        self._btn_start.place(x=220)
        self._btn_stop = tk.Button(main_frame, text="Stop", width=10, command=self.onBtnStopClick)
        self._btn_stop.config(state='disabled')
        self._btn_stop.place(x=310)
        
        tk.Label(main_frame, text="Translator :").place(x=400)
        self._cb_translator = tk.ttk.Combobox(main_frame,
                                              state="readonly",
                                              width=15,
                                              textvariable=self._selected_translator,
                                              values=self._translators)
        self._cb_translator.bind('<<ComboboxSelected>>', self.onComboBoxSelection)
        self._cb_translator.place(x=470, y=2)
        self._cb_translator.current(0)
        
        tk.Label(main_frame, text="Audio Capture Time :").place(x=600)
        self._audio_val.set(5)
        self._nud_audio = tk.Spinbox(main_frame, from_=0, to=600, width=4, textvariable=self._audio_val, command=self.nudAudioUpdated)
        self._nud_audio.bind('<Return>', self.nudAudioUpdated)
        self._nud_audio.place(x=720)
        
        tk.Label(main_frame, text="Original:").place(x=2, y=40)
        self._txt_transcribed = scrolledtext.ScrolledText(main_frame, width=52)
        self._txt_transcribed.config(state='disabled')
        self._txt_transcribed.tag_add("time", "1.0", "1.20", "start")
        self._txt_transcribed.tag_config("time", foreground="red")
        self._txt_transcribed.place(x=2, y=60, height=415)
        
        tk.Label(main_frame, text="Translated:").place(x=400, y=40)
        self._txt_translated = scrolledtext.ScrolledText(main_frame, width=52)
        self._txt_translated.config(state='disabled')
        self._txt_translated.tag_add("time", "1.0", "1.20", "start")
        self._txt_translated.tag_config("time", foreground="red")
        self._txt_translated.place(x=400, y=60, height=415)
        
    def create_devices_frame(self):
        devices_frame = tk.LabelFrame(self._root_window, text="Devices", width = 790, height = 185)
        devices_frame.place(x=5, y=505)
        
        tk.Label(devices_frame, text="Select Device:").place(x=2, y=2)
        
        self._listbox_devices = tk.Listbox(devices_frame, width=60, height=8)
        self._listbox_devices.bind('<<ListboxSelect>>', self.onListBoxSelection)
        self._listbox_devices.place(x=2, y=30)
        scrollbar = Scrollbar(devices_frame, orient="vertical")
        scrollbar.config(command=self._listbox_devices.yview)
        scrollbar.place(x=350, y=32, height=130)
        self._listbox_devices.configure(yscrollcommand=scrollbar.set)
        
        tk.Label(devices_frame, text="Device Info:").place(x=380, y=2)
        self._txt_device_info = scrolledtext.ScrolledText(devices_frame, width=55, height=10)
        self._txt_device_info.place(x=380, y=30)
        
        self._btn_refresh = tk.Button(devices_frame, text="Refresh", width=10)
        self._btn_refresh.place(x=284, y=0)
        
        self._btn_select = tk.Button(devices_frame, text="Select", width=10, 
                                     command=self.onbtnSelectClick)
        self._btn_select.place(x=704, y=0)
        
        devices = self._presenter.get_device_list()
        
        for i in range(len(devices)):
            self._listbox_devices.insert(i, str(f'{devices[i]["index"]}: ') + devices[i]["name"])
           
    # Other functions       
    def UpdateTextFields(self, original, translated):
        formatted_string = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d.%H:%M:%S")
        
        self._txt_transcribed.config(state='normal')
        self._txt_transcribed.insert(tk.END, formatted_string + ":\n",("time"))
        self._txt_transcribed.yview(tk.END)
        self._txt_transcribed.insert(tk.END, original + '\n')
        self._txt_transcribed.yview(tk.END)
        
        
        self._txt_transcribed.config(state='disabled')
        
        self._txt_translated.config(state='normal')
        self._txt_translated.insert(tk.END, formatted_string + ":\n", ("time"))
        self._txt_translated.yview(tk.END)
        self._txt_translated.insert(tk.END, translated + '\n')
        self._txt_translated.yview(tk.END)
        self._txt_translated.config(state='disabled')
        
        self.UpdateView()
        
    def UpdateView(self):            
        if self._presenter._workers_running:
            self._btn_start.config(state='disabled')
            self._btn_stop.config(state='normal')
            self._btn_select.config(state='disabled')
            self._listbox_devices.config(state='disabled')
        else:
            self._btn_start.config(state='normal')
            self._btn_stop.config(state='disabled')
            self._btn_select.config(state='normal')
            self._listbox_devices.config(state='normal')
            
        if not self._presenter._device_selected:
            self._btn_start.config(state='disabled')
            self._btn_stop.config(state='disabled')
        
    # Event/Gui functions     
    def onListBoxSelection(self, event=None):
        self._selected_device_index = self._listbox_devices.curselection()[0]
        device_info = self._presenter.get_device_list()[self._selected_device_index]
        device_host_info = self._presenter.get_device_host_api_info(self._selected_device_index)
        
        self._txt_device_info.config(state='normal')
        self._txt_device_info.delete(1.0, tk.END)
        
        for key, value in device_info.items():
            self._txt_device_info.insert(tk.END, key + " : " + str(value) + "\n")
            
        self._txt_device_info.insert(tk.END,"\nHost Api Info:\n")
        
        for key, value in device_host_info.items():
            self._txt_device_info.insert(tk.END, key + " : " + str(value) + "\n")
        
        self.UpdateView()
            
    def onBtnStartClick(self):
        self._presenter.start_translating()
        self.UpdateView()
        
    def onBtnStopClick(self):
        self._presenter.stop_translating()
        self.UpdateView()
        
    def onbtnSelectClick(self):
        self._presenter.set_device(self._selected_device_index)
        self.UpdateView()
        
    def onComboBoxSelection(self, event=None):
        self._presenter.set_translation_lang(self._cb_from_lang.get(), self._cb_to_lang.get())
        self._presenter.set_translator(self._cb_translator.current())
        
        if self._cb_translator.current() == 1:
            self.UpdateTextFields("Warning: Whisper is mostly trained for translating to english. Audio will only translate to english.",
                                  "Warning: Whisper is mostly trained for translating to english. Audio will only translate to english.")
            self._cb_to_lang.current(0)
        
        self.UpdateView()
        
    def nudAudioUpdated(self, event=None):
        self._presenter.set_audio_time_acquire(self._audio_val.get())