from unittest.case import TestCase
from connector import FileStorageConnector
import urllib.error
from Meta import MetaInf


class EmptyStorageCase(TestCase):
    connector = FileStorageConnector("http://127.0.0.1:8000")

    """набор тестов для определенного состояния приложения"""

    def setUpClass(cls) -> None:
        cls.connector = FileStorageConnector("http://127.0.0.1:8000")

    def tearDown(self) -> None:
        result = self.connector.get()
        for json in result:
            self.connector.delete({id: json["id"]})

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

    def upload_file_by_name(self):
        meta = MetaInf(params={"name": ["file_name"]}, payload="My text", content_type="txt")
        result = self.connector.upload(payload="My text", meta=meta)

        res_json = result[0]
        res_status = result[1]

        self.assertEqual(type(res_json), dict)
        self.assertEqual(res_status, 200)
        self.assertEqual(res_json["name"], "file_name")
        self.assertEqual(res_json["tag"], "")
        self.assertEqual(res_json["size"], meta.size)
        self.assertEqual(res_json["mimeType"], "txt")
        self.assertEqual(res_json["modificationTime"], "")

    def upload_file_by_id(self):
        meta = MetaInf(params={"id": ["0"]}, payload="My text", content_type="txt")
        result = self.connector.upload(payload="My text", meta=meta)

        res_json = result[0]
        res_status = result[1]

        self.assertEqual(type(res_json), dict)
        self.assertEqual(res_status, 200)
        self.assertEqual(res_json["id"], "0")
        self.assertEqual(res_json["name"], "file_name")
        self.assertEqual(res_json["tag"], "")
        self.assertEqual(res_json["size"], meta.size)
        self.assertEqual(res_json["mimeType"], "txt")
        self.assertEqual(res_json["modificationTime"], "")

    def delete_file_by_id(self):
        result = self.connector.delete({"id": "0"})
        with self.assertRaises(urllib.error.HTTPError):
            result = self.connector.delete({"id": "0"})
            error = result.urllib.error.HTTPError.status
        self.assertEqual(error, 400)

    def delete_file_by_name(self):
        with self.assertRaises(urllib.error.HTTPError):
            result = self.connector.delete({"name": "file_name"})
            error = result.urllib.error.HTTPError.status
        self.assertEqual(error, 400)

    def delete_file_without_params(self):
        with self.assertRaises(urllib.error.HTTPError):
            result = self.connector.delete({"id": "0"})
            error = result.urllib.error.HTTPError.status
        self.assertEqual(error, 400)


class SingleFileDtorageCase(TestCase):
    pass