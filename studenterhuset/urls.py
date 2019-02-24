"""studenterhuset URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.utils.translation import ugettext_lazy

import festivals.urls
import northern_winter_beat.urls

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('old/', include(northern_winter_beat.urls)),
    path('', include(festivals.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Text to put at the end of each page's <title>.
admin.site.site_title = ugettext_lazy('Studenthouse festivals')

# Text to put in each page's <h1> (and above login form).
admin.site.site_header = ugettext_lazy('Studenthouse festivals administration')

# Text to put at the top of the admin index page.
admin.site.index_title = ugettext_lazy('Studenthouse festivals administration')
