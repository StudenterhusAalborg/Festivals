from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.utils.timezone import now
from django.views.decorators.clickjacking import xframe_options_exempt

from northern_winter_beat.models import Page, Artist, WinterbeatSettings, Post


def index(request):
    return render(request, "winter-beat/index.html", {
        "artists": Artist.objects.released(),
    })


def show_page(request, page_slug):
    page = get_object_or_404(Page, slug=page_slug)

    return render(request, "winter-beat/page.html", {
        "page": page,
    })


@xframe_options_exempt
def show_artist(request, artist_slug):
    artist = get_object_or_404(Artist, slug=artist_slug)

    return render(request, "winter-beat/artist.html", {
        "artist": artist,
    })


def list_posts(request):
    data = {
        "posts": Post.objects.all() \
            if request.user.is_authenticated and request.user.is_superuser \
            else Post.objects.filter(created__lte=now())
    }
    return render(request, "winter-beat/list_posts.html", data)
