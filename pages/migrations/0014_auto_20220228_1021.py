# Generated by Django 3.2.12 on 2022-02-28 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0013_auto_20220228_0953'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notes',
            old_name='file',
            new_name='pdf_file',
        ),
        migrations.AddField(
            model_name='notes',
            name='ppt_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
