# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 11:07:14 2024

@author: Tony
"""

import SoundDevice
import Presenter
import Gui

class RealtimeAudioTranslate():
    """Wrapper class for setting the main window"""

    def __init__(self):  
        view = Gui.Gui()
        model = SoundDevice.SoundDevice() 
             
        self._presenter = Presenter.Presenter(model, view)
        view.set_presenter(self._presenter)
        self._presenter.initialize()

if __name__ == "__main__":
    app = RealtimeAudioTranslate()