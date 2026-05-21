# 
from imports import *
from engine import speak
import os
import pyautogui
from PIL import ImageGrab # Screenshot lene ke liye
import webbrowser
import pywhatkit
import requests
import xml.etree.ElementTree as ET
import ctypes # PC Lock ke liye

def capture_and_analyze():
    """Screenshot lene ka function"""
    # Ek 'temp' folder bana lo agar nahi hai
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    path = "temp/screen_shot.png"
    screenshot = ImageGrab.grab() # Screen capture
    screenshot.save(path)
    
    speak("Screenshot le liya hai. Main dekh kar batati hoon.")
    # Yahan par aap apne AI (Gemini) ko ye image bhej sakte hain
    return path

def system_control(query):
    """System commands ko handle karne ka function"""
    query = query.lower().strip()

    # 0. Exit
    if any(w in query for w in ["exit", "bye", "quit", "band ho jao", "chalo bye"]):
        speak("Alvida Alok! Phir milte hain.")
        os._exit(0) 
        return True
    
    # 1. PC Lock
    if any(w in query for w in ["lock the pc", "lock karo", "system lock"]):
        speak("Theek hai Alok, PC lock kar rahi hoon.")
        ctypes.windll.user32.LockWorkStation()
        return True

    # 2. Shutdown
    if "shutdown" in query and "pc" in query:
        speak("PC 10 second mein shutdown ho jayega. Bye bye!")
        os.system("shutdown /s /f /t 10")
        return True

    # 3. Window Management (Minimize/Close/Maximize - Bina desktop_tasks ke)
    if any(w in query for w in ["minimize", "desktop dikhao", "saare window", "everything", "all windows"]):
        speak("Theek hai Alok, saare windows minimize kar rahi hoon.")
        pyautogui.hotkey('win', 'd') 
        return True

    if any(w in query for w in ["close the window", "window band karo", "alt f4", "current window"]):
        speak("Current window band kar rahi hoon.")
        pyautogui.hotkey('alt', 'f4')
        return True
        
    if "maximize" in query or "fit to screen" in query:
        speak("Window size adjust kar rahi hoon.")
        # Maximize karne ke liye pyatugui ka direct shortcut
        pyautogui.hotkey('alt', 'space')
        pyautogui.press('x')
        return True

    # 4. Volume Control
    if any(w in query for w in ["volume", "awaaz"]):
        if any(w in query for w in ["up", "badhao", "high"]):
            for _ in range(10): pyautogui.press("volumeup")
            speak("Volume badha di hai.")
        else:
            for _ in range(10): pyautogui.press("volumedown")
            speak("Volume kam kar di hai.")
        return True

    # 5. Brightness Control
    if "brightness" in query:
        try:
            curr = sbc.get_brightness()[0] # Make sure 'sbc' is in imports.py
            if any(w in query for w in ["up", "badhao", "zyada"]):
                sbc.set_brightness(min(100, curr + 25))
            else:
                sbc.set_brightness(max(0, curr - 25))
            speak("Brightness adjust kar di.")
        except Exception as e:
            print(f"Brightness Error: {e}")
        return True

    # 6. Screenshot command
    if "dekh kar batao" in query or "analyze screen" in query:
        img_path = capture_and_analyze()
        return True

    return False

def handle_youtube(query):
    """YouTube commands handle karne ka function"""
    query = query.lower()
    
    if "open youtube" in query:
        print("Kai: Opening YouTube...")
        webbrowser.open("https://www.youtube.com")
        return True

    elif "play" in query or "bajao" in query:
        song_name = query.replace("play", "").replace("bajao", "").replace("youtube pe", "").strip()
        if song_name:
            print(f"Kai: Playing {song_name} on YouTube...")
            pywhatkit.playonyt(song_name)
            return True
        else:
            print("Kai: Kya bajau Boss? Gaane ka naam bataiye.")
            return False

    return False

def get_weather(query):
    """Weather API function"""
    try:
        location = query.replace("weather", "").replace("in", "").replace("what is the", "").strip()
        if not location: 
            location = "Bihar" 

        url = f"https://wttr.in/{location}?format=%C+%t" 
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            weather_data = response.text.strip()
            return f"{location} ka mausam abhi {weather_data} hai."
        else:
            return "Mausam ka server abhi busy hai."
            
    except Exception as e:
        print(f"Weather Error: {e}")
        return "Internet connection mein dikkat hai ya mausam fetch nahi ho paaya."

def get_news():
    """News API function"""
    try:
        url = "https://news.google.com/rss/search?q=India+latest+news&hl=en-IN&gl=IN&ceid=IN:en"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            news_list = []
            
            for item in root.findall('./channel/item')[:3]:
                title = item.find('title').text
                news_list.append(title)
            
            full_news = " . ".join(news_list)
            return f"Aaj ki taza khabrein: {full_news}"
        else:
            return "News server response nahi de raha."
            
    except Exception as e:
        print(f"News Error: {e}")
        return "News fetch karne mein problem hui."