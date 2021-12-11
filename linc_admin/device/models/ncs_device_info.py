from django.db import models


class NcsDeviceInfo(models.Model):
    deveui = models.CharField(primary_key=True, max_length=16)
    appeui = models.CharField(null=False, max_length=16)
    if_type = models.CharField(null=False, max_length=1)
    tp_id = models.CharField(null=True, max_length=256)
    tp_subs_ul_yn = models.CharField(max_length=1, default='Y')
    tp_subs_ack_yn = models.CharField(max_length=1, default='Y')

    create_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, auto_now=True)

    class Meta:
        db_table = 't_ncs_device_info'
        managed = False
