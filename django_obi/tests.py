import re
import json
from urllib2 import urlopen, HTTPError, URLError

from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import get_callable


class SettingsTests(TestCase):
    def test_existence(self):
        self.assertTrue(hasattr(settings, 'MOZBADGES'),
            'Settings missing MOZBADGES attribute')
        self.assertTrue(isinstance(settings.MOZBADGES, dict),
            'settings.MOZBADGES should be a dict')

    def test_hub(self):
        # url regex taken from http://mathiasbynens.be/demo/url-regex,
        # using the @stephenhay method.
        url_re = re.compile(r'^https?://[^\s/$.?#].[^\s]*$', re.I)
        hub_uri = settings.MOZBADGES.get('hub', '')

        self.assertTrue(url_re.match(hub_uri),
            "settings.MOZBADGES['hub'] must be valid http(s) uri.")

    def test_badge_getter(self):
        q_getter = settings.MOZBADGES.get('badge_getter', '')
        self.assertTrue(q_getter,
            "settings.MOZBADGES['badge_getter'] must be set.")

        self.assertIn('.', q_getter,
            "Invalid settings.MOZBADGES['badge_getter']. " +
            "Expecting 'module.funcion'.")

        method = get_callable(q_getter)
        self.assertTrue(callable(method),
            "%s not a callable object." % q_getter)
