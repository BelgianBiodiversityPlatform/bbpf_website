# -*- coding: utf-8 -*-

from .resources import PHCResource

def includeme(config):
    config.include('.views')
