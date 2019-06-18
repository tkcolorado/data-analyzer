from __future__ import unicode_literals
from django.test import TestCase
from datetime import datetime
from consumption.models import User_data, Consumption


class TestModels(TestCase):

    def setUp(self):
        self.datetime = datetime.now()     
        self.user = User_data.objects.create(id=1, area='a1', tariff='t2')
        self.user.save()

    def test_user_data(self):
        user_data = User_data.objects.get(area='a1')
        self.assertEqual(self.user, user_data)

    def test_consumption(self):
        consumption = Consumption(user_data=self.user,
                                datetime=self.datetime,
                                consumption=400)
        consumption.save()
        consumption_db = Consumption.objects.get(datetime=self.datetime)
        self.assertEqual(consumption, consumption_db)