from django.db import models


class SwatchBase(models.Model):
    DB_KEY = 'Spdlqmf1!'

    class Meta:
        abstract = True
