import pymysql
from sql_module.db_conf import db_connection

cursor = db_connection.cursor(pymysql.cursors.DictCursor)

# admin 즐겨 찾기를 위한 admin id
admin_id = 1
# 최소 터치 기준 5회 이상
act_standard = 5

# 시작일자 - 행동일자
act_start = '2020-11-02'
act_end = '2020-11-05'

# 제외할 활동
no_count = ['WALK', 'WAKE_UP', 'NO_KITCHEN', 'NO_TOILET', 'NO_TOUCH', 'NO_MOVEMENT', 'NO_WAKE_UP', 'NO_RETURN']

# admin 즐겨찾기 사용자 id 배열
admin_fav_id = []


# admin의 즐겨찾기 사용자 id를 가져오는 쿼리
admin_fav_query = "SELECT owner_id " + \
                    "FROM admin_favorite f INNER JOIN xc_user u ON f.owner_id = u.user_id " + \
                    "WHERE admin_id = " + str(admin_id)
cursor.execute(admin_fav_query)


for single in cursor.fetchall():
    admin_fav_id.append(str(single['owner_id']))

str_admin_fav = ','.join(admin_fav_id)

# 즐겨 찾기 유저의 행동 데이터를 가져오는 쿼리
tag_memory_query = 'SELECT x.owner_id, x.act_type ' + \
                   'FROM xc_activity x ' + \
                   'WHERE x.owner_id IN (' + str_admin_fav + \
                    ') AND x.act_date >= \'' + act_start + \
                    '\' AND x.act_date <=  \'' + act_end + '\''


cursor.execute(tag_memory_query)
tag_result = cursor.fetchall()

tag_result_map = {}

# 조건에 맞게 태그 데이터 파싱
for single in tag_result:
    if single['act_type'] in no_count:
        continue
    if single['owner_id'] in tag_result_map:
        tag_result_map[single['owner_id']] += 1
    else:
        tag_result_map[single['owner_id']] = 1

no_act_candidate = []

for key in tag_result_map.keys():
    if tag_result_map[key] <= act_standard:
        no_act_candidate.append(key)

print(no_act_candidate)
