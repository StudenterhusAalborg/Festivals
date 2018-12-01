from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy
from django_summernote.admin import SummernoteModelAdmin
from orderable.admin import OrderableAdmin
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
class PageAdmin(SummernoteModelAdmin):
    exclude = ["pk", "slug"]
    summernote_fields = ["body_da", "body_en"]


@admin.register(Artist)
class ArtistAdmin(OrderableAdmin, SummernoteModelAdmin):

    def get_changeform_initial_data(self, request):
        return {'date': WinterbeatSettings.get_solo().start_date}

    exclude = ["pk", "slug", "sort_order"]
    list_display = ["name", "release_date", "subtitle", 'sort_order_display']
    summernote_fields = ["description_da", "description_en"]


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    exclude = ["pk", "slug"]
    list_display = ["title", "created"]
    summernote_fields = ["body_da", "body_en"]
