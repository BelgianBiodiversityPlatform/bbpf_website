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
from amnesiabbpf.phc import PHCRegistryResource


log = logging.getLogger(__name__)


def includeme(config):
    ''' Pyramid includeme func '''
    config.scan(__name__)


@view_defaults(context=PHCRegistryResource)
class PHCRegistry(BaseView):

    @view_config(request_method='GET', name='schemes', renderer='json')
    def schemes(self):
        return self.context.get_schemes()

    @view_config(request_method='GET', name='people',
                 renderer='amnesiabbpf:phc/templates/registry/list.pt')
    def people(self):
        skills = self.request.GET.getall('class_ids')
        people = self.context.people(skills)
        return {'data': people}

    @view_config(request_method='GET', name='person',
                 renderer='amnesiabbpf:phc/templates/registry/person.pt')
    def person(self):
        person_id = self.request.GET.get('id')
        person, classifications = self.context.person(person_id)

        # See https://github.com/malthe/chameleon/issues/170
        classifications = ((scheme, list(cl)) for scheme, cl in classifications)

        return {'person': person, 'classifications': classifications}

    @view_config(request_method='GET', name='cl',
                 renderer='amnesiabbpf:phc/templates/registry/cl.pt')
    def cl(self):
        person_id = self.request.GET.get('id')
        cl = self.context.classifications(person_id)
        return {'cl': cl}

    @view_config(request_method='GET', name='',
                 renderer='amnesiabbpf:phc/templates/registry/index.pt')
    def index(self):
        schemes = self.context.get_schemes()
        return {'schemes': schemes}
