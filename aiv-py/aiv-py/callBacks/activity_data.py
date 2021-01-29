from dbModule import DataBase


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