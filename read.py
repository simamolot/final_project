from db_connector import get_read_connection


class Search:
    def __init__(self, value):

        self.value = value
        self.connection = get_read_connection()
        self.cursor = self.connection.cursor()

    def execute_search(self, field, limit):
        query = f"""
        SELECT 
            subquery.title, 
            subquery.description, 
            subquery.release_year, 
            subquery.category, 
            subquery.first_name, 
            subquery.last_name
        FROM (
            SELECT 
                t1.title, 
                t1.description, 
                t1.release_year, 
                t3.name AS category, 
                t5.first_name, 
                t5.last_name,
                DENSE_RANK() OVER (PARTITION BY t1.film_id ORDER BY t1.film_id) AS rnk
            FROM film AS t1
            LEFT JOIN film_category AS t2 ON t1.film_id = t2.film_id
            LEFT JOIN category AS t3 ON t3.category_id = t2.category_id
            LEFT JOIN film_actor AS t4 ON t1.film_id = t4.film_id
            LEFT JOIN actor AS t5 ON t4.actor_id = t5.actor_id
            WHERE {field} LIKE '%{self.value}%'
        ) AS subquery
        WHERE subquery.rnk = 1
        LIMIT {limit};
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()



class Title(Search):
    def execute_search(self):
        return super().execute_search('t1.title', 10)


class Actor(Search):
    def execute_search(self):
        return super().execute_search("CONCAT(t5.first_name, ' ', t5.last_name)",5)


class Category(Search):
    def execute_search(self):
        return super().execute_search('t3.name', 10)


class Year(Search):
    def execute_search(self):
        return super().execute_search('t1.release_year', 10)


class Description(Search):
    def execute_search(self):
        return super().execute_search('t1.description', 10)
