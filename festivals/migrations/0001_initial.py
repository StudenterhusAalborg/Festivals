# Generated by Django 2.1.7 on 2019-02-21 15:47

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, db_index=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('one_line', models.BooleanField(default=False, help_text='Do you want title on splash screen on one singular line?', verbose_name='One line')),
                ('description_da', models.TextField(blank=True, default='', verbose_name='description [Danish]')),
                ('description_en', models.TextField(blank=True, default='', verbose_name='description [English]')),
                ('subtitle', models.CharField(blank=True, default='', max_length=128, verbose_name='subtitle')),
                ('youtube_video_link', models.CharField(blank=True, default='', max_length=128)),
                ('release_date', models.DateTimeField(default=django.utils.timezone.now, help_text='The time when this band is going to be released on the website.', verbose_name='Release date')),
            ],
            options={
                'verbose_name': 'artist',
                'verbose_name_plural': 'artists',
                'ordering': ('sort_order',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, db_index=True)),
                ('title', models.CharField(blank=True, help_text='If you want the title to be something else than the artist name', max_length=128, null=True, verbose_name='title')),
                ('sub_title', models.CharField(blank=True, max_length=128, null=True)),
                ('date', models.DateField(blank=True, help_text='The day the artist is going to play', null=True, verbose_name='date')),
                ('artist', models.ForeignKey(help_text='The artist that is going to play the concert', on_delete=django.db.models.deletion.CASCADE, to='festivals.Artist', verbose_name='artist')),
            ],
            options={
                'verbose_name': 'concert',
                'verbose_name_plural': 'concerts',
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Festival',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('domain_name', models.CharField(max_length=64)),
                ('top_text_da', models.TextField(default='', help_text='the paragraph above the list of bands. Is hidden if empty', verbose_name='Top text [Danish]')),
                ('top_text_en', models.TextField(default='', help_text='the paragraph above the list of bands. Is hidden if empty', verbose_name='Top text [English]')),
                ('bottom_text_da', models.TextField(default='', help_text='The paragraph below the list of bands. It is hidden if empty', verbose_name='Bottom text [Danish]')),
                ('bottom_text_en', models.TextField(default='', help_text='The paragraph below the list of bands. It is hidden if empty', verbose_name='Bottom text [English]')),
                ('description', models.TextField(default='', help_text='The description that is used when linking to winterbeat from another page', verbose_name='Description')),
                ('show_nav_bar', models.BooleanField(default=False, help_text='Show the bar of pages on top or not.', verbose_name='Show navigation bar')),
                ('show_schedule', models.BooleanField(default=False, help_text='Show the page with the date each artist is going to play', verbose_name='Show schedule')),
                ('youtube_link', models.CharField(blank=True, help_text='If you have a link to a playlist on Youtube relevant to the festival', max_length=255, null=True, verbose_name='Link to Youtube')),
                ('spotify_link', models.CharField(blank=True, help_text='If you have a link to a playlist on Spotify relevant to the festival', max_length=255, null=True, verbose_name='Link to Spotify')),
                ('ticket_link', models.CharField(blank=True, help_text='This link will show up as the tickets sales', max_length=255, null=True, verbose_name='Link to tickets')),
                ('start_date', models.DateField(help_text='The date the festival starts', verbose_name='Start date')),
                ('end_date', models.DateField(help_text='The date the festival ends', verbose_name='End date')),
            ],
            options={
                'verbose_name': 'Festival',
                'verbose_name_plural': 'Festivals',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_da', models.CharField(max_length=64, verbose_name='title [Danish]')),
                ('title_en', models.CharField(max_length=64, verbose_name='title [English]')),
                ('slug', models.CharField(max_length=64, verbose_name='slug')),
                ('body_da', models.TextField(help_text="Accepts HTML etc. make sure you don't abuse this!", verbose_name='body [Danish]')),
                ('body_en', models.TextField(help_text="Accepts HTML etc. make sure you don't abuse this!", verbose_name='body [English]')),
                ('festival', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='festivals.Festival')),
            ],
            options={
                'verbose_name': 'page',
                'verbose_name_plural': 'pages',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_da', models.CharField(max_length=128, verbose_name='title [Danish]')),
                ('title_en', models.CharField(max_length=128, verbose_name='title [English]')),
                ('body_da', models.TextField(help_text='Can contain HTML, however be careful as this could make fucked up shit', verbose_name='body [Danish]')),
                ('body_en', models.TextField(help_text='Can contain HTML, however be careful as this could make fucked up shit', verbose_name='body [English]')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('festival', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='festivals.Festival')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='concert',
            name='festival',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='festivals.Festival'),
        ),
        migrations.AddField(
            model_name='artist',
            name='festival',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='festivals.Festival'),
        ),
    ]
