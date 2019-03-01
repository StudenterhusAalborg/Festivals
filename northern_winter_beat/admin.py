from django.contrib import admin
# Register your models here.
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from django_summernote.admin import SummernoteModelAdmin
from orderable.admin import OrderableAdmin

from northern_winter_beat.models import Page, Artist, Post, Festival, Concert


class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('Studenthouse Festival')

    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('Studenthouse Festival administration')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Studenthouse Festival administration')


admin_site = MyAdminSite()


@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    exclude = ["pk"]
    list_display = ["__str__"]


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    exclude = ["pk", "slug"]
    summernote_fields = ["body_da", "body_en"]


@admin.register(Concert)
class ConcertAdmin(OrderableAdmin):
    exclude = ["pk", "sort_order"]
    list_display = ["__str__", "date", "sort_order_display"]

    def get_changeform_initial_data(self, request):
        """
        The default playday should be the first day of the festival.
        This is so it's easier than to scroll all the way through and make sure it is the correct day
        :param request:
        :return:
        """
        return {'date': Festival.get_solo().start_date}


@admin.register(Artist)
class ArtistAdmin(OrderableAdmin, SummernoteModelAdmin):
    exclude = ["pk", "slug", "sort_order"]
    list_display = ["name", "release_date", "subtitle", 'sort_order_display']
    summernote_fields = ["description_da", "description_en"]


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    exclude = ["pk", "slug"]
    list_display = ["title", "created"]
    summernote_fields = ["body_da", "body_en"]
