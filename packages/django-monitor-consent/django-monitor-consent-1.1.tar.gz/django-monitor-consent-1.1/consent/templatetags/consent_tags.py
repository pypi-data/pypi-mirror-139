from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_consent_paragraphs():
    return settings.CONSENT_TEXT.split("\n\n")
