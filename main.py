from imports import *
import engine
from engine import get_identity, speak, take_command, welcome
from actions import system_control, handle_youtube, get_weather, get_news
import datetime
import random
from colorama import Fore, init
import threading
import sys
import time   # Exit animation ke delay ke liye add kiya hai
import gui    # Aapka GUI import

import os
from dotenv import load_dotenv
from groq import Groq  # जो भी आपकी Groq लाइब्रेरी है

# 1. सबसे पहले .env फ़ाइल से वेरिएबल्स लोड करें
load_dotenv()

# 2. अब एन्वायरमेंट वेरिएबल से Key निकालें
groq_api_key = os.getenv("MY_API_KEY")

# 3. चेक करें कि की लोड हुई या नहीं
if not groq_api_key:
    raise ValueError("Error: MY_API_KEY नहीं मिली! कृपया चेक करें कि .env फ़ाइल सही जगह पर है।")

# 4. अब Groq क्लाइंट को इनिशियलाइज़ करें
client = Groq(api_key=groq_api_key)

# Initialize colorama to handle cautions
init(autoreset=True)

# Groq Client Initialization (Apni API key yahan lagayein ya .env use karein)
# client = Groq(api_key=groq_api_key)

# Greetings Object
from greetings import Greetings
kai_greet = Greetings()

def get_live_data(query):
    """Internet se live data nikalne ka function (DuckDuckGo Search)"""
    try:
        results_str = ""
        with DDGS() as ddgs:
            search_results = ddgs.text(query, region='in-en', max_results=3)
            for res in search_results:
                results_str += f"\n- {res['body']}"
        return results_str if results_str else "No data found."
    except:
        return "Search failed."

