from django.contrib import admin

from klimaat_helpdesk.experts.models import Expert


admin.site.register([
    Expert,
])
