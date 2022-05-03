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

    def _make_req_string(self, params):
        sql = """SELECT * FROM file_storage WHERE"""
        for key, value in params.items():
            if type(value) == list:
                sql += " ("
                for item in value:
                    string = " " + key + "==" + "\"" + item + "\"" + " OR"
                    sql += string
                sql = sql.strip(" OR")
                sql += ") AND"
            else:
                string = " " + key + "==" + "\"" + value + "\"" + " AND"
                sql += string
        sql = sql.strip(" AND")
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
        print(data.tag)
        self.connection.commit()

    def get_from_database(self, params: dict):

        req_string = self._make_req_string(params)
        self.cursor.execute(req_string)
        data = self.cursor.fetchall()

        return data

    def drop_data(self):
        self.cursor.execute("DELETE FROM file_storage")
        self.connection.commit()
