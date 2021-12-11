from django.db import models

from device.models.swatch_device import SwatchDeviceInfo
from device.models.swatch_user_info import SwatchUserInfo


class SwatchDeviceUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(SwatchUserInfo, on_delete=models.CASCADE, db_column='user_id')
    device = models.ForeignKey(SwatchDeviceInfo, on_delete=models.CASCADE, db_column='deveui')

    nickname = models.CharField(null=False, max_length=20)
    photo_url = models.URLField(null=False, max_length=500)

    class Meta:
        db_table = 't_swatch_device_user'
        managed = False

        unique_together = (('user', 'device'), )


class SwatchDeviceUserPush(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(SwatchUserInfo, on_delete=models.CASCADE, db_column='user_id')
    device = models.ForeignKey(SwatchDeviceInfo, on_delete=models.CASCADE, db_column='deveui')

    push_id = models.IntegerField(null=False)

    class Meta:
        db_table = 't_swatch_device_user_push'
        managed = False

        unique_together = (('user', 'device', 'push_id'), )
