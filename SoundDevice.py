import pyaudio

class SoundDevice:
    def __init__(self):
        self._pyaudio = pyaudio.PyAudio()
        self._device_list = []
        
        self._current_device = None
        
        
    def __exit__(self):
        print('')
        
    def enumerate_devices(self):
        for i in range(self._pyaudio.get_device_count()):
            self._device_list.append(self._pyaudio.get_device_info_by_index(i))
            
        return self._device_list