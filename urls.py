from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail_helpdesk.urls import urlpatterns as helpdesk_urlpatterns

from apps.users.urls import urlpatterns as users_urlpatterns

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("__healthcheck__/", include("health_check.urls")),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Add views for testing 404 and 500 templates
    urlpatterns += [
        path("test404", TemplateView.as_view(template_name="404.html")),
        path("test500", TemplateView.as_view(template_name="500.html")),
    ]
urlpatterns += [
    path("", include(wagtail_urls)),
    path("", include(helpdesk_urlpatterns)),
    path("", include(users_urlpatterns)),
]
