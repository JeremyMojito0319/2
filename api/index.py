import sys
import os

# Add the project root to Python path  
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import Flask app
from src.main import app

# Vercel expects 'app' variable for Python runtime
# This is the WSGI application object
app = app
