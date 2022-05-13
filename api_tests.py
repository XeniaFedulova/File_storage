from main import set_modificationTime
from unittest.case import TestCase
from connector import FileStorageConnector
import requests
from Meta import MetaInf


class EmptyStorageCase(TestCase):
    connector = FileStorageConnector("http://127.0.0.1:8000")

    """тесты для пустой базы данных"""

    def setUp(self) -> None:
        self.connector = FileStorageConnector("http://127.0.0.1:8000")
        result = self.connector.get()
        result = result[0]
        for json in result:
            file_id = json["id"]
            self.connector.delete({'id': file_id})

    def tearDown(self) -> None:
        result = self.connector.get()
        result = result[0]
        for json in result:
            file_id = json["id"]
            self.connector.delete({'id': file_id})

    def test_empty_get_without_params(self):
        result = self.connector.get()
        self.assertEqual(result, ([], 200))

    def test_empty_get_by_id(self):
        result = self.connector.get({"id": "0"})
        self.assertEqual(result, ([], 200))

    def test_empty_get_by_name(self):
        result = self.connector.get({"name": "name"})
        self.assertEqual(result, ([], 200))

    def test_empty_get_by_name_and_id(self):
        result = self.connector.get({"id": "0", "name": "name"})
        self.assertEqual(result, ([], 200))

    def test_upload_file_by_name(self):
        payload = "My text".encode("utf-8")
        size = len(payload)
        meta = MetaInf(params={"name": "my_file_name"}, size=size, content_type="text/plain")
        result = self.connector.upload(payload="My text", meta=meta)
        file_id = meta.id
        time = set_modificationTime()

        expected = {
            "id": file_id,
            "name": "my_file_name",
            "tag": "",
            "size": meta.size,
            "mimeType": "text/plain",
            "modificationTime": time
        }
        self.assertEqual(result, (expected, 201))

    def test_upload_file_by_id(self):
        payload = "My text".encode("utf-8")
        size = len(payload)
        meta = MetaInf(params={"id": "my_file_id"}, size=size, content_type="text/plain")
        result = self.connector.upload(payload="My text", meta=meta)
        time = set_modificationTime()

        expected = {
            "id": "my_file_id",
            "name": "my_file_id",
            "tag": "",
            "size": meta.size,
            "mimeType": "text/plain",
            "modificationTime": time
        }
        self.assertEqual(result, (expected, 201))

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

    def test_download_file_by_id(self):
        with self.assertRaises(requests.exceptions.HTTPError) as excep:
            self.connector.download({"id": "some_id"})
        error = excep.exception.response.status_code
        self.assertEqual(error, 404)

    def test_download_file_without_id(self):
        with self.assertRaises(requests.exceptions.HTTPError) as excep:
            self.connector.download({})
        error = excep.exception.response.status_code
        self.assertEqual(error, 400)


