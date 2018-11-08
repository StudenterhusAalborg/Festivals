from django.utils.timezone import now

from northern_winter_beat.models import Post, Page


def AddMenuAndNewsProcessor(request):
    # TODO make sure only NorthernWinterBeat gets this or only if relevant etc.
    return {
        'posts': (
            Post.objects.all()
            if request.user.is_authenticated and request.user.is_superuser
            else Post.objects.filter(created__lte=now())
        ),
        'pages': Page.objects.all()}
