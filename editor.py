#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 14:52:19 2017

@author: Falaize
"""
from __future__ import absolute_import

from PyQt5.QtWidgets import QApplication
from pyphs.pyphs_gui.editor_mainwindow import NetlistEditor
import sys
import os


def editor():
	app = QApplication(sys.argv)
	e = NetlistEditor()
	sys.exit(app.exec_())
