# -*- coding: utf-8 -*-

from .resources import PHCResource
from .resources import PHCResourceMixin
from .resources import PHCRegistryResource

def includeme(config):
    config.include('.views')
