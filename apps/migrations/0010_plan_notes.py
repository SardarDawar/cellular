# Generated by Django 2.2.12 on 2020-04-27 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0009_plan_linkweb'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='notes',
            field=models.TextField(default='', max_length=500, null=True),
        ),
    ]
