# Generated by Django 3.2.12 on 2022-02-28 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0014_auto_20220228_1021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notes',
            name='cover',
        ),
    ]