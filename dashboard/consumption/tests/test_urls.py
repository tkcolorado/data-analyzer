from __future__ import unicode_literals
from django.urls import reverse
from django.test import TestCase, Client

from ..models import User_data

class TestUrls(TestCase):

    def setUp(self): 
        self.c = Client()    
        self.user = User_data.objects.create(id=1, area='a1', tariff='t2')
        self.user.save()


    def test_home(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    
    def test_details(self):
        response = Client().get(reverse('details'))
        self.assertEqual(response.status_code, 200)