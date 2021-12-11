from django.db import models


class SwatchDeviceSn(models.Model):
    deveui = models.CharField(primary_key=True, max_length=16)
    serial_no = models.CharField(null=False, max_length=16)
    appkey = models.CharField(null=True, max_length=32)

    create_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, auto_now=True)

    class Meta:
        db_table = 't_swatch_device_sn'
        managed = False
