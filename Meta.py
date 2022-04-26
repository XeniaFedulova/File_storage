import json
import random
import uuid
from DB import DataStorage
import os
import datetime


class MetaInf():
    payload = None

    id = None
    name: str = 'name'
    tag: str = 'tag'
    size: int = None
    mimeType: str = None
    modificationTime: str = ""

    def __init__(self, params, payload, content_type):
        self.id = self._generate_id()
        self._set_params(params, required_params=[self.name, self.tag])

        self.payload = payload
        self.size = self._file_size(payload)

        self.mimeType = content_type
        # self.modificationTime = datetime()

    def _generate_id(self):
        file_id = uuid.uuid4()
        return file_id

    def _file_size(self, payload):
        stat = os.stat(payload)
        size = stat.st_size
        return size

    def return_meta_info(self):
        """делает JSON из полей класса"""
        data_dict = {}
        for attribute in dir(self):
            data_dict[attribute] = getattr(self, attribute)
        data_str = str(data_dict)
        data_json = json.loads(data_str)
        return data_json

    def _set_params(self, params, required_params):
        for param in params.keys():
            params[param] = "".join(params[param])
        for req_param in required_params:
            if req_param in params.keys():
                req_param = params[req_param]
            else:
                req_param = ""


