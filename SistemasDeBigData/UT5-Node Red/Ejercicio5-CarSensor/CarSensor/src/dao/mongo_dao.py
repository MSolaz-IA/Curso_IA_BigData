from pymongo import MongoClient

class MongoDao:
    def __init__(self, hostname, database, user, password, port=27017):
        connection_string = f'mongodb://{user}:{password}@{hostname}:{port}'
        self.__connection = MongoClient(connection_string)
        self.__database = self.__connection.get_database(database)

    
    def close(self):
        self.__connection.close()

    def find(self, collection, filter = {}, projection = {}):
        collection_conn = self.__database.get_collection(collection)
        return [str(r) for r in collection_conn.find(filter, projection)]

    def find_one(self, collection, filter = {}, projection= {}):
        collection_conn = self.__database.get_collection(collection)
        return collection_conn.find_one(filter, projection)
    
    def inser_one(self, collection, record):
        collection_conn = self.__database.get_collection(collection)
        return collection_conn.insert_one(record)
    
    """ TODO: crear los metodos necesarios para realizar las llamadas a Mongo """
    