def run_kai_logic():
    # --- INITIAL SETTINGS ---
    is_awake = True
    MAX_HISTORY = 10
    chat_history = []
    
    # --- 1. STARTUP GREETING ---
    welcome_msg = kai_greet.get_time_based_greeting()
    gui.gui_chat_history.append(f"Kai: {welcome_msg}")
    print(Fore.LIGHTMAGENTA_EX + "Kai: " + welcome_msg)
    
    # Starting animation update
    gui.current_kai_status = "talking"
    speak(welcome_msg)
    # Bolne ke baad default state 'listening' honi chahiye (jab jagi ho)
    gui.current_kai_status = "listening" 
    
    # --- MAIN LOOP ---
    while True:
        # 1. Take Command (Awake/Sleep check karke GUI update karein)
        if is_awake:
            print("Listening...")
            gui.current_kai_status = "listening"
        else:
            gui.current_kai_status = "sleep"
            
        raw_input = take_command(silent=not is_awake)
        
        # Agar user ne kuch nahi bola toh loop wapas start hoga
        if not raw_input:
            continue

        # 2. MANUAL TYPE MODE
        if raw_input == "manual_type_mode":
            raw_input = input(Fore.YELLOW + "Alok (Type here): ").lower()

        if raw_input and raw_input.strip() != "":
            user_input = raw_input.replace("vedar", "weather").replace("khabar", "news").lower()
            user_input = user_input.replace("pahla", "first").replace("dusra", "second")
            
            gui.gui_chat_history.append(f"Alok: {user_input}")

            wake_words = ["wake up", "kai", "hey kai", "utho", "shuru ho jao"]
            sleep_words = ["rest", "sleep", "so jao", "wait", "ruko", "chup ho jao"]
            exit_words = ["exit", "quit", "chhutti", "band ho jao"]

            # --- EXIT CONDITION (FIXED) ---
            if any(word in user_input for word in exit_words):
                msg = "Theek hai Boss, ab main chalti hoon. Bye bye!"
                gui.gui_chat_history.append(f"Kai: {msg}")
                
                gui.current_kai_status = "talking"
                speak(msg)
                
                # Exit pe 'sleep' nahi balki 'logout' animation aayega
                gui.current_kai_status = "logout"
                time.sleep(2.5) # Thoda delay taaki logout animation screen par dikh sake
                break # Loop todega aur AI thread band ho jayega

            # --- PHASE A: WAKE/SLEEP LOGIC (FIXED) ---
            if not is_awake:
                if any(word in user_input for word in wake_words):
                    is_awake = True
                    msg = "I am back Boss! Batao kya help karoon?"
                    gui.gui_chat_history.append(f"Kai: {msg}")
                    
                    gui.current_kai_status = "wakeup" # Optionally wakeup animation agar ho toh
                    gui.current_kai_status = "talking"
                    speak(msg)
                    gui.current_kai_status = "listening" # Jaagne ke baad wapas sunne lagegi
                    continue
                else:
                    print(Fore.CYAN + "... Kai is Sleeping ...")
                    gui.current_kai_status = "sleep" # Jab tak nahi uthegi, soti rahegi
                    continue

            if any(word in user_input for word in sleep_words):
                is_awake = False
                msg = "Theek hai Boss, main rest kar rahi hoon. Bulana ho toh Wakeup bol dena."
                gui.gui_chat_history.append(f"Kai: {msg}")
                
                gui.current_kai_status = "talking"
                speak(msg)
                gui.current_kai_status = "sleep" # Sirf yahan permanently 'sleep' state aayegi
                continue

            # --- PHASE B: GREETINGS & IDENTITY ---
            if "kaun ho" in user_input or "who are you" in user_input or "identity" in user_input:
                res = get_identity() 
                gui.gui_chat_history.append(f"Kai: {res}")
                print(Fore.CYAN + "Kai: " + res)
                
                gui.current_kai_status = "talking"
                speak(res)
                gui.current_kai_status = "listening" # Reply ke baad dobara sunne ke liye ready
                continue

            elif "kya kar sakti ho" in user_input or "capabilities" in user_input:
                res = kai_greet.show_capabilities()
                gui.gui_chat_history.append(f"Kai: Capabilities shown")
                
                gui.current_kai_status = "talking"
                speak("Main ye sab kar sakti hoon Boss.")
                gui.current_kai_status = "listening"
                continue

            # --- PHASE C: ACTIVE FEATURES ---
            if "weather" in user_input or "mausam" in user_input:
                res = get_weather(user_input)
                gui.gui_chat_history.append(f"Kai: {res}")
                
                gui.current_kai_status = "talking"
                speak(res)
                gui.current_kai_status = "listening"
                continue

            if "news" in user_input or "khabar" in user_input:
                res = get_news()
                gui.gui_chat_history.append(f"Kai: News updated")
                
                gui.current_kai_status = "talking"
                speak(res)
                gui.current_kai_status = "listening"
                continue

            if system_control(user_input) or handle_youtube(user_input):
                # System commands (jaise volume up/down) ke baad sidhe listen karegi
                gui.current_kai_status = "listening"
                continue

            # --- Memory Song Selection ---
            selection_words = ["first", "second", "third", "pahla", "dusra", "tisra", "1st", "2nd", "3rd"]
            if any(word in user_input for word in selection_words) and ("play" in user_input or "bajao" in user_input):
                last_ai_msg = next((msg["content"] for msg in reversed(chat_history) if msg["role"] == "assistant"), None)
                if last_ai_msg:
                    try:
                        prompt = f"From this list: '{last_ai_msg}', pick the {user_input} song. Just give name and artist."
                        res = client.chat.completions.create(
                            messages=[{"role": "user", "content": prompt}],
                            model="llama-3.3-70b-versatile"
                        )
                        song_to_play = res.choices[0].message.content.strip()
                        if song_to_play:
                            gui.gui_chat_history.append(f"Kai: Playing {song_to_play}")
                            gui.current_kai_status = "talking"
                            speak(f"Ok Boss, {song_to_play} play karti hoon.")
                            gui.current_kai_status = "listening"
                            handle_youtube(f"play {song_to_play}")
                            continue
                    except:
                        pass

            # --- PHASE D: AI CONVERSATION (LLaMA) ---
            now = datetime.datetime.now()
            h = now.strftime('%I')
            m = now.strftime('%M')
            p = "shaam ke" if now.hour >= 12 else "subah ke"
            readable_time = f"{int(h)} baj kar {m} minute ho rahe hain {p}"
            
            search_keywords = ["today", "score", "price", "sale", "flipkart"]
            
            system_msg = (
                "Your name is Kai, a smart Indian girl. "
                "### STRICT RULES ### "
                "1. LANGUAGE: Speak ONLY in natural Hinglish (Roman script). "
                "2. NO TRANSLATIONS: Do NOT provide English versions or brackets for your sentences. "
                "3. NO REPETITION: Reply only once. Do not repeat the same meaning in English. "
                "4. PERSONALITY: Speak like a close friend. Address the user as 'Boss'. "
                f"5. CONTEXT: The time is {readable_time}. When asked for time, say it in this word format."
            )
            
            if any(w in user_input for w in search_keywords):
                live_info = get_live_data(user_input)
                system_msg += f"\n\nLIVE WEB DATA:\n{live_info}"

            try:
                messages = [{"role": "system", "content": system_msg}]
                for msg in chat_history[-MAX_HISTORY:]:
                    messages.append(msg)
                messages.append({"role": "user", "content": user_input})

                chat = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.1-8b-instant",
                    temperature=0.3
                )
                
                reply = chat.choices[0].message.content.strip()

                # History Update
                chat_history.append({"role": "user", "content": user_input})
                chat_history.append({"role": "assistant", "content": reply})
                
                # --- Chat History Update GUI ---
                gui.gui_chat_history.append(f"Kai: {reply}")
                print(Fore.LIGHTMAGENTA_EX + "Kai: " + reply)

                # --- Status Update & Speak ---
                gui.current_kai_status = "talking"  
                speak(reply)                        
                gui.current_kai_status = "listening" # Reply dene ke baad wapas next command ka wait karegi
                
            except Exception as e:
                print(Fore.RED + f"Error: {e}")
                gui.current_kai_status = "talking"
                speak("Sorry Boss, internet issue lag raha hai.")
                gui.current_kai_status = "listening"

# --- THREADING AND ENTRY POINT ---
if __name__ == "__main__":
    # AI Logic ko alag thread mein start kar rahe hain bina daemon=True ke
    ai_thread = threading.Thread(target=run_kai_logic)
    ai_thread.start()

    # GUI loop main thread mein chalega
    try:
        gui.main_gui_loop()
    except KeyboardInterrupt:
        print("Closing KAI Assistant...")
        sys.exit()