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
        
        self._selected_from_lang = None
        self._selected_to_lang = None
        self._selected_device_index = -1
        
        self._supported_langs = ["en", "jp"]
        
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
        
        lb_from = tk.Label(main_frame, text="From: ")
        lb_from.place(x=2, y=2)
        self._cb_from_lang = tk.ttk.Combobox(main_frame,
                                             state="readonly",
                                             width=5,
                                             textvariable=self._selected_from_lang,
                                             values=self._supported_langs)
        self._cb_from_lang.place(x=40, y=2)
        
        lb_to = tk.Label(main_frame, text="To: ")
        lb_to.place(x=110, y=2)
        self._cb_to_lang = tk.ttk.Combobox(main_frame,
                                             state="readonly",
                                             width=5,
                                             textvariable=self._selected_from_lang,
                                             values=self._supported_langs)
        self._cb_to_lang.place(x=135, y=2)
        self._cb_from_lang.current(0)
        self._cb_to_lang.current(1)
        
        self._btn_start = tk.Button(main_frame, text="Start", width=10, command=self.onBtnStartClick)
        self._btn_start.place(x=220)
        self._btn_stop = tk.Button(main_frame, text="Stop", width=10)
        self._btn_stop.place(x=310)
        
        self._txt_response = scrolledtext.ScrolledText(main_frame, width=108)
        self._txt_response.config(state='disabled')
        self._txt_response.place(x=2, y=30, height=445)
        
    def create_devices_frame(self):
        devices_frame = tk.LabelFrame(self._root_window, text="Devices", width = 790, height = 185)
        devices_frame.place(x=5, y=505)
        
        lb_devices = tk.Label(devices_frame, text="Select Device:")
        lb_devices.place(x=2, y=2)
        
        self._listbox_devices = tk.Listbox(devices_frame, width=60, height=8)
        self._listbox_devices.bind('<<ListboxSelect>>', self.onListBoxSelection)
        self._listbox_devices.place(x=2, y=30)
        scrollbar = Scrollbar(devices_frame, orient="vertical")
        scrollbar.config(command=self._listbox_devices.yview)
        scrollbar.place(x=350, y=32, height=130)
        self._listbox_devices.configure(yscrollcommand=scrollbar.set)
        
        lb_device_info = tk.Label(devices_frame, text="Device Info:")
        lb_device_info.place(x=380, y=2)
        self._txt_device_info = scrolledtext.ScrolledText(devices_frame, width=55, height=10)
        self._txt_device_info.place(x=380, y=30)
        
        self._btn_refresh = tk.Button(devices_frame, text="Refresh", width=10)
        self._btn_refresh.place(x=284, y=0)
        
        self._btn_select = tk.Button(devices_frame, text="Select", width=10, 
                                     command= lambda: self._presenter._sound_device.set_device(self._selected_device_index))
        self._btn_select.place(x=704, y=0)
        
        devices = self._presenter.get_device_list()
        
        for i in range(len(devices)):
            self._listbox_devices.insert(i, devices[i]["name"])
           
            
    def onListBoxSelection(self, event):
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
            
    def onBtnStartClick(self):
        self._presenter._sound_device.open_stream()
        self._presenter._sound_device.record_audio(5)
        self._presenter._sound_device.save_audio()