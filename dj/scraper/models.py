from django.db import models

# Create your models here.


class Make(models.Model):
    name = models.CharField(max_length=50)


class CarModel(models.Model):
    name = models.CharField(max_length=100)
    make = models.ForeignKey(
        'Make', on_delete=models.CASCADE, related_name='car_model_rel')


class Year(models.Model):
    name = models.IntegerField()
    make = models.ForeignKey(
        'Make', on_delete=models.CASCADE, related_name='year_rel')


class Car(models.Model):
    name = models.CharField(max_length=100)
    model = models.ForeignKey(
        'CarModel', on_delete=models.CASCADE, related_name='car_rel')
    make = models.ForeignKey(
        'Make', on_delete=models.CASCADE, related_name='car_rel')
    year = models.ForeignKey(
        'Year', on_delete=models.CASCADE, related_name='car_rel')
    zero_to_sixty = models.IntegerField()
    hp = models.IntegerField()
    hp_rpm = models.IntegerField()
    torque = models.IntegerField()
    torque_rpm = models.IntegerField()
    cylinders = models.IntegerField()
    displacement = models.DecimalField(max_digits=4, decimal_places=2)
    front_diameter = models.DecimalField(max_digits=4, decimal_places=2)
    front_width = models.DecimalField(max_digits=4, decimal_places=2)
    front_tire = models.CharField(max_length=12)
    rear_diameter = models.DecimalField(max_digits=4, decimal_places=2)
    rear_width = models.DecimalField(max_digits=4, decimal_places=2)
    rear_tire = models.CharField(max_length=12)
    length = models.DecimalField(max_digits=4, decimal_places=2)
    width = models.DecimalField(max_digits=4, decimal_places=2)
    height = models.DecimalField(max_digits=4, decimal_places=2)
