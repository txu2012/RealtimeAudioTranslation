import tkinter as tk
from tkinter.ttk import *
import tkinter.scrolledtext as scrolledtext

class Gui(object):
    def __init__(self):
        self._root_window = tk.Tk()
        self._root_window.title("Audio Translation")
        #self._root_window.iconbitmap("yukkuri_mini.ico")
        
        self._root_window_width = 800
        self._root_window_height = 700
        
        self._presenter = None
        self._main_frame = None
        
    def __enter__(self):
        return self    
        
    def __exit__(self):
        print('')
        
    def set_presenter(self, presenter):
        self._presenter = presenter
        
    def on_closing(self):        
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
        
        self._txt_response = scrolledtext.ScrolledText(main_frame, width=95)
        self._txt_response.config(state='disabled')
        self._txt_response.place(x=2, height=475)
        
    def create_devices_frame(self):
        devices_frame = tk.LabelFrame(self._root_window, text="Devices", width = 790, height = 180)
        devices_frame.place(x=5, y=505)
        
        lb_devices = tk.Label(devices_frame, text="Select Device:")
        lb_devices.place(x=2, y=2)
        
        self._listbox_devices = tk.Listbox(devices_frame, width=60, height=8)
        self._listbox_devices.place(x=2, y=25)
        
        lb_device_info = tk.Label(devices_frame, text="Device Info:")
        lb_device_info.place(x=380, y=2)
        self._txt_device_info = scrolledtext.ScrolledText(devices_frame, width=30, height=8)
        self._txt_device_info.place(x=380, y=25)
        
        self._btn_refresh = tk.Button(devices_frame, text="Refresh", width=10)
        self._btn_refresh.place(x=280, y=0)