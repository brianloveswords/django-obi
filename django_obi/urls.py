from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('django_obi.views',
    url(r'^mine/$', 'user_badges', name='obi-my-badges'),
    url(r'^(?P<identifier>.*)\.badge$',  'retrieve_badge',
        name='obi-retrieve-badge'),
)
