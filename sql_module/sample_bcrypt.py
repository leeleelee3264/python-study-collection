# Project: sql
# Author: absin
# Date: 2021-07-02
# DESC: bcrypt 예시

import bcrypt
import pymysql
from sql_module.db_conf import db_connection



# db에서 어드민 정보를 가져옵니다
def get_admin():

    # 단순 디비에 접근해서 데이터를 불러오는 부분이라 이 부분은 신경 안 쓰셔도 되어요!
    cursor = db_connection.cursor(pymysql.cursors.DictCursor)

    get_admin_query = 'SELECT a.id, a.login_id, a.password ' \
                      'FROM admin_user a ' \
                      'WHERE a.login_id = \'seungmin\''

    cursor.execute(get_admin_query)
    raw_rst = cursor.fetchall()

    # {'id': 7, 'login_id': 'seungmin', 'password': '$2a$10$aIxQoCmQn8x3CSMU3TfrfeoKm3K9DVOIkcukST/GUcSV8qz92ezI.'} 딕셔너리 형태로 이 정보를 리턴합니다.
    return raw_rst[0]



# db에서 가져온 어드민 비밀번호와 사용자가 입력한 비밀번호가 동일한지 체크
def match_pw(plain, encrypted):
    encoded_plain = plain.encode('utf-8')
    encoded_encrypted = encrypted.encode('utf-8')
    return bcrypt.checkpw(encoded_plain, encoded_encrypted)




# 실행부분
my_admin = get_admin()
print(my_admin)
db_pw = my_admin['password']
my_pw = 'admin!@34'
my_false_pw = 'thisiswrongpassword'

# (1) 디비에 들어가있는 비밀번호는 이미 암호화가 되어있는 상태 (db_pw)
# (2) 사용자는 암호화가 되어있지 않은 my_pw 입력
# (3) 라이브러리 bcrypt 가 자신들만의 알고리즘을 가지고(어떤 방식인지는 우리도 모름) 암호화된 db_pw와 일반 텍스트인 my_pw가 원래는 동일한 비밀번호인지를 판별


# True 가 나와야 한다.
print(match_pw(my_pw, db_pw))

# False 가 나와야 한다
print(match_pw(my_false_pw, db_pw))