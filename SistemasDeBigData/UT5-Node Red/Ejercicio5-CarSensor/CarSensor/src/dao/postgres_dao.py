import psycopg2

class PostgresDao:
    def __init__(self, hostname, database, user, password, port=5432):
        self.__connection = psycopg2.connect(
                        host=hostname,
                        user=user,
                        password=password,
                        port=port,
                        database=database)

    
    def close(self):
        self.__connection.close()

    
    def find_all(self, table):
        cursor = self.__connection.cursor()
        cursor.execute(f'select * from {table}')
        return cursor.fetchall()
    
    def insert(self, sql, values: set):
        self.__connection.cursor().execute(sql, values)
        self.__connection.commit()
