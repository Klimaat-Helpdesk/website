from django.conf import settings
from django.contrib import admin

# Set the admin site title, display the current release version.
admin.site.site_header = (
    admin.site.site_title
) = f"klimaat-helpdesk versie: {settings.RELEASE_VERSION}"
