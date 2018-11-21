# Generated by Django 2.1.1 on 2018-11-21 13:36

from django.db import migrations
from django.template.defaultfilters import linebreaks

def convert_newlines_to_br(apps, schema_editor):
    Post = apps.get_model('northern_winter_beat', 'Post')

    for post in Post.objects.all():
        post.body_en = linebreaks(post.body_en)
        post.body_da = linebreaks(post.body_da)
        post.save()

class Migration(migrations.Migration):

    dependencies = [
        ('northern_winter_beat', '0022_auto_20181121_1157'),
    ]

    operations = [
        migrations.RunPython(convert_newlines_to_br, lambda x, y: None)
    ]
