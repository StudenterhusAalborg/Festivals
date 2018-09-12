from northern_winter_beat.models import Post, Page




def AddMenuAndNewsProcessor(request):
    # TODO make sure only NorthernWinterBeat gets this or only if relevant etc.
    return {'posts': Post.objects.all(), 'pages': Page.objects.all()}
