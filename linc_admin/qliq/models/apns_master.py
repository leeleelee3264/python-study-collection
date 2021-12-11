from django.db import models, transaction


class ApnsMaster(models.Model):
    id = models.AutoField(primary_key=True)

    did = models.CharField(null=False, max_length=256)
    phone_num = models.CharField(null=False, max_length=50)
    os_type = models.CharField(null=True, max_length=10)
    is_service = models.BooleanField(null=False, default=False)
    phone_cc = models.CharField(null=True, max_length=10)
    device_type = models.CharField(null=True, max_length=64)

    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'apns_master'
        managed = False
        app_label = 'qliq'

    def get_did(self):
        return '' if self.did is None else self.did

    @classmethod
    def clear_invalid_did(cls, did, device_type):
        try:
            with transaction.atomic():
                ApnsMaster.objects.filter(did=did, device_type=device_type).delete()
        except:
            print('fail to delete did :', did)
