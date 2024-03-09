"""
Created on Fri Mar  8 11:07:14 2024

@author: Tony
"""

import whisper as wh
import wave
import os
import torch
from deep_translator import GoogleTranslator

class Translate(object):
    def __init__(self):
        self._languages = ["en", "ja"]
        self._selected_translate_lang = "ja"
        self._config = {}
        self._google_translator = GoogleTranslator(source='ja', target='en')
        self._translator_list = ["Google", "Whisper"]
        self._whisper_device = "cuda" if torch.cuda.is_available() else "cpu"
        self._model = wh.load_model("base", self._whisper_device)
        
        
        if os.path.isfile("out.wav"):
            os.remove("out.wav")
        
    def set_translation_config(self, source, target, translator: int = 0):
        if translator == 0:
            self._google_translator.target = target
            self._google_translator.source = source

    def set_audio_data_config(self, config):
        self._config = config
    
    def process_data(self, data, translator: int = 0):
        filename = "out.wav"
        waveFile = wave.open(filename, 'wb')
        waveFile.setnchannels(self._config["Channels"])
        waveFile.setsampwidth(self._config["SampleWidth"])
        waveFile.setframerate(int(self._config["Framerate"]))
        waveFile.writeframes(b''.join(data))
        waveFile.close()
        
        audio = wh.pad_or_trim(wh.load_audio("out.wav"))
        orig = wh.transcribe(self._model, audio, fp16=False)["text"]
        
        if translator == 0:
            return orig, self._google_translator.translate(text=orig)
        else:
            translated = wh.transcribe(self._model, audio, fp16=False, task="translate")["text"]
            return orig, translated