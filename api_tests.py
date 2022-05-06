from main import set_modificationTime
from unittest.case import TestCase
from connector import FileStorageConnector
import requests
from Meta import MetaInf


class EmptyStorageCase(TestCase):
    connector = FileStorageConnector("http://127.0.0.1:8000")

    """тесты для пустой базы данных"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.connector = FileStorageConnector("http://127.0.0.1:8000")
        result = cls.connector.get()
        result = result[0]
        for key, value in result.items():
            file_id = value["id"]
            cls.connector.delete({'id': file_id})

    @classmethod
    def tearDown(self) -> None:
        result = self.connector.get()
        result = result[0]
        for key, value in result.items():
            file_id = value["id"]
            self.connector.delete({'id': file_id})

    def test_empty_get_without_params(self):
        result = self.connector.get()
        self.assertEqual(result, ({}, 200))

    def test_empty_get_by_id(self):
        result = self.connector.get({"id": "0"})
        self.assertEqual(result, ({}, 200))

    def test_empty_get_by_name(self):
        result = self.connector.get({"name": "name"})
        self.assertEqual(result, ({}, 200))

    def test_empty_get_by_name_and_id(self):
        result = self.connector.get({"id": "0", "name": "name"})
        self.assertEqual(result, ({}, 200))

    def test_upload_file_by_name(self):
        payload = "My text".encode("utf-8")
        size = len(payload)
        meta = MetaInf(params={"name": "my_file_name"}, size=size, content_type="text/plain")
        result = self.connector.upload(payload="My text", meta=meta)

        time = set_modificationTime()

        res_json = result[0]
        res_status = result[1]

        self.assertEqual(type(res_json), dict)
        self.assertEqual(res_status, 201)
        self.assertEqual(res_json["name"], "my_file_name")
        self.assertEqual(res_json["tag"], "")
        self.assertEqual(res_json["size"], meta.size)
        self.assertEqual(res_json["mimeType"], "text/plain")
        self.assertEqual(res_json["modificationTime"], time)

    def test_upload_file_by_id(self):
        payload = "My text".encode("utf-8")
        size = len(payload)
        meta = MetaInf(params={"id": "my_file_id"}, size=size, content_type="text/plain")
        result = self.connector.upload(payload="My text", meta=meta)

        time = set_modificationTime()

        res_json = result[0]
        res_status = result[1]

        self.assertEqual(type(res_json), dict)
        self.assertEqual(res_status, 201)
        self.assertEqual(res_json["id"], "my_file_id")
        self.assertEqual(res_json["name"], "my_file_id")
        self.assertEqual(res_json["tag"], "")
        self.assertEqual(res_json["size"], meta.size)
        self.assertEqual(res_json["mimeType"], "text/plain")
        self.assertEqual(res_json["modificationTime"], time)

    def test_delete_file_by_id(self):
        result = self.connector.delete({"id": "my_file_id"})
        self.assertEqual(("", 200, "0 files deleted"), result)

    def test_delete_file_by_name(self):
        result = self.connector.delete({"name": "my_file_name"})
        self.assertEqual(("", 200, "0 files deleted"), result)

    def test_delete_file_without_params(self):
        with self.assertRaises(requests.exceptions.HTTPError) as excep:
            self.connector.delete({})
        error = excep.exception.response.status_code
        self.assertEqual(error, 400)

class StorageWithOneFile(TestCase):
    connector = FileStorageConnector("http://127.0.0.1:8000")

    """тесты для базы данных с одним файлом"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.connector = FileStorageConnector("http://127.0.0.1:8000")
        result = cls.connector.get()
        result = result[0]
        for key, value in result.items():
            file_id = value["id"]
            cls.connector.delete({'id': file_id})

    @classmethod
    def tearDown(self) -> None:
        result = self.connector.get()
        result = result[0]
        for key, value in result.items():
            file_id = value["id"]
            self.connector.delete({'id': file_id})