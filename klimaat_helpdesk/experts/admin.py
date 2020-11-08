from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from klimaat_helpdesk.experts.models import Expert


class ExpertAdmin(ModelAdmin):
    model = Expert
    menu_label = _('Experts')
    menu_icon = 'user'
    menu_order = 280
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', 'affiliation', 'email')
    list_filter = ('featured', 'affiliation')
    search_fields = ('name', 'affiliation')


modeladmin_register(ExpertAdmin)

admin.site.register([
    Expert,
])
