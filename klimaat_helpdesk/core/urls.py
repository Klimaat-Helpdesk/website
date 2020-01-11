from django.urls import path

from klimaat_helpdesk.core.views import home_page

app_name = 'core'

urlpatterns = [
    path("", view=home_page, name='home'),
]
