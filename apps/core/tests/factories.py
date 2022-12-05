from wagtail_factories import PageFactory
from wagtail_helpdesk.cms.models import HomePage


class HomePageFactory(PageFactory):
    class Meta:
        model = HomePage
