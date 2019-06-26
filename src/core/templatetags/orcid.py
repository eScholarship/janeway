from django import template

from utils.orcid import build_redirect_uri

register = template.Library()


@register.simple_tag(takes_context=True)
def orcid_redirect_uri(context):
    request = context.get('request')
    if request:
        return build_redirect_uri(request.site_type)
    else:
        return ""

@register.simple_tag(takes_context=True)
def orcidUrl(context):
    r = None
    request = context.get('request')
    if request:
        user = request.user
        if user.socialaccount_set.filter(provider='orcid'):
            r =  user.socialaccount_set.filter(provider='orcid')[0].extra_data['orcid-identifier']['uri']
    return r
