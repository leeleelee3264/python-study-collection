from django.db import models


class NcsThingPlugInfo(models.Model):
    tp_id = models.CharField(primary_key=True, max_length=40)
    tp_ukey = models.CharField(null=False, max_length=1024)
    tp_domain = models.CharField(null=False, max_length=256)
    tp_port = models.IntegerField(null=False)

    create_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, auto_now=True)

    class Meta:
        db_table = 't_ncs_thingplug_info'
        managed = False
