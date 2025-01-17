import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI') or \
        f"sqlite:///{os.path.join(basedir, 'app.db')}"  # Correct the path here
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Debugging: Print loaded values
    
