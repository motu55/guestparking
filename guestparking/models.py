from django.db import models


class Flat(models.Model):
    email = models.EmailField()
    hash = models.TextField()

class Car(models.Model):
    plate = models.TextField()
    starttime = models.DateTimeField()
    parked = models.BooleanField(default=True)
    endtime = models.DateTimeField(null=True)
    blocked = models.BooleanField(default=False)
    flat = models.ForeignKey(Flat,models.CASCADE)
