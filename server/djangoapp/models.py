from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Car Make model
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


# Car Model model
class CarModel(models.Model):

    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    ]

    # Many-to-one relationship:
    # one CarMake can have many CarModels
    car_make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE
    )

    # Dealer ID refers to a dealer stored in the external database
    dealer_id = models.IntegerField()

    name = models.CharField(max_length=100)

    type = models.CharField(
        max_length=10,
        choices=CAR_TYPES,
        default='SUV'
    )

    year = models.IntegerField(
        default=2023,
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(2023),
        ]
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name}"
