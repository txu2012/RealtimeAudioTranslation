import SoundDevice
import Translation
import AudioCapture as ac
import asyncio
import threading

sd = SoundDevice.SoundDevice()
tr = Translation.Translate()

ac = ac.AudioCapture()

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

devices = ac.sd_query_devices()
print(f'{devices}')

ac.sd_record_audio(57)

def thread_acquire():
    while True:
        ac.get_data()

def thread_translate():
    while True:
        tr.process_data_fw(ac._queue.get())
        ac._queue.task_done()       
    
t0 = threading.Thread(target=thread_acquire, daemon=True).start()     
t1 = threading.Thread(target=thread_translate, daemon=True).start()