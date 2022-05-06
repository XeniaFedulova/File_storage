import requests
import json
from Meta import MetaInf

upload = "/api/upload"
get = "/api/get"
delete = "/api/delete"
download = "/api/download"

endpoints = {
    upload: "post",
    get: "get",
    delete: "delete",
    download: "get"
}


def prepare_request(base_url: str, endpoint: str):
    url = base_url + endpoint
    method = endpoints[endpoint]

    def make_request(params=None, data=None, headers=None):
        response = requests.request(method=method, url=url, data=data, params=params, headers=headers)
        response.raise_for_status()
        status_code = response.status_code
        response_status = (response.content.decode("utf-8"), status_code)
        return response_status

    return make_request


class FileStorageConnector:

    def __init__(self, base_url: str):
        self._upload = prepare_request(base_url, upload)
        self._get = prepare_request(base_url, get)
        self._delete = prepare_request(base_url, delete)
        self._download = prepare_request(base_url, download)

    def upload(self, payload, meta: MetaInf):
        params = {"id": meta.id, "name": meta.name, "tag": meta.tag}
        content_type = meta.mimeType
        size = str(meta.size)
        response = self._upload(params=params, data=payload, headers={"Content-Type": content_type, "Content-Length": size})
        # content = json.loads(response[0])
        # status = response[1]
        # response_status = (content, status)
        # return response_status

    def get(self, params=None):
        response = self._get(params=params)
        response_meta = json.loads(response[0])
        status = response[1]
        response_and_status = (response_meta, status)
        return response_and_status

    def download(self, params):
        response = self._download(params=params)
        response = json.loads(response[0])
        status = response[1]
        response_status = (response, status)
        return response_status

    def delete(self, params):
        response = self._delete(params=params)
        print(response)
        response_data = response[0]
        status = response[1]
        response_and_status = (response_data, status)
        return response_and_status


payload = open("file_text", "rb")
payload = "kdkd".encode("utf-8")
a = MetaInf(params={"id": "gg"}, size=8, content_type="application/json")
b = FileStorageConnector(base_url='http://127.0.0.1:8000')
a = b.delete({"id": "0"})
print(a)
print(type(payload))