class StorageWithOneFile(TestCase):
    connector = FileStorageConnector("http://127.0.0.1:8000")
    time = set_modificationTime()
    default_file_data = {
        "id": "def_id",
        "name": "def_name",
        "tag": "def_tag",
        "size": 12,
        "mimeType": "application/json",
        "modificationTime": time
    }

    """тесты для базы данных с одним файлом"""

    def setUp(self) -> None:
        self.connector = FileStorageConnector("http://127.0.0.1:8000")
        payload = "default_file".encode("utf-8")
        meta = MetaInf(params={"id": "def_id", "name": "def_name", "tag": "def_tag"}, size=12,
                       content_type="application/json")
        self.time = set_modificationTime()
        self.connector.upload(payload, meta)

    def tearDown(self) -> None:
        result = self.connector.get()
        result = result[0]
        for json in result:
            file_id = json["id"]
            self.connector.delete({'id': file_id})
        print("delete")

    def test_get_without_params(self):
        result = self.connector.get({})
        self.assertEqual(result, ([self.default_file_data], 200))

    def test_get_default_file_by_id(self):
        result = self.connector.get({"id": "def_id"})
        self.assertEqual(result, ([self.default_file_data], 200))

    def test_get_default_file_by_name(self):
        result = self.connector.get({"name": "def_name"})
        self.assertEqual(result, ([self.default_file_data], 200))

    def test_default_get_file_by_tag(self):
        result = self.connector.get({"name": "def_tag"})
        self.assertEqual(result, ([self.default_file_data], 200))

    def test_upload_file_by_name(self):
        payload = "My text".encode("utf-8")
        size = len(payload)
        meta = MetaInf(params={"name": "my_file_name"}, size=size, content_type="text/plain")
        file_id = meta.id
        result = self.connector.upload(payload="My text", meta=meta)
        time = set_modificationTime()

        expected = {
            "id": file_id,
            "name": "my_file_name",
            "tag": "",
            "size": meta.size,
            "mimeType": "text/plain",
            "modificationTime": time
        }
        self.assertEqual(result, (expected, 201))

    def test_upload_file_by_id(self):
        payload = "My text".encode("utf-8")
        size = len(payload)
        meta = MetaInf(params={"id": "my_file_id"}, size=size, content_type="text/plain")
        result = self.connector.upload(payload="My text", meta=meta)
        time = set_modificationTime()

        expected = {
            "id": "my_file_id",
            "name": "my_file_id",
            "tag": "",
            "size": meta.size,
            "mimeType": "text/plain",
            "modificationTime": time
        }
        self.assertEqual(result, (expected, 201))

    def test_upload_file_with_default_id(self):
        """перезапись файла при попытке загрузить файл с имеющимся в безе id"""

        payload = "New text".encode("utf-8")
        size = len(payload)
        meta = MetaInf(params={"id": "def_id"}, size=size, content_type="text/plain")
        result = self.connector.upload(payload="New text", meta=meta)
        time = set_modificationTime()

        res_json = result[0]
        expected = {
            "id": "def_id",
            "name": "def_id",
            "tag": "",
            "size": meta.size,
            "mimeType": "text/plain",
            "modificationTime": time
        }
        self.assertEqual(result, (expected, 201))

        result = self.connector.get({"id": "def_id"})
        self.assertEqual(result, ([res_json], 200))

    def test_delete_def_file_by_id(self):
        result = self.connector.delete({"id": "def_id"})
        self.assertEqual(("", 200, "1 files deleted"), result)

    def test_delete_def_file_by_name(self):
        result = self.connector.delete({"name": "def_name"})
        self.assertEqual(("", 200, "1 files deleted"), result)

    def test_delete_file_without_params(self):
        with self.assertRaises(requests.exceptions.HTTPError) as excep:
            self.connector.delete({})
        error = excep.exception.response.status_code
        self.assertEqual(error, 400)

    def test_delete_not_found_file(self):
        result = self.connector.delete({"name": "some_name"})
        self.assertEqual(("", 200, "0 files deleted"), result)

    def test_download_def_file_by_id(self):
        """скачивание исходного файла, добавить проверку на скачивание в директорию"""
        result = self.connector.download({"id": "def_id"})
        self.assertEqual(result, ("", 200, "default_file"))

    def test_download_def_file_by_name(self):
        with self.assertRaises(requests.exceptions.HTTPError) as excep:
            self.connector.download({"name": "def_name"})
        error = excep.exception.response.status_code
        self.assertEqual(error, 400)

    def test_download_def_file_without_params(self):
        with self.assertRaises(requests.exceptions.HTTPError) as excep:
            self.connector.download({})
        error = excep.exception.response.status_code
        self.assertEqual(error, 400)


class ManyFilesStorageCase(TestCase):
    connector = FileStorageConnector("http://127.0.0.1:8000")
    file_ids = [str(i) for i in range(0, 10)]
    file_names = ["test_name_" + str(digit) for digit in range(0, 10)]
    payloads = ["test_payload" + str(digit) for digit in range(0, 10)]
    times = []

    """тесты для базы данных с несколькими файлами (10)"""

    def setUp(self) -> None:
        self.connector = FileStorageConnector("http://127.0.0.1:8000")

        for file in range(10):
            payload = self.payloads[file]
            if file % 2 == 0:
                tag = "even"
            else:
                tag = "odd"
            file_to_upload = {
                "id": self.file_ids[file],
                "name": self.file_names[file],
                "tag": tag,
            }
            meta = MetaInf(params=file_to_upload, size=len(payload),
                           content_type="text/plain")
            self.connector.upload(payload, meta)
            self.times.append(set_modificationTime())

    def tearDown(self) -> None:
        result = self.connector.get()
        result = result[0]
        for json in result:
            file_id = json["id"]
            self.connector.delete({'id': file_id})
        print("delete")

    def test_get_one_def_file_by_id(self):
        result = self.connector.get({"id": "1"})
        expected = {
            "id": self.file_ids[1],
            "name": self.file_names[1],
            "tag": "odd",
            "size": len(self.payloads[1]),
            "mimeType": "text/plain",
            "modificationTime": self.times[1]
        }
        self.assertEqual(result, ([expected], 200))