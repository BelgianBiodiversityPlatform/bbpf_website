# -*- coding: utf-8 -*-

import logging

from pyramid.decorator import reify

from amnesia.resources import Resource
from amnesia.modules.folder import FolderEntity


log = logging.getLogger(__name__)


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
