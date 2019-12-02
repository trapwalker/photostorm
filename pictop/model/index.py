
import sqlite3


class Index:
    def __init__(self, filename=':memory:'):
        self.filename = filename
        self.db = sqlite3.connect(self.filename)

    def close(self):
        self.db.close()

    def find(self, photo):
        cursor = self.db.cursor()
        try:
            cursor.execute("""
                SELECT 
            """)
        finally:
            cursor.close()

    def find_all(self, photo):
        raise NotImplementedError


class IndexGroup:
    def __init__(self, *items: Index):
        self.items = items

    def __iter__(self):
        return iter(self.items)

    def find(self, photo):
        for item in self:
            result = item.find(photo)
            if result:
                return result

    def find_all(self, photo):
        results = []
        for item in self:
            results.extend(item.find_all(photo))

        return results
