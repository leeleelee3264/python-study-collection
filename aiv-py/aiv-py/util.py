# util function
from datetime import date, timedelta


class Util:

    def __init__(self):
        pass

    @classmethod
    def get_previous_month_with_last_date(cls, target_date: date):
        return target_date.replace(day=1) - timedelta(1)



