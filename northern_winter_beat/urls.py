from django.conf.urls import url
from django.urls import path

from .views import index, show_page, show_artist

app_name = "winterbeat"

urlpatterns = [
    path('', index, name='home'),
    path('page/<slug:page_slug>', show_page, name='page'),
    path('artist/<slug:artist_slug>', show_artist, name='artist'),
]
