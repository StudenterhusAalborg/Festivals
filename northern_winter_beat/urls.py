from django.urls import path

from .views import index, show_page, show_artist, list_posts, view_post

app_name = "winterbeat"

urlpatterns = [
    path('', index, name='home'),
    path('page/<slug:page_slug>', show_page, name='page'),
    path('news', list_posts, name="list_posts"),
    path('news/<int:pk>', view_post, name="view_post"),
    path('artist/<slug:artist_slug>', show_artist, name='artist'),
]
