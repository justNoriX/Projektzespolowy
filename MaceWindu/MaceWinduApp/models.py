from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

only_letters = RegexValidator(
    regex=r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż]+$',
    message='To pole może zawierać tylko litery alfabetu (bez cyfr i znaków specjalnych).'
)

letters_with_space = RegexValidator(
    regex=r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż ]+$',
    message='To pole może zawierać tylko litery i spacje (bez cyfr i znaków specjalnych).'
)


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
        validators=[MinLengthValidator(2),only_letters]

    )
    last_name = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(2),letters_with_space]
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

