import re

from django.db import models

from common.util import mysql_aes_str
from device.models.swatch_base import SwatchBase


class SwatchUserInfo(SwatchBase):
    id = models.AutoField(primary_key=True, db_column='user_id')
    phone_no = models.CharField(max_length=20, null=False, unique=True)
    name = models.CharField(max_length=20, null=True)
    password = models.BinaryField(max_length=100, null=False, db_column='password_enc')
    session_key = models.CharField(null=False, max_length=100)

    app_lang = models.CharField(max_length=2, null=False)
    app_os_type = models.CharField(max_length=1, null=False)
    gcm_id = models.CharField(max_length=4096)

    is_admin = models.BooleanField(null=False)

    last_login = models.DateTimeField(null=True, db_column='last_login_time')

    is_authenticated = True

    class Meta:
        db_table = 't_swatch_user_info'
        managed = False

    def has_gcm_token(self):
        return self.gcm_id is not None and len(self.gcm_id) > 0

    def get_password(self):
        return mysql_aes_str(self.password, self.DB_KEY)

    def get_normalized_phone_no(self):
        if not 10 <= len(self.phone_no) <= 11:
           return self.phone_no


        return f'{self.phone_no[:3]}-{self.phone_no[3:-4]}-{self.phone_no[-4:]}'

    def is_android(self):
        return self.app_os_type == 'A'
