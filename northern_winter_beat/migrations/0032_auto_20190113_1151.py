# Generated by Django 2.1.4 on 2019-01-13 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('northern_winter_beat', '0031_concert_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='concert',
            options={'ordering': ['sort_order'], 'verbose_name': 'concert', 'verbose_name_plural': 'concerts'},
        ),
        migrations.RenameField(
            model_name='winterbeatsettings',
            old_name='show_timeline',
            new_name='show_schedule',
        ),
    ]
