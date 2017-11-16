from __future__ import absolute_import

import os
here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]
iconspath = os.path.join(here[:here.rfind(os.sep)], 'icons')

from .main.gui_pyphs import PyphsGui


__all__ = ['PyphsGui', 'iconspath']
