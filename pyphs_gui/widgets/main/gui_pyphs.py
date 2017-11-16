#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

This example shows
how to use QSplitter widget.

author: Jan Bodnar
website: zetcode.com
last edited: January 2015
"""

from __future__ import absolute_import, division, print_function

from PyQt5.QtWidgets import (QAction, QMainWindow, QVBoxLayout,
                             QHBoxLayout, QWidget)
from PyQt5.QtGui import QIcon

from ..netlist.netlist import NetlistWidget
from ..core.core import CoreWidget
from ..method.method import MethodWidget
from ..graph.graph import GraphWidget
from ..numerics.numerics import NumericWidget
from ..simulation.simulation import SimulationWidget

from .. import iconspath
import os


class MainWidget(QWidget):
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

        self.simulation = NumericWidget(self.numeric, self)
        vboxR.addWidget(self.simulation)

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


class PyphsGui(QMainWindow):

    def __init__(self, netpath=None):

        QMainWindow.__init__(self)

        self.initUI(netpath)

#        if self.netlist._new:
#            self.initUI()
#        else:
#            qApp.quit()
#
    def initUI(self, netpath):

        self.mainWidget = MainWidget(netpath=netpath)

        self.setCentralWidget(self.mainWidget)

        #############################################################
        #############################################################
        #############################################################

        # Define Main Actions

        # Exit Action
        exitAction = QAction(QIcon(os.path.join(iconspath, 'exit.png')),
                             '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit PyPHS Editor')
        exitAction.triggered.connect(self.destroy)

        # Simulation Action
        simuAction = QAction(QIcon(os.path.join(iconspath,
                                                'simulation.png')),
                             '&Simulation tool', self)
        simuAction.setShortcut('Ctrl+Shift+S')
        simuAction.setStatusTip('Show simulation tool')

        #############################################################
        #############################################################
        #############################################################

        # TOOLBAR

#        self.toolbar = self.addToolBar('PyPHS GUI')
#        self.toolbar.addAction(self.mainWidget.netlist.newAction)
#        self.toolbar.addAction(self.mainWidget.netlist.openAction)
#        self.toolbar.addAction(self.mainWidget.netlist.saveAction)
#        self.toolbar.addAction(self.mainWidget.netlist.saveasAction)
#        self.toolbar.addAction(self.mainWidget.netlist.addlineAction)
#        self.toolbar.addAction(self.mainWidget.netlist.dellineAction)
#        self.toolbar.addAction(self.mainWidget.netlist.editAction)
#        self.toolbar.addAction(self.mainWidget.graph.plotgraphAction)
#        self.toolbar.addAction(self.mainWidget.graph.plotSTAction)
#        self.toolbar.addAction(simuAction)
#
        #############################################################
        #############################################################
        #############################################################

        # Status Bar

        self.statusBar()

        #############################################################
        #############################################################
        #############################################################

        # MENU BAR

        menubar = self.menuBar()

        #############################################################
        # Needed on MacOSX only.                                    #
        # This forces in-window menu instead of standard OSX menu   #
        menubar.setNativeMenuBar(False)                             #
        #############################################################

        # PyPHS menu
        fileMenu = menubar.addMenu('&Netlist')
        fileMenu.addAction(self.mainWidget.netlist.newAction)
        fileMenu.addAction(self.mainWidget.netlist.openAction)
        fileMenu.addAction(self.mainWidget.netlist.saveAction)
        fileMenu.addAction(self.mainWidget.netlist.saveasAction)
        fileMenu.addAction(exitAction)

        # Netlist menu
        netlistMenu = menubar.addMenu('&Line')
        netlistMenu.addAction(self.mainWidget.netlist.addlineAction)
        netlistMenu.addAction(self.mainWidget.netlist.dellineAction)
        netlistMenu.addAction(self.mainWidget.netlist.editAction)

        # Plots menu
        plotsMenu = menubar.addMenu('&Plots')
        plotsMenu.addAction(self.mainWidget.graph.plotgraphAction)
        plotsMenu.addAction(self.mainWidget.graph.plotSTAction)

        simuMenu = menubar.addMenu('&Simulation')
        simuMenu.addAction(simuAction)

        #############################################################

        self.setWindowTitle('PyPHS')
        self.setWindowIcon(QIcon(os.path.join(iconspath,
                                              'pyphs.png')))
        self.setContentsMargins(0, 0, 0, 0)
        self.show()
