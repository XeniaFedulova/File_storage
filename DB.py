import sqlite3


class DataStorage:
    data_base_name = None
    connection = None
    cursor = None

    def __init__(self, data_base_name: str):
        self.data_base_name = data_base_name
        self.connection = sqlite3.connect(data_base_name)
        self.cursor = self.connection.cursor()
        self._create_database()

    def _make_req_string(self, base_string, params):
        for key, value in params.items():
            if type(value) == list:
                if len(params) > 1:
                    base_string += " ("
                for item in value:
                    string = " " + key + "==" + "\"" + item + "\"" + " OR"
                    base_string += string
                base_string = base_string.strip(" OR")
                if len(params) > 1:
                    base_string += ") AND"
                else:
                    sql = base_string.strip(" OR")
            else:
                string = " " + key + "==" + "\"" + value + "\"" + " AND"
                base_string += string
        if base_string.startswith("SELECT"):
            sql = base_string.strip(" AND")
        return sql

    def _create_database(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS file_storage(
            id TEXT,
            name TEXT,
            tag TEXT,
            size INTEGER,
            mimeType TEXT,
            modificationTime TEXT,
            UNIQUE(id));
            """)

        self.connection.commit()

    def load_to_database(self, data):
        self.cursor.execute(
            "INSERT OR IGNORE INTO file_storage(id, name, tag, size, mimeType, modificationTime) VALUES (?, ?, ?, ?, ?, ?)",
            (data.id, data.name, data.tag, data.size, data.mimeType, data.modificationTime)
        )
        self.connection.commit()

    def get_from_database(self, params: dict = None, get_all_data: bool = False, download:bool = False):
        if get_all_data:
            req_string = "SELECT * FROM file_storage"
        else:
            if download:
                base_string = """SELECT id, name FROM file_storage WHERE"""
            else:
                base_string = """SELECT * FROM file_storage WHERE"""
            req_string = self._make_req_string(base_string, params)
        self.cursor.execute(req_string)
        data = self.cursor.fetchall()
        print(data)
        return data

    def delete_from_db(self, file_ids: dict):
        base_string = "DELETE FROM file_storage WHERE"
        req_string = self._make_req_string(base_string, file_ids)
        self.cursor.execute(req_string)
        self.connection.commit()

    def drop_data(self):
        self.cursor.execute("DELETE FROM file_storage")
        self.connection.commit()
