from db_connector import get_write_connection


class Counter:
    def __init__(self, query):
        self.query = query
        self.connection = get_write_connection()
        self.cursor = self.connection.cursor()

    def insert_or_update(self):
        self.cursor.execute("SELECT * FROM query_results WHERE query = %s;", (self.query,))
        result = self.cursor.fetchone()

        if result:
            self.cursor.execute("UPDATE query_results SET count = %s WHERE id = %s",
                                (result[2] + 1, result[0]))
        else:
            self.cursor.execute("INSERT INTO query_results (query, count) VALUES (%s, %s)",
                                (self.query, 1))
        self.connection.commit()

    def top_result(self):
        self.cursor.execute("SELECT query, count FROM query_results ORDER BY count DESC LIMIT 10;")
        return self.cursor.fetchall()

    def close(self):
       if self.cursor:
        self.cursor.close()
        if self.connection:
            self.connection.close()
