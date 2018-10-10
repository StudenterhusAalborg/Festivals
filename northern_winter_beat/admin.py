from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from solo.admin import SingletonModelAdmin

from northern_winter_beat.models import Page, Artist, Post, WinterbeatSettings

admin.site.register(WinterbeatSettings, SingletonModelAdmin)


class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('Studenthouse festivals')

    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('Studenthouse festivals administration')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Studenthouse festivals administration')


admin_site = MyAdminSite()


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    exclude = ["pk", "slug"]


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    exclude = ["pk", "slug"]
    list_display = ["name", "subtitle"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    exclude = ["pk", "slug"]
    list_display = ["title", "created"]
