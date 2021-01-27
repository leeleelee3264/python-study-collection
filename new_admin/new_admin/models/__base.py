from django.db import models

class XCBase(models.Model):
    class Meta:
        abstract = True