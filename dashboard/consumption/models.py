from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class User_data(models.Model):

    id = models.IntegerField(primary_key=True)
    area = models.CharField(max_length=100)
    tariff = models.CharField(max_length=100)

    class Meta:
        db_table = "user_data"

    def __str__(self):
        return str(self.id)


class Consumption(models.Model):

    user_data = models.ForeignKey(User_data, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)
    consumption = models.FloatField()

    class Meta:
        db_table = "consumption"

    def __str__(self):
        return str(self.user_data)


    @classmethod
    def get_total(cls, user):
        """
        Get total consumption given a User
        :param user: (model.User object) an instance of User class
        :return: (float) total User consumption
        """

        user_consumptions = Consumption.objects.filter(user_data_id=user)
        total_consumptions = 0.0

        for consumption_record in user_consumptions:
            total_consumptions += consumption_record.consumption

        return total_consumptions


    @classmethod
    def get_average(cls, user):
        """
        Get average (mean) consumption given a User
        :param user: (model.User object) an instance of User class
        :return: (float) average User consumption
        """

        user_consumptions = Consumption.objects.filter(user_data_id=user)
        consumptions = []

        for consumption_record in user_consumptions:
            consumptions.append(consumption_record.consumption)

        if consumptions:
            avg_consumption = sum(consumptions)/float(len(consumptions))
        else:
            avg_consumption = 0.0

        return avg_consumption