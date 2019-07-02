import logging
import csv
from consumption.models import User_data, Consumption
from django.core.management.base import BaseCommand
from django.db import models
import glob 

    # もしデータがあったら全削除
    # データインポートを始める
    # リストにぶち込んでbulk_create
class Command(BaseCommand):

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - '
                            '%(filename)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def handle(self, *args, **options):
        self.logger.info("Initiate Import.")
        self.store_user_data()
        self.store_consumption_data()
        self.logger.info("Import complete.")    

    def store_user_data(self, *args, **options):

        if User_data.objects.exists():
            self.logger.info('user_data table data already exist,'
                    ' drop the table import again.')
            User_data.objects.all().delete()

        user_datas = []

        with open('../data/user_data.csv', 'r') as f:
            rows = csv.reader(f)
            next(rows)
            for row in rows:
                info = {
                    'id': row[0],
                    'area': row[1],
                    'tariff': row[2],
                }

                try:
                    User_data.objects.get(pk=info['id'])                    
                except:
                    User_data(**info).save()       

            self.logger.info('User data imported')   
            f.close()

    def store_consumption_data(self, *args, **kwargs):

        if Consumption.objects.exists():
            self.logger.info('consumption table data already exist,'
                    ' drop the table import again.')
            Consumption.objects.all().delete()

        consumptions = []

        for i in glob.glob('../data/consumption/*.csv'):
            user_id = i.replace('../data/consumption/', '').replace('.csv', '')
            user_data = User_data.objects.get(pk=user_id)
            with open(i, 'r') as f:
                rows = csv.reader(f)
                next(rows)
                for row in rows:
                    info = {
                        'user_data': user_data,
                        'datetime': row[0],
                        'consumption': row[1]
                    }

                    consumptions.append(Consumption(**info))

                # print(consumptions)
                
        self.logger.info('Consumption data imported')
        new_instances = Consumption.objects.bulk_create(consumptions)
        new_instances

        f.close()