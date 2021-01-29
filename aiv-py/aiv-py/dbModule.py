import pymysql
from application_properties import info

class DataBase():
    def __init__(self):
        self.db = pymysql.connect(
                host= info['p_host'],
                user= info['p_user'],
                password= info['p_password'],
                database= info['p_database'],
                charset='utf8mb4',
        )

        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute_all(self, query, args=None):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        print(self.cursor._last_executed)
        return row

    def execute_one(self, query, args=None):
        self.cursor.execute(query, args)
        single = self.cursor.fetchone()
        print(self.cursor._last_executed)
        return single

    # only read. don't have to use commit on select.
    def commit(self):
        self.db.commit()



