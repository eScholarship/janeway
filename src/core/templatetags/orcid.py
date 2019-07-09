from django import template

from utils import orcid

register = template.Library()


@register.simple_tag(takes_context=True)
def orcidUrl(context):
    request = context.get('request')
    if request and request.user:
        return orcid.orcidUrl(request.user)
    else:
        return None
