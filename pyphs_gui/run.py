#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 14:52:19 2017

@author: Falaize
"""
from __future__ import absolute_import

from PyQt5.QtWidgets import QApplication
from widgets.main.gui_pyphs import PyphsGui
import sys
import os

from PyQt5.QtWidgets import (QWidget, QAction, QLabel,
                             QFileDialog, QScrollArea, QVBoxLayout,
                             QPushButton, QMessageBox,
                             QTableWidget, QTableWidgetItem, QInputDialog,
                             QAbstractItemView, QComboBox, QGridLayout,
                             QHBoxLayout)

from widgets.netlist.netlist import NetlistWidget
from widgets.core.core import CoreWidget
from widgets.method.method import MethodWidget
from widgets.numerics.numerics import NumericWidget


here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]
netpath = os.path.join(here, 'tests', 'rlc', 'rlc2.net')

class MyWidget(QWidget):
    def __init__(self, netpath):
        QWidget.__init__(self)

        self.netlist = NetlistWidget(netpath, self)

        self.core = CoreWidget(self.netlist, self)

        self.method = MethodWidget(self.core, self)

        self.numeric = NumericWidget(self.method, self)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.netlist)
        vbox.addWidget(self.core)
        vbox.addWidget(self.method)
        vbox.addWidget(self.numeric)
        hbox.addLayout(vbox)
        scrollnodes = QScrollArea()
        widget = QWidget()
        widget.setLayout(hbox)
        scrollnodes.setWidget(widget)
        scrollnodes.setFixedHeight(500)
        scrollnodes.setWidgetResizable(True)
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(scrollnodes)
        self.resize(hbox.sizeHint())

if __name__ is '__main__':
    app = QApplication(sys.argv)
    e = MyWidget(netpath)
    e.show()
    e.raise_()
    sys.exit(app.exec_())
