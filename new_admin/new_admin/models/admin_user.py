from django.db import models
from new_admin.models.__base import XCBase


class AdminUser(XCBase):
    id = models.IntegerField(primary_key=True)
    login_id = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    group_name = models.CharField(max_length=50)
    api_key = models.CharField(max_length=200)
    is_extendible = models.CharField(max_length=1)
    name = models.CharField(max_length=20)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()



    class Meta:
        db_table = 'admin_user'