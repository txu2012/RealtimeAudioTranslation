"""
Created on Fri Mar  8 11:07:14 2024

@author: Tony
"""

from faster_whisper import WhisperModel
import wave
import os
import torch
from deep_translator import (GoogleTranslator,
                             DeeplTranslator)

class Translate(object):
    def __init__(self, config):
        self._selected_source = "ja"
        self._selected_target = "en"
        
        print(f'config: {config}')
        
        self._api_config = config
        
        self._whisper_device = "cuda" if torch.cuda.is_available() else "cpu"
        self._model = WhisperModel("large-v3", device="cuda", compute_type="int8_float16")
              
        self._active_translators = {
            "deepl": False,
            "google": True,
            "whisper": True
        }
        
        if self._api_config["deepl"] != "":
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
            self._api_config["deepl"] = api_keys["deepl"]
            self._active_translators["deepl"] = True   

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
        
    def get_transcription(self, translate:bool = False):
        if translate:
            segments, _ = self._model.transcribe("out.wav", beam_size=5, task="translate", vad_filter=True)
        else:    
            segments, _ = self._model.transcribe("out.wav", beam_size=5, vad_filter=True)

        segments = list(segments)        
        text = ""
        for segment in segments:
            text += segment.text
            
        return text    
        
    def process_data(self, data, translator: int = 0):
        self.audio_to_wav(data)
        orig = self.get_transcription()
        
        if translator == 0:
            return orig, GoogleTranslator(source=self._selected_source, 
                                          target=self._selected_target).translate(text=orig)
        elif translator == 1:
            if not self._active_translators["deepl"]:
                return orig, "Valid DeepL API key required."
            try:
                return orig, DeeplTranslator(source=self._selected_source, 
                                            target=self._selected_target,
                                            api_key=self._api_config["deepl"],
                                            use_free_api=True).translate(text=orig)
            except Exception as ex:
                return orig, f'Failed to translate. Valid DeepL API key required. {ex}'
        else:
            translated = self.get_transcription(True)
            return orig, translated