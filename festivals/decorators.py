from django.http import Http404
from django.shortcuts import redirect


def festival_required(func=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """

    def decorator(func):
        def newfn(request, **kwargs):
            if not hasattr(request,'festival') or request.festival is None:
                raise Http404()

            return func(request, **kwargs)

        return newfn

    if func:
        return decorator(func)
    return decorator
