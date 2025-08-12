import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

# Import Django and configure
import django
django.setup()

# Import the WSGI application
from blog_project.wsgi import application

# Vercel requires these variables
app = application
handler = application
