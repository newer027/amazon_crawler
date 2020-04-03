from django.conf.urls import url

from .views import HelpPageView, MailingListSignupAjaxView,rich_text


urlpatterns = [
    url(r'^help/',HelpPageView.as_view(),name='help',),
    url(r'^rich_text/',rich_text,name='rich_text',),
    url(r'^mailing-list-signup-ajax-view/',MailingListSignupAjaxView.as_view(),
        name='mailing_list_signup_ajax_view'),
]