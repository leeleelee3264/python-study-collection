from dbModule import DataBase
import pandas as pd
import datetime


db = DataBase()

def activity_data(userIdStr, startDate, endDate, actType, weeks, legend, limit):

    qeruy = '''
            SELECT owner_id, act_type, act_date, weekday, start_time, end_time
            FROM xc_activity
            WHERE owner_id IN (%s) 
            AND act_date >= %s AND act_date <= %s
            AND weekday in %s AND act_type = %s
        '''

    dbResult = db.execute_all(qeruy, (userIdStr, startDate, endDate, weeks, actType))
    return dbResult


def act_duration(userId, actType, startDate, endDate):

    query = '''
            SELECT act_date, start_time, end_time
            FROM xc_activity 
            WHERE owner_id = %s
            AND act_type = %s AND end_time IS NOT NULL 
            AND (act_date BETWEEN %s AND %s)
    '''

    dbResult = db.execute_all(query, (userId, actType, startDate, endDate))

    for single in dbResult:
        duration_sec = single['end_time'] - single['start_time']
        single['duration'] = duration_sec

    return pd.DataFrame(dbResult)