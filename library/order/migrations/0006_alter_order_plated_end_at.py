# Generated by Django 4.1 on 2022-11-27 23:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_order_options_alter_order_book_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='plated_end_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 11, 23, 31, 11, 335241), verbose_name='Плановий кінець'),
        ),
    ]
