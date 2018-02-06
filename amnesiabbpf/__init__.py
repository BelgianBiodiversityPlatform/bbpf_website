# -*- coding: utf-8 -*-

import logging

from pyramid.config import Configurator
from amnesia.resources import Resource
from amnesia.resources import Root
from amnesia.resources import get_root
from amnesiabbpf.phc import PHCResource

log = logging.getLogger(__name__)  # pylint: disable=invalid-name


class BBPFRoot(Root):

    def __getitem__(self, path):
        # Public health
        if path == 'health':
            return PHCResource(self.request, self)

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
