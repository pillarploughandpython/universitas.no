# -*- coding: utf-8 -*-
"""
Urls that are only used for development.
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from debug_toolbar import urls as debug_toolbar_urls

from .urls import urlpatterns

# menu
devurlpatterns = [
    # develop urls
    url(r'^menu$', TemplateView.as_view(
        template_name='devmenu.html'), name='top-menu'),
    # django debug toolbar
    url(r'^__debug__/', include(debug_toolbar_urls)),
]

# serve media files from development server
devurlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

urlpatterns = devurlpatterns + urlpatterns
