# -*- coding: utf-8 -*-

import json
import logging

from itertools import groupby

from urllib.parse import urlencode
from urllib.parse import urljoin
from urllib.request import urlopen

from pyramid.decorator import reify

from amnesia.resources import Resource
from amnesia.modules.folder import FolderEntity
from amnesia.modules.folder import Folder


log = logging.getLogger(__name__) # pylint: disable=invalid-name


class PHCResourceMixin:

    @reify
    def phc_root_id(self):
        return self.settings.get('phc_root_id')

    @reify
    def phc_registry_id(self):
        return self.settings.get('phc_registry_id')


class PHCResource(FolderEntity, PHCResourceMixin):

    def __init__(self, request, entity, parent=None):
        super().__init__(request, entity, parent)

    @property
    def __parent__(self):
        return self.request.root

    @property
    def __name__(self):
        return self.phc_root_id


class PHCRegistryResource(Resource, PHCResourceMixin):
    '''Public Health registry resource, which query the BeCRIS (old BioBel
    database)'''

    def __init__(self, request, parent):
        super().__init__(request)
        self.parent = parent
        self.registry_url = self.settings['phc_registry_url']
        self.source_id = self.settings['phc_registry_source_id']

    @property
    def __name__(self):
        return self.phc_registry_id

    @property
    def __parent__(self):
        return self.parent

    @property
    def entity(self):
        return self.dbsession.query(Folder).get(self.phc_registry_id)

    def url(self, sub):
        return urljoin(self.registry_url, sub)

    def get_schemes(self):
        params = urlencode({'source_id': self.source_id})
        url = self.url('schemes.json?{}'.format(params))
        return json.loads(urlopen(url).read().decode('utf-8'))

    def people(self, skills):
        params = urlencode({
            'source': self.source_id,
            'skills[]': skills # needed for Rails
        }, doseq=True)

        url = self.url('people/listExperts.json?{}'.format(params))
        return json.loads(urlopen(url).read().decode('utf-8'))

    def person(self, person_id):
        url = self.url('people/{}.json'.format(person_id))
        person = json.loads(urlopen(url).read().decode('utf-8'))

        classifications = sorted(person['person']['classifications'],
                                 key=lambda x: x['scheme'])
        classifications = groupby(classifications, lambda x: x['scheme'])

        return (person, classifications)

    def classifications(self, person_id):
        url = self.url('classifications/{}.json'.format(person_id))
        return json.loads(urlopen(url).read().decode('utf-8'))
