# -*- coding: utf-8 -*-

import json
import logging

from itertools import groupby
from urllib.parse import urlencode
from urllib.parse import urljoin
from urllib.request import urlopen

from pyramid.view import view_config
from pyramid.view import view_defaults

from amnesia.views import BaseView
from amnesiabbpf.phc import PHCResource


log = logging.getLogger(__name__)


def includeme(config):
    ''' Pyramid includeme func '''
    config.scan(__name__)


@view_defaults(context=PHCResource)
class PHCRegistry(BaseView):

    @view_config(request_method='GET', name='schemes', renderer='json')
    def schemes(self):
        params = urlencode({'source_id': self.context.source_id})
        url = urljoin(self.context.registry_url,
                      'schemes.json?{}'.format(params))
        response = json.loads(urlopen(url).read().decode('utf-8'))

        return response

    @view_config(request_method='GET', name='people',
                 renderer='amnesiabbpf:phc/templates/phc_registry_list.pt')
    def people(self):
        params = urlencode({
            'source': self.context.source_id,
            'skills[]': self.request.GET.getall('class_ids')  # needed for Rails
        }, doseq=True)

        url = urljoin(self.context.registry_url,
                      'people/listExperts.json?{}'.format(params))
        response = json.loads(urlopen(url).read().decode('utf-8'))

        return {'data': response}

    @view_config(request_method='GET', name='person',
                 renderer='amnesiabbpf:phc/templates/phc_registry_person.pt')
    def person(self):
        person_id = self.request.GET.get('id')
        url = urljoin(self.context.registry_url,
                      'people/{}.json'.format(person_id))
        person = json.loads(urlopen(url).read().decode('utf-8'))

        classifications = sorted(person['person']['classifications'],
                                 key=lambda x: x['scheme'])
        classifications = groupby(classifications, lambda x: x['scheme'])

        # See https://github.com/malthe/chameleon/issues/170
        classifications = ((scheme, list(cl)) for scheme, cl in classifications)

        return {'person': person, 'classifications': classifications}

    @view_config(request_method='GET', name='cl',
                 renderer='amnesiabbpf:phc/templates/phc_registry_cl.pt')
    def cl(self):
        person_id = self.request.GET.get('id')
        url = urljoin(self.context.registry_url,
                      'classifications/{}.json'.format(person_id))
        classifications = json.loads(urlopen(url).read().decode('utf-8'))

        return {'cl': classifications}

    @view_config(request_method='GET', name='',
                 renderer='amnesiabbpf:phc/templates/index.pt')
    def index(self):
        params = urlencode({'source_id': self.context.source_id})
        url = urljoin(self.context.registry_url,
                      'schemes.json?{}'.format(params))
        response = json.loads(urlopen(url).read().decode('utf-8'))

        return {'schemes': response}
