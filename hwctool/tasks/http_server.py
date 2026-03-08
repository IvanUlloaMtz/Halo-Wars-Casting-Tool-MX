import http.server
import socketserver
import threading
import os
import logging
import time
import re

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
        root_dir_to_serve = os.path.abspath(self.root_dir)
        
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=root_dir_to_serve, **kwargs)

            def do_GET(self):
                # TAREA 3: Asset resolution normalization for leaders
                if self.path.startswith('/leaders/'):
                    filename = os.path.basename(self.path.split('?')[0])
                    name, ext = os.path.splitext(filename)
                    # Normalize to lowercase .webp
                    normalized_name = name.lower() + ".webp"
                    target_path = os.path.join(root_dir_to_serve, 'leaders', normalized_name)
                    
                    if not os.path.exists(target_path):
                        logger.warning(f"Asset no encontrado: {normalized_name}, sirviendo placeholder.webp")
                        target_path = os.path.join(root_dir_to_serve, 'leaders', 'placeholder.webp')
                    
                    self.send_response(200)
                    if target_path.endswith('.webp'):
                        self.send_header('Content-Type', 'image/webp')
                    elif target_path.endswith('.png'):
                        self.send_header('Content-Type', 'image/png')
                    self.end_headers()
                    try:
                        with open(target_path, 'rb') as f:
                            self.wfile.write(f.read())
                    except Exception as e:
                        logger.error(f"Error sirviendo asset {target_path}: {e}")
                    return

                # TAREA 4: Dynamic Cache-Bust injection for main overlays
                requested_file = self.path.split('?')[0]
                if requested_file in ['/', '/score.html', '/card.html', '/intro.html']:
                    file_to_serve = requested_file
                    if file_to_serve == '/': file_to_serve = '/score.html'
                    
                    full_path = os.path.join(root_dir_to_serve, file_to_serve.lstrip('/'))
                    if os.path.exists(full_path):
                        try:
                            with open(full_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            # Inject timestamp
                            ts = int(time.time())
                            # Replace .css and .js with ?v={ts}
                            # Matches src="path.js" or href="path.css"
                            content = re.sub(r'(href|src)="([^"]+\.(?:css|js))(?:\?v=[^"]*)?"', rf'\1="\2?v={ts}"', content)
                            
                            self.send_response(200)
                            self.send_header('Content-Type', 'text/html')
                            self.end_headers()
                            self.wfile.write(content.encode('utf-8'))
                            return
                        except Exception as e:
                            logger.error(f"Error procesando {full_path}: {e}")

                return super().do_GET()

        try:
            with ReusableTCPServer(("127.0.0.1", self.port), Handler) as httpd:
                self.httpd = httpd
                logger.info(f"Iniciando Servidor HTTP en puerto {self.port} sirviendo {self.root_dir}")
                httpd.serve_forever()
        except Exception as e:
            logger.error(f"Error en servidor HTTP: {e}")

    def stop(self):
        import threading
        httpd = self.httpd
        if httpd is not None:
            # Run shutdown in a thread with timeout to avoid blocking forever
            t = threading.Thread(target=httpd.shutdown, daemon=True)
            t.start()
            t.join(timeout=2)
            try:
                httpd.server_close()
            except Exception:
                pass
