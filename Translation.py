"""
Created on Fri Mar  8 11:07:14 2024

@author: Tony
"""

import whisper as wh
from faster_whisper import WhisperModel
import wave
import os
import torch
import assemblyai as aai
from deep_translator import (GoogleTranslator,
                             DeeplTranslator)

class Translate(object):
    def __init__(self, config):
        self._selected_source = "ja"
        self._selected_target = "en"
        
        self._config = config
        
        self._whisper_device = "cuda" if torch.cuda.is_available() else "cpu"
        self._model = wh.load_model("base", self._whisper_device)
        self._model_2 = WhisperModel("large-v3", device="cuda", compute_type="float16")
              
        self._active_translators = {
            "deepl": False,
            "google": True,
            "whisper": True
        }
        
        if self._config["deepl"] != "":
            self._active_translators["deepl"] = True
        else:
            self._active_translators["deepl"] = False

        if os.path.isfile("out.wav"):
            os.remove("out.wav")
        
    def set_translation_config(self, source, target):
        self._selected_source = source
        self._selected_target = target

    def set_api_keys(self, api_keys):
        if api_keys["deepl"] != "":
            self._config["deepl"] = api_keys["deepl"]
            self._active_translators["deepl"] = True
        
        print(f'keys: {api_keys}')    

    def set_audio_data_config(self, config):
        self._config = config
    
    def audio_to_wav(self, data):
        filename = "out.wav"
        waveFile = wave.open(filename, 'wb')
        waveFile.setnchannels(self._config["Channels"])
        waveFile.setsampwidth(self._config["SampleWidth"])
        waveFile.setframerate(int(self._config["Framerate"]))
        waveFile.writeframes(b''.join(data))
        waveFile.close()
    
    def process_data(self, data, translator: int = 0):
        self.audio_to_wav(data)
        
        audio = wh.pad_or_trim(wh.load_audio("out.wav"))
        orig = wh.transcribe(self._model, audio, fp16=False)["text"]
        
        if translator == 0:
            return orig, GoogleTranslator(source=self._selected_source, 
                                          target=self._selected_target).translate(text=orig)
        elif translator == 1:
            if not self._active_translators["deepl"]:
                return orig, "Valid DeepL API key required."
            try:
                return orig, DeeplTranslator(source=self._selected_source, 
                                            target=self._selected_target,
                                            api_key=self._config["deepl"],
                                            use_free_api=True).translate(text=orig)
            except Exception as ex:
                return orig, "Valid DeepL API key required."
        else:
            translated = wh.transcribe(self._model, audio, fp16=False, task="translate")["text"]
            return orig, translated
        
    def process_data_fw(self, data):
        #self.audio_to_wav(data)
        #segments, info = self._model_2.transcribe(data, beam_size=5)
        
        #segments = list(segments)
        #print(f'output: {segments}')
        
        #text = ""
        #for segment in segments:
        #    text += segment.text
            
        #print(f'Full text: {text}')
        orig = wh.transcribe(self._model, data, fp16=False)["text"]
        print(f'Full text: {orig}')