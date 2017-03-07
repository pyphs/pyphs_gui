#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 14:52:19 2017

@author: Falaize
"""
from __future__ import absolute_import

from PyQt5.QtWidgets import QApplication
from simulator_mainwindow import Simulation
import sys


def editor():
    app = QApplication(sys.argv)
    e = Simulation()
    sys.exit(app.exec_())


if __name__ is '__main__':
    editor()
