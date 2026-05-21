from imports import *
from faster_whisper import WhisperModel
import asyncio
import pygame
import time
import datetime
import numpy as np
import sounddevice as sd
import queue
import threading
from colorama import Fore
import edge_tts
from greetings import Greetings
from pynput import keyboard

# --- INITIALIZATION ---
stop_talking = False
manual_trigger = False
is_typing = False
q = queue.Queue()

# Whisper Model Setup
whisper_model = WhisperModel("./whisper-small-model", device="cpu", compute_type="int8")
kai_greet = Greetings()
pygame.mixer.init()

# --- KEYBOARD LISTENER (Reserved your K and T keys) ---
def on_press(key):
    global stop_talking, manual_trigger, is_typing
    if is_typing: return
    try:
        if hasattr(key, 'char'):
            if key.char == 'k': 
                stop_talking = True
                pygame.mixer.music.stop()
            if key.char == 't': 
                manual_trigger = True
                print(f"\n{Fore.YELLOW}[Switching to Type Mode...]")
    except: pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

# --- AUDIO CALLBACK ---
def audio_callback(indata, frames, time, status):
    q.put(indata.copy())

# --- TTS LOGIC (With your Phonetic Fixes) ---
async def amain(text) -> None:
    VOICE = "hi-IN-SwaraNeural" 
    communicate = edge_tts.Communicate(text, VOICE, rate="-5%", pitch="+0Hz")
    await communicate.save("reply.mp3")

def get_identity():
    try:
        return kai_greet.tell_identity()
    except:
        return "I am KAI, your AI assistant."

def get_caps():
    try:
        return kai_greet.show_capabilities()
    except:
        return "I can chat, tell time, and help with tasks."
def speak(text):
    global stop_talking
    stop_talking = False
    
    # 1. Pehle music stop karein aur file unload karein taaki Permission Error na aaye
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload() # Ye line sabse zaroori hai
    except:
        pass

    # --- Gender & Phonetic Fixes ---
    gender_fixes = {"bol raha hoon": "bol rahi hoon", "jaa raha hoon": "jaa rahi hoon"}
    for old, new in gender_fixes.items():
        text = text.lower().replace(old, new)

    replacements = {"main": "मैं", "hu": "हूँ", "ho": "हो", "rha": "रहा", "rhi": "रही","par": "पर", "kya": "क्या","kai": "काई ", "hai": "है", "kaise": "कैसे", "dene": "देने ", "hoon": "हूँ"}
    words = text.split()
    final_text = " ".join([replacements.get(w, w) for w in words])
    
    # 2. Ab naya audio save karein
    asyncio.run(amain(final_text)) 
    
    try:
        pygame.mixer.music.load("reply.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            if stop_talking: 
                pygame.mixer.music.stop()
                pygame.mixer.music.unload() # Stop hone par bhi unload karein
                break
            time.sleep(0.05)
    except Exception as e: 
        print(f"Audio Error: {e}")

# --- NEW SMART LISTENING (Replaces old take_command) ---
# Purana: def take_command():
# Naya:
def take_command(silent=False): 
    global stop_talking, manual_trigger
    # ... baaki pura code same rahega ...
    
    fs = 16000
    
    # InputStream setup for continuous mic access
    with sd.InputStream(samplerate=fs, channels=1, callback=audio_callback):
        print(f"{Fore.WHITE}[Kai is Always Listening...]")
        
        while True:
            # Check for Manual Type Trigger ('t' key)
            if manual_trigger:
                return "manual_type_mode"
            
            # Get audio chunk from queue
            data = q.get()
            
            # Volume Trigger: User bolna shuru kare tabhi trigger ho
            if np.max(np.abs(data)) > 0.04: 
                # Immediate Interrupt: User bola toh Kai chup
                if pygame.mixer.music.get_busy():
                    stop_talking = True
                    pygame.mixer.music.stop()

                # Record current chunk + next 4 seconds for context
                recording = [data]
                for _ in range(int(fs / len(data) * 4)):
                    recording.append(q.get())
                
                audio_np = np.concatenate(recording, axis=0).flatten()
                audio_np = np.clip(audio_np * 4.0, -1.0, 1.0) # Boost

                # Transcription
                segments, _ = whisper_model.transcribe(
                    audio_np, 
                    beam_size=5,
                    initial_prompt="Kaise ho? Hello Kai, suno. What is the time?"
                )
                
                query = "".join([segment.text for segment in segments]).strip().lower()
                if query:
                    print(f"{Fore.CYAN}Alok: {query}")
                    return query

# --- WELCOME FUNCTION ---
def welcome():
    try:
        message = kai_greet.get_time_based_greeting()
        speak(message)
    except:
        speak("Namaste Alok, main taiyaar hoon.")

# --- MAIN LOOP ---
if __name__ == "__main__":
    print(f"{Fore.GREEN}[Kai is Online and Ready!]")
    welcome()
    
    while True:
        cmd = take_command()
        
        if not cmd:
            continue
            
        if cmd == "manual_type_mode":
            manual_trigger = False
            is_typing = True
            cmd = input(f"{Fore.YELLOW}Type your command: ").lower()
            is_typing = False
            
        if "exit" in cmd or "quit" in cmd or "bye" in cmd:
            speak("Bye! Apna khayal rakhiyega.")
            break
            
        # --- COMMAND LOGIC ---
        if "hello" in cmd:
            speak("नमस्ते आलोक, मैं आपकी क्या मदद कर सकती हूँ?")
        
        elif "time" in cmd:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Abhi {current_time} ho rahe hain")