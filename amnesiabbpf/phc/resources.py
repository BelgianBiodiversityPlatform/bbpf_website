# -*- coding: utf-8 -*-

import logging

from amnesia.resources import Resource


log = logging.getLogger(__name__)


class PHCResource(Resource):

    __name__ = 'phc'

    def __init__(self, request, parent=None):
        super().__init__(request)
        self.parent = parent
        self.registry_url = self.settings['phc_registry_url']
        self.source_id = self.settings['phc_registry_source_id']

    @property
    def __parent__(self):
        return self.request.root
