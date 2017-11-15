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
                             QPushButton, QMessageBox, QSplitter,
                             QTableWidget, QTableWidgetItem, QInputDialog,
                             QAbstractItemView, QComboBox, QGridLayout,
                             QHBoxLayout)

from widgets.netlist.netlist import NetlistWidget
from widgets.graph.graph import GraphWidget
from widgets.core.core import CoreWidget
from widgets.method.method import MethodWidget
from widgets.numerics.numerics import NumericWidget

from widgets.misc import VListWidget

#from widgets.method.method import MethodWidget
#from widgets.numerics.numerics import NumericWidget


here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]
netpath = os.path.join(here, 'tests', 'clipper.net')


class MyWidget(QWidget):
    def __init__(self, netpath):
        QWidget.__init__(self)

        hbox = QHBoxLayout()

        vboxL = QVBoxLayout()

        self.netlist = NetlistWidget(netpath, self)
        vboxL.addWidget(self.netlist)

        self.graph = GraphWidget(self.netlist, self)
        vboxL.addWidget(self.graph)

        self.core = CoreWidget(self.graph, self)
        vboxL.addWidget(self.core)

        vboxR = QVBoxLayout()

        self.method = MethodWidget(self.core, self)
        vboxR.addWidget(self.method)

        self.numeric = NumericWidget(self.method, self)
        vboxR.addWidget(self.numeric)

#        spliter = QSplitter()
#        wL = QWidget()
#        wL.setLayout(vboxL)
#        wR = QWidget()
#        wR.setLayout(vboxL)
#        spliter.addWidget(wL)
#        spliter.addWidget(wR)

        hbox.addLayout(vboxL)
        hbox.addLayout(vboxR)
#        vbox.addWidget(self.core)
#
#        self.method = MethodWidget(self.core, self)
#        vbox.addWidget(self.method)
#
#        self.numeric = NumericWidget(self.method, self)
#        vbox.addWidget(self.numeric)

        self.setLayout(hbox)
        self.resize(self.sizeHint())


if __name__ is '__main__':
    app = QApplication(sys.argv)
    e = MyWidget(netpath)
    e.show()
    e.raise_()
    sys.exit(app.exec_())
