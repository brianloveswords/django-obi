from django import template
from django.conf import settings


register = template.Library()


def send_badges_action():
    return {'hub': settings.MOZBADGES['hub']}

register.inclusion_tag('django_obi/send.html')(
    send_badges_action)
