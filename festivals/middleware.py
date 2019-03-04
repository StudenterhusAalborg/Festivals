from urllib.parse import urlparse

from django.shortcuts import get_object_or_404

from festivals.models import Festival


def set_festival_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        parsed_url = urlparse(request.META['HTTP_HOST'])
        domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path.split(":")[0]
        domain = domain.replace("www.", "")

        festival = Festival.objects.filter(domain_name=domain).first()

        request.festival = festival
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
