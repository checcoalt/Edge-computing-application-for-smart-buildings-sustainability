from django.db import models

# Create your models here.

class Libellium(models.Model):
    timestamp = models.DateTimeField()
    # id = models.IntegerField(primary_key=True)
    CO = models.FloatField()
    O3 = models.FloatField()
    TC = models.FloatField()
    HUM = models.FloatField()
    PRES = models.FloatField()