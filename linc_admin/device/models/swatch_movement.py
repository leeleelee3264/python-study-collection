from django.db import models

from device.models.swatch_device import SwatchDeviceInfo


class SwatchMovement(models.Model):
    device = models.ForeignKey(SwatchDeviceInfo, on_delete=models.CASCADE, db_column='deveui')
    stat_time = models.CharField(null=False, max_length=14)

    create_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, auto_now=True)

    class Meta:
        db_table = 't_swatch_movement'
        managed = False


class SwatchMovementStat1d(models.Model):
    device = models.ForeignKey(SwatchDeviceInfo, on_delete=models.CASCADE, db_column='deveui')
    stat_date = models.CharField(null=False, max_length=8)

    create_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, auto_now=True)

    class Meta:
        db_table = 't_swatch_movement_stat_1d'
        managed = False


class SwatchMovementPattern(models.Model):
    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(SwatchDeviceInfo, on_delete=models.CASCADE, db_column='deveui')

    class Meta:
        db_table = 't_swatch_movement_pattern'
        managed = False
