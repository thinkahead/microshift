import pprint
from pymongo import MongoClient

class MongoDBClient:
    def __init__(self, host, username, password, db, port=27017):
        self.host = host
        self.username = username
        self.__password = password
        self.db = db
        self.__connection = None
        self.port = port

    def connect_if_not_connected(self):
        if self.__connection is None:
            self.__connection = MongoClient(f"mongodb://{self.username}:{self.__password}@{self.host}:{self.port}")[self.db]

    def get_connection(self):
        return self.__connection
    
    # define other getters/setters accordingly

    def insert_row(self, table, primary_id, name, age, country):
        self.connect_if_not_connected()
        db_connection = self.get_connection()
        student={"id":primary_id,"name":name,"age":age,"country":country}
        db_connection[table].insert_one(student)

    def delete_row(self, table, primary_id):
        self.connect_if_not_connected()
        db_connection = self.get_connection()
        db_connection[table].delete_one({"id":primary_id})
