from django.db import models


class NcsDeviceRange(models.Model):
    deveui_from = models.CharField(primary_key=True, null=False, max_length=16)
    deveui_to = models.CharField(null=False, max_length=16)

    class Meta:
        db_table = 't_ncs_deveui_range'
        managed = False
