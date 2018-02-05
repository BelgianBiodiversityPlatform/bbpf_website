# -*- coding: utf-8 -*-

import json
import logging

from itertools import groupby
from urllib.parse import urlencode
from urllib.parse import urljoin
from urllib.request import urlopen

from pyramid.view import view_config

from amnesia.views import BaseView


log = logging.getLogger(__name__)


def includeme(config):
    ''' Pyramid includeme func '''
    config.scan(__name__)


class PHCRegistry(BaseView):

    @property
    def source_id(self):
        return self.request.registry.settings['phc_registry_source_id']

    @property
    def registry_url(self):
        return self.request.registry.settings['phc_registry_url']

    @view_config(request_method='GET',
                 name='phc_registry_schemes', renderer='json')
    def schemes(self):
        params = urlencode({'source_id': self.source_id})
        url = urljoin(self.registry_url, 'schemes.json?{}'.format(params))
        response = json.loads(urlopen(url).read().decode('utf-8'))
        return response

    @view_config(request_method='GET', name='phc_registry_people',
                 renderer='amnesiabbpf:templates/_custom/document/phc_registry_list.pt')
    def people(self):
        params = urlencode({
            'source': self.source_id,
            'skills[]': self.request.GET.getall('class_ids')  # needed for Rails
        }, doseq=True)

        url = urljoin(self.registry_url, 'people/listExperts.json?{}'.format(params))
        response = json.loads(urlopen(url).read().decode('utf-8'))

        return {'data': response}

    @view_config(request_method='GET', name='phc_registry_person',
                 renderer='amnesiabbpf:templates/_custom/document/phc_registry_person.pt')
    def person(self):
        person_id = self.request.GET.get('id')
        url = urljoin(self.registry_url, 'people/{}.json'.format(person_id))
        person = json.loads(urlopen(url).read().decode('utf-8'))

        classifications = sorted(person['person']['classifications'],
                                 key=lambda x: x['scheme'])
        classifications = groupby(classifications, lambda x: x['scheme'])

        # See https://github.com/malthe/chameleon/issues/170
        classifications = ((scheme, list(cl)) for scheme, cl in classifications)

        return {'person': person, 'classifications': classifications}

    @view_config(request_method='GET', name='phc_cl',
                 renderer='amnesiabbpf:templates/_custom/document/phc_registry_cl.pt')
    def cl(self):
        person_id = self.request.GET.get('id')
        url = urljoin(self.registry_url, 'classifications/{}.json'.format(person_id))
        classifications = json.loads(urlopen(url).read().decode('utf-8'))

        return {'cl': classifications}

#
#
#
#class RegistryController(object):
#
#    def index(self):
#        filters = { 'source_id': source_id() }
#        schemes = requests.get(registry_url() + '/schemes.json', params=filters).json()
#        return render('registry/index.html', schemes=schemes)
