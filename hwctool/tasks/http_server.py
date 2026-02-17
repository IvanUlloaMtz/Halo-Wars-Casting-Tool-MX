import http.server
import socketserver
import threading
import os
import logging

logger = logging.getLogger('root')

class HTTPServerThread(threading.Thread):
    def __init__(self, port=8000, root_dir='casting_html'):
        super().__init__()
        self.port = port
        self.root_dir = root_dir
        self.httpd = None
        self.daemon = True

    def run(self):
        # Create a custom TCPServer with allow_reuse_address=True
        class ReusableTCPServer(socketserver.TCPServer):
            allow_reuse_address = True
        
        # Custom Handler to pass directory argument
        root_dir_to_serve = self.root_dir
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=root_dir_to_serve, **kwargs)

        try:
            with ReusableTCPServer(("127.0.0.1", self.port), Handler) as httpd:
                self.httpd = httpd
                logger.info(f"Iniciando Servidor HTTP en puerto {self.port} sirviendo {self.root_dir}")
                httpd.serve_forever()
        except Exception as e:
            logger.error(f"Error en servidor HTTP: {e}")

    def stop(self):
        httpd = self.httpd
        if httpd is not None:
            httpd.shutdown()
            httpd.server_close()
