# Generated by Django 2.2 on 2023-04-23 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery_list', '0004_auto_20230423_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='listitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
