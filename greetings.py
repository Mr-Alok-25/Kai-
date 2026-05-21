# 
import random
from datetime import datetime

class Greetings:
    def __init__(self):
        self.owner_name = "Alok"
        
    def get_time_based_greeting(self):
        hour = datetime.now().hour
        
        # 1. Morning (4 AM to 12 PM)
        if 4 <= hour < 12:
            morning_list = [
                "Good morning, Boss! Systems are fresh and ready.",
                "Suprabhat Boss. Ready to start the day?",
                "Morning, Boss! All modules are green.",
                "Good morning! Hope you have a productive day, Boss.",
                "System is up, Boss. Let's get to work."
            ]
            return random.choice(morning_list)
        
        # 2. Afternoon (12 PM to 4 PM)
        elif 12 <= hour < 16:
            afternoon_list = [
                "Good afternoon, Boss! Hope the day is going well.",
                "Afternoon, Boss. Need help with anything?",
                "Good afternoon! Systems are running smooth.",
                "Lunch break done? I'm ready when you are, Boss.",
                "Working hard as always, Boss? I'm here to assist."
            ]
            return random.choice(afternoon_list)
        
        # 3. Evening (4 PM to 8 PM)
        elif 16 <= hour < 20:
            evening_list = [
                "Good evening, Boss! How was your day?",
                "Evening, Boss. Time for a quick update?",
                "Good evening! I've updated the logs for you.",
                "Sunset vibes, Boss. Any more tasks for today?",
                "Systems are stable this evening, Boss."
            ]
            return random.choice(evening_list)
        
        # 4. Night (8 PM to 4 AM)
        else:
            night_list = [
                "Good night, Boss! Up late today?",
                "Still working, Boss? I've got your back.",
                "Good late night. Systems on silent mode, Boss.",
                "Night owl mode activated. Command me, Boss.",
                "It's late, Boss. I'm here if you need anything."
            ]
            return random.choice(night_list)

    def tell_identity(self):
        return f"Main {self.owner_name} ki personal AI assistant hoon. Aap mujhe Kai keh sakte hain."

    def show_capabilities(self):
        caps = [
            "Main aapke liye ye sab kar sakti hoon:",
            "• System Health & Thermals (Pending)",
            "• Web Searching & Wikipedia",
            "• YouTube & Media Control",
            "• Weather & News Updates"
        ]
        return "\n".join(caps)