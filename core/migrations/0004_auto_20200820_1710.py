# Generated by Django 3.0.8 on 2020-08-20 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200820_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='informacao',
            field=models.TextField(max_length=2000),
        ),
    ]
