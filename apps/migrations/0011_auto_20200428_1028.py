# Generated by Django 2.2.12 on 2020-04-28 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0010_plan_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='notes',
            field=models.TextField(blank=True, default='', max_length=500, null=True),
        ),
    ]