# Generated by Django 2.1 on 2018-09-12 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('northern_winter_beat', '0002_page_path'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='path',
            new_name='slug',
        ),
    ]
