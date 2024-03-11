import SoundDevice
import Translation
import AudioCapture as ac
import asyncio
import threading
import JsonConfig
import queue

_config = JsonConfig.Config('config.json')
_config.load_json()
#_translator = Translation.Translate(_config.load_values())


#sd = SoundDevice.SoundDevice()
tr = Translation.Translate(_config.load_values())

#ac = ac.AudioCapture()

#for device in sd.enumerate_devices():
#    if "CABLE" in device["name"]:
#        print(f'{device}')
#        print(f'{sd.get_device_host_api_info(device["index"])}\n')

#sd.enumerate_devices()

#sd.set_device(56)
#audio_config = sd.open_stream()
#tr.set_audio_data_config(audio_config)
#sd.save_audio(sd.record_audio())

#tr.process_data_fw(sd.record_audio())
#sd.close_stream()

import sounddevice as sd

#devices = ac.sd_query_devices()
#print(f'{devices}')

#ac.set_device(73)
#ac.sd_record_audio()

devices = sd.query_devices()
device = devices[73]
sd.default.device = 73
sd.default.samplerate = 48000
sd.default.channels = 1
sd.default.dtype = 'float32'

data = sd.rec(int(5))

q1 = queue.Queue()
q1.put(data)
#def thread_acquire():
#    while True:
#        q1.put(ac.get_data())
        

def thread_translate():
    while True:
        print('Preprocess')
        data = q1.get()
        tr.process_data_fw(data)
        print("processing")
        q1.task_done()       
    
#t0 = threading.Thread(target=thread_acquire, daemon=False).start()     
t1 = threading.Thread(target=thread_translate, daemon=False).start()