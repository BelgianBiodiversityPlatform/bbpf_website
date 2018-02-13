# -*- coding: utf-8 -*-

import logging

from pyramid.config import Configurator
from amnesia.resources import Resource
from amnesia.resources import Root
from amnesia.resources import get_root
from amnesia.modules.folder import Folder
from amnesiabbpf.phc import PHCResource
from amnesiabbpf.phc import PHCResourceMixin
from amnesiabbpf.phc import PHCRegistryResource

log = logging.getLogger(__name__)  # pylint: disable=invalid-name


class BBPFRoot(Root, PHCResourceMixin):


    def __getitem__(self, path):
        # Public health
        if path == self.phc_root_id:
            phc_folder = self.dbsession.query(Folder).get(self.phc_root_id)
            return PHCResource(self.request, phc_folder, self)

        # Public health registry
        if path == self.phc_registry_id:
            return PHCRegistryResource(self.request, self)

        return super().__getitem__(path)

def bbpf_root(request):
    return BBPFRoot(request)


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """

    config = Configurator(settings=settings, root_factory=bbpf_root)
    config.include('amnesia')
    config.include('amnesiabbpf.widgets')
    config.include('amnesiabbpf.views')
    config.include('amnesiabbpf.phc')
    config.add_static_view(name='static', path='amnesiabbpf:static/')
    config.override_asset(
        to_override='amnesia:templates/',
        override_with='amnesiabbpf:templates/'
    )

    return config.make_wsgi_app()
