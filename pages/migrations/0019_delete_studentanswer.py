# Generated by Django 3.2.12 on 2022-03-03 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0018_alter_notes_tutorial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StudentAnswer',
        ),
    ]