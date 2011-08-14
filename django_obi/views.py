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


from django_obi.utils import decode_badge, encode_badge
from django_obi.forms import SendBadgesForm


try:
    badge_getter = settings.MOZBADGES['badge_getter']
    get_awarded_badges = get_callable(badge_getter)
    hub_uri = settings.MOZBADGES['hub']
    # TODO: do a better job of defining API paths
    issue_path = "%s/badges/issue" % hub_uri
except KeyError:
    raise ImproperlyConfigured()

json_mime = 'application/json'
badge_mime = 'application/x-badge-manifest'


def _badge_urls(badges, request):
    urls = []
    email = request.user.email
    for badge_id in badges:
        identifier = encode_badge(badge_id, email)
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
        badge_id, email = decode_badge(str(identifier))
        user = User.objects.get(email=email)
        badge = get_awarded_badges(user)[badge_id]
    except (KeyError, User.DoesNotExist, TypeError):
        pass

    if not badge:
        raise Http404

    response = {
        'spec': '0.1.0',
        'name': badge['name'],
        'evidence': request.build_absolute_uri(badge['evidence']),
        'image': badge['image'],
        'recipient': email,
        'description': badge['description'],
        'template': request.build_absolute_uri(badge['template']),
    }
    return HttpResponse(json.dumps(response),
        mimetype='application/x-badge-manifest')


@login_required
def user_badges(request):
    badges = get_awarded_badges(request.user)
    urls = _badge_urls(badges, request)
    return HttpResponse(json.dumps(urls), mimetype=json_mime)


@login_required
def default_render_failure(request, message, status=500,
                           template_name='django_obi/failure.html'):
    """Render an error page to the user."""
    data = render_to_string(
        template_name, dict(message=message),
        context_instance=RequestContext(request))
    return HttpResponse(data, status=status)


@login_required
def send_badges(request, template_name='django_obi/send.html',
        send_badges_complete_view='obi-send-badges-done',
        form_class=SendBadgesForm, render_failure=default_render_failure,
        extra_context=None):

    user = request.user
    if not user.email:
        return render_failure(request,
            _("An email address is required for sending badges."), status=500)
    badges = get_awarded_badges(user)

    if request.POST:
        send_form = form_class(badges, data=request.POST)
        if send_form.is_valid():
            badges = dict(send_form.cleaned_data['badges'])
            postdata = urlencode({'urls': json.dumps(
                _badge_urls(badges, request))})
            error_msg = _("Could not open connection to hub: %s")
            try:
                hubresp = urlopen(issue_path, postdata)
                return HttpResponseRedirect(reverse(send_badges_complete_view))
            except HTTPError, e:
                try:
                    errors = json.loads(e.read())['errors']
                    return render_failure(request, errors, status=500)
                except (UnicodeEncodeError, KeyError, ValueError):
                    return render_failure(request, error_msg % str(e),
                        status=500)
            except URLError, e:
                return render_failure(request, error_msg % str(e), status=500)
    else:
        send_form = form_class(badges)

    context = {
        'form': send_form,
        'badges': badges,
    }
    context.update(extra_context or {})

    return render_to_response(template_name, context,
        context_instance=RequestContext(request))


@login_required
def send_badges_done(request,
                         template_name='django_obi/send_done.html',
                         extra_context=None):
    context = {}
    context.update(extra_context or {})
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))
