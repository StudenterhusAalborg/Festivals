from django.contrib import admin

# Register your models here.
from northern_winter_beat.models import Page, Artist, Concert, Post


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    exclude = ["pk", "slug"]


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    exclude = ["pk", "slug"]
    list_display = ["name", "subtitle"]


@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    exclude = ["pk", "slug"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    exclude = ["pk", "slug"]
    list_display = ["title", "created"]