import whisper as wh
import wave
import os
from deep_translator import GoogleTranslator

class Translate(object):
    def __init__(self):
        self._model = wh.load_model("base")
        self._languages = ["en", "ja"]
        self._selected_translate_lang = "ja"
        self._config = {}
        self._translator = GoogleTranslator(source='ja', target='en')
        
    def set_translation_config(self, source, target):
        self._translator.target = target
        self._translator.source = source

    def set_audio_data_config(self, config):
        self._config = config
    
    def process_data(self, data):
        filename = "out.wav"
        waveFile = wave.open(filename, 'wb')
        waveFile.setnchannels(self._config["Channels"])
        waveFile.setsampwidth(self._config["SampleWidth"])
        waveFile.setframerate(int(self._config["Framerate"]))
        waveFile.writeframes(b''.join(data))
        waveFile.close()
        
        audio = wh.pad_or_trim(wh.load_audio("out.wav"))
        result = wh.transcribe(self._model, audio, fp16=False)["text"]
        os.remove("out.wav")
        
        return result, GoogleTranslator(source='ja', target='en').translate(text=result)
    
    def translate_text(self, text):
        return GoogleTranslator(source='ja', target='en').translate(text=text)