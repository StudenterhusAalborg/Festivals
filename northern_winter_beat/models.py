from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
from django.utils.safestring import mark_safe
from django.utils.timezone import now


class Page(models.Model):
    title = models.CharField(max_length=64)
    slug = models.CharField(max_length=64)
    # page including html
    body = models.TextField(help_text="Accepts HTML etc. make sure you don't abuse this!")

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        super().save(**kwargs)

    def __str__(self):
        return self.title


class Artist(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    slug = models.CharField(max_length=64)
    subtitle = models.CharField(max_length=128, blank=True, default="")
    youtube_video_link = models.CharField(max_length=128, blank=True, default="")

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super().save(**kwargs)

    def __str__(self):
        return self.name

    @property
    def body(self):
        return ((self.description + (f"<br><br> {self.embedded_youtube}" if self.youtube_video_link else "")).\
            replace("\r\n","<br>").replace("\n","<br>"))

    @property
    def embedded_youtube(self):
        link = self.youtube_video_link.replace("watch?v=", "embed/")
        return f'<div class="embed-responsive embed-responsive-16by9"><iframe src="{link}" width="100%" class="embed-responsive-item" allowfullscreen></iframe></div>'


class Post(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField(help_text="Can contain HTML, however be careful as this could make fucked up shit")
    created = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.title} ({self.created})"


class Concert(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    slug = models.CharField(max_length=64)
    length = models.IntegerField(help_text="in minutes")

    def save(self, **kwargs):
        self.slug = slugify(f"{self.artist.name}-{self.start_time}")
        super().save(**kwargs)

    def __str__(self):
        return f"{self.artist.name} - {self.start_time} ({self.length} minutes)"
