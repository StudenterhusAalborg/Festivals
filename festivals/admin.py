from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from django_summernote.admin import SummernoteModelAdmin
from orderable.admin import OrderableAdmin

from festivals.models import Page, Artist, Post, Festival, Stage


class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('Studenthouse Festival')

    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('Studenthouse Festival Administration')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Studenthouse Festival Administration')


admin_site = MyAdminSite()


class FestivalModelAdmin(admin.ModelAdmin):
    """
    Handles only fetching relevant objects
    """

    def get_queryset(self, request):
        return super().get_queryset(request).filter(festival=request.festival)

    def get_fields(self, request, obj=None):
        """
        remove festival from display. NEVER display that shit.
        """
        return tuple(x for x in super().get_fields(request, obj) if x != "festival")

    def save_model(self, request, obj, form, change):
        """
        Auto set festival if not set.
        """
        if hasattr(type(obj), "festival") and not hasattr(obj, "festival"):
            obj.festival = request.festival
        super().save_model(request, obj, form, change)


@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    exclude = ["pk"]
    list_display = ["__str__"]

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(Stage)
class StageAdmin(OrderableAdmin, FestivalModelAdmin):
    exclude = ["pk", "sort_order"]
    list_display = ["name", "festival", "sort_order_display"]


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin, FestivalModelAdmin):
    exclude = ["pk", "slug"]
    summernote_fields = ["body_da", "body_en"]


# @admin.register(Concert)
class ConcertAdmin(OrderableAdmin, FestivalModelAdmin):
    exclude = ["pk", "sort_order"]
    list_display = ["__str__", "date", "sort_order_display"]

    def get_changeform_initial_data(self, request):
        """
        The default playday should be the first day of the festival.
        This is so it's easier than to scroll all the way through and make sure it is the correct day
        :param request:
        :return:
        """
        return None  # {'date': Festival.get_solo().start_date}


@admin.register(Artist)
class ArtistAdmin(OrderableAdmin, SummernoteModelAdmin, FestivalModelAdmin):
    exclude = ["pk", "slug", "sort_order"]
    list_display = [
        "name", "release_date", "subtitle", "date", "concert_time", "stage", 'sort_order_display'
    ]
    summernote_fields = ["description_da", "description_en"]


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin, FestivalModelAdmin):
    exclude = ["pk", "slug"]
    list_display = ["title", "created"]
    summernote_fields = ["body_da", "body_en"]
