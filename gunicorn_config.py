# gunicorn_config.py
import os
from dotenv import load_dotenv

# Load .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
print(f".env path: {dotenv_path}")
if os.path.exists(dotenv_path):
    result = load_dotenv(dotenv_path)
    print(f".env loaded: {result}")
else:
    print(".env file does not exist")


# Gunicorn config
bind = "0.0.0.0:8000"
workers = 1