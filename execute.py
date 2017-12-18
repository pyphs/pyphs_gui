#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 15:04:01 2017

@author: afalaize
"""

from pyphs_gui import runner

import os
path = os.path.join('/Users/afalaize/Developement/repos/pyphs_gui',
                    'pyphs_gui', 'tests', 'rlc.net')

runner(path=path)
