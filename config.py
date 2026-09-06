# config.py
import os

# Folder where history is saved (Pydroid-friendly)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "micro_grolk_history.json")

MAX_HISTORY = 10
APP_NAME = "micro_grolk"
VERSION = "1.0"