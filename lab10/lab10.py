import time
import requests
import webbrowser
import numpy as np
import pyaudio
import pyttsx3
from faster_whisper import WhisperModel
import os


os.environ["HF_TOKEN"] = 'your token'
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

class Speech():
    def __init__(self):
        self.tts = pyttsx3.init('sapi5')
        self.voices = self.tts.getProperty('voices')
    
    def set_voice(self, speaker_index):
        if 0 <= speaker_index < len(self.voices):
            return self.voices[speaker_index].id
        return self.voices[0].id
    
    def text2voice(self, speaker=1, text='Ready'):
        self.tts.setProperty('voice', self.set_voice(speaker))
        self.tts.say(text)
        self.tts.runAndWait()

class Recognize:
    def __init__(self):
        self.model = WhisperModel("distil-large-v3", device="cuda", compute_type="float16")
        
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000
        )

    def listen(self):
        print("Listening...")
        while True:
            data = self.stream.read(64000, exception_on_overflow=False)
            audio_np = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
            
            segments, _ = self.model.transcribe(
                audio_np, 
                language="en", 
                beam_size=7,
                vad_filter=True,
                no_speech_threshold=0.6, 
                vad_parameters=dict(min_silence_duration_ms=500) 
            )
            
            for segment in segments:
                if segment.text.strip():
                    yield segment.text.lower().replace('.', '').replace('?', '').strip()
    
    def clear(self):
        if self.stream.get_read_available() > 0:
            self.stream.read(self.stream.get_read_available(), exception_on_overflow=False)

def get_word_info(word):
    try:
        response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
        if response.status_code == 200:
            return response.json()[0]
    except Exception as e:
        print(f'Error: {e}')
    return None

speech = Speech()
rec = Recognize()

current_data = None
current_word = ''

speech.text2voice(text='Voice assistant started. Use find command')

for text in rec.listen():
    print(f'Recognized: {text}')
    rec.stream.stop_stream()

    if 'find' in text:
        parts = text.split('find', 1)
        if len(parts) > 1:
            raw_word = parts[1].strip()
            current_word = raw_word.replace(' ', '-')
            print(f"Searching for: {current_word}")
            current_data = get_word_info(current_word)
            
            if current_data:
                speech.text2voice(text=f'I found {raw_word}. What info do you need?')
            else:
                speech.text2voice(text=f'Sorry, I can\'t find {raw_word}')
                current_data = None

    if current_data:
        if 'meaning' in text or 'definition' in text:
            try:
                definition = current_data['meanings'][0]['definitions'][0]['definition']
                print(f'Definition: {definition}')
                speech.text2voice(text=definition)
            except (KeyError, IndexError):
                speech.text2voice(text="I can't explain this word.")

        elif 'sample' in text or 'usage' in text:
            found_ex = None
            for meaning in current_data.get('meanings', []):
                for defn in meaning.get('definitions', []):
                    if defn.get('example'):
                        found_ex = defn.get('example')
                        break
                if found_ex: break
            
            if found_ex:
                print(f'Example found: {found_ex}')
                speech.text2voice(text=f"Here is a sample sentence: {found_ex}")
            else:
                speech.text2voice(text="I couldn't find any usage examples for this word.")

        elif 'link' in text:
            url = current_data.get('sourceUrls', [None])[0]
            if url:
                webbrowser.open(url)
                speech.text2voice(text='Opening link.')
            else:
                speech.text2voice(text='Link not found.')
        
        elif 'synonyms' in text or 'similar' in text:
            all_synonyms = []
            for meaning in current_data.get('meanings', []):
                for synonym in meaning.get('synonyms', []):
                    all_synonyms.append(synonym)
            
            if all_synonyms:
                unique_syns = list(set(all_synonyms))[:4]
                syns_string = ", ".join(unique_syns)
                print(f"Synonyms found: {syns_string}")
                speech.text2voice(text=f"Some synonyms for {current_word} are: {syns_string}")
            else:
                speech.text2voice(text=f"I couldn't find any synonyms for {current_word}.")
        
        elif 'spell' in text:
            word_to_spell = current_word.replace('-', ' ')
            spelled_word = ". ".join(list(word_to_spell)).upper()
            
            print(f"Spelling: {spelled_word}")
            
            current_rate = speech.tts.getProperty('rate')
            speech.tts.setProperty('rate', 130)
            
            speech.text2voice(text=f"It is spelled as: {spelled_word}")
            
            speech.tts.setProperty('rate', current_rate)

        elif 'save' in text:
            try:
                word_to_save = current_data.get('word', current_word)
                def_to_save = current_data['meanings'][0]['definitions'][0]['definition']
                
                with open('dictionary.txt', 'a', encoding='utf-8') as f:
                    f.write(f"WORD: {word_to_save}\nDEF: {def_to_save}\n{'='*20}\n")
                
                print(f"Saved {word_to_save} to dictionary.txt")
                speech.text2voice(text=f"I saved the word {word_to_save} to your file.")
            except Exception as e:
                print(f"Save error: {e}")
                speech.text2voice(text="I couldn't save this word.")

    if any(cmd in text for cmd in ['close', 'exit', 'quit', 'goodbye']):
        speech.text2voice(text='Goodbye!')
        break

    time.sleep(0.1)
    rec.stream.start_stream()
    rec.clear()