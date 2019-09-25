__copyright__ = "Copyright 2017 Birkbeck, University of London"
__author__ = "Martin Paul Eve & Andy Byers"
__license__ = "AGPL v3"
__maintainer__ = "Birkbeck Centre for Technology and Publishing"

import json
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount import models as social_models
from core import models as core_models
from urllib.parse import urlencode

from django.conf import settings
from django.urls import reverse
import requests
from requests.exceptions import HTTPError

from utils import logic, setting_handler
from utils.logger import get_logger

logger = get_logger(__name__)


def orcidUrl(user):
    """ Get ORCID id from socialaccount
    :param user object
    :return: ORCID ID or None
    """
    if user and user.socialaccount_set.filter(provider='orcid'):
        return user.socialaccount_set.filter(provider='orcid')[0].\
            extra_data['orcid-identifier']['uri']
    return None

def copyOrcidProfileToAccount(user, social_user, commit=True):
    """ Copy ORCID user's data that maps to Janeway profile, from socialaccount
    table to core_account table, just for those fields that are empty.
    (Copying the data as opposed to having the user profile form access multiple models)  """
    if social_user and social_user[0]:
        person = social_user[0].extra_data['person']
        activities = social_user[0].extra_data['activities-summary']
        if person['addresses']['address']:
            country = person['addresses']['address'][0]['country']['value']
            try:
                user.country = core_models.Country.objects.get(name=country) \
                if not user.country else user.country
            except Exception:
                logger.warning(
                    "Country not found: %s" % country)
        if activities['employments']['employment-summary']:
            user.institution = \
                activities['employments']['employment-summary'][0]['organization']['name'] \
                if not user.institution else user.institution
            user.department = \
                activities['employments']['employment-summary'][0]['department-name'] \
                if not user.department else user.department
        if person['researcher-urls']['researcher-url']:
            user.website = person['researcher-urls']['researcher-url'][0]['url']['value'] \
                if not user.website else user.website
        if person['biography'] and person['biography']['content']:
            user.biography = person['biography']['content'] \
                if not user.biography else user.biography
        if commit:
            user.save()
    return user

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super(SocialAccountAdapter, self).save_user(request, user, form)
        social_user = social_models.SocialAccount.objects.filter(user_id=user.id)
        if social_user and social_user[0] and social_user[0].provider == 'orcid':
            user = copyOrcidProfileToAccount(user, social_user, commit)

        """ Like normal Account, new ORCID users are also automatically given the author role """
        if request.journal:
            user.add_account_role('author', request.journal)
        return user


class AccountAdapter(DefaultAccountAdapter):
    """ ORCID notification emails are sent from this address """
    def get_from_email(self):
        if self.request.journal:
            return setting_handler.get_setting('email', 'from_address', \
                self.request.journal).value
        else:
            return self.request.press.main_contact

    def get_email_confirmation_redirect_url(self, request):
        if request.user.is_authenticated and request.journal:
            return request.journal.site_url()
        else:
            super(AccountAdapter, self).get_email_confirmation_redirect_url(request)

