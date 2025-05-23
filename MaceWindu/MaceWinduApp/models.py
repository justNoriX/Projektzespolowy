from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):

    username = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(5)]
    )
    email = models.EmailField(
        _('email address'),
        unique=True
    )
    first_name = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(2)]

    )
    last_name = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(2)]
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    def __str__(self):
        return "{}".format(self.email)

class ObservationPoint(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE)
    title = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(5)]
    )
    description = models.CharField(
        max_length=100
    )
    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        validators=[
            MinValueValidator(-90.0),
            MaxValueValidator(90.0)
        ]
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(-180.0),
            MaxValueValidator(180.0)
        ]
    )
    energyCostPerKWh=models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(99.99)
        ]
    )

class SnapShot(models.Model):
    observation_point = models.ForeignKey(
        ObservationPoint,
        on_delete=models.CASCADE)
    title = models.CharField(
        max_length=20,
        validators=[
            MinLengthValidator(5)
        ]
    )
    description = models.TextField(
        max_length=100
    )
    snapshot_date=models.DateField(db_default=Now())

class WindValue(models.Model):
    snapshot = models.ForeignKey(
        SnapShot,
        on_delete=models.CASCADE
    )
    time = models.TimeField(db_default=Now())
    wind_direction = models.IntegerField()
    speed_value = models.FloatField()
    gust_value = models.FloatField()

