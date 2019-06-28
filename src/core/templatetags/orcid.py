from django import template

from utils import orcid

register = template.Library()


@register.simple_tag(takes_context=True)
def orcid_redirect_uri(context):
    request = context.get('request')
    if request:
        return orcid.build_redirect_uri(request.site_type)
    else:
        return ""

@register.simple_tag(takes_context=True)
def orcidUrl(context):
    request = context.get('request')
    if request:
        return orcid.orcidUrl(request.user)
    else:
        return None
