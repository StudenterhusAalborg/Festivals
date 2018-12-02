from django.utils.timezone import now

from northern_winter_beat.models import Post, Page


def AddMenuAndNewsProcessor(request):
    # TODO make sure only NorthernWinterBeat gets this or only if relevant etc.
    return {
        'pages': Page.objects.all()}
