import sqlite3

'''
Класс для работы с СУБД
Методы соединения с БД, отключения от нее
Получение курсора и коммита
'''


class DBConnection:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, db_name):
        self.__connection = self.connect(db_name)

    def connect(self, db_name):
        self.__connection = sqlite3.connect(db_name)
        return self.__connection

    def query(self, query, params=None):
        try:
            cursor = self.__connection.cursor()
            cursor.execute(query, params)
            self.__connection.commit()
            result = cursor.fetchall()
            cursor.close()
            return True, result
        except sqlite3.Error as er:
            self.__connection.rollback()
            return False, er.args

    def get_connection(self):
        return self.__connection
