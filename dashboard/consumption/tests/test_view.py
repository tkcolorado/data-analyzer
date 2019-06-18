from django.test import TestCase
from consumption.models import Consumption, User_data

import pandas as pd
from django.db.models import Sum, Avg
# Create your tests here.
# testした方が良いもの
# - importした値がきちんと入ってくるかどうか/
# - modelのtest
# - uriに対して呼び出されるメソッドが正しいか
# - メソッドに対して返されるHTMLが正しいか


class SummaryTestCase(TestCase):
    '''This class contains methods to test the functionality of functions in
       views.py.'''

    def setUp(self):
        Consumption.objects.create(id=1, datetime='2016-10-31 20:00:00',
                                   consumption=1, user_data_id=1)
        Consumption.objects.create(id=2, datetime='2016-10-31 18:00:00',
                                   consumption=2, user_data_id=1)
        Consumption.objects.create(id=3, datetime='2016-10-31 10:00:00',
                                   consumption=3, user_data_id=1)
        User_data.objects.create(id=1, area='a1', tariff='t2')


    def test_user_id_table(self):
        '''Test that the table containing average and total consumption for
           each user is generated correctly.'''
        df = pd.DataFrame(
            list(Consumption.objects.values('user_data_id')
                 .order_by('user_data_id')
                 .annotate(Average_consumption=Avg('consumption'),
                           Total_consumption=Sum('consumption'))
                 )
                          )[['user_data_id', 'Average_consumption',
                             'Total_consumption']]
        df['Average_consumption'] = round(df['Average_consumption'], 2)
        df['Total_consumption'] = round(df['Total_consumption'], 2)
        self.assertEqual(df.at[0, 'user_data_id'], 1)
        self.assertEqual(df.at[0, 'Average_consumption'], 2.0)
        self.assertEqual(df.at[0, 'Total_consumption'], 6.0)