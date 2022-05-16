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
        response_message = response.reason
        status_code = response.status_code
        response_status = {
            "body": response.content.decode("utf-8"),
            "status_code": status_code,
            "message": response_message
        }
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
        response = self._upload(params=params, data=payload,
                                headers={"Content-Type": content_type, "Content-Length": size})
        response_meta = json.loads(response["body"])
        response["body"] = response_meta
        return response

    def get(self, params=None):
        response = self._get(params=params)
        response_meta = json.loads(response["body"])
        response["body"] = response_meta
        return response

    def download(self, params):
        response = self._download(params=params)
        return response

    def delete(self, params):
        response = self._delete(params=params)
        return response

    def any_endpoint(self, base_url, endpoint):
        prepare_request(base_url, endpoint)

# payload = "kdkd".encode("utf-8")
# a = MetaInf(params={"id": "0"}, size=8, content_type="application/json")
# b = FileStorageConnector(base_url='http://127.0.0.1:8000')
# a = b.upload(payload, a)
#
# print(b.download({"id": "0"}))
