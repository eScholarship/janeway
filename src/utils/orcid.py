__copyright__ = "Copyright 2017 Birkbeck, University of London"
__author__ = "Martin Paul Eve & Andy Byers"
__license__ = "AGPL v3"
__maintainer__ = "Birkbeck Centre for Technology and Publishing"

import json
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
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
        return user.socialaccount_set.filter(provider='orcid')[0].extra_data['orcid-identifier']['uri']
    return None

def build_redirect_uri(site):
    """ builds the landing page for ORCID requests
    :site: Object implementing the AbstractSiteModel interface
    :return: (str) Redirect URI for ORCID requests
    """
    request = logic.get_current_request()
    path = reverse("core_login_orcid")

    return request.site_type.site_url(path)


def retrieve_record(orcid_id, access_token):
    """ Uses ORCID API to retrieve an ORCID record
    :param orcid_id: (str) ORCID ID
    :param acess_token:  (str) code provided by ORCID
    :return (json) in ORCID API record schema
    """
    headers = {
      'Accept': 'application/json',
      'Authorization': 'Bearer ' + str(access_token),
    }

    api_url = settings.ORCID_API_URL
    logger.info("Reading data from ORCID using %s" % api_url)
    r = requests.get('%s/%s/record' % (api_url, orcid_id), headers=headers)
    try:
        r.raise_for_status()
    except HTTPError as e:
        logger.error("ORCID record request failed: %s" % str(e))
        orcid_record = None
    else:
        orcid_record = r.json()

    return orcid_record


def form_fields(orcid_id, access_token):
    """ ORCID fields relevant for Account form
    :param orcid_id: (str) ORCID ID
    :param acess_token:  (str) code provided by ORCID
    :return (dict) form fields
    """
    form_initial = None
    orcid_record = retrieve_record(orcid_id, access_token)
    if orcid_record:
        person = orcid_record['person']
        form_initial = {
            # ToDo: Filter for primary email
            'email': person['emails']['email'][0]['email'] \
                if len(person['emails']['email']) > 0 else '',
            'first_name': person['name']['given-names']['value'],
            'last_name': person['name']['family-name']['value'],
            'department': orcid_record['activities-summary']['employments'] \
                ['employment-summary'][0]['department-name'],
            'institution': orcid_record['activities-summary']['employments'] \
                ['employment-summary'][0]['organization']['name'],
            'country': person['addresses']['address'][0]['country']['value']
        }

    return form_initial


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super(SocialAccountAdapter, self).save_user(request, user, form)
        if request.journal:
            user.add_account_role('author', request.journal)
        return user


class AccountAdapter(DefaultAccountAdapter):
    def get_from_email(self):
        if self.request.journal:
            return setting_handler.get_setting('email', 'from_address', self.request.journal).value
        else:
            return self.request.press.main_contact

