#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" __init__.py
bases provides several base classes.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Local Packages #
from .baseobject import BaseObject, search_sentinel
from .singlekwargdispatchmethod import singlekwargdispatchmethod
from .basemethod import BaseMethod
from .basemeta import BaseMeta
