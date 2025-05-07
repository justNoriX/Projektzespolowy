from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True
    )
    first_name = models.CharField(
        max_length=20
    )
    surname = models.CharField(
        max_length=30
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','surname']

    def __str__(self):
        return "{}".format(self.email)

class ObservationPoint(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    title = models.CharField(
        max_length=20
    )
    description = models.TextField(
        max_length=100
    )
    longitude = models.FloatField()
    latitude = models.FloatField()
    energyCostPerKWh = models.FloatField()

class SnapShot(models.Model):
    observation_point = models.ForeignKey(
        ObservationPoint,
        on_delete=models.CASCADE)
    title = models.CharField(
        max_length=20
    )
    description = models.TextField(
        max_length=100
    )

class WindValue(models.Model):
    snapshot = models.ForeignKey(
        SnapShot,
        on_delete=models.CASCADE
    )
    date = models.DateField()
    wind_direction = models.IntegerField()
    speed_value = models.FloatField()
    gust_value = models.FloatField()

