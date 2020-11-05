import pymysql

db_connection = pymysql.connect(
    user='root',
    passwd='1234',
    host='127.0.0.1',
    db='example',
    charset='utf8'
)
