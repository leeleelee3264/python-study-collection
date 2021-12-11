from django.db import models
from django.utils import timezone

from common.util import mysql_aes_float
from device.models.swatch_base import SwatchBase
from device.models.swatch_user_info import SwatchUserInfo


class SwatchDeviceInfo(SwatchBase):
    TRACE_TYPE_NONE = 'N'

    deveui = models.CharField(primary_key=True, null=False, max_length=16, db_column='deveui')
    appeui = models.CharField(null=False, max_length=16)
    power_yn = models.CharField(null=False, max_length=1)

    trace_id = models.IntegerField(null=False, db_column='trace_id')
    trace_type = models.CharField(null=False, max_length=1, db_column='trace_yn')
    trace_req_user_id = models.IntegerField(null=False, default=0)

    fw_ver = models.CharField(max_length=20)
    fw_mode = models.IntegerField()
    lora_period_min = models.IntegerField()
    battery_level = models.IntegerField(null=True, db_column='battery_level')

    latitude = models.BinaryField(null=True, db_column='latitude_enc')
    longitude = models.BinaryField(null=True, db_column='longitude_enc')
    height = models.FloatField(default=0)

    gw_latitude = models.BinaryField(null=True, db_column='gw_latitude_enc')
    gw_longitude = models.BinaryField(null=True, db_column='gw_longitude_enc')

    last_location_time = models.DateTimeField()
    last_uplink_time = models.DateTimeField()
    begin_date = models.DateField()
    expire_date = models.DateField()

    # owner = models.ForeignKey(SwatchUserInfo, null=True, on_delete=models.DO_NOTHING, to_field='id', db_column='owner_id')
    owner_id = models.IntegerField(null=False, default=0)
    owner_latitude = models.FloatField(default=0)
    owner_longitude = models.FloatField(default=0)
    owner_height = models.FloatField(default=0)
    owner_location_time = models.DateTimeField(null=True)

    create_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, auto_now=True)

    class Meta:
        db_table = 't_swatch_device_info'
        managed = False

    def delete(self, *args, **kwargs):
        return

    def get_recent_level(self):
        """
        최근 시간에 따른 레벨 값 계산

        :return: -1: 미개통, 0: 1주일, 1: 1~2주일, 2: 2주~1달, 3: 1달 초과
        """
        if self.create_time is None or self.last_uplink_time is None:
            return -1

        now = timezone.now()

        delta = now - self.last_uplink_time
        if delta.days < 7:
            return 0
        elif delta.days < 14:
            return 1
        elif delta.days < 30:
            return 2
        else:
            return 3

    def get_latitude(self):
        return 0.0 if self.latitude is None else mysql_aes_float(self.latitude, self.DB_KEY)

    def get_longitude(self):
        return 0.0 if self.longitude is None else mysql_aes_float(self.longitude, self.DB_KEY)

    def get_gw_latitude(self):
        return 0.0 if self.gw_latitude is None else mysql_aes_float(self.gw_latitude, self.DB_KEY)

    def get_gw_longitude(self):
        return 0.0 if self.gw_longitude is None else mysql_aes_float(self.gw_longitude, self.DB_KEY)

    def get_last_location_time(self):
        return 0 if self.last_location_time is None else int(self.last_location_time.timestamp())

    def get_last_uplink_time(self):
        return 0 if self.last_uplink_time is None else int(self.last_uplink_time.timestamp())

    def is_valid(self):
        today = timezone.datetime.now().date()

        return self.expire_date >= today

    def is_sleep(self):
        return self.power_yn == 'N' and self.battery_level >= 10

    def is_poweroff(self):
        return self.power_yn == 'N' and self.battery_level < 10


class SwatchDeviceExtendHistory(models.Model):
    id = models.AutoField(primary_key=True)

    deveui = models.CharField(null=False, max_length=16, db_column='deveui')
    is_extend = models.BooleanField(null=False)
    days = models.SmallIntegerField(null=False)
    prev_expire_date = models.DateField(null=True)
    expire_date = models.DateField(null=False)

    # create_time = models.DateTimeField(null=False, auto_now_add=True)

    class Meta:
        db_table = 't_swatch_device_extend_hist'
        managed = False


class SwatchDeviceDelivery(models.Model):
    STATUS_HOME = 0
    STATUS_DELIVER = 1
    STATUS_REGISTER = 2

    id = models.AutoField(primary_key=True)

    device = models.ForeignKey(SwatchDeviceInfo, on_delete=models.CASCADE, db_column='deveui')
    status = models.SmallIntegerField(null=False, default=False)
    days = models.IntegerField(null=False)
    start_date = models.DateField(null=True)
    create_time = models.DateTimeField(null=False, auto_now_add=True)

    class Meta:
        db_table = 't_swatch_device_delivery'
        managed = False
