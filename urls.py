from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import views

urlpatterns = patterns('',
    url(r"(?P<identifier>.*)\.badge",  views.retrieve_badge),
    url(r"info",  direct_to_template, {'template': 'info.html'}),
    url(r'mine/?', views.user_badges),
    url(r'send/?', views.send_badges),
)

if settings.DEBUG:
    urlpatterns += patterns('', url(r"diagnose/?", views.diagnose))
