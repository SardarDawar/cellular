# Generated by Django 2.2.12 on 2020-04-27 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_plan_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='number_of_open_slots',
            field=models.IntegerField(default=0),
        ),
    ]