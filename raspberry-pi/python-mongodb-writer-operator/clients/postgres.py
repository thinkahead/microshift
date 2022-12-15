import psycopg2

class PostgresClient:
    def __init__(self, host, username, password, db):
        self.host = host
        self.username = username
        self.__password = password
        self.db = db
        self.__connection = None

    def connect_if_not_connected(self):
        if self.__connection is None:
            self.__connection = psycopg2.connect(database=self.db, user=self.username, password=self.__password, host=self.host)

    def get_connection(self):
        return self.__connection
    
    # define other getters/setters accordingly

    def insert_row(self, table, primary_id, name, age, country):
        self.connect_if_not_connected()
        db_connection = self.get_connection()
        # Idempotent insertions <3
        insert_query = """INSERT INTO {table_name} (id, name, age, country) VALUES ('{id}', '{name}', {age}, '{country}')  ON CONFLICT (id) DO NOTHING""".format(
            table_name=table, 
            id=primary_id, 
            name=name, 
            age=age, 
            country=country
        )

        # RIP exception handling :P
        with db_connection.cursor() as cursor:
            cursor.execute(insert_query)
            db_connection.commit()

    def delete_row(self, table, primary_id):
        self.connect_if_not_connected()
        db_connection = self.get_connection()
        delete_query = """DELETE FROM {table_name} WHERE id='{id}'""".format(
            table_name=table, 
            id=primary_id
        )
        # RIP exception handling :P
        with db_connection.cursor() as cursor:
            cursor.execute(delete_query)
            db_connection.commit()