from typing import Type, Tuple

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Field
from django.template.defaultfilters import slugify
# Create your models here.
from django.utils.safestring import mark_safe
from django.utils.text import format_lazy
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy, get_language, ugettext
from orderable.managers import OrderableManager
from orderable.models import Orderable
from solo.models import SingletonModel


def create_field_for_both_languages(field_type: Type[Field], pretty_name: str, **kwargs) -> Tuple[Field, Field]:
    """
    helper for making the same textfield for danish and english.
    :param field_type:
    :param pretty_name:
    :param kwargs:
    :return: a 2-tuple of two fields
    """
    ret: Tuple[Field, Field] = tuple(field_type(
        format_lazy("{pretty_name} [{lang}]", pretty_name=pretty_name, lang=lang),
        **kwargs
    ) for lang in [ugettext_lazy("Danish"), ugettext_lazy("English")])

    return ret


class WinterbeatSettings(SingletonModel):
    top_text_da, top_text_en = create_field_for_both_languages(
        models.TextField,
        ugettext_lazy("Top text"),
        help_text=ugettext_lazy("the paragraph above the list of bands. Is hidden if empty"),
        default=""
    )
    bottom_text_da, bottom_text_en = create_field_for_both_languages(
        models.TextField,
        ugettext_lazy("Bottom text"),
        help_text=ugettext_lazy("The paragraph below the list of bands. It is hidden if empty"),
        default=""
    )

    description = models.TextField(
        ugettext_lazy("Description"),
        help_text=ugettext_lazy("The description that is used when linking to winterbeat from another page"),
        default=""
    )

    show_nav_bar = models.BooleanField(
        ugettext_lazy("Show navigation bar"),
        help_text=ugettext_lazy("Show the bar of pages on top or not."),
        default=False
    )

    show_timeline = models.BooleanField(
        ugettext_lazy("Show timeline"),
        help_text=ugettext_lazy("Show the page with the date each artist is going to play"),
        default=False
    )

    youtube_link = models.CharField(
        ugettext_lazy("Link to Youtube"),
        help_text=ugettext_lazy("If you have a link to a playlist on Youtube relevant to the festival"),
        max_length=255,
        null=True,
        blank=True
    )

    spotify_link = models.CharField(
        ugettext_lazy("Link to Spotify"),
        help_text=ugettext_lazy("If you have a link to a playlist on Spotify relevant to the festival"),
        max_length=255,
        null=True,
        blank=True,
    )

    ticket_link = models.CharField(
        ugettext_lazy("Link to tickets"),
        help_text=ugettext_lazy("This link will show up as the tickets sales"),
        max_length=255,
        null=True,
        blank=True
    )

    start_date = models.DateField(
        ugettext_lazy("Start date"),
        help_text=ugettext_lazy("The date the festival starts")
    )

    end_date = models.DateField(
        ugettext_lazy("End date"),
        help_text=ugettext_lazy("The date the festival ends")
    )

    def __str__(self):
        return ugettext("Winterbeat Settings")

    @property
    def bottom_text(self):
        return mark_safe(self.bottom_text_da if get_language() == "da" else self.bottom_text_en)

    def top_text(self):
        return mark_safe(self.top_text_da if get_language() == "da" else self.top_text_en)

    class Meta:
        verbose_name = ugettext_lazy("Winterbeat Settings")


class Page(models.Model):
    title_da, title_en = create_field_for_both_languages(
        models.CharField,
        ugettext_lazy("title"),
        max_length=64
    )
    slug = models.CharField(
        ugettext_lazy("slug"),
        max_length=64
    )
    # page including html
    body_da, body_en = create_field_for_both_languages(
        models.TextField,
        ugettext_lazy("body"),
        help_text="Accepts HTML etc. make sure you don't abuse this!"
    )

    @property
    def title(self):
        return self.title_da if get_language() == "da" else self.title_en

    @property
    def body(self):
        return mark_safe(self.body_da if get_language() == "da" else self.body_en)

    def save(self, **kwargs):
        self.slug = slugify(self.title_en)
        super().save(**kwargs)

    def __str__(self):
        return self.title_en

    class Meta:
        verbose_name = ugettext_lazy("page")
        verbose_name_plural = ugettext_lazy("pages")


