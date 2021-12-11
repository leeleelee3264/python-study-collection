from django.db import models

from device.models.swatch_device import SwatchDeviceInfo


class SwatchAttendance(models.Model):
    id = models.AutoField(primary_key=True)

    device = models.ForeignKey(SwatchDeviceInfo, on_delete=models.CASCADE, db_column='deveui')
    attend_date = models.DateField(null=False)
    combo = models.PositiveSmallIntegerField(null=False)

    class Meta:
        db_table = 't_swatch_attendance'
        managed = False

        unique_together = (('device', 'attend_date'), )


class SwatchQuizAnswer(models.Model):
    id = models.AutoField(primary_key=True, db_column='answer_id')

    device = models.ForeignKey(SwatchDeviceInfo, on_delete=models.CASCADE, db_column='deveui')

    class Meta:
        db_table = 't_swatch_quiz_answer'
        managed = False
