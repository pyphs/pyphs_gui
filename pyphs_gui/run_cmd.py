#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 14:52:19 2017

@author: Falaize
"""
from __future__ import absolute_import

import sys

from PyQt5.QtWidgets import QApplication

from .widgets import PyphsGui


def runner(path=None):
    app = QApplication(sys.argv)
    sys.argv
    e = PyphsGui(path)
    e.show()
    e.raise_()
    sys.exit(app.exec_())
    return True
