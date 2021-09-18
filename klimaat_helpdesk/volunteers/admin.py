from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from klimaat_helpdesk.volunteers.models import Volunteer


class VolunteerAdmin(ModelAdmin):
    model = Volunteer
    menu_label = _('Volunteers')
    menu_icon = 'user'
    menu_order = 280
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', 'affiliation', 'email')
    search_fields = ('name', 'affiliation')


modeladmin_register(VolunteerAdmin)

admin.site.register([
    Volunteer,
])
