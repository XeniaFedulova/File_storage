import uuid
import datetime


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
    modificationTime: datetime = None


    def __init__(self, params: dict = None,
                 size: int = 0, content_type: str = "", modificationTime: datetime = None):

        if "id" in params.keys():
            self.id = params["id"]
        else:
            self.file_id = self._generate_id()
        if "name" in params.keys():
            self.name = params["name"]
        else:
            self.name = self.id
        if "tag" in params.keys():
            self.name = params["tag"]

        self.size = size
        self.mimeType = content_type
        self.modificationTime = modificationTime

    @string
    def _generate_id(self):
        file_id = uuid.uuid4()
        return file_id

    def return_meta_info(self):
        """делает JSON из полей класса"""
        data_dict = {}
        for attribute in self.__annotations__:
            data_dict[attribute] = getattr(self, attribute)
        return data_dict

