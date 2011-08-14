from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('django_obi.views',
    url(r'^mine/$', 'user_badges', name='obi-my-badges'),
    url(r'^send/$', 'send_badges', name='obi-send-badges'),
    url(r'^send/done/$', 'send_badges_done',
        name='obi-send-badges-done'),
    url(r'^(?P<identifier>.*)\.badge$',  'retrieve_badge',
        name='obi-retrieve-badge'),
)
