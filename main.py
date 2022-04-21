import email.message
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)

        content_length = self.headers.get("Content-Length")
        if content_length == None:
            print("None")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write('<html><head><meta charset="utf-8">'.encode('utf-8'))
        self.wfile.write('<title>Простой HTTP-сервер.</title></head>'.encode('utf-8'))
        self.wfile.write('<body>Был получен GET-запрос.</body></html>'.encode('utf-8'))

    def do_POST(self):
        params = parse_qs(urlparse(self.path).query)
        print(params)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write('<html><head><meta charset="utf-8">'.encode('utf-8'))
        self.wfile.write('<title>Простой HTTP-сервер.</title></head>'.encode('utf-8'))
        self.wfile.write('<body>Был получен POST-запрос.</body></html>'.encode('utf-8'))

    def do_DELETE(self):
        params = parse_qs(urlparse(self.path).query)
        print(params)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write('<html><head><meta charset="utf-8">'.encode('utf-8'))
        self.wfile.write('<title>Простой HTTP-сервер.</title></head>'.encode('utf-8'))
        self.wfile.write('<body>Был получен DELETE-запрос.</body></html>'.encode('utf-8'))
        pass


server = HTTPServer(("127.0.0.1", 8000), RequestHandler)
server.serve_forever()


