import os
import asyncio
import edge_tts
import speech_recognition as sr
from groq import Groq
from duckduckgo_search import DDGS
import pygame
import time
import datetime
import webbrowser
import threading
import pyautogui
import screen_brightness_control as sbc
import ctypes 
from pynput import keyboard
from colorama import Fore, init
import os
import desktop_tasks
from PIL import ImageGrab
# Initialization
init(autoreset=True)
pyautogui.FAILSAFE = False 

CORRECT_MIC_ID = 33