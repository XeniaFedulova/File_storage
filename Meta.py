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
    # унаследовать от NamedTuple для более простого перечисления свойств
    id: str = ""
    name: str = ""
    tag: str = ""
    size: int = 0
    mimeType: str = ""
    modificationTime: str = ""

    def __init__(self, file_id: str = "", name: str = "", tag: str = "",
                 size: int = 0, content_type: str = ""):
        if file_id != "":
            self.file_id = self._generate_id()
        else:
            self.id = file_id
        if name == "":
            self.name = self.file_id
        else:
            self.name = name
        self.tag = tag
        self.size = size
        self.mimeType = content_type
        # self.modificationTime = modificationTime

    @string
    def _generate_id(self):
        file_id = uuid.uuid4()
        return file_id

    def return_meta_info(self):
        """делает JSON из полей класса"""
        data_dict = {}
        for attribute in self.__annotations__:
            data_dict[attribute] = getattr(self, attribute)
        data_json = json.dumps(data_dict)
        return data_json

