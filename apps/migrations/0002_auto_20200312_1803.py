# Generated by Django 2.2.7 on 2020-03-12 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilemodel',
            name='contactNumber',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
