# Generated by Django 4.1 on 2022-11-14 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='middle_name',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
