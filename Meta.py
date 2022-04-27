import json
import uuid
import os
import datetime
import tempfile


def string(func: callable):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        result = str(result)
        return result

    return wrapper


class MetaInf:
    #унаследовать от NamedTuple для более простого перечисления свойств
    id: str = None
    name: str = 'name'
    tag: str = 'tag'
    size: str = None
    mimeType: str = None
    modificationTime: str = ""

    def __init__(self, params, payload, content_type):
        self.id = self._generate_id()
        self._set_params(params, required_params=[self.name, self.tag])
        self.size = self._file_size(payload)
        self.mimeType = content_type
        # self.modificationTime = datetime()

    @string
    def _generate_id(self):
        file_id = uuid.uuid4()
        return file_id

    @string
    def _file_size(self, payload):
        file = tempfile.NamedTemporaryFile("wb")
        file.write(payload)
        stat = os.stat(file.name)
        size = stat.st_size
        return size

    def return_meta_info(self):
        """делает JSON из полей класса"""
        data_dict = {}
        for attribute in self.__annotations__:
            data_dict[attribute] = getattr(self, attribute)
        data_json = json.dumps(data_dict)
        return data_json

    def _set_params(self, params, required_params):
        for param in params.keys():
            params[param] = "".join(params[param])
        for req_param in required_params:
            if req_param in params.keys():
                req_param = params[req_param]
            else:
                req_param = ""
