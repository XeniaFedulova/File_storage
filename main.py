import email.message
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import os
from Meta import MetaInf
from DB import DataStorage




class RequestHandler(BaseHTTPRequestHandler):

    storage = DataStorage("File_storage")


    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        content_length = self.headers.get("Content-Length")
        if content_length == None:
            self.send_response(411)
        else:
            self.send_response(200)
            body = self.rfile.read(content_length)
            print(body)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write('<html><head><meta charset="utf-8">'.encode('utf-8'))
            self.wfile.write('<title>Простой HTTP-сервер.</title></head>'.encode('utf-8'))
            self.wfile.write('<body>Был получен GET-запрос.</body></html>'.encode('utf-8'))

    def do_POST(self):

        def put_file_to_dir(directory, payload, file_id, filename: str = None):
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(os.path.join(directory, filename), "wb") as f:
                f.write(payload)

        def upload():
            content_length = int(self.headers.get("Content-Length"))

            if content_length == None or content_length <= 0:
                self.send_error(411, message="No content")
                self.send_response(411)
            else:
                params = parse_qs(urlparse(self.path).query)
                filename = str(params['name'][0])
                directory = "C:\\Users\\user\\storage_files"
                payload = self.rfile.read(content_length)
                content_type = self.headers.get_content_type()


                info = MetaInf(params, payload, content_type)
                self.storage.load_to_database(info)
                file_id = info.id


                put_file_to_dir(directory, payload, file_id, filename=filename)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                with open(os.path.join(directory, filename), "wb") as f:
                    f.write(payload)

                meta = info.return_meta_info()
                # self.send_response(201)
                self.send_response_only(201, message=meta)
                print(meta)
                # self.wfile.write(meta)


        end = urlparse(self.path).path
        if end == '/api/upload':
            upload()
        else:
            self.send_error(404)




            # self.send_header("Content-type", "text/html")
            # self.end_headers()
            # self.wfile.write('<html><head><meta charset="utf-8">'.encode('utf-8'))
            # self.wfile.write('<body>Был получен POST-запрос.</body></html>'.encode('utf-8'))

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


