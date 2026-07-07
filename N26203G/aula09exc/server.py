import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import model
import controller
import view

PORT = 8000

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    """
    Multi-threaded HTTP server that spawns a new thread for each connection,
    preventing browser socket lockups and keep-alive delays.
    """
    daemon_threads = True

class PetFelizHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Keep a clean diagnostic log
        print(f"[LOG] {self.address_string()} - {format % args}")

    def do_OPTIONS(self):
        """Handles CORS preflight options requests with boundary safety."""
        try:
            if self.path == "/pets":
                view.render_cors_preflight(self)
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            print(f"[ERROR] Exception on OPTIONS {self.path}: {str(e)}")

    def do_GET(self):
        """Routes GET requests with global exception fallback."""
        try:
            if self.path == "/pets":
                controller.handle_list_pets(self)
            elif self.path in ("/", "/index.html"):
                self.serve_static("index.html", "text/html; charset=utf-8")
            elif self.path == "/style.css":
                self.serve_static("style.css", "text/css; charset=utf-8")
            elif self.path == "/app.js":
                self.serve_static("app.js", "application/javascript; charset=utf-8")
            else:
                view.render_error(self, 404, "Caminho não encontrado.")
        except Exception as e:
            print(f"[ERROR] Exception on GET {self.path}: {str(e)}")
            try:
                view.render_error(self, 500, f"Erro interno no servidor: {str(e)}")
            except:
                pass

    def do_POST(self):
        """Routes POST requests with boundary safety."""
        try:
            if self.path == "/pets":
                try:
                    content_length = int(self.headers.get('Content-Length', 0))
                except ValueError:
                    content_length = 0
                
                body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ""
                controller.handle_create_pet(self, body)
            else:
                view.render_error(self, 404, "Caminho não encontrado.")
        except Exception as e:
            print(f"[ERROR] Exception on POST {self.path}: {str(e)}")
            try:
                view.render_error(self, 500, f"Erro interno no servidor: {str(e)}")
            except:
                pass

    def serve_static(self, filename, content_type):
        """Helper to safely read and serve local static assets (HTML, CSS, JS)."""
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        if not os.path.exists(filepath):
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b"Arquivo estatico nao encontrado")
            return
        
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"Erro ao ler arquivo: {str(e)}".encode('utf-8'))

def run(server_class=ThreadingHTTPServer, handler_class=PetFelizHandler, port=PORT):
    # Initialize sqlite3 database schema
    print("Inicializando banco de dados...")
    model.init_db()
    
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Servidor PetFeliz multi-thread iniciado com sucesso em http://localhost:{port}/")
    print("Pressione Ctrl+C para encerrar o servidor.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor sendo encerrado...")
        httpd.server_close()
        print("Servidor finalizado.")

if __name__ == "__main__":
    run()