class ArtistManager(OrderableManager):
    def released(self):
        return self.filter(release_date__lte=now())


class Artist(Orderable):
    name = models.CharField(
        ugettext_lazy("name"),
        max_length=128
    )
    one_line = models.BooleanField(
        ugettext_lazy("One line"),
        default=False,
        help_text=ugettext_lazy("Do you want title on splash screen on one singular line?")
    )
    description_da, description_en = create_field_for_both_languages(
        models.TextField,
        ugettext_lazy("description"),
        blank=True,
        default=""
    )
    subtitle = models.CharField(
        ugettext_lazy("subtitle"),
        max_length=128,
        blank=True,
        default="")
    youtube_video_link = models.CharField(
        max_length=128,
        blank=True,
        default="")

    release_date = models.DateTimeField(
        ugettext_lazy("Release date"),
        help_text=ugettext_lazy("The time when this band is going to be released on the website."),
        default=now
    )

    objects = ArtistManager()

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super().save(**kwargs)

    def __str__(self):
        return self.name

    @property
    def name_len(self):
        return len(self.name)

    @property
    def description(self):
        return self.description_da if get_language() == "da" else self.description_en

    @property
    def body(self):
        out = mark_safe(self.description + (f"<br><br> {self.embedded_youtube}" if self.youtube_video_link else ""))
        return out

    @property
    def embedded_youtube(self):
        link = self.youtube_video_link.replace("watch?v=", "embed/")
        return f'<div class="embed-responsive embed-responsive-16by9"><iframe src="{link}" width="100%" ' \
               f'class="embed-responsive-item" allowfullscreen></iframe></div> '

    class Meta(Orderable.Meta):
        verbose_name = ugettext_lazy("artist")
        verbose_name_plural = ugettext_lazy("artists")
        ordering = ("sort_order",)


class Concert(Orderable):
    artist = models.ForeignKey(
        Artist,
        verbose_name=ugettext_lazy('artist'),
        help_text=ugettext_lazy('The artist that is going to play the concert'),
        on_delete=models.CASCADE)

    title = models.CharField(
        verbose_name=ugettext_lazy('title'),
        max_length=128,
        help_text=ugettext_lazy('If you want the title to be something else than the artist name'),
        blank=True,
        null=True
    )

    sub_title = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )

    date = models.DateField(
        ugettext_lazy("date"),
        help_text=ugettext_lazy('The day the artist is going to play'),
        blank=True,
        null=True,
    )

    def clean(self):
        super().clean()
        settings = WinterbeatSettings.get_solo()
        if not settings.start_date <= self.date <= settings.end_date:
            raise ValidationError(ugettext(
                "Concert date has to be while the festival is running (between %(start_date)s and %(end_date)s)"
            ) % {'start_date': settings.start_date.strftime('%x'), 'end_date': settings.end_date.strftime('%x')})

    def __str__(self):
        title = (self.title or self.artist.name) + (f" {self.sub_title}" if self.sub_title else "")
        return f"{title} - {self.date:%c}"

    class Meta(Orderable.Meta):
        verbose_name = ugettext_lazy("concert")
        verbose_name_plural = ugettext_lazy("concerts")


class Post(models.Model):
    title_da, title_en = create_field_for_both_languages(
        models.CharField,
        ugettext_lazy("title"),
        max_length=128
    )
    body_da, body_en = create_field_for_both_languages(
        models.TextField,
        ugettext_lazy("body"),
        help_text="Can contain HTML, however be careful as this could make fucked up shit"
    )
    created = models.DateTimeField(default=now)

    def title(self):
        return self.title_da if get_language() == "da" else self.title_en

    def body(self):
        return self.body_da if get_language() == "da" else self.body_en

    def __str__(self):
        return f"{self.title_en} ({self.created})"

    class Meta:
        verbose_name = ugettext_lazy("post")
        verbose_name_plural = ugettext_lazy("posts")
        ordering = ('-created',)
