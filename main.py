import datetime
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


def handle_params_from_req(params):
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
    response = []
    counter = 0
    for obj in data:
        params = {"id": obj[0],
                  "name": obj[1],
                  "tag": obj[2]}
        size = int(obj[3])
        mimeType = obj[4]
        modificationTime = obj[5]
        inf = MetaInf(params, size, mimeType, modificationTime)
        meta = inf.return_meta_info()
        response.append(meta)
        counter += 1

    data_json = json.dumps(response)
    return data_json


def set_modificationTime():
    time_format = "%Y-%m-%d %H:%M:%S"
    now = datetime.datetime.now().strftime(time_format)
    return now


def get_ids_of_delete_files(data_from_db: list):
    file_ids = []
    for obj in data_from_db:
        file_id = obj[0]
        file_ids.append(file_id)
    return file_ids

def delete_unexpected_params(expected_params, params: dict):
    for param in params.keys():
        if param not in expected_params:
            params.pop(param)


class RequestHandler(BaseHTTPRequestHandler):
    storage = DataStorage("File_storage")
    # storage.drop_data()
    directory = "C:\\Users\\user\\storage_files"
    expected_params = ["id", "name", "tag", "size", "mimeType"]


    def do_GET(self):

        def get():
            flag = False
            params = parse_qs(urlparse(self.path).query)
            if len(params) == 0:
                flag = True
            params = handle_params_from_req(params)
            delete_unexpected_params(self.expected_params, params)
            data = self.storage.get_from_database(params=params, get_all_data=flag)
            if len(data) == 0:
                flag = True
                data = self.storage.get_from_database(get_all_data=flag)
            meta = handle_info_from_db(data)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(meta.encode('utf-8'))

        def download():
            params = parse_qs(urlparse(self.path).query)
            params = handle_params_from_req(params)
            delete_unexpected_params(self.expected_params, params)
            try:
                param = {"id": params['id']}
                data = self.storage.get_from_database(param, download=True)
                if len(data) == 0:
                    self.send_error(404)
                for file in data:
                    file_id = file[0]
                    path = self.directory + "\\" + file_id
                    with open(path, 'rb') as f:
                        name = file[1]
                        self.send_response(200)
                        self.send_header("Content-Type", 'application/octet-stream')
                        self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(name))
                        fs = os.fstat(f.fileno())
                        self.send_header("Content-Length", str(fs.st_size))
                        self.end_headers()
                        self.wfile.write(f.read())
            except KeyError:
                self.send_error(400)

        end = urlparse(self.path).path
        if end == '/api/get':
            get()
        elif end == '/api/download':
            download()
        else:
            self.send_error(501)

    def do_POST(self):

        def upload():
            content_length = int(self.headers.get("Content-Length"))

            if content_length == None:
                self.send_error(411)
            params = parse_qs(urlparse(self.path).query)
            params = handle_params_for_upload(params)

            payload = self.rfile.read(content_length)
            modificationTime = set_modificationTime()
            content_type = self.headers.get_content_type()

            info = MetaInf(params, content_length, content_type, modificationTime)
            self.storage.load_to_database(info)
            file_id = info.id

            put_file_to_dir(self.directory, payload, filename=file_id)
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
            with open(os.path.join(self.directory, file_id), "wb") as f:
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
            self.send_error(501)

    def do_DELETE(self):

        def delete():
            params = parse_qs(urlparse(self.path).query)
            params = handle_params_from_req(params)
            delete_unexpected_params(self.expected_params, params)
            if len(params) == 0:
                self.send_error(400)
            else:
                data = self.storage.get_from_database(params)
                files_to_delete = get_ids_of_delete_files(data)

                for file_id in files_to_delete:
                    delete_path = self.directory + "\\" + file_id
                    os.remove(delete_path)

                amount_of_deleted_files = str(len(files_to_delete))
                if int(amount_of_deleted_files) > 0:
                    self.storage.delete_from_db(files_to_delete)
                message = amount_of_deleted_files + " files deleted"
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(message.encode('utf-8'))

        end = urlparse(self.path).path
        if end == '/api/delete':
            delete()
        else:
            self.send_error(501)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), RequestHandler)
    server.serve_forever()
