# -*- coding: utf-8 -*-

import logging

from pyramid.config import Configurator
from amnesia.resources import get_root

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """

    config = Configurator(settings=settings, root_factory=get_root)
    config.include('amnesia')
    config.include('amnesiabbpf.widgets')
    config.include('amnesiabbpf.views')
    config.add_static_view(name='static', path='amnesiabbpf:static/')
    config.override_asset(
        to_override='amnesia:templates/',
        override_with='amnesiabbpf:templates/'
    )

    return config.make_wsgi_app()
