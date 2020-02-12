# Generated by Django 2.2.2 on 2019-06-18 04:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_data',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('area', models.CharField(max_length=100)),
                ('tariff', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'user_data',
            },
        ),
        migrations.CreateModel(
            name='Consumption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('consumption', models.FloatField()),
                ('user_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consumption.User_data')),
            ],
            options={
                'db_table': 'consumption',
            },
        ),
    ]