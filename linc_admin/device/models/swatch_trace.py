from django.db import models

from common.util import mysql_aes_float
from device.models.swatch_base import SwatchBase
from device.models.swatch_device import SwatchDeviceInfo
from device.models.swatch_user_info import SwatchUserInfo


class SwatchTraceHist(models.Model):
    trace_id = models.BigAutoField(primary_key=True)
    device = models.ForeignKey(SwatchDeviceInfo, on_delete=models.DO_NOTHING, db_column='deveui')
    trace_type = models.CharField(null=False, max_length=1,
                                  help_text='T: 안심귀가(사용않음), L: 위치요청, R: 경로추적, S: 세이프존, E: 긴급호출')

    create_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, auto_now=True)

    class Meta:
        db_table = 't_swatch_trace_hist'
        managed = False


class SwatchTraceDetail(SwatchBase):
    trace_detail_id = models.BigAutoField(primary_key=True)
    trace_id = models.ForeignKey(SwatchTraceHist, on_delete=models.CASCADE, db_column='trace_id')

    latitude = models.BinaryField(null=True, db_column='latitude_enc')
    longitude = models.BinaryField(null=True, db_column='longitude_enc')

    create_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, auto_now=True)

    class Meta:
        db_table = 't_swatch_trace_detail'
        managed = False

    def get_latitude(self):
        return 0.0 if self.latitude is None else mysql_aes_float(self.latitude, self.DB_KEY)

    def get_longitude(self):
        return 0.0 if self.longitude is None else mysql_aes_float(self.longitude, self.DB_KEY)


class SwatchTraceSummary(SwatchBase):
    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(SwatchDeviceInfo, on_delete=models.DO_NOTHING, db_column='deveui')

    class Meta:
        db_table = 't_swatch_trace_summary'
        managed = False


class SwatchLocationReservation(SwatchBase):
    reservation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(SwatchUserInfo, on_delete=models.CASCADE, db_column='user_id')
    device = models.ForeignKey(SwatchDeviceInfo, on_delete=models.CASCADE, db_column='deveui')

    class Meta:
        db_table = 't_swatch_location_reservation'
        managed = False
