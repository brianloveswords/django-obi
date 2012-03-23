import json
from urllib2 import urlopen, URLError, HTTPError
from urllib import urlencode

from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import get_callable, reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.sites.models import Site


from django_obi.utils import decode_badge, encode_badge, hash_recipient


try:
    badge_getter = settings.MOZBADGES['badge_getter']
    get_awarded_badges = get_callable(badge_getter)
    hub_uri = settings.MOZBADGES['hub']
except KeyError:
    raise ImproperlyConfigured()


def _badge_urls(badges, request):
    urls = []
    username = request.user.username
    for badge_id in badges:
        identifier = encode_badge(badge_id, username)
        path = reverse('obi-retrieve-badge',
            kwargs=dict(identifier=identifier))
        urls.append(request.build_absolute_uri(path))
    return urls


def retrieve_badge(request, identifier):
    """
    Gets the manifest for a specific badge based on identifier.
    See util.encode_badge() for how identifiers are determined.
    """
    badge = None
    try:
        badge_id, username = decode_badge(str(identifier))
        user = User.objects.get(username=username)
        badge = get_awarded_badges(user)[badge_id]
    except (KeyError, User.DoesNotExist, TypeError):
        pass

    if not badge:
        raise Http404

    recipient, salt = hash_recipient(user.email)
    issuer = Site.objects.get_current()
    origin = "http://%s" % issuer.domain
    # the obi is not appending the origin to the image url.
    image = badge['image']
    if image.startswith('/'):
        image = origin + image

    response = {
        'recipient': recipient,
        'salt': salt,
        'evidence': badge['evidence'],
        'badge': {
            'version': '0.5.0',
            'name': badge['name'][:128],
            'image': image,
            'description': badge['description'][:128],
            'criteria': badge['criteria'],
            'issuer': {
                'origin': origin,
                'name': issuer.name,
             }
        }
    }
    return HttpResponse(json.dumps(response),
        mimetype='application/json')


@login_required
def user_badges(request):
    badges = get_awarded_badges(request.user)
    urls = _badge_urls(badges, request)
    return HttpResponse(json.dumps(urls), mimetype='application/json')
