from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from klimaat_helpdesk.cms.models import Answer, GeneralPage


class AnswerAdmin(ModelAdmin):
    model = Answer
    menu_label = _('Answers')
    menu_icon = 'doc-full'
    list_display = ('title', 'live', 'featured', 'categories')
    menu_order = 180
    search_fields = ('title', 'page_content')


modeladmin_register(AnswerAdmin)


class GeneralPageAdmin(ModelAdmin):
    model = GeneralPage
    menu_label = _('General Pages')
    menu_icon = 'doc-empty'
    list_display = ('title', 'slug', 'subtitle', )
    menu_order = 450


modeladmin_register(GeneralPageAdmin)
