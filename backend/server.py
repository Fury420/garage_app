import http.server
import socketserver
import subprocess
import os

PORT = 5001

BASE_DIR = os.path.dirname(__file__)
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
RESOURCES_DIR = os.path.join(BASE_DIR, "..", "resources")

os.makedirs(RESOURCES_DIR, exist_ok=True)

class OCRHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == "/ocr":
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)

            upload_path = os.path.join(RESOURCES_DIR, "upload.jpg")
            output_base = os.path.join(RESOURCES_DIR, "output")

            with open(upload_path, "wb") as f:
                f.write(data)

            subprocess.run(["tesseract", upload_path, output_base, "-l", "slk"], check=True)

            with open(output_base + ".txt", "r") as f:
                result = f.read()

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(result.encode("utf-8"))
        else:
            self.send_error(404, "Not Found")

os.chdir(FRONTEND_DIR)

with socketserver.TCPServer(("", PORT), OCRHandler) as httpd:
    print(f"Server beží na http://localhost:{PORT}")
    httpd.serve_forever()

