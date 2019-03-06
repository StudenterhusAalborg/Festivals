from typing import Type, Tuple

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Field
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.utils.text import format_lazy
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy, get_language, ugettext

from orderable.managers import OrderableManager
from orderable.models import Orderable


def create_field_for_both_languages(field_type: Type[Field], pretty_name: str, **kwargs) -> Tuple[
    Field, Field]:
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


class Festival(models.Model):
    name = models.CharField(max_length=128)
    domain_name = models.CharField(max_length=64)
    theme = models.CharField(
        max_length=128,
        help_text="just dont touch if Casper hasn't told you to."
    )
    top_text_da, top_text_en = create_field_for_both_languages(
        models.TextField,
        ugettext_lazy("Top text"),
        help_text=ugettext_lazy("the paragraph above the list of bands. Is hidden if empty"),
        default="",
        blank=True
    )
    bottom_text_da, bottom_text_en = create_field_for_both_languages(
        models.TextField,
        ugettext_lazy("Bottom text"),
        help_text=ugettext_lazy("The paragraph below the list of bands. It is hidden if empty"),
        default="",
        blank=True,
    )

    description = models.TextField(
        ugettext_lazy("Description"),
        help_text=ugettext_lazy(
            "The description that is used when linking to winterbeat from another page"),
        default=""
    )

    show_nav_bar = models.BooleanField(
        ugettext_lazy("Show navigation bar"),
        help_text=ugettext_lazy("Show the bar of pages on top or not."),
        default=False
    )

    show_schedule = models.BooleanField(
        ugettext_lazy("Show schedule"),
        help_text=ugettext_lazy("Show the page with the date each artist is going to play"),
        default=False
    )

    youtube_link = models.CharField(
        ugettext_lazy("Link to Youtube"),
        help_text=ugettext_lazy(
            "If you have a link to a playlist on Youtube relevant to the festival"),
        max_length=255,
        null=True,
        blank=True
    )

    spotify_link = models.CharField(
        ugettext_lazy("Link to Spotify"),
        help_text=ugettext_lazy(
            "If you have a link to a playlist on Spotify relevant to the festival"),
        max_length=255,
        null=True,
        blank=True,
    )

    facebook_link = models.CharField(
        ugettext_lazy("Link to Facebook"),
        help_text=ugettext_lazy("If you have a link to a facebook page"),
        max_length=255,
        null=True,
        blank=True
    )

    instagram_link = models.CharField(
        ugettext_lazy("Link to Instagram"),
        help_text=ugettext_lazy("If you have a link to a instagram page"),
        max_length=255,
        null=True,
        blank=True
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
        return self.name

    @property
    def bottom_text(self):
        return mark_safe(self.bottom_text_da if get_language() == "da" else self.bottom_text_en)

    @property
    def top_text(self):
        return mark_safe(self.top_text_da if get_language() == "da" else self.top_text_en)

    class Meta:
        verbose_name = ugettext_lazy("Festival")
        verbose_name_plural = ugettext_lazy("Festivals")


class Page(models.Model):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
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


class Stage(Orderable):
    name_da, name_en = create_field_for_both_languages(
        models.CharField,
        ugettext_lazy("name"),
        max_length=128,
        help_text=ugettext_lazy('The name of the stage'),
    )
    festival = models.ForeignKey(
        Festival,
        verbose_name=ugettext_lazy("festival"),
        help_text=ugettext_lazy("The festival that the stage is used on"),
        on_delete=models.CASCADE,
    )


    @property
    def name(self):
        return self.name_da if get_language() == "da" else self.name_en

    def __str__(self):
        return f"{self.name} ({self.festival})"


class ArtistManager(OrderableManager):
    def released(self):
        return self.filter(release_date__lte=now())


class Artist(Orderable):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
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

    stage = models.ForeignKey(
        Stage,
        verbose_name=ugettext_lazy("stage"),
        help_text=ugettext_lazy("The stage that the concert will be on"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    concert_time = models.DateTimeField(
        ugettext_lazy("concert time"),
        help_text=ugettext_lazy('The time of the concert'),
        blank=True,
        null=True,
    )

    objects = ArtistManager()

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        if self.festival != self.stage.festival:
            raise ValidationError("Artist cannot play at a stage that isn't ")
        super().save(**kwargs)

    def __str__(self):
        return self.name

    @property
    def name_len(self):
        return len(self.name)

    @property
    def date(self):
        return self.concert_time.date()

    @property
    def description(self):
        return self.description_da if get_language() == "da" else self.description_en

    @property
    def body(self):
        return mark_safe(
            self.description +
            (f"<br><br> {self.embedded_youtube}" if self.youtube_video_link else "")
        )

    @property
    def as_link(self):
        classes = " ".join(["artist", "clickable" if self.body else ""])
        modal_attributes = "data-toggle='modal'  data-target='#exampleModal' " \
            f"onclick='setModal({self.pk})'"
        name = " ".join([
            self.name,
            f"<p class='subtitle'>{self.subtitle}</p>" if self.subtitle else ""
        ])
        return mark_safe(
            f"<a class='{classes}' {modal_attributes if self.body else ''}> {name} </a>"
        )

    @property
    def as_schedule_link(self):
        classes = " ".join(["artist", "clickable" if self.body else ""])
        modal_attributes = "data-toggle='modal'  data-target='#exampleModal' " \
            f"onclick='setModal({self.pk})'"
        name = " ".join([
            self.concert_time.strftime('%H:%M'),
            self.name,
            f"<p class='subtitle'>{self.subtitle}</p>" if self.subtitle else ""
        ])
        return mark_safe(
            f"<a class='{classes}' {modal_attributes if self.body else ''}> {name} </a>"
        )

    @property
    def embedded_youtube(self):
        link = self.youtube_video_link.replace("watch?v=", "embed/")
        return f'<div class="embed-responsive embed-responsive-16by9"><iframe src="{link}" width="100%" ' \
            f'class="embed-responsive-item" allowfullscreen></iframe></div> '

    class Meta(Orderable.Meta):
        verbose_name = ugettext_lazy("artist")
        verbose_name_plural = ugettext_lazy("artists")
        ordering = ("sort_order",)


class Post(models.Model):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
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
