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
            
            # Create a file-like object for wsgi.input
            if content_length > 0:
                body_bytes = self.rfile.read(content_length)
                from io import BytesIO
                wsgi_input = BytesIO(body_bytes)
            else:
                from io import BytesIO
                wsgi_input = BytesIO(b'')
            
            # Create a Django-compatible request environment
            environ = {
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
                'wsgi.input': wsgi_input,
                'wsgi.url_scheme': 'https',
                'wsgi.version': (1, 0),
                'wsgi.errors': sys.stderr,
                'wsgi.multithread': False,
                'wsgi.multiprocess': False,
                'wsgi.run_once': True,
            }
            
            # Create Django request object
            django_request = WSGIRequest(environ)
            
            # Create a start_response callable for WSGI
            def start_response(status, headers, exc_info=None):
                # Parse status code from status string (e.g., "200 OK")
                status_code = int(status.split()[0])
                self.send_response(status_code)
                
                # Send headers
                for header, value in headers:
                    self.send_header(header, value)
                self.end_headers()
                
                return self.wfile.write
            
            # Process through Django with proper WSGI interface
            response_iterable = application(django_request, start_response)
            
            # Write response content
            for chunk in response_iterable:
                if isinstance(chunk, bytes):
                    self.wfile.write(chunk)
                else:
                    self.wfile.write(chunk.encode('utf-8'))
            
            # Close the response if it has a close method
            if hasattr(response_iterable, 'close'):
                response_iterable.close()
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Internal Server Error: {str(e)}'.encode())

# Vercel requires these exports
handler = VercelHandler
app = VercelHandler
