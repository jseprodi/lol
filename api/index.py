import os
import sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

# Import Django and configure
import django
django.setup()

# Import Django components
from django.core.handlers.wsgi import WSGIRequest
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.conf import settings

# Get the WSGI application
application = get_wsgi_application()

class VercelHandler(BaseHTTPRequestHandler):
    """Vercel-compatible HTTP request handler"""
    
    def do_GET(self):
        """Handle GET requests"""
        self._handle_request('GET')
    
    def do_POST(self):
        """Handle POST requests"""
        self._handle_request('POST')
    
    def _handle_request(self, method):
        """Handle HTTP requests"""
        try:
            # Parse the URL
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            query_params = parse_qs(parsed_url.query)
            
            # Read request body for POST
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else b''
            
            # Create a Django-compatible request
            django_request = WSGIRequest({
                'REQUEST_METHOD': method,
                'PATH_INFO': path,
                'QUERY_STRING': parsed_url.query,
                'SERVER_NAME': 'vercel',
                'SERVER_PORT': '80',
                'HTTP_HOST': self.headers.get('Host', ''),
                'HTTP_USER_AGENT': self.headers.get('User-Agent', ''),
                'HTTP_ACCEPT': self.headers.get('Accept', ''),
                'CONTENT_TYPE': self.headers.get('Content-Type', ''),
                'CONTENT_LENGTH': content_length,
                'wsgi.input': body,
                'wsgi.url_scheme': 'https',
                'wsgi.version': (1, 0),
                'wsgi.errors': sys.stderr,
                'wsgi.multithread': False,
                'wsgi.multiprocess': False,
                'wsgi.run_once': True,
            })
            
            # Process through Django
            response = application(django_request)
            
            # Send response
            self.send_response(response.status_code)
            for header, value in response.items():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response.content)
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Internal Server Error: {str(e)}'.encode())

# Vercel requires these exports
handler = VercelHandler
app = VercelHandler
