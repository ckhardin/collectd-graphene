# -*- coding: utf-8 -*-
from .app import create_app as _create_app

__author__ = 'Charles Hardin'
__email__ = 'ckhardin@gmail.com'
__version__ = '0.2.0'


def create_app(**kwargs):
    if not 'static_folider' in kwargs:
        kwargs['static_folder'] = "frontend"
    if not 'template_folider' in kwargs:
        kwargs['template_folder'] = "frontend"
    return _create_app(**kwargs)
