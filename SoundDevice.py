import pyaudio
import wave
import numpy
import whisper

class SoundDevice(object):
    def __init__(self):
        self._default_frames = 512
        self._record_time = 5
        self._pyaudio = pyaudio.PyAudio()
        self._device_list = []
        
        self._current_device = None
        self._current_device_index = -1
        self._current_device_stream = None
        self._current_device_wasapi = False
        self._current_device_channel_count = 0
        
        self._recorded_chunks = []
        self._model = whisper.load_model("base")
        
    def __enter__(self):
        return self
        
    def __exit__(self, exception_type, exception_value, traceback):
        self._pyaudio.terminate()
        print('')
        
    def enumerate_devices(self):
        for i in range(self._pyaudio.get_device_count()):
            self._device_list.append(self._pyaudio.get_device_info_by_index(i))
            
        return self._device_list
    
    def set_device(self, index):
        assert 0 <= index < len(self._device_list), 'Index out of Range'

        self._current_device = self._device_list[index]
        self._current_device_wasapi = (self._pyaudio.get_host_api_info_by_index(self._current_device["hostApi"])["name"]).find("WASAPI") != -1
        
    def get_device_host_api_info(self, index):
        return self._pyaudio.get_host_api_info_by_index(self._device_list[index]["hostApi"])
    
    def open_stream(self):
        self._current_device_channel_count = self._current_device["maxInputChannels"]  \
            if (self._current_device["maxOutputChannels"] < self._current_device["maxInputChannels"]) \
            else self._current_device["maxOutputChannels"] 
        #self._current_device_channel_count = self._current_device["maxInputChannels"] 
        
        self._current_device_stream = \
            self._pyaudio.open(format=pyaudio.paInt16,
                               channels=self._current_device_channel_count,
                               rate=int(self._current_device["defaultSampleRate"]),
                               input=True,
                               frames_per_buffer=self._default_frames,
                               input_device_index=self._current_device["index"]
                               )
            
    def record_audio(self, length: int):    
        self._recorded_chunks = []    
        for i in range(0, int(int(self._current_device["defaultSampleRate"]) / self._default_frames * length)):
            self._recorded_chunks.append(self._current_device_stream.read(self._default_frames))
            #data = self._current_device_stream.read(self._default_frames)
            #data_proc = numpy.frombuffer(data, dtype=numpy.int16).flatten().astype(numpy.float32) / (2**15)
            #data_proc = whisper.pad_or_trim(data_proc)
            
            #recorded_audio.append(data_proc)
        
        return self._recorded_chunks
        
    def save_audio(self):
        filename = "out.wav"
        waveFile = wave.open(filename, 'wb')
        waveFile.setnchannels(self._current_device_channel_count)
        waveFile.setsampwidth(self._pyaudio.get_sample_size(pyaudio.paInt16))
        waveFile.setframerate(int(self._current_device["defaultSampleRate"]))
        waveFile.writeframes(b''.join(self._recorded_chunks))
        waveFile.close()
        
    def close_stream(self):
        self._current_device_stream.stop_stream()
        self._current_device_stream.close()
        
#with SoundDevice() as sd:
#    dev = sd.enumerate_devices()
#    
#    sd.set_device(71)
#    sd.open_stream()
#    data = sd.record_audio(5)
#    sd.close_stream()
#    sd.save_audio()
#    
#    print('Finished.')