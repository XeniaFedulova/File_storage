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

    def _create_database(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS file_storage(
            id TEXT,
            name TEXT,
            tag TEXT,
            size TEXT,
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

    def get_from_database(self, name):
        self.cursor.execute("SELECT * FROM file_storage where name == \'%s\'"
                            % (name)
                            )
        data = self.cursor.fetchall()
        return data

    # def drop_data(self):
    #     self.cursor.execute("DELETE FROM file_storage")
    #     self.connection.commit()
