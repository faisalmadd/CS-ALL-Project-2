# Generated by Django 3.2.12 on 2022-02-16 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_auto_20220216_0657'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Topic',
            new_name='Course',
        ),
    ]
