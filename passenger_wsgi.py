import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Set the Django settings module (update if you use a different one)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')

# Import the WSGI application
from myapp.wsgi import application
