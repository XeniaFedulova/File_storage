import email.message
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import os
from Meta import MetaInf
from DB import DataStorage


def put_file_to_dir(directory, payload, filename: str = ""):
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, filename), "wb") as f:
        f.write(payload)


def handle_params(params):
    for param, value in params.items():
        if len(value) == 1:
            params[param] = "".join(value)
    return params


def handle_params_for_upload(params):
    for param, value in params.items():
        if len(value) > 1:
            params[param] = value[0]
        else:
            params[param] = "".join(value)
    return params


def handle_info_from_db(data: list):
    response = {}
    counter = 0
    for obj in data:
        file_id = obj[0]
        name = obj[1]
        tag = obj[2]
        size = obj[3]
        mimeType = obj[4]

        inf = MetaInf(file_id, name, tag, size, mimeType)
        meta = inf.return_meta_info()
        response[str(counter)] = meta
        counter += 1

    data_json = json.dumps(response)
    return data_json


class RequestHandler(BaseHTTPRequestHandler):
    storage = DataStorage("File_storage")

    def do_GET(self):

        def get():
            params = parse_qs(urlparse(self.path).query)
            params = handle_params(params)
            data = self.storage.get_from_database(params)
            meta = handle_info_from_db(data)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(meta.encode('utf-8'))

        end = urlparse(self.path).path
        if end == '/api/get':
            get()
        else:
            self.send_error(404)

    def do_POST(self):

        def upload():
            content_length = int(self.headers.get("Content-Length"))

            if content_length == None or content_length <= 0:
                self.send_error(411, message="No content")
                self.send_response(411)
            else:
                params = parse_qs(urlparse(self.path).query)
                params = handle_params_for_upload(params)
                file_id, name, tag = params["id"], params["name"], params["tag"]

                directory = "C:\\Users\\user\\storage_files"
                payload = self.rfile.read(content_length)
                content_type = self.headers.get_content_type()

                info = MetaInf(file_id, name, tag, content_length, content_type)
                self.storage.load_to_database(info)
                file_name = info.name

                put_file_to_dir(directory, payload, filename=file_name)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                with open(os.path.join(directory, file_name), "wb") as f:
                    f.write(payload)

                meta = info.return_meta_info()
                meta = json.dumps(meta)
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(meta.encode('utf-8'))

        end = urlparse(self.path).path
        if end == '/api/upload':
            upload()
        else:
            self.send_error(404)

    def do_DELETE(self):
        params = parse_qs(urlparse(self.path).query)
        print(params)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write('<html><head><meta charset="utf-8">'.encode('utf-8'))
        self.wfile.write('<title>Простой HTTP-сервер.</title></head>'.encode('utf-8'))

        pass


server = HTTPServer(("127.0.0.1", 8000), RequestHandler)
server.serve_forever()
